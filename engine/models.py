class RouteStop:
    def __init__(self, name, distance_from_start, chargers):
        self.name = name
        self.distance_from_start = distance_from_start
        self.chargers = chargers

class Bus:
    def __init__(self, bus_id, operator, direction, departure_time):
        self.id = bus_id
        self.operator = operator
        self.direction = direction
        self.departure_time = departure_time        

class StationSchedule:
    def __init__(self, station_name):
        self.station_name = station_name
        self.next_available_time = 0
        self.queue = []