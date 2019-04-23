from OpenGL import GLU
import roboschool, gym

#print("\n".join(['- ' + spec.id for spec in gym.envs.registry.all() if spec.id.startswith('Roboschool')]))

env=gym.make('RoboschoolAnt-v1')
env.reset()
while True:
    env.step(env.action_space.sample())
    env.render()
