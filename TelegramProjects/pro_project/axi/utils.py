import math


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(math.radians(lat1)) *
            math.cos(math.radians(lat2)) *
            math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def find_driver(user_lat, user_lon, drivers):
    nearest_driver = None
    min_distance = float("inf")

    for driver in drivers:
        driver_id, lat, lon = driver

        distance = calculate_distance(user_lat, user_lon, lat, lon)

        if distance < min_distance:
            min_distance = distance
            nearest_driver = driver_id

    return nearest_driver, min_distance

