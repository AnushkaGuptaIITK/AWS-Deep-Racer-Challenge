import math

def reward_function(params):
    # Example of rewarding the agent to follow the center line

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.4 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 100.0
    elif distance_from_center <= marker_2:
        reward = 50.0
    elif distance_from_center <= marker_3:
        reward = 5.0
        if speed > 0.5:
            reward *= 0.5
    else:
        reward = 1e-3  # likely crashed/ close to off track

    '''
    Example of using waypoints and heading to make the car point in the right direction
    '''

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering = params['steering_angle']
    left = params['is_left_of_center']

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = (track_direction - heading)
    # if direction_diff > 180:
    #     direction_diff = 360 - direction_diff

    if direction_diff > 0:
        if steering < direction_diff * 0.5:
            reward *= 0.5
        # Penalize the reward if the difference is too large
        DIRECTION_THRESHOLD1 = 10.0
        DIRECTION_THRESHOLD2 = 20.0

        if direction_diff > DIRECTION_THRESHOLD1:
            reward *= 0.6
        if direction_diff > DIRECTION_THRESHOLD2 and distance_from_center >= marker_2:
            reward *= 0.4
            if speed > 0.85:
                reward *= 0.5
    elif direction_diff < 0:
        DIRECTION_THRESHOLD3 = -10.0
        DIRECTION_THRESHOLD4 = -20.0
        if steering > direction_diff * 0.5:
            reward *= 0.5
        # Penalize the reward if the difference is too large
        DIRECTION_THRESHOLD3 = -10.0
        DIRECTION_THRESHOLD4 = -20.0
        if direction_diff < DIRECTION_THRESHOLD3:
            reward *= 0.6
        if direction_diff < DIRECTION_THRESHOLD4 and distance_from_center >= marker_2:
            reward *= 0.4
            if speed > 0.85:
                reward *= 0.5
    if abs(steering) < 0.1 and speed > 1:
        reward *= 1.5

    if steering < 30:
        if left:
            reward *= 1.5
    if steering > 30:
        if left:
            reward *= 0.5

    progress = params['progress']
    steps = params['steps']
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS = 300
    # Initialize the reward with typical value

    # Give additional reward if the car passes every 100 steps faster than expected
    if (steps % 10) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 10:
        reward *= 5.0

    # Exponential reward function
    exp_reward = math.exp(reward)

    return float(exp_reward)
