## Reinforcement Learning

相比与监督学习，强化学习没有训练数据的输出值，但是有奖励值； 相比与无监督学习，除了训练数据还有奖励规则。

- env: environment
- agent: intelligent robot

强化学习八要素：

1. S: state
2. A: action
3. R: reward，个体在$S_t$采取动作$A_t$对应的奖励为$R_{t+1}$
4. $\pi$: policy,策略，即在某一状态下如何选择动作，常以条件概率表示为$\pi(a/s)=P(A_t=a|S_t=s)$，即在状态s时采取动作a的概率
5. v: value, 在策略$\pi$和状态s下，进入下一个状态后的价值，又被称为值函数，表示为$v_\pi(s)$. 事实上值函数代表当前状态的价值，而是否能达到目的还跟未来的状态有关，故当前值函数也跟未来状态的值函数有关:
$$v_\pi(s)=\mathbf{E}_\pi(R_{t+1}+\gamma R_{t+2}+\cdots| S_t=s)$$
6. $\gamma$: reward decay rate, 如果为0，则是贪婪法，即价值只由当前延时奖励决定，如果是1，则所有的后续状态奖励和当前奖励一视同仁。大多数时候，我们会取一个0到1之间的数字，即当前延时奖励的权重比后续奖励的权重大
7. $P^a_{ss'}$: 状态转化模型，在当前状态s采取动作a后撞到下一个状态s‘的概率，虽然大部分问题的的状态转化模型为1.
8. $\epsilon$: exploration rate

## Markov Decision Process

- 状态转化模型：$P_{ss'}^a=E(S_{t+1}=s'|S_t=s,A_t=a)$
- 策略：$\pi(a/s)=P(A_t=a|S_t=s)$
- 价值函数：$v_\pi(s)=E(G_t|S_t=s)=E_\pi(R_{t+1}+\gamma R_{t+2}+\cdots| S_t=s)$
- 动价值作函数：$q_\pi(s,a)=E(G_t|S_t=s,A_t=a)=E_\pi(R_{t+1}+\gamma R_{t+2}+\cdots| S_t=s,A_t=a)$

价值函数表示该状态下的价值，而动作价值函数是在该状态下可能的各个动作的价值，价值函数是由这些动作价值函数的期望共同构成的。

递推关系:

$$v_\pi(s)=\sum_{a\in A}\pi(a/s)q_\pi(s,a)\\
q_\pi(s,a)=R_{t+1}+\gamma\sum_{s'\in S}P_{ss'}^av_\pi(s')\\
v_\pi(s)=\sum_{a\in A}\pi(a/s)(R_{t+1}+\gamma\sum_{s'\in S}P_{ss'}^av_\pi(s'))\\
q_\pi(s,a)=R_{t+1}+\gamma\sum_{s'\in S}P_{ss'}^a\sum_{a\in A}\pi(a'/s')q_\pi(s',a')$$

最优价值函数：
在局部最优的策略下，状态价值函数应局部最大，动作价值函数应局部最大。

$$v_*(s)=\max_{\pi}v_\pi(s)\\
q_*(s,a)=\max_{\pi}q_\pi(s,a)\\
\pi_*(a/s)=
\begin{cases}
0& \text{if } a=\arg \max_{a\in A}q_*(s,a)\\
1& \text{else}
\end{cases}$$

因此值函数便不再是各个值函数的期望，而直接选择最大的值函数。
$$v_*\pi*(s)=\max_a(R_{t+1}+\gamma\sum_{s'\in S}P_{ss'}^av_*(s'))\\
q_*(s,a)=R_{t+1}+\gamma\sum_{s'\in S}P_{ss'}^a\max_{a'}q_\pi(s',a')$$

## Dynamic Programming

- 预测：给定强化学习的6个要素：状态集S, 动作集A, 模型状态转化概率矩阵P, 即时奖励$r$，衰减因子$\gamma$,  给定策略$\pi$， 求解该策略的状态价值函数$v(\pi)$
- 控制：求解最优的价值函数和策略。给定强化学习的5个要素：状态集S, 动作集A, 模型状态转化概率矩阵P, 即时奖励r，衰减因子$\gamma$, 求解最优的状态价值函数$v_*$和最优策略$\pi_*$

对于预测问题，相当策略已知，通过贝尔曼方程迭代可以求得。而对于控制问题，需要不断更新Q表使其收敛，则最优策略也即得出（最有策略依据最大值函数）。策略迭代：根据探索率更新策略。价值迭代：探索率接近0时，依据值函数更新。

## Monte Carlo Methods

不基于模型的强化学习问题，即状态转化概率未知。