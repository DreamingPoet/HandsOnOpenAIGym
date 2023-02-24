

import numpy as np
import pandas as pd
import time 

# 说明，地图隐藏有个宝藏，玩家每次进行左右移动搜索，直到找到则获得1分的奖励
# 每次获得奖励
# observation(int) : maze_position - player_position
# action(int) : 0 - left, 1 - right

class Env:
    def __init__(self, map_size, maze_position, render_mode = None ):
        """Compute the render frames as specified by render_mode attribute during initialization of the environment.

        Args:
            map_size (int): 地图尺寸
            maze_position (int): 宝藏所在位置
            render_mode (optional str): None / human / array
                - None (default): no render is computed.
                - human: render return None.
                    The environment is continuously rendered in the current display or terminal. Usually for human consumption.
                - array: render return None.
                    The environment is continuously rendered in the current display or terminal. Usually for human consumption.

        Returns:
            observation (object): Observation of the initial state. This will be an element of :attr:`observation_space`
                (typically a numpy array) and is analogous to the observation returned by :meth:`step`.
            info (dictionary):  This dictionary contains auxiliary information complementing ``observation``. It should be analogous to
                the ``info`` returned by :meth:`step`.

        Note:
            Make sure that ... ...
        """
        self.render_mode = render_mode
        self.map_size = map_size               # 表示地图的长度
        self.maze_position = maze_position - 1          # 宝藏所在的位置
        self.player_position = 0                    # 初始化玩家位置
        # map = [0, 1, 2, 3 ...]
        self.map = np.arange(map_size)              # 给予每个地点一个标号
        self.count = 0                              # 一共走了多少步
        

    def render(self):
        if self.render_mode == "human":
            a = []
            for j in range(self.map_size) :               #更新图画
                if j == self.player_position:
                    a.append('o')
                elif j == self.maze_position:
                    a.append('m')
                else:
                    a.append('_')
            interaction = ''.join(a)
            print('\r{}'.format(interaction),end = '')
            time.sleep(0.3)
        elif self.render_mode == "array":
            pass
        elif self.render_mode == None:
            pass
        

    def reset(self):
        """Compute the render frames as specified by render_mode attribute during initialization of the environment.

        Args:
            map_size (int): 地图尺寸
            maze_position (int): 宝藏所在位置
            render_mode (optional str): None / human / array
                - None (default): no render is computed.
                - human: render return None.
                    The environment is continuously rendered in the current display or terminal. Usually for human consumption.
                - array: render return None.
                    The environment is continuously rendered in the current display or terminal. Usually for human consumption.

        Returns:
            observation (object): Observation of the initial state. This will be an element of :attr:`observation_space`
                (typically a numpy array) and is analogous to the observation returned by :meth:`step`.
            info (dictionary):  This dictionary contains auxiliary information complementing ``observation``. It should be analogous to
                the ``info`` returned by :meth:`step`.

        Note:
            Make sure that ... ...
        """
        self.player_position = 0
        self.count = 0
        return self.map[self.player_position] # 返回现在在所


    def step(self, action):
        self._update_place(action) # 更新位置
        return (self._get_obs(), self._get_reward(action), self._terminal(), {})

    def _get_obs(self):
        """ 获取观测值 """
        return None

    def _terminal(self) -> bool:
        """ 判断是否到底结束状态 """
        if self.player_position >= self.maze_position:              #如果得到了宝藏，则返回已经完成
            done = True
        else:
            done = False
        return done

    def _get_reward(self, action) -> int:
        """ 获取分数奖励 """
        if action == 'right':                        #获得下一步的环境的实际情况
            if self.player_position + 1 == self.maze_position:
                score = 1
                pre_done = True
            else:
                score = 0
                pre_done = False
            return self.map[self.player_position + 1],score,pre_done
        elif action == 'left':   #left
            if self.player_position - 1 == self.maze_position:
                score = 1
                pre_done = True
            else:
                score = 0
                pre_done = False
            return score


    def _update_place(self, action):
        self.count += 1                              #更新的时候表示已经走了一步
        if action == 1:                                  
            if self.player_position < self.map_size - 1:
                self.player_position += 1
        elif action == 0:   #left
            if self.player_position > 0:
                self.player_position -= 1