## DQN

- [DQN NIPS 2013](https://arxiv.org/pdf/1312.5602.pdf)
- [DQN NIPS 2015](http://web.stanford.edu/class/psych209/Readings/MnihEtAlHassibis15NatureControlDeepRL.pdf)
- [DDQN](https://link.zhihu.com/?target=http%3A//www.aaai.org/ocs/index.php/AAAI/AAAI16/paper/download/12389/11847)
- [Prioritized Replay DQN](https://arxiv.org/pdf/1511.05952.pdf)
- [Dueling DQN](https://arxiv.org/pdf/1511.06581.pdf)

对于参数较多的或连续S/A的问题，用离散的Q表来存储显得不太现实。故考虑用神经网络拟合出Q(S,A).

神经网络的参数更新依赖于损失函数，损失函数定义为当前Q值与预测Q之间的误差。当网络参数收敛时，当前和预测值之间误差为0.

经验回放

伪代码

## Nature DQN

## DDQN

## Prioritized Replay DQN

## Dueling DQN