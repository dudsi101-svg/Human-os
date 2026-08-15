from __future__ import annotations

import statistics
import uuid
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from enum import Enum
from random import Random
from typing import Any


class SimulationStatus(str, Enum):
    PASSED="PASSED"; FAILED="FAILED"; REQUIRES_REVIEW="REQUIRES_REVIEW"

@dataclass(frozen=True)
class Scenario:
    scenario_id:str
    name:str
    initial_state:dict[str,float]
    assumptions:dict[str,Any]=field(default_factory=dict)
    horizon_steps:int=1

@dataclass(frozen=True)
class Intervention:
    intervention_id:str
    name:str
    effects:dict[str,float]
    uncertainty:dict[str,float]=field(default_factory=dict)
    reversible:bool=True
    affects_people:bool=False

@dataclass(frozen=True)
class Invariant:
    invariant_id:str
    name:str
    check:Callable[[dict[str,float]],bool]
    failure_message:str
    severity:str="HIGH"

@dataclass(frozen=True)
class SimulationRun:
    run_id:str
    scenario_id:str
    intervention_id:str
    final_state:dict[str,float]
    invariant_failures:tuple[str,...]
    score:float
    status:SimulationStatus
    seed:int

@dataclass(frozen=True)
class SimulationSummary:
    scenario_id:str
    intervention_id:str
    runs:int
    mean_score:float
    score_stddev:float
    worst_score:float
    best_score:float
    failure_rate:float
    review_rate:float
    recommended_status:SimulationStatus

class OutcomeScorer:
    def __init__(self, weights:dict[str, float] | None=None):
        self.weights=weights or {
            "autonomy":1.0,"creative_agency":1.0,"relationships":1.0,
            "responsibility":1.0,"energy":0.8,"attention":0.8,"value_alignment":1.0
        }
    def score(self,before:dict[str,float],after:dict[str,float])->float:
        total=sum((after.get(k,0)-before.get(k,0))*w for k,w in self.weights.items())
        total-=max(0,after.get("degrading_dependency",0)-before.get("degrading_dependency",0))
        total-=max(0,after.get("extraction",0)-before.get("extraction",0))
        denom=sum(abs(x) for x in self.weights.values()) or 1
        return round(total/denom,6)

class SimulationEngine:
    def __init__(self, scorer:OutcomeScorer | None=None):
        self.scorer=scorer or OutcomeScorer()
    def simulate_once(self,scenario:Scenario,intervention:Intervention,
                      invariants:Sequence[Invariant],seed:int=0)->SimulationRun:
        rng=Random(seed); state=dict(scenario.initial_state)
        for _ in range(max(1,scenario.horizon_steps)):
            for key,effect in intervention.effects.items():
                noise=intervention.uncertainty.get(key,0)
                state[key]=min(1,max(0,state.get(key,0)+effect+rng.uniform(-noise,noise)))
        failures=tuple(i.failure_message for i in invariants if not i.check(state))
        score=self.scorer.score(scenario.initial_state,state)
        if failures: status=SimulationStatus.FAILED
        elif intervention.affects_people and not intervention.reversible or score<0: status=SimulationStatus.REQUIRES_REVIEW
        else: status=SimulationStatus.PASSED
        return SimulationRun("HOS-SIM-"+uuid.uuid4().hex[:12].upper(),scenario.scenario_id,
            intervention.intervention_id,state,failures,score,status,seed)
    def monte_carlo(self,scenario:Scenario,intervention:Intervention,
                    invariants:Sequence[Invariant],runs:int=100,seed:int=0)->SimulationSummary:
        if runs<1: raise ValueError("runs must be at least 1")
        xs=[self.simulate_once(scenario,intervention,invariants,seed+i) for i in range(runs)]
        scores=[x.score for x in xs]
        fr=sum(x.status==SimulationStatus.FAILED for x in xs)/runs
        rr=sum(x.status==SimulationStatus.REQUIRES_REVIEW for x in xs)/runs
        recommendation=SimulationStatus.FAILED if fr>0.05 else (
            SimulationStatus.REQUIRES_REVIEW if rr>0.20 else SimulationStatus.PASSED)
        return SimulationSummary(scenario.scenario_id,intervention.intervention_id,runs,
            round(statistics.mean(scores),6),round(statistics.pstdev(scores),6),
            round(min(scores),6),round(max(scores),6),round(fr,6),round(rr,6),recommendation)
    def compare(self,scenario:Scenario,interventions:Iterable[Intervention],
                invariants:Sequence[Invariant],runs:int=100,seed:int=0)->list[SimulationSummary]:
        out=[self.monte_carlo(scenario,i,invariants,runs,seed) for i in interventions]
        return sorted(out,key=lambda x:(x.recommended_status!=SimulationStatus.PASSED,-x.mean_score,x.failure_rate))

def constitutional_invariants()->list[Invariant]:
    return [
        Invariant("INV-AUTONOMY","Autonomy floor",lambda s:s.get("autonomy",0)>=0.30,
                  "Autonomy fell below the constitutional floor.","CRITICAL"),
        Invariant("INV-EXTRACTION","Extraction ceiling",lambda s:s.get("extraction",0)<=0.50,
                  "Extraction exceeded the constitutional ceiling.","CRITICAL"),
        Invariant("INV-DEPENDENCY","Dependency ceiling",lambda s:s.get("degrading_dependency",0)<=0.60,
                  "Dependence on degrading systems exceeded the ceiling.","HIGH"),
    ]
