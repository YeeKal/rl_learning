## policy gradient
**paper**

- [policy_gradient](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf)

优势：  
    - 连续动作
    - 随机策略

**function approximation**

在value_based方法中，由参数$w$对价值函数进行近似表示：
$$\hat{q}(s,a,w)\approx q_{\pi}(s,a)$$
在policy_based方法中，策略$\pi$被描述为一个包含参数$\theta$的函数，即最优策略是由以状态作为输入的网络输出的概率值来决定的：
$$\pi_\theta(s,a)=P(a|s,\theta)\approx\pi(a|s)$$

If the action space is discrete and not too large, then a natural and common kind of parameterization is to form parameterized numerical preferences $h(s,a,\theta)\in R$ for each state–action pair. The actions with the highest preferences in each state are given the highest probabilities of being selected, for example, according to an exponential softmax distribution:
$$\pi(a|s,\theta)=\frac{e^{h(s,a,\theta)}}{\sum_b e^{h(s,b,\theta)}}$$
The action preferences $h$ themselves can be parameterized arbitrarily, by deep neural network or just linear, $h(s,a,\theta)=\theta^Tx(s,a)$

the advantage of parameterizing policies according to the softmax in action preferences:  
- the approximate policy can approach a deterministic policy
- enables the selection of actions with arbitrary probabilities


**objective**

$J(\theta)$: performance measure

在这里神经网络的更新不是依靠误差，而是依靠奖励。梯度上升法最大化目标函数。

1. start value: 在一个完整的序列下，以初始状态的累计奖励值来衡量策略的优势. $V_{\pi_\theta}$ is the true value for $\pi_\theta$, the policy determined by $\theta$. In this discussion the discounting rate $\gamma$ is not included.
$$J_1(\theta)=V_{\pi_\theta}(s_1)=E_{\pi_\theta}[v_1]$$
2. average reward: 在连续环境条件下，不存在某个初始状态。把个体在某时刻下的状态看成各个状态概率分布，则把每一时刻得到的奖励按各状态的概率分布求和：
$$J_{avV}(\theta)=\sum_sd_{\pi_\theta}V_{\pi_\theta}(s)$$
3. average reward per time-step: 每一时间步长下的平均奖励：
$$J_{avR}(\theta)=\sum_sd_{\pi_\theta}(s)\sum_a\pi_\theta(s,a)R^a_s$$

**optimization**

## actor-critic

learn approximations to both policy and value functions.

