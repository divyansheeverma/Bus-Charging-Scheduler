# engine/simulator.py

from engine.utils import (
    format_time
)

def parse_time(time_str):

    hours, minutes = map(
        int,
        time_str.split(":")
    )

    return hours * 60 + minutes


# def format_time(total_minutes):

#     total_minutes = total_minutes % (24 * 60)

#     hours = total_minutes // 60

#     minutes = total_minutes % 60

#     return f"{hours:02}:{minutes:02}"


def minutes_between(distance_km, speed_kmph):

    hours = distance_km / speed_kmph

    return int(hours * 60)


def simulate_plan(
    bus,
    charging_plan,
    route,
    constants,
    station_manager
):

    speed = constants["speed_kmph"]

    charge_time = constants["charge_time_min"]

    stops = route["stops"]

    stop_map = {
        stop["name"]: stop
        for stop in stops
    }

    current_time = parse_time(
        bus["departure_time"]
    )

    timeline = []

    total_wait_time = 0

    # =====================================================
    # BUILD FULL TRAVEL PATH
    # =====================================================

    if bus["direction"] == "forward":

        path = (
            ["Bengaluru"]
            + charging_plan
            + ["Kochi"]
        )

    else:

        reversed_plan = list(
            reversed(charging_plan)
        )

        path = (
            ["Kochi"]
            + reversed_plan
            + ["Bengaluru"]
        )

    # =====================================================
    # TRAVEL THROUGH PATH
    # =====================================================

    for i in range(len(path) - 1):

        current_stop = path[i]

        next_stop = path[i + 1]

        current_distance = stop_map[
            current_stop
        ]["distance_from_start"]

        next_distance = stop_map[
            next_stop
        ]["distance_from_start"]

        travel_distance = abs(
            next_distance - current_distance
        )

        travel_minutes = minutes_between(
            travel_distance,
            speed
        )

        arrival_time = (
            current_time
            + travel_minutes
        )

        # =================================================
        # DESTINATION REACHED
        # =================================================

        if next_stop in ["Bengaluru", "Kochi"]:

            timeline.append({
                "type": "arrival",
                "location": next_stop,
                "time": format_time(arrival_time)
            })

            current_time = arrival_time

            continue

        # =================================================
        # CHARGING STATION
        # =================================================

        station_free_time = (
            station_manager.get_next_available_time(
                next_stop
            )
        )

        # First bus at station
        if station_free_time is None:

            charge_start_time = arrival_time

        else:

            charge_start_time = max(
                arrival_time,
                station_free_time
            )

        wait_minutes = (
            charge_start_time
            - arrival_time
        )

        total_wait_time += wait_minutes

        charge_end_time = (
            charge_start_time
            + charge_time
        )

        # =================================================
        # OCCUPY CHARGER
        # =================================================

        station_manager.occupy_station(
            station_name=next_stop,
            start_time=charge_start_time,
            end_time=charge_end_time,
            bus_id=bus["id"]
        )

        timeline.append({
            "type": "charging",

            "station": next_stop,

            "arrival_time":
                format_time(arrival_time),

            "charge_start":
                format_time(charge_start_time),

            "charge_end":
                format_time(charge_end_time),

            "wait_minutes": wait_minutes
        })

        # Bus leaves after charging
        current_time = charge_end_time

    # =====================================================
    # FINAL RESULT
    # =====================================================

    return {
        "bus_id": bus["id"],

        "timeline": timeline,

        "total_wait_time": total_wait_time,

        "final_arrival_time":
            format_time(current_time)
    }