from __future__ import annotations
from typing import Generator
from clase_estado import Estado
from clases_operadores import OperadorProblemaBicing
from aima.search import Problem

class BicingProblem(Problem):
    def __init__(self, initial_state: Estado, es_hill_climbing: bool = True, es_heuristic1: bool = True):
        super().__init__(initial_state)
        self.es_hill_climbing = es_hill_climbing
        self.es_heuristic1 = es_heuristic1

    def actions(self, state: Estado) -> Generator[OperadorProblemaBicing, None, None]:
        if self.es_hill_climbing:
            return state.generar_acciones()
        else:
            return state.generar_una_accion()

    def result(self, state: Estado, accion: OperadorProblemaBicing) -> Estado:
        return state.aplicar_acciones(accion)

    def value(self, state: Estado) -> float:
        if self.es_heuristic1:
            return state.heuristico1()
        else:
            return state.heuristico2()

    def get_problem(self, state:Estado):
        return state

    def goal_test(self, state: Estado) -> bool:
        return False