import json

def load_scenario(path):
    with open(path, "r") as f:
        return json.load(f)
def format_time(total_minutes):

    total_minutes = total_minutes % (24 * 60)

    hours = total_minutes // 60

    minutes = total_minutes % 60

    return f"{hours:02}:{minutes:02}"        