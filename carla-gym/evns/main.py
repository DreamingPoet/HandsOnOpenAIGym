#!/usr/bin/env python

# Copyright (c) 2019: Jianyu Chen (jianyuchen@berkeley.edu).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import gym
import sys
import numpy as np
import matplotlib.pyplot as plt

try:
    sys.path.append('/home/shy/CARLA_0.9.6/PythonAPI/carla/dist/carla-0.9.6-py3.5-linux-x86_64.egg')
except IndexError:
    pass
import gym_carla
import carla


def select_action(action_number):
    if action_number == 0:
        real_action = [1, -0.2]
    elif action_number == 1:
        real_action = [1, 0]
    elif action_number == 2:
        real_action = [1, 0.2]
    elif action_number == 3:
        real_action = [2, -0.2]
    elif action_number == 4:
        real_action = [2, 0]
    elif action_number == 5:
        real_action = [2, 0.2]
    elif action_number == 6:
        real_action = [3.0, -0.2]
    elif action_number == 7:
        real_action = [3.0, 0]
    elif action_number == 8:
        real_action = [3.0, 0.2]
    return real_action


def discrete_state(obs):
    distance = np.floor(obs['state'][0])
    if distance < -3:
        distance_number = 0
    elif distance == -3:
        distance_number = 1
    elif distance == -2:
        distance_number = 2
    elif distance == -1:
        distance_number = 3
    elif distance == 0:
        distance_number = 4
    elif distance == 1:
        distance_number = 5
    elif distance == 2:
        distance_number = 6
    elif distance == 3:
        distance_number = 7
    else:
        distance_number = 8
    return distance_number


def main():
    # parameters for the gym_carla environment
    params = {
        'number_of_vehicles': 100,
        'number_of_walkers': 0,
        'display_size': 512,  # screen size of bird-eye render
        'max_past_step': 1,  # the number of past steps to draw
        'dt': 0.1,  # time interval between two frames
        'discrete': False,  # whether to use discrete control space
        'discrete_acc': [-3.0, 0.0, 3.0],  # discrete value of accelerations
        'discrete_steer': [-0.2, 0.0, 0.2],  # discrete value of steering angles
        'continuous_accel_range': [-3.0, 3.0],  # continuous acceleration range
        'continuous_steer_range': [-0.3, 0.3],  # continuous steering angle range
        'ego_vehicle_filter': 'vehicle.lincoln*',  # filter for defining ego vehicle
        'port': 2000,  # connection port
        'town': 'Town03_Opt',  # which town to simulate
        'task_mode': 'random',  # mode of the task, [random, roundabout (only for Town03_Opt)]
        'max_time_episode': 1000,  # maximum timesteps per episode
        'max_waypt': 12,  # maximum number of waypoints
        'obs_range': 32,  # observation range (meter)
        'lidar_bin': 0.125,  # bin size of lidar sensor (meter)
        'd_behind': 12,  # distance behind the ego vehicle (meter)
        'out_lane_thres': 2.0,  # threshold for out of lane
        'desired_speed': 10,  # desired speed (m/s)
        'max_ego_spawn_times': 200,  # maximum times to spawn ego vehicle
        'display_route': True,  # whether to render the desired route
        'pixor_size': 64,  # size of the pixor labels
        'pixor': False,  # whether to output PIXOR observation
        'learning_rate': 0.1,
        'discount': 0.9,
        'epsilon': 0.8,
    }

    env = gym.make('carla-v0', params=params)
    env.reset()
    q_table = np.zeros([9, 9])  # 创建一个空的Q值表
    action_number = 7  # 选择初始动作为油门，不转向
    reward_list = []
    for episode in range(10000):

        if np.random.random() > params['epsilon']:
            action = select_action(action_number)
        else:
            action = select_action(np.random.randint(0, 8))
        print("# Episode{} start!".format(episode))
        print("choose_action ", action)
        obs, reward, done, info = env.step(action)  # 根据初始动作观察环境状态，此时done=False
        reward_list.append(reward)
        s = discrete_state(obs)
        print("# the reward is", reward)
        print("# the state distance is", s)
        if not done:
            max_future_q = np.max(q_table[s, :])
            q_table[s, action_number] = (1 - params["learning_rate"]) * q_table[s, action_number] + params[
                "learning_rate"] * (reward + params["discount"] * max_future_q)
            action_number = np.argmax(q_table[s, :])
            print("new_action number",action_number)
        else:
            env.reset()
    return q_table, reward_list


if __name__ == '__main__':
    q_table, reward_list = main()
    print(q_table)