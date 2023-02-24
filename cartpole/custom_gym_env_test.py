import gym
class CustomEnv(gym.Env):
    """
    A template to implement custom OpenAI Gym environments
    """
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.__version__ = "0.0.1"
        # 根据自定义环境的需要修改 observation space, low, high and shape values
        self.observation_space = gym.spaces.Box(low=0.0, high=1.0,shape=(3,))
        # 根据自定义环境的需要修改 action space, and dimension
        self.action_space = gym.spaces.Box(4)
        
    def step(self, action):
        # Implement your step method here
        # - Calculate reward based on the action
        # - Calculate next observation
        # - Set done to True if end of episode else set done to False
        # - Optionally, set values to the info dict
        # return (observation, reward, done, info)
        return

    def reset(self):
        # Implement your reset method here
        # return observation
        return

    def render(self, mode='human', close=False):
        return