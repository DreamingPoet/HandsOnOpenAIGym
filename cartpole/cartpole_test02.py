import gym
env = gym.make('CartPole-v0', render_mode="human")

# 玩20局并记录每一局结束时，操作了多少歩
for i_episode in range(20):
    # 每一局游戏开始都，重置环境
    observation = env.reset()
    # 如果操作了 100 歩，游戏还没结束，该局结束
    for t in range(100):
        env.render()
        # print(observation)
        action = env.action_space.sample() # 随机操作
        observation, reward, done, _,info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break