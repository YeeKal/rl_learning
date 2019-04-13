
import gym
env=gym.make('CartPole-v0')
for  epi in range(20):
    observation=env.reset()
    for t in range(100):
        env.render() #plot once
        print(observation)
        action=env.action_space.sample()
        observation,reward,done,info=env.step(action)
        if done:
            print("finished after {} timesteps".format(t+1))
            break