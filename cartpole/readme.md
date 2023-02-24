配置环境(win10 64)：
    本次采用 python 3.8.10
    用 virtualenv 20.19.0 来管理不同的虚拟环境，不同的虚拟环境下可以包含不同版本的python包
    安装 virtualenv
    pip install virtualenv==20.19.0
    新建环境 openai-gym，会在命令行当前目录下创建 openai-gym-env 虚拟环境文件夹
    在 C:\Users\Administrator 目录执行：
    virtualenv openai-gym-env

    激活 openai-gym-env 环境
    进入环境目录执行 activate：
    cd C:\Users\Administrator\openai-gym-env\scripts
    activate
    
    安装 gym 环境
    pip install gym

    安装 atari 环境包，Atari 提供了⼏个经典 Atari 控制台游戏的接⼝
    pip install gym[atari]

    安装其他必要的包，包括 pygame， zipp 等
    pip install gym[classic_control]



前置知识：
    agent：智能体，也就是机器人，你的代码本身。
    environment：环境，也就是游戏本身，openai gym提供了多款游戏，也就是提供了多个环境。
    action：行动，比如玩超级玛丽，向上向下等动作。
    state：状态，每次智能体做出行动，环境会相应地做出反应，返回一个状态和奖励。
    reward：奖励：根据游戏规则的得分。智能体不知道怎么才能得分，它通过不断地尝试来理解游戏规则，比如它在这个状态做出向上的动作，得分，那么下一次它处于这个环境状态，就倾向于做出向上的动作。

    Spaces: Gym 的仿真环境中，有运动空间 action_space 和观测空间observation_space 两个指标，程序中被定义为 Space类型，用于描述有效的运动和观测的格式和范围。

    episode: 当done 为真时，控制失败，此 episode 结束，一个 episode 可以理解为游戏的一局

    每一个时间步长，Agent 都选择一个action，Environment返回一个observation和reward。
    环境的step 函数返回需要的信息，step 函数返回四个值observation、reward、done、info，下面是具体信息：
        observation (object):一个与环境相关的对象描述你观察到的环境，如相机的像素信息，机器人的角速度和角加速度，棋盘游戏中的棋盘状态。
        reward (float):先前行为获得的所有回报之和，不同环境的计算方式不 一，但目标总是增加自己的总回报。
        terminated (boolean): 判断是否达到“终止状态”，为True表示episode已终止。
        truncated，是否满足MDP范围外的截断条件。通常是时间限制，但也可用于指示代理物理上越界。可用于在达到“终止状态”之前提前结束剧集。
        info (dict):用于调试的诊断信息，有时也用于学习，但正式的评价不允许使用该信息进行学习。 这是一个典型的agent-environment loop 的实现。

    gym的核心接口是Env，作为统一的环境接口。Env包含下面几个核心方法：
        1、reset(self):重置环境的状态，返回观察。
        2、step(self,action):推进一个时间步长，返回observation，reward，done，info
        3、render(self,mode=’human’,close=False):重绘环境的一帧。默认模式一般比较友好，如弹出一个窗口。


    MDP：马尔可夫决策过程



示例 ： cartpole-v0

https://blog.csdn.net/qq_32892383/article/details/89576003

这个游戏的规则是让杆不倒。Openai gym提供了行动的集合，环境的集合等等。Cartpole-v0来说，动作空间包括向左拉和向右拉两个动作。其实你并不需要关心它的动作空间是什么，当你的学习算法越好，你就越不需要解释这些动作。

观测值（observation）含义 [-0.15585865 -0.96372634  0.2372634   1.7114952 ]：
    小车在轨道上的位置（position of the cart on the track）
    杆子与竖直方向的夹角（angle of the pole with the vertical）
    小车速度（cart velocity）
    角度变化率（rate of change of the angle）


游戏奖励（reward）：
    在gym的Cart Pole环境（env）里面，左移或者右移小车的action之后，env会返回一个+1的reward。其中CartPole-v0中到达200个reward之后，游戏也会结束，而CartPole-v1中则为500。最大奖励（reward）阈值可通过前面介绍的注册表进行修改。


运行CartPole-v0环境1000个时间步(timestep)。
``` python
    import gym
    env = gym.make('CartPole-v0')
    env.reset()
    for _ in range(1000):
        env.render()
        env.step(env.action_space.sample())
```
可以看到随机控制算法发散，游戏很快结束。

观察
如果我们想做得好一点，观察周围的环境是必须的。环境的step函数返回四个值：

Observation(object):返回一个特定环境的对象，描述对环境的观察。比如，来自相机的像素数据，机器人的关节角度和关节速度，或棋盘游戏中的棋盘状态。
Reward(float)：返回之前动作收获的总的奖励值。不同的环境计算方式不一样，但总体的目标是增加总奖励。
Done(boolean)：返回是否应该重新设置（reset）环境。大多数游戏任务分为多个环节（episode），当done=true的时候，表示这个环节结束了。
Info(dict)：用于调试的诊断信息（一般没用）。
这是一个典型的“智能体-环境循环”的实现。每个时间步长（timestep），智能体选择一个行动，环境返回一个观察和奖励值。

过程一开始调用reset，返回一个初始的观察。并根据done判断是否再次reset。

``` python
import gym
env = gym.make('CartPole-v0')
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
```



QLearning和DQN

QLearning
https://blog.csdn.net/weixin_43283397/article/details/103228165

