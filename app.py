import os
import pandas as pd
import streamlit as st

from engine.scheduler import Scheduler
from engine.utils import (
    load_scenario,
    format_time
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Bus Charging Scheduler",
    layout="wide"
)

st.title("🚌 Bus Charging Scheduler")

# =====================================================
# SCENARIO DROPDOWN
# =====================================================

scenario_files = sorted(
    os.listdir("scenarios")
)

selected_scenario = st.selectbox(
    "Select Scenario",
    scenario_files
)

# =====================================================
# LOAD SCENARIO
# =====================================================

scenario_path = os.path.join(
    "scenarios",
    selected_scenario
)

scenario = load_scenario(
    scenario_path
)

# =====================================================
# SHOW SCENARIO INFO
# =====================================================

st.header("Scenario Input")

buses_df = pd.DataFrame(
    scenario["buses"]
)

st.dataframe(
    buses_df,
    use_container_width=True
)

# =====================================================
# RUN SCHEDULER
# =====================================================

scheduler = Scheduler(scenario)

results = scheduler.run()

# =====================================================
# BUS TIMELINES
# =====================================================

st.header("Per Bus Timelines")

for bus_id, result in results.items():

    with st.expander(f"{bus_id}"):

        st.write(f"### Charging Plan")
        st.write(result["plan"])

        st.write(f"### Score")
        st.write(result["score"])

        simulation = result["simulation"]

        st.write(f"### Final Arrival")
        st.write(
            simulation["final_arrival_time"]
        )

        st.write(f"### Total Wait")
        st.write(
            f"{simulation['total_wait_time']} mins"
        )

        timeline_rows = []

        for event in simulation["timeline"]:

            if event["type"] == "charging":

                timeline_rows.append({
                    "Station":
                        event["station"],

                    "Arrival":
                        event["arrival_time"],

                    "Charge Start":
                        event["charge_start"],

                    "Charge End":
                        event["charge_end"],

                    "Wait (mins)":
                        event["wait_minutes"]
                })

            elif event["type"] == "arrival":

                timeline_rows.append({
                    "Station":
                        event["location"],

                    "Arrival":
                        event["time"],

                    "Charge Start":
                        "-",

                    "Charge End":
                        "-",

                    "Wait (mins)":
                        "-"
                })

        timeline_df = pd.DataFrame(
            timeline_rows
        )

        st.dataframe(
            timeline_df,
            use_container_width=True
        )

# =====================================================
# STATION SCHEDULES
# =====================================================

st.header("Station Charging Schedules")

station_data = (
    scheduler.station_manager
    .get_station_schedules()
)

for station_name, station_info in station_data.items():

    st.subheader(f"Station {station_name}")

    rows = []

    for session in station_info["schedule"]:

        rows.append({
            "Bus ID":
                session["bus_id"],

            "Charge Start":
                format_time(session["start"]),

            "Charge End":
                format_time(session["end"])
        })

    station_df = pd.DataFrame(rows)

    st.dataframe(
        station_df,
        use_container_width=True
    )