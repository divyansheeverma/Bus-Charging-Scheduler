# test.py

from engine.scheduler import Scheduler
from engine.utils import (
    load_scenario,
    format_time
)


# =====================================================
# LOAD SCENARIO
# =====================================================

scenario = load_scenario(
    "scenarios/scenario_1.json"
)

# =====================================================
# RUN SCHEDULER
# =====================================================

scheduler = Scheduler(scenario)

results = scheduler.run()

# =====================================================
# PRINT BUS RESULTS
# =====================================================

for bus_id, result in results.items():

    print("\n" + "=" * 60)

    print(f"BUS: {bus_id}")

    print(f"PLAN: {result['plan']}")

    print(f"SCORE: {result['score']}")

    simulation = result["simulation"]

    print(
        f"FINAL ARRIVAL: "
        f"{simulation['final_arrival_time']}"
    )

    print(
        f"TOTAL WAIT: "
        f"{simulation['total_wait_time']} mins"
    )

    print("\nTIMELINE:")

    for event in simulation["timeline"]:

        if event["type"] == "charging":

            print(
                f"  Station {event['station']} | "
                f"Arrive: {event['arrival_time']} | "
                f"Start: {event['charge_start']} | "
                f"End: {event['charge_end']} | "
                f"Wait: {event['wait_minutes']} mins"
            )

        elif event["type"] == "arrival":

            print(
                f"  Arrived at "
                f"{event['location']} "
                f"at {event['time']}"
            )

# =====================================================
# PRINT STATION SCHEDULES
# =====================================================

print("\n" + "=" * 60)
print("STATION SCHEDULES")
print("=" * 60)

station_data = (
    scheduler.station_manager.get_station_schedules()
)

for station_name, station_info in station_data.items():

    print(f"\nSTATION: {station_name}")

    for session in station_info["schedule"]:

        print(
            f"  {session['bus_id']} | "
            f"{format_time(session['start'])} "
            f"-> "
            f"{format_time(session['end'])}"
        )