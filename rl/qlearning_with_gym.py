'''
https://github.com/simoninithomas/Deep_reinforcement_learning_Course/blob/master/Q%20learning/FrozenLake/Q%20Learning%20with%20FrozenLake.ipynb
'''

import numpy as np
import gym
import random

#hyperpaameters
total_episodes=15000
learning_rate=0.8
max_steps=99
gamma=0.95      #discounting rate

# Exploration parameters
epsilon = 1.0                 # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.01            # Minimum exploration probability 
decay_rate = 0.005             # Exponential decay rate for exploration prob

env = gym.make("FrozenLake-v0")

action_size=env.action_space.n
state_size=env.observation_space.n
qtable=np.zeros((state_size,action_size))
print(qtable)

rewards=[]

for episode in range(total_episodes):
    state=env.reset()
    step=0
    done=False
    total_rewards=0

    for step in range(max_steps):
        #choose an action
        exp_exp_tradeoff=random.uniform(0,1)

        if exp_exp_tradeoff>epsilon:
            action=np.argmax(qtable[state,:])
        else:#else doing a random choice
            action=env.action_space.sample()
        new_state,reward,done,info=env.step(action)
        #update q-table

        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        # qtable[new_state,:] : all the actions we can take from new state
        qtable[state,action]=qtable[state,action]+learning_rate*(reward+gamma*np.max(qtable[new_state, :]) - qtable[state, action])

        total_rewards +=reward
        state=new_state
        if done==True:
            break
    # Reduce epsilon (because we need less and less exploration)
    epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode) 
    rewards.append(total_rewards)
        
print ("Score over time: " +  str(sum(rewards)/total_episodes))
print(qtable)

#use q-table to play FrozenLake

env.reset()


for episode in range(5):
    state = env.reset()
    step = 0
    done = False
    print("****************************************************")
    print("EPISODE ", episode)

    for step in range(max_steps):
        
        # Take the action (index) that have the maximum expected future reward given that state
        action = np.argmax(qtable[state,:])
        
        new_state, reward, done, info = env.step(action)
        
        if done:
            # Here, we decide to only print the last state (to see if our agent is on the goal or fall into an hole)
            env.render()
            
            # We print the number of step it took.
            print("Number of steps", step)
            break
        state = new_state
env.close()
