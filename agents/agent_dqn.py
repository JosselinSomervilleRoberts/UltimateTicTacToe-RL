from agents.agent import Agent

import gym
import numpy as np
import torch
from torch.optim import Adam
from torch.nn import Linear, ReLU, Dropout, BatchNorm1d

## agent

class ReplayBuffer(object):
    def __init__(self, state_len, mem_size):
        self.state_len = state_len
        self.mem_size = mem_size
        self.mem_counter = 0
        self.states = np.zeros((mem_size, state_len), dtype=np.float32)
        self.actions = np.zeros(mem_size, dtype=np.int32)
        self.rewards = np.zeros(mem_size, dtype=np.float32)
        self.new_states = np.zeros((mem_size, state_len), dtype=np.float32)
        self.dones = np.zeros(mem_size, dtype=np.int32)


    def store_transition(self, state, action, reward, new_state, done):
        index = self.mem_counter%self.mem_size
        self.states[index, :] = state
        self.actions[index] = action
        self.rewards[index] = reward
        self.new_states[index, :] = new_state
        self.dones[index] = done
        self.mem_counter += 1

    def sample_memory(self, batch_size):
        max_memory = min(self.mem_size, self.mem_counter)
        batch = np.random.choice(np.arange(max_memory), batch_size, replace=False)
        states = self.states[batch, :]
        actions = self.actions[batch]
        rewards = self.rewards[batch]
        new_states = self.new_states[batch, :]
        dones = self.dones[batch]
        return states, actions, rewards, new_states, dones


class DQNetwork(torch.nn.Module):
    def __init__(self, state_len, n_actions,learning_rate):
        super(DQNetwork, self).__init__()
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.learning_rate = learning_rate
        self.n_actions = n_actions
        self.network = torch.nn.Sequential(
            torch.nn.Linear(state_len, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, n_actions)
        )
        self.optimizer = Adam(self.parameters(), lr = learning_rate)
        self.loss = torch.nn.MSELoss(reduction='sum')
        self.to(self.device)


    def forward(self,state):
        return self.network(state)


class DQNAgent(Agent):

    def __init__(self, player = 1, env = gym.make('LunarLander-v2')):

        learning_rate=0.001
        gamma=0.99
        batch_size=64
        state_len=len(env.reset())
        n_actions = env.action_space.n
        mem_size = 1000000
        min_memory_for_training=1000
        epsilon=1
        epsilon_dec=0.995
        epsilon_min = 0.02
        frozen_iterations=6


        super().__init__(self)
        self.it_counter = 0            # how many timesteps have passed already
        self.gamma = gamma             # gamma hyperparameter
        self.batch_size = batch_size   # batch size hyperparameter for neural network
        self.state_len = state_len     # how long the state vector is
        self.n_actions = n_actions     # number of actions the agent can take
        self.epsilon = epsilon         # epsilon start value (1=completly random)
        self.epsilon_min = epsilon_min # the minimum value
        self.epsilon_dec = epsilon_dec
        self.mem_size = mem_size

        self.min_memory_for_training = min_memory_for_training
        self.q = DQNetwork(state_len, n_actions, learning_rate)
        self.replay_buffer = ReplayBuffer(self.state_len, mem_size)

        self.learnNN(env)

    def getAction(self, env, observation):
        valid_actions = env.valid_actions()
        observation = torch.tensor(np.array(observation), dtype = torch.float32).to(self.q.device)
        q= self.q.forward(observation)
        action = torch.argmax(q)
        mask = np.array([True if i in valid_actions else False for i in range(env.action_space.n)])
        action = torch.argmax(q)
        while not mask[int(action)] :
            q[int(action)] = -100000
            action = torch.argmax(q)
        return int(action)

    def pickActionMaybeRandom(self, env, observation):
        valid_actions = env.valid_actions()
        if np.random.random() < self.epsilon:
            action = np.random.choice(valid_actions)
        else:
            observation = torch.tensor(np.array(observation), dtype = torch.float32).to(self.q.device)
            q= self.q.forward(observation)
            mask = np.array([True if i in valid_actions else False for i in range(env.action_space.n)])
            # truc à faire avec quelque chose comme torch.argmax(torch.masked_select(q,torch.BoolTensor(mask))) pour éviter le while dégueu
            action = torch.argmax(q)
            while not mask[int(action)] :
                q[int(action)] = -100000
                action = torch.argmax(q)
        return int(action)

    def learn(self):
        if self.replay_buffer.mem_counter < self.min_memory_for_training:
            return
        states, actions, rewards, new_states, dones = self.replay_buffer.sample_memory(self.batch_size)
        self.q.optimizer.zero_grad()
        states_batch = torch.tensor(states, dtype = torch.float32).to(self.q.device)
        new_states_batch = torch.tensor(new_states,dtype = torch.float32).to(self.q.device)
        actions_batch = torch.tensor(actions, dtype = torch.long).to(self.q.device)
        rewards_batch = torch.tensor(rewards, dtype = torch.float32).to(self.q.device)
        dones_batch = torch.tensor(dones, dtype = torch.float32).to(self.q.device)

        target = rewards_batch + torch.mul(self.gamma* self.q(new_states_batch).max(axis = 1).values, (1 - dones_batch))
        prediction = self.q.forward(states_batch).gather(1,actions_batch.unsqueeze(1)).squeeze(1)

        loss = self.q.loss(prediction, target)
        loss.backward()  # Compute gradients
        self.q.optimizer.step()  # Backpropagate error

        # decrease epsilon:
        self.epsilon = self.epsilon * self.epsilon_dec if self.epsilon *self.epsilon_dec \
                                                          > self.epsilon_min else self.epsilon_min
        self.it_counter += 1
        return

    def learnNN(self,env):
        n_hidden_episodes = 10
        n_episodes = 100 #1000
        for episode in range(n_episodes):
            state = env.reset()           # resetting the environment after each episode
            score = 0
            done = 0
            while not done:               # while the episode is not over yet
                action = self.pickActionMaybeRandom(env,state)           # let the agent act
                #print("action chosen : (",action//9,",",action%9,")")
                new_state,reward, done, info = env.step(action) # performing the action in the environment
                #print("new state : \n",state.reshape((9,9)))
                score+=reward                            #  the total score during this round
                self.replay_buffer.store_transition(state, action, reward, new_state, done)   # store timestep for experiene replay
                self.learn()                            # the agent learns after each timestep
                state = new_state
            print("Pourcentage du learning effectué : ",round(100*episode/float(n_episodes),2), " %",end="\r")
        env.close()