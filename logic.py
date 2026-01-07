def get_level(points):
    if points < 100:
        return 1
    if points < 250:
        return 2
    if points < 500:
        return 3
    return 4
