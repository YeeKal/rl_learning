
'''
refer: https://github.com/MorvanZhou/train-robot-arm-from-scratch
@desc: use ddpg to train a 2-link robot to reach the goal
@date: 2019-04-22
'''

from ddpg import DDPG
from env_two_arm import TwoArms
import time
import numpy as np
import sys

#global variables
MAX_EPISODES=900
MAX_STEPS=200
TEST_STEPS=5

env=TwoArms()
s_dim=env.state_dim
a_dim=env.action_dim
a_bound=env.action_bound

rl=DDPG(s_dim,a_dim,a_bound)
var = 3

def train():
    for episode in range(MAX_EPISODES):
        s=env.reset()
        ep_reward=0
        for j in range(MAX_STEPS):
            env.render()
            a=rl.choose_action(s)
            #a = np.clip(np.random.normal(a, var), -2, 2)
            s_,r,done=env.step(a)

            rl.store_transition(s,a,r,s_)
            if rl.memoryFull():
                #var *= .9995 
                rl.learn()
            
            s=s_
            ep_reward += r
            if done or j == MAX_STEPS-1:
                print('Episode:', episode, ' Reward: %f' % int(ep_reward),'Step:%d'%j )
                break
    rl.save()

def test():
    rl.restore()
    env.viewer.set_vsync(True)
    state = env.reset()
    while True:
        env.render()
        action = rl.choose_action(state) # direct action for test
        state,reward,done= env.step(action)
        time.sleep(0.05)



if __name__ == '__main__':
    t1=time.time()
    if len(sys.argv)==1:
        train()
        sys.exit(0)
    command=sys.argv[1]
    if command=='train':
        train()
    elif command=='test':
        test()
    print('Running time: ', time.time() - t1)
    input("any key to quit:")




'''
1. not converge
2. not stop on goal

reward engineering
feature engineering

solution:
1. continuous reward
2. add features

the scale of features should be in the same order of magnitudes
'''
    
