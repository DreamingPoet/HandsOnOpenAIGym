import gym
env = gym.make('CartPole-v1', render_mode="human")
env.reset()

# 游戏渲染 100 帧就结束
for _ in range(100):
    # 渲染 1 帧画面
    env.render()
    # 获取一个随机 action
    action = env.action_space.sample()
    # 用该 action 来驱动环境中的动态对象
    env.step(action)
    