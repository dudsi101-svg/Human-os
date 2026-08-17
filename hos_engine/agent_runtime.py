from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from .call_authorization import CallAuthorizer


class RiskLevel(str, Enum):
    LOW="LOW"; MEDIUM="MEDIUM"; HIGH="HIGH"; CRITICAL="CRITICAL"

class ApprovalMode(str, Enum):
    AUTOMATIC="AUTOMATIC"; HUMAN_REQUIRED="HUMAN_REQUIRED"; FORBIDDEN="FORBIDDEN"

@dataclass(frozen=True)
class Capability:
    capability_id:str; action:str; resource_scope:str
    risk_level:RiskLevel; approval_mode:ApprovalMode
    constraints:dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True)
class AgentManifest:
    agent_id:str; name:str; purpose:str; owner_id:str; capabilities:set[str]
    may_delegate:bool=False; max_delegation_depth:int=0

@dataclass(frozen=True)
class Delegation:
    delegation_id:str; delegator_id:str; delegate_id:str
    capability_ids:set[str]; depth:int; reason:str; approved_by:str | None=None

@dataclass
class InvocationRequest:
    request_id:str; agent_id:str; capability_id:str; action:str
    resource:str; arguments:dict[str,Any]
    human_approval_id:str | None=None
    delegation_chain:list[str]=field(default_factory=list)

@dataclass(frozen=True)
class ActionReceipt:
    receipt_id:str; request_id:str; agent_id:str; capability_id:str
    status:str; reason:str; occurred_at:str; result_summary:str | None=None

class CapabilityRegistry:
    def __init__(self)->None: self._items:dict[str,Capability]={}
    def register(self,c:Capability)->None:
        if c.capability_id in self._items: raise ValueError("Capability already exists")
        self._items[c.capability_id]=c
    def get(self,cid:str)->Capability: return self._items[cid]

class AgentRegistry:
    def __init__(self)->None:
        self._agents:dict[str,AgentManifest]={}; self._delegations:dict[str,Delegation]={}
    def register(self,a:AgentManifest)->None:
        if a.agent_id in self._agents: raise ValueError("Agent already exists")
        self._agents[a.agent_id]=a
    def get(self,aid:str)->AgentManifest: return self._agents[aid]
    def delegate(self,d:Delegation)->None:
        src=self.get(d.delegator_id); self.get(d.delegate_id)
        if not src.may_delegate: raise PermissionError("Delegation forbidden")
        if d.depth>src.max_delegation_depth: raise PermissionError("Delegation depth exceeded")
        if not d.capability_ids.issubset(src.capabilities): raise PermissionError("Capability not owned")
        self._delegations[d.delegation_id]=d
    def for_delegate(self,aid:str)->list[Delegation]:
        return [d for d in self._delegations.values() if d.delegate_id==aid]

class AgentRuntime:
    def __init__(self,capabilities:CapabilityRegistry,agents:AgentRegistry,
                 call_authorizer:CallAuthorizer | None=None)->None:
        self.capabilities=capabilities; self.agents=agents
        self._call_authorizer=call_authorizer
        self._tools:dict[str,Callable[[dict[str,Any]],Any]]={}; self._receipts:list[ActionReceipt]=[]
    def register_tool(self,cid:str,fn:Callable[[dict[str,Any]],Any])->None:
        self.capabilities.get(cid); self._tools[cid]=fn
    def evaluate(self,r:InvocationRequest)->ActionReceipt:
        # An unknown agent or capability is a first-class DENIED receipt, not
        # a KeyError -- callers (e.g. ExecutionLoop) treat evaluate() as a
        # gate that refuses, never as something that raises.
        try: agent=self.agents.get(r.agent_id)
        except KeyError: return self._receipt(r,"DENIED","Unknown agent")
        try: cap=self.capabilities.get(r.capability_id)
        except KeyError: return self._receipt(r,"DENIED","Unknown capability")
        if r.action!=cap.action: return self._receipt(r,"DENIED","Action mismatch")
        if not self._has_cap(agent,r.capability_id,r.delegation_chain): return self._receipt(r,"DENIED","Missing capability")
        if not self._scope(cap.resource_scope,r.resource): return self._receipt(r,"DENIED","Resource outside scope")
        if cap.approval_mode==ApprovalMode.FORBIDDEN: return self._receipt(r,"DENIED","Forbidden by policy")
        if cap.approval_mode==ApprovalMode.HUMAN_REQUIRED and not r.human_approval_id:
            return self._receipt(r,"REQUIRES_HUMAN_APPROVAL","Human approval required")
        # Per-call authorization (AR-003): the grant said "may use this
        # tool"; the authorizer judges *this* call -- its arguments and its
        # delegation context. A denied verdict is a DENIED receipt.
        if self._call_authorizer is not None:
            verdict=self._call_authorizer.authorize(capability_id=r.capability_id,
                arguments=r.arguments,delegation_chain_length=len(r.delegation_chain))
            if not verdict.allowed: return self._receipt(r,"DENIED",f"Call refused: {verdict.reason}")
        if r.capability_id not in self._tools: return self._receipt(r,"DENIED","No tool implementation")
        try: result=self._tools[r.capability_id](r.arguments)
        except Exception as exc: return self._receipt(r,"FAILED",f"Tool failed: {exc}")  # noqa: BLE001 -- any tool failure must degrade to a FAILED receipt, never propagate
        return self._receipt(r,"EXECUTED","Checks passed",str(result)[:500])
    def _has_cap(self,a:AgentManifest,cid:str,chain:list[str])->bool:
        if cid in a.capabilities: return True
        ds={d.delegation_id:d for d in self.agents.for_delegate(a.agent_id)}
        if not chain: return False
        current=a.agent_id
        for did in reversed(chain):
            d=ds.get(did)
            if not d or d.delegate_id!=current or cid not in d.capability_ids: return False
            current=d.delegator_id
        return True
    @staticmethod
    def _scope(scope:str,res:str)->bool:
        return scope=="*" or res==scope or res.startswith(scope.rstrip("/")+"/")
    def _receipt(self,r:InvocationRequest,status:str,reason:str,result_summary:str | None=None)->ActionReceipt:
        x=ActionReceipt("HOS-RCP-"+uuid.uuid4().hex[:12].upper(),r.request_id,r.agent_id,
                        r.capability_id,status,reason,datetime.now(UTC).isoformat(),result_summary)
        self._receipts.append(x); return x
    def receipts(self)->list[ActionReceipt]: return list(self._receipts)
