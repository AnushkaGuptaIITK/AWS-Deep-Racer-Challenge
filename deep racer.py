import math

def reward_function(params):
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering = params['steering_angle']
    left = params['is_left_of_center']
    progress = params['progress']
    steps = params['steps']
    objects_location = params['objects_location']
    agent_x = params['x']
    agent_y = params['y']
    _, next_object_index = params['closest_objects']
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']

    # Initialize reward with a small number
    reward = 1e-3

    # SECTION 1: Reward for staying close to the center
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.4 * track_width

    if distance_from_center <= marker_1:
        reward = 100.0
    elif distance_from_center <= marker_2:
        reward = 50.0
    elif distance_from_center <= marker_3:
        reward = 5.0
        if speed > 0.5:
            reward *= 0.5
    else:
        reward = 1e-3  # likely crashed or close to off-track

    # SECTION 2: Reward for staying on track
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward += 1.0

    # SECTION 3: Reward based on direction alignment
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction of the track (angle) and difference to car heading
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)
    direction_diff = track_direction - heading

    # Penalize the reward if the direction difference is too large
    DIRECTION_THRESHOLD1 = 10.0
    DIRECTION_THRESHOLD2 = 20.0

    if abs(direction_diff) > DIRECTION_THRESHOLD1:
        reward *= 0.6
    if abs(direction_diff) > DIRECTION_THRESHOLD2 and distance_from_center >= marker_2:
        reward *= 0.4
        if speed > 0.85:
            reward *= 0.5

    # SECTION 4: Reward for smooth steering
    if abs(steering) < 0.1 and speed > 1:
        reward *= 1.5

    # Penalize for high steering angle when left or right
    if steering < 30 and left:
        reward *= 1.5
    elif steering > 30 and left:
        reward *= 0.5

    # SECTION 5: Progress reward
    TOTAL_NUM_STEPS = 300
    if (steps % 10) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 10:
        reward *= 5.0

    # SECTION 6: Avoid objects
    next_object_loc = objects_location[next_object_index]
    distance_closest_object = math.sqrt((agent_x - next_object_loc[0])**2 + (agent_y - next_object_loc[1])**2)
    is_same_lane = objects_left_of_center[next_object_index] == is_left_of_center

    if is_same_lane:
        if 0.5 <= distance_closest_object < 0.8:
            reward *= 0.5
        elif 0.3 <= distance_closest_object < 0.5:
            reward *= 0.2
        elif distance_closest_object < 0.3:
            reward = 1e-3  # Likely crashed

    # SECTION 7: Apply exponential scaling to the reward
    exp_reward = math.exp(reward)

    # Return the final reward
    return float(exp_reward)

