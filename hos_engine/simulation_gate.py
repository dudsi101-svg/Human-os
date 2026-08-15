from collections.abc import Sequence
from dataclasses import dataclass

from .agent_runtime import InvocationRequest
from .simulation import (
    Intervention,
    Invariant,
    Scenario,
    SimulationEngine,
    SimulationStatus,
    SimulationSummary,
)


@dataclass(frozen=True)
class GateDecision:
    status:str
    reason:str
    simulation:SimulationSummary

class SimulationGate:
    def __init__(self,engine:SimulationEngine): self.engine=engine
    def evaluate(self,request:InvocationRequest,scenario:Scenario,intervention:Intervention,
                 invariants:Sequence[Invariant],runs:int=100)->GateDecision:
        s=self.engine.monte_carlo(scenario,intervention,invariants,runs,0)
        if s.recommended_status==SimulationStatus.FAILED:
            return GateDecision("BLOCKED","Simulation predicts unacceptable constitutional risk.",s)
        if s.recommended_status==SimulationStatus.REQUIRES_REVIEW:
            return GateDecision("REQUIRES_HUMAN_REVIEW","Simulation predicts meaningful downside.",s)
        return GateDecision("ALLOWED","Simulation passed current thresholds.",s)
