def calculate_score(
    simulation_result,
    weights
):

    total_wait = simulation_result[
        "total_wait_time"
    ]

    number_of_stops = len([
        event
        for event in simulation_result["timeline"]
        if event["type"] == "charging"
    ])

    stop_penalty = number_of_stops * 5

    score = (
        total_wait
        + stop_penalty
    )

    return score