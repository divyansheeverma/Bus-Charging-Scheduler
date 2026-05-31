import copy


class StationManager:

    def __init__(self, route):

        self.stations = {}

        for stop in route["stops"]:

            if stop["chargers"] > 0:

                self.stations[stop["name"]] = {
                    "next_available_time": None,
                    "schedule": []
                }

    def get_next_available_time(self, station_name):

        return self.stations[station_name][
            "next_available_time"
        ]

    def occupy_station(
        self,
        station_name,
        start_time,
        end_time,
        bus_id
    ):

        self.stations[station_name][
            "next_available_time"
        ] = end_time

        self.stations[station_name][
            "schedule"
        ].append({
            "bus_id": bus_id,
            "start": start_time,
            "end": end_time
        })
    def get_station_schedules(self):

        return self.stations    

    def clone(self):

        return copy.deepcopy(self)