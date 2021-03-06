import gym
from rl_m19.envs import BaseEnv

# https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py

'''
Description:
    A pole is attached by an un-actuated joint to a cart, which moves along
    a frictionless track. The pendulum starts upright, and the goal is to
    prevent it from falling over by increasing and reducing the cart's
    velocity.
Source:
    This environment corresponds to the version of the cart-pole problem
    described by Barto, Sutton, and Anderson
Observation:
    Type: Box(4)
    Num     Observation               Min                     Max
    0       Cart Position             -4.8                    4.8
    1       Cart Velocity             -Inf                    Inf
    2       Pole Angle                -0.418 rad (-24 deg)    0.418 rad (24 deg)
    3       Pole Angular Velocity     -Inf                    Inf
Actions:
    Type: Discrete(2)
    Num   Action
    0     Push cart to the left
    1     Push cart to the right
    Note: The amount the velocity that is reduced or increased is not
    fixed; it depends on the angle the pole is pointing. This is because
    the center of gravity of the pole increases the amount of energy needed
    to move the cart underneath it
Reward:
    Reward is 1 for every step taken, including the termination step
Starting State:
    All observations are assigned a uniform random value in [-0.05..0.05]
Episode Termination:
    Pole Angle is more than 12 degrees.
    Cart Position is more than 2.4 (center of the cart reaches the edge of
    the display).
    Episode length is greater than 200.
    Solved Requirements:
    Considered solved when the average return is greater than or equal to
    195.0 over 100 consecutive trials.
'''


class CartPole_v0(BaseEnv):
    def __init__(self, device, plotter=None):
        super().__init__(device, plotter)
        self.env = gym.make('CartPole-v0').unwrapped
        # self.env = gym.make('Pendulum-v1').unwrapped
        self.state_dim = 4
        self.action_dim = 2

    def step(self, action):
        # next_state, reward, done, info = self.env.step([action])
        next_state, reward, done, info = self.env.step(action)
        # reward = 1 - 10 * abs(next_state[2])/0.209
        # reward = 1 - 10 * (abs(next_state[0])/2.4 + abs(next_state[2])/0.209)
        return self._unsqueeze_tensor(next_state), reward, done, info

    def reset(self):
        state = self.env.reset()
        return self._unsqueeze_tensor(state)

    def render(self):
        return self.env.render()

    def close(self):
        return self.env.close()