QLearning是强化学习中的一种Value-Based算法，通过计算出一张Q-Table表，用来记录每种状态下采取每个动作能够获得的最大奖励，然后通过这张表就能找到每个状态下的最优动作，从而保证最后的收益最大化
参数：
actions：所有动作集合
learning_rate：学习率， 位于[0,1]之间，值越小，意味着旧的信息越重要
discount_factor：折扣因子，位于[0,1]之间，表示远见程度，值越小，意味着当下的奖励越比未来的奖励重要
epsilon：贪婪系数，位于[0,1]之间，采用贪心策略的概率
q_table：Q-Table表，用来记录每种状态下采取每个动作能够获得的最大奖励，初持状态全部为0


QLearning是强化学习算法中value-based的算法，Q即为Q（s,a）就是在某一时刻的 s 状态下(s∈S)，采取 动作a (a∈A)动作能够获得收益的期望，环境会根据agent的动作反馈相应的回报reward r，所以算法的主要思想就是将State与Action构建成一张Q-table来存储Q值，然后根据Q值来选取能够获得最大的收益的动作。

| Q-Table| 	a1| 	a2| 
|  ----  | ----  | ----  |
| s1 | 	q(s1,a1) | 	q(s1,a2) | 
| s2 | 	q(s2,a1) | 	q(s2,a2) | 
| s3 | 	q(s3,a1) | 	q(s3,a2) | 

Q_learning算法理解
    建立Q表，行是每种状态，列是每种状态的行为，值是某状态下某行为估计获得的奖励
    每次进行状态转移时有e_greedy概率选当前状态最优方法，有 1- e_greedy选随机方法
    选完之后就更新当前状态下对应所选行为的Q值（估计值）
    更新方法：其自身= 其自身+学习率*（估计-现实） —> (实际更新 = 实际未更新+学习率*（预测-实际发生）)


DQN（Deep Q Network）
QLearning问题：Q-Table的大小等于状态数量*动作数量。当状态和动作数量很多的时候，Q-Table就会变的很大，查找和存储都会消耗大量的时间和空间。
QLearning本质上是建立了个（状态+动作）与（在该状态下执行该动作所获得最大奖励）之间的映射关系，抽象来看就是在输入参数和输出参数之间建立了一种映射关系，而这恰好就是神经网络所擅长的，于是自然而然的想到能不能利用神经网络来取代Q函数的计算，进一步的，我们计算出Q-Table后还需要根据Q-Table来选择当前状态下的最优动作，那能不能直接实现当前状态到最优动作之间的端到端映射呢？这种方法就叫做Deep Q Network。

具体：
QLearning：Q(s,a)=Q(s,a)+alpha*[r+gammamaxQ(s’,a’)-Q(s,a)]
求解出一个函数来近似Q函数
f(s,a,w)≈Q(s,a)，w是一个参数矩阵，比如最简单的线性函数：
Q(s,a) ≈f(s,a,w)= w1s+w2a+w3
实际不可能这么简单，f应该是一个非常复杂的函数，所以可以采用神经网络来表示这个函数，神经网络可以从大量的样本数据中拟合出一个最相似的f来表示Q，而这需要一个前置条件：确定损失函数（判定f接近Q的标准）
借鉴QLearning的算法，利用r+gammamaxQ(s’,a’)-Q(s,a)来作为损失函数（因为我们的目标也是为了让Q值逼近目标Q值），即
r+gammamaxQ(s’,a’,w)-Q(s,a,w)
为了方便后期数学计算的方便，取个平方，最终
L(w)=E[(r+gammamaxQ(s′,a′,w)−Q(s,a,w))^2]
有了损失函数，那么就可以开始训练神经网络了

DQN与QLearning算法的不同点
用神经网络取代Q-Table来计算Q值，解决维度爆炸的问题
记忆库 ，用于存储过去的经验，记忆库有两个特点
1. 随机抽取，可以移除数据之间的相关性。如果我们采用的不是随机抽取，有可能我们获取到的数据都是连续相关的，那么就可能出现训练的数据都是某个状态下的数据，那么训练就会失败，通过随机抽取，可以切断这种相关性，保证训练数据样本分布的均匀。
2. 滚动更新，即用最新的记忆替换掉最老的记忆，因为我们的记忆库肯定是有限的，不可能无限存储记忆，因此需要对记忆进行更新，而正常的逻辑里面，新的记忆会比老的记忆更有价值（当然，这个并不是绝对的，也有可能老的记忆里面也有重要的经验，这个属于DQN后期的优化内容）
暂时冻结 q_target 参数 ，让目标固定，使神经网络更好的收敛






OpenAI Gym Environment 结构组成


继承 gym.Env 类
实现 reset和step ⽅法
修改 observation_space 和 action_space 属性
该将其注册到 OpenAI Gym 注册表，以便我们可以使⽤gym.make(ENV_NAME)创建环境实例：
``` python
from gym.envs.registration import register
register(
 id='CustomEnv-v0',
 entry_point='custom_environments.envs:CustomEnv',
)
```


以及其他可选实现的⽅法：

|  方法   | 方法描述  |
|  ----  | ----  |
| observation_space  | 环境返回的观测值(observation)的形状和类型 |
| action_space  | 环境接受的动作(action)的形状和类型 |
|  reset()  | 在剧集开始或结束时重置环境  |
|  step(...)  | 步进（推进游戏，或者仿真进行下一步）。在环境中应用选择的动作，计算奖励，产生下一个观察结果，并确定一个事件是否已经结束  |
|  _render()  | (可选) 这呈现了 Gym 环境的状态或观察  |
|  _close()  | (可选) 关闭 Gym 环境.  |
|  _seed  | (可选)这为 Gym 环境中的随机函数播种了一个使环境以可重现的方式运行的自定义种子给的种子。  |
|  _configure  | (可选) 这会启用额外的环境配置  |