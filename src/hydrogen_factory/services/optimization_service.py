from pulp import *
from hydrogen_factory.models.schedule import OptimizationInput, OptimizationOutput
from hydrogen_factory.services.electrolyzer_service import ElectrolyzerService
from hydrogen_factory.services.storage_service import StorageService

class OptimizationService:
    def __init__(self, electrolyzer_service: ElectrolyzerService, storage_service: StorageService):
        """Initialize the OptimizationService with dependencies for electrolyzer and storage services.

        Args:
        - electrolyzer_service (ElectrolyzerService): Service to retrieve electrolyzer configurations.
        - storage_service (StorageService): Service to retrieve storage configurations.

        Variables:
        - self.electrolyzer_service (ElectrolyzerService): Instance for accessing electrolyzer configs.
        - self.storage_service (StorageService): Instance for accessing storage configs.
        """
        self.electrolyzer_service = electrolyzer_service
        self.storage_service = storage_service

    def optimize(self, input: OptimizationInput) -> OptimizationOutput:
        """Optimize the 24-hour hydrogen production schedule to minimize electricity costs.

        Args:
        - input (OptimizationInput): Pydantic model containing optimization inputs
          (electrolyzer_id, storage_id, electricity_prices, hydrogen_demand).

        Returns:
        - OptimizationOutput: Pydantic model containing the optimized schedule
          (power_schedule, hydrogen_produced, storage_levels, total_cost).

        Variables:
        - electrolyzer (ElectrolyzerConfig): Configuration of the specified electrolyzer.
        - storage (StorageConfig): Configuration of the specified storage.
        - T (int): Number of time periods (24 hours).
        - P_max (float): Maximum power capacity of the electrolyzer (kW).
        - S_min (float): Minimum storage level (0.0 kg).
        - S_max (float): Maximum storage capacity (kg).
        - S_0 (float): Initial storage level (0.0 kg).
        - C_t (list[float]): Electricity prices for each hour (€/kWh).
        - D_t (list[float]): Hydrogen demand for each hour (kg).
        - eta (float): Electrolyzer efficiency (kg H₂/kWh).
        - model (LpProblem): PuLP linear programming model for optimization.
        - P_t (list[LpVariable]): Power input variables for each hour (kW).
        - H_t (list[LpVariable]): Hydrogen production variables for each hour (kg).
        - S_t (list[LpVariable]): Storage level variables for each hour (kg).
        - power_schedule (list[float]): Optimized power inputs for each hour.
        - hydrogen_produced (list[float]): Optimized hydrogen production for each hour.
        - storage_levels (list[float]): Optimized storage levels for each hour.
        - total_cost (float): Total electricity cost for the schedule (€).

        Raises:
        - ValueError: If the optimization fails (e.g., infeasible problem) or if
          electrolyzer_id/storage_id is not found.
        """
        electrolyzer = self.electrolyzer_service.get_config(input.electrolyzer_id)
        storage = self.storage_service.get_config(input.storage_id)

        T = 24
        P_max = electrolyzer.capacity
        S_min = 0.0
        S_max = storage.max_capacity
        S_0 = 0.0
        C_t = input.electricity_prices
        D_t = input.hydrogen_demand
        eta = electrolyzer.efficiency

        model = LpProblem("Hydrogen_Optimization", LpMinimize)

        P_t = [LpVariable(f"P_{t}", 0, P_max) for t in range(T)]
        H_t = [LpVariable(f"H_{t}", 0) for t in range(T)]
        S_t = [LpVariable(f"S_{t}", S_min, S_max) for t in range(T)]

        model += lpSum(C_t[t] * P_t[t] for t in range(T))

        for t in range(T):
            model += H_t[t] == eta * P_t[t]
            model += S_t[t] == (S_0 if t == 0 else S_t[t-1]) + H_t[t] - D_t[t]

        model.solve(PULP_CBC_CMD(msg=0))

        if model.status != LpStatusOptimal:
            raise ValueError("Optimization failed")

        power_schedule = [P_t[t].value() for t in range(T)]
        hydrogen_produced = [H_t[t].value() for t in range(T)]
        storage_levels = [S_t[t].value() for t in range(T)]
        total_cost = sum(C_t[t] * P_t[t].value() for t in range(T))

        return OptimizationOutput(
            power_schedule=power_schedule,
            hydrogen_produced=hydrogen_produced,
            storage_levels=storage_levels,
            total_cost=total_cost,
        )