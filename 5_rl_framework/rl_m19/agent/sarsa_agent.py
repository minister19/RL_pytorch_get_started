import numpy as np
import pandas as pd
from itertools import count
from rl_m19.agent.q_learning_agent import QLearningAgent, AgentUtils


class SarsaAgent(QLearningAgent):
    def __init__(self, config):
        super().__init__(config)

    def learn(self, state, action, reward, next_state, next_action):
        # convert tensor to string, number
        state = AgentUtils.tensor2str(state.cpu())
        reward = AgentUtils.tensor2number(reward.cpu())
        next_state = AgentUtils.tensor2str(next_state.cpu())

        # record unknown state
        self._check_state_exist(next_state)

        q_predict = self.q_table.loc[state, action]
        if next_state != None:
            # next state is not terminal
            q_target = reward + self.config.gamma * self.q_table.loc[next_state, next_action]
        else:
            # next state is terminal
            q_target = reward
        self.q_table.loc[state, action] += self.config.lr * (q_target - q_predict)

    def episode_learn(self, i_episode, step_render=False):
        state = self.config.env.reset()

        for t in count():
            if step_render:
                self.config.env.render()

            # choose action
            action = self.select_action(state)

            # take action and observe
            next_state, reward, done, info = self.config.env.step(action)

            # choose next_action
            next_action = self.select_action(state)

            if done or t >= self.config.episode_lifespan:
                self.episode_t.append(t)
                break
            else:
                # learn
                self.learn(state, action, reward, next_state, next_action)

                # update state
                state = next_state
