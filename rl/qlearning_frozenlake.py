'''
@FrozenLake by hand
ref:https://github.com/simoninithomas/Deep_reinforcement_learning_Course/blob/master/Q_Learning_with_FrozenLakev2.ipynb

@experiment:
some factor amy affect the result
- hole numbers
- reward
'''
import numpy as np
import pandas as pd
import random

#parameters
state_size=16
action_size=4

total_episodes=15000
max_steps=99

gamma=0.95
alpha=0.7			#learning rate
  		#exploration rate
max_epsilon = 0.9   # Exploration probability at start
min_epsilon = 0.01  # Minimum exploration probability 
decay_rate = 0.01  # Exponential decay rate for exploration prob


class EnvLake:
	def __init__(self):
		#actions: 0-top,1-right,2-bottom,3-lefts
		#states:0-15
		self.state_size=16
		self.action_size=4
		self.obstacles=[5,7,11]
		#self.actions=np.array()
		self.start=0
		self.target=15
		self.epsilon=1.0
		self.q_tables=np.zeros((self.state_size,self.action_size))
		
	def chooseAction(self,state,is_greedy=True):
		#get valid actions
		valid_actions=[]
		valid_states=[]
		valid_q=[]
		#top
		if state-self.action_size>=0:
			valid_actions.append(0)
			valid_states.append(state-self.action_size)
			valid_q.append(self.q_tables[state,0])
		#right
		if state%self.action_size !=3:
			valid_actions.append(1)
			valid_states.append(state+1)
			valid_q.append(self.q_tables[state,1])
		#bottom
		if state+self.action_size<self.state_size-1:
			valid_actions.append(2)
			valid_states.append(state+self.action_size)
			valid_q.append(self.q_tables[state,2])
		#left
		if state%self.action_size>0:
			valid_actions.append(3)
			valid_states.append(state-1)
			valid_q.append(self.q_tables[state,3])

		valid_actions=np.array(valid_actions)
		valid_states=np.array(valid_states)
		valid_q=np.array(valid_q)


		exp_exp_tradeoff = random.uniform(0, 1)
		#exploration
		#print(self.epsilon)
		if is_greedy:
			if exp_exp_tradeoff<self.epsilon or valid_states.any()==0: ##any numberis 0 or empty
				new_action_index=np.random.randint(np.size(valid_actions))
			else:
				new_action_index=valid_q.argmax()
		else:
			new_action_index=valid_q.argmax()
		new_action=valid_actions[new_action_index]
		new_state=valid_states[new_action_index]

		reward=0
		#get reward
		if new_state in self.obstacles:
			reward=-10
		elif new_state==self.target:
			reward=10
		else:
			reward=0

		return new_action,new_state,reward

	def updateEnv(self):
		a=0

	# take a action
	# return: new state and reward
	def takeAction(self,action):
		b=0
	
	def qLearning(self):
		#build q_table
		for episode in range(total_episodes):
			step=0
			terminated=False
			self.updateEnv()
			state=self.start
			reward_all=0
			while not terminated and step<max_steps:

				step +=1
				action,new_state,reward=self.chooseAction(state,True)
				# print(reward)
				q_current=self.q_tables[state,action]

				#update: Q(s,a):=Q(s,a)+\alpha[r+\gamma \max_{a'}Q(s',a')-Q(s,a)]
				self.q_tables[state,action] +=alpha*(reward+gamma*self.maxQ(new_state)-q_current)
				if new_state==self.target:
					terminated=True
				elif new_state in self.obstacles:
					terminated=True

				state=new_state
				reward_all +=reward
				self.updateEnv()
				
			#reduce exploration
			self.epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
		print(self.q_tables)
	def move(self,steps):
		for s in range(steps):
			step=0
			terminated=False
			state=self.start
			reward_all=0
			while not terminated and step<max_steps:
				print("%d->"%state,end='')

				step +=1
				action,new_state,reward=self.chooseAction(state,True)

			
				if new_state==self.target:
					terminated=True
					print("%d"%new_state)
					print("%d:reach the goal"%step)
				elif new_state in self.obstacles:
					terminated=True
					print("%d"%new_state)
					print("%d:fell into a hole"%step)

				state=new_state
				reward_all +=reward
		print()
		print("reward:%s"%reward_all)
	def maxQ(self,state):
		valid_actions,valid_q,valid_states=self.getValidActions(state)
		return max(valid_q)
	def getValidActions(self,state):
		valid_actions=[]
		valid_states=[]
		valid_q=[]
		#top
		if state-self.action_size>=0:
			valid_actions.append(0)
			valid_states.append(state-self.action_size)
			valid_q.append(self.q_tables[state,0])
		#right
		if state%self.action_size !=3:
			valid_actions.append(1)
			valid_states.append(state+1)
			valid_q.append(self.q_tables[state,1])
		#bottom
		if state+self.action_size<self.state_size-1:
			valid_actions.append(2)
			valid_states.append(state+self.action_size)
			valid_q.append(self.q_tables[state,2])
		#left
		if state%self.action_size>0:
			valid_actions.append(3)
			valid_states.append(state-1)
			valid_q.append(self.q_tables[state,3])
		return valid_actions,valid_q,valid_states

lake=EnvLake()
print(lake.q_tables)
lake.qLearning()
lake.move(3)