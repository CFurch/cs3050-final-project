import math


def euclidean_distance(point1, point2):
    """
    for use in several functions to calculate the pixel distance
    :param point1: (x, y) both integers
    :param point2: (x, y)
    :return: float distance between points
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def calculate_direction_vector_positive(facing_direction):
    # Calculate the angle in radians
    angle_radians = math.atan2(facing_direction[1], facing_direction[0])
    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def calculate_direction_vector_negative(facing_direction):
    # Calculate the angle in radians
    angle_radians = math.atan2(facing_direction[1], facing_direction[0])
    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees % 360


def is_within_facing_direction(self_position, self_facing_direction, target_position, swath_degrees=30):
    # Calculate the turret's direction in radians
    turret_direction_radians = math.radians(self_facing_direction)

    # Calculate the vector from the turret position to the target position
    dx = target_position[0] - self_position[0]
    dy = target_position[1] - self_position[1]

    # Calculate the angle between the turret's direction vector and the vector to the target
    angle_to_target = math.atan2(dy, dx)

    # Convert the angle to be between -π and π
    angle_diff = (angle_to_target - turret_direction_radians + math.pi) % (2 * math.pi) - math.pi

    # Convert the angle to degrees
    angle_diff_degrees = math.degrees(angle_diff)

    # Check if the absolute angle difference is within the swath degrees
    return abs(angle_diff_degrees) <= swath_degrees

