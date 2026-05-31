
from itertools import combinations

from engine.simulator import simulate_plan
from engine.scorer import calculate_score
from engine.station_manager import StationManager


class Scheduler:

    def __init__(self, scenario):

        self.scenario = scenario

        self.route = scenario["route"]
        self.buses = scenario["buses"]
        self.constants = scenario["constants"]
        self.weights = scenario["weights"]

        self.max_range = self.constants["battery_range_km"]

        self.stops = self.route["stops"]

        # Only charging stations
        self.charging_stations = [
            stop for stop in self.stops
            if stop["chargers"] > 0
        ]

        # Map:
        # {
        #   "A": 100,
        #   "B": 220
        # }
        self.stop_distances = {
            stop["name"]: stop["distance_from_start"]
            for stop in self.stops
        }
        # keep station manager on the instance for later use
        self.station_manager = StationManager(
            self.route
        )

    # =========================================================
    # MAIN ENTRY
    # =========================================================

    def run(self):

        final_results = {}
        sorted_buses = sorted(

            self.buses,
            key=lambda bus: bus["departure_time"]
        )

        for bus in sorted_buses:

            valid_plans = self.generate_valid_plans(bus)
            best_result = None

            best_score = float("inf")


            for plan in valid_plans:
                temp_manager = self.station_manager.clone()

                simulation_result = simulate_plan(
                    bus=bus,
                    charging_plan=plan,
                    route=self.route,
                    constants=self.constants,
                    station_manager=temp_manager
                )

                score = calculate_score(
                    simulation_result=simulation_result,
                    weights=self.weights
                )

                if score < best_score:
                    best_score = score
                    best_result = {
                        "plan": plan,
                        "simulation": simulation_result,
                        "score": score
                    }
                    best_manager_state = temp_manager

            self.station_manager = best_manager_state

            final_results[bus["id"]] = best_result

        return final_results

    # =========================================================
    # GENERATE VALID CHARGING PLANS
    # =========================================================

    def generate_valid_plans(self, bus):

        station_names = [
            station["name"]
            for station in self.charging_stations
        ]

        valid_plans = []

        # Generate combinations:
        # 1 stop
        # 2 stops
        # 3 stops
        # 4 stops
        for r in range(1, len(station_names) + 1):

            possible_combinations = combinations(
                station_names,
                r
            )

            for combo in possible_combinations:

                plan = list(combo)

                if self.is_valid_plan(plan, bus):
                    valid_plans.append(plan)

        return valid_plans

    # =========================================================
    # CHECK IF PLAN IS VALID
    # =========================================================

    def is_valid_plan(self, plan, bus):

        if bus["direction"] == "forward":

            start_distance = 0

            end_distance = self.stop_distances["Kochi"]

            full_path = ["START"] + plan + ["END"]

            distances = []

            for point in full_path:

                if point == "START":
                    distances.append(start_distance)

                elif point == "END":
                    distances.append(end_distance)

                else:
                    distances.append(
                        self.stop_distances[point]
                    )

        else:

            # Reverse route:
            # Kochi -> D -> C -> B -> A -> Bengaluru

            total_route_distance = self.stop_distances["Kochi"]

            reversed_plan = list(reversed(plan))

            full_path = ["START"] + reversed_plan + ["END"]

            distances = []

            for point in full_path:

                if point == "START":
                    distances.append(total_route_distance)

                elif point == "END":
                    distances.append(0)

                else:
                    distances.append(
                        self.stop_distances[point]
                    )

        # Validate every jump
        for i in range(len(distances) - 1):

            current_distance = distances[i]
            next_distance = distances[i + 1]

            travel_distance = abs(
                next_distance - current_distance
            )

            if travel_distance > self.max_range:
                return False

        return True

    # =========================================================
    # PICK BEST PLAN
    # =========================================================

    def choose_best_plan(self, evaluations):

        if not evaluations:
            return None

        best = min(
            evaluations,
            key=lambda x: x["score"]
        )

        return best
    