import math
import torch
from rl_m19.config import Config
from rl_m19.agent import QLearningAgent, SarsaAgent
from rl_m19.network import ReplayMemory, PureLinear
from rl_m19.utils import Plotter
from maze_2d import TwoDimensionMaze

config = Config()
config.episode_lifespan = 10**3
config.episodes = 10**5
config.BATCH_SIZE = 64
config.GAMMA = 0.999
# config.EPS_fn = lambda s: 0.9
config.EPS_fn = lambda s: 0.05 + (0.9 - 0.05) * math.exp(-1. * s / 1000)
config.LR = 0.001  # LEARNING_RATE
config.MC = 1000  # MEMORY_CAPACITY
config.TUF = 10  # TARGET_UPDATE_FREQUENCY

config.plotter = Plotter()
config.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
config.env = TwoDimensionMaze(config.device)
config.states_dim = config.env.states_dim
config.actions_dim = config.env.actions_dim

config.memory = ReplayMemory(config.MC)
config.policy_net = PureLinear(config)
config.target_net = PureLinear(config)
config.optimizer = torch.optim.RMSprop(config.policy_net.parameters(), config.LR)
config.loss_fn = torch.nn.MSELoss()


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == 'sarsa':
        agent = SarsaAgent(config)
    else:
        agent = QLearningAgent(config)
    agent.episodes_learn()
    config.env.render()
    config.env.close()
    config.plotter.plot_end()