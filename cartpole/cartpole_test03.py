import gym
import numpy as np

#定义一些常量
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
# 游戏名称：CartPole-vo 也就是我们的平衡倒立摆
ENV = 'CartPole-v0'
# 离散化区间.小车的状态是有无限多钟，但我们的Q表格里只能表示有限的映射关系。所以将原先连续的一个状态，分为6个区间。
NUM_DIGITIZED = 6
# GAMMA就是Q学习中的折扣率（0~1），用以表示智能体对长期回报的看法。GAMMA为0，表示只看当前的回报。GAMMA为1，则是极其重视长期回报。
GAMMA = 0.99 
# 学习率。ETA越大，则进行每一步更新时，受reward影响更多。
ETA = 0.5 
# 假如连续控制200次，游戏还没结束，视为成功通关。
MAX_STEPS = 200
# 总共进行2000次训练。（不一定会训练2000次，详情见env.run，有详解。）
NUM_EPISODES = 2000 



#定义Brain类，智能体与环境交互的主要实现途径。
class Brain:
    #num_states为4，代表着Cart的位置和速度，Pole的角度和角速度四种状态变量。num_action为2，分别为向左和向右。
    #这俩个参数从环境env中获取，然后传入Brain.
    def  __init__(self, num_states = 4, num_actions = 2):
        self.num_actions = num_actions 
        #创建一个Q表格，也就是我们的Q函数。这里是一个(6^4,2)格式的矩阵。
        #其中所有数字为0~1的随机数。这是一种启动方式，也可以全部为0。毕竟只是初始化一个表格，最终都能通过学习收敛。当然，如果通过设置初始化值
        #加快收敛速度，也是一个研究方向。
        self.q_table = np.random.uniform(low=0, high=1, size=(NUM_DIGITIZED**num_states, num_actions)) 

        q_table = np.zeros([9, 9])

env = gym.make('CartPole-v0', render_mode="human")

# 玩20局并记录每一局结束时，操作了多少歩
for i_episode in range(20):
    # 每一局游戏开始都，重置环境
    observation = env.reset()
    # 如果操作了 100 歩，游戏还没结束，该局结束
    for t in range(100):
        env.render()
        action = env.action_space.sample() # 随机操作
        observation, reward, done, _,info = env.step(action)
        print(reward)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break