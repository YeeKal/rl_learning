Q learning algorithm:

1. initialize $Q$-values($Q(s,a)$) arbitrarity for all state-action pairs.
2. For the life or unitil learning is stopped...
    - Choose an action $(a)$ in the current world state $(s)$ based on current Q-value estimates $(Q(s,:))$.
    - Take the action $(a)$ and observe the outcome state $(s')$ and reward $(r)$.
    - Update $Q(s,a):=Q(s,a)+\alpha[r+\gamma \max_{a'}Q(s',a')-Q(s,a)]$


