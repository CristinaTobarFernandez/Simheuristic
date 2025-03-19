from enum import Enum

class MultiScenarioMethod(Enum):
    MAXIMUM_EXPECTATION = "Maximum expectation"
    CVAR = "Conditional Value at Risk (CVaR)"
    WORST_CASE_ANALYSIS = "Worst Case Analysis"

