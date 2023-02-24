from enviroment import Env
from agent import QLearingAgent as QL
import time

LONG = 15                    # 总长度为6
MAZE_PLACE = 15              # 宝藏在第 6 位
MAX_EPISODE = 15                  # 进行15次迭代

agent = QL([0,1])       # 生成QLearn主体的对象，包含left和right
evn = Env(LONG, MAZE_PLACE, render_mode="human")         # 生成测试环境
for episode in range(MAX_EPISODE):
    observation = evn.reset()  # 观察初始环境

    print(observation)

    while(1):
        evn.render()                     # 生成图像
        action = agent.choose_action(observation)
        obs, reward, done, info = evn.step(action)  # 判断当前环境是否到达最后

        if done:                    # 如果到达，则初始化
            interaction = '\n第%s次迭代，共使用步数：%s。'%(episode+1 ,evn.count)
            print(interaction)
            # evn.reset()
            # time.sleep(2)
            break
        # action = agent.choose_action(observation)                        # 获得下一步方向
        # state_after,score,pre_done = evn.get_target(action)        # 获得下一步的环境的实际情况
        # agent.learn(observation,action,score,state_after,pre_done)       # 根据所处的当前环境对各个动作的预测得分和下一步的环境的实际情况更新当前环境的q表
        # evn.update_place(action)                                   # 更新位置
        # observation = state_after                                         # 状态更新
        # evn.render()                                                 # 更新画布

print(agent.q_table)