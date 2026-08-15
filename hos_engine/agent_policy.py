from __future__ import annotations

from typing import Any

from .agent_runtime import ApprovalMode, Capability, RiskLevel


def constitutional_capability(capability_id:str, action:str, resource_scope:str,
    risk_level:RiskLevel, *, changes_external_state:bool, affects_people:bool,
    reversible:bool, handles_sensitive_data:bool,
    constraints:dict[str,Any]|None=None)->Capability:
    data=dict(constraints or {})
    data.update(changes_external_state=changes_external_state, affects_people=affects_people,
                reversible=reversible, handles_sensitive_data=handles_sensitive_data)
    if handles_sensitive_data and changes_external_state or affects_people or not reversible or risk_level in {RiskLevel.HIGH,RiskLevel.CRITICAL}:
        mode=ApprovalMode.HUMAN_REQUIRED
    else:
        mode=ApprovalMode.AUTOMATIC
    return Capability(capability_id,action,resource_scope,risk_level,mode,data)
