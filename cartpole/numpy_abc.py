import time
import numpy as np


# q_table = np.random.uniform(low=0, high=1, size=(6**4, 2)) 
# print(q_table)


# q_table = np.zeros([6**4, 2])
# print(q_table)


# with open('a.npy', 'wb') as f:
#     np.save(f, np.array([1,2,3,4,5]))
#     np.save(f, np.array([1, 3]))
# with open('a.npy', 'rb') as f:
#     a = np.load(f)
#     # b = np.load(f)
#     # print(a, b)
#     print(a)


def draw(x):
    a = []
    for j in range(15) :               #更新图画
        if j == x:
            a.append('o')
        elif j == 14:
            a.append('m')
        else:
            a.append('_')
    interaction = ''.join(a)
    # \r 表示将光标的位置回退到本行的开头位置
    # end = '' 表示不换行
    print('\r{}'.format(interaction), end = '')

# 返回给定间隔内的等间距值。
map = np.arange(5, step= 3)
print(map)

# x = 0
# while(1):
#     x = x + 1

#     print
#     draw(x)
#     time.sleep(0.3)