ZONE_GROUPS = {

    1: [1,2],

    2: [1,2],

    3: [3,4],

    4: [3,4]

}


def score_order(current, candidate, route):

    score = 0

    if candidate.zone in ZONE_GROUPS[current.zone]:
        score += 50

    if candidate.temperature == current.temperature:
        score += 40

    if candidate.customer == current.customer:
        score += 20

    if candidate.destination == current.destination:
        score += 25

    if route.total_pallets + candidate.pallets > 53:
        score -= 100

    return score