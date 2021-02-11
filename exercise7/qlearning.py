import numpy as np
import gym
import random
import matplotlib.pyplot as plt


class QLearning:
    def __init__(self, episodes, learning_rate, max_steps_nr, gamma, epsilon, max_epsilon, min_epsilon, decay_rate):
        self.episodes = episodes
        self.learning_rate = learning_rate
        self.max_steps_nr = max_steps_nr
        self.gamma = gamma
        self.epsilon = epsilon
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = decay_rate
        self.total_rewards = 0
        self.rewards = []
        self.q_table_history = []
        self.score_history = []

        self.env = gym.make("FrozenLake8x8-v0")
        self.state = self.env.reset()
        self.action_size = self.env.action_space.n
        self.state_size = self.env.observation_space.n
        self.q_table = np.zeros((self.state_size, self.action_size))

    def choose_action(self, q_table, state, epsilon):
        rand = random.uniform(0, 1)    
        ## If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
        if rand > epsilon:
            self.action = np.argmax(self.q_table[self.state,:])

        # Else doing a random choice --> exploration
        else:
            self.action = self.env.action_space.sample()

    def take_step(self):
        self.choose_action(self.q_table, self.state, self.epsilon)

        new_state, reward, done, info = self.env.step(self.action)

        self.q_table[self.state, self.action] = self.q_table[self.state, self.action] + self.learning_rate * (reward + self.gamma * np.max(self.q_table[new_state, :]) - self.q_table[self.state, self.action])
        
        self.total_rewards += reward
        
        # Our new state is state
        self.state = new_state
        
        # If done (if we're dead) : finish episode
        if done == True: 
            return  True
        else:
            return  False

    def run_episode(self):
        self.state = self.env.reset()
        step = 0
        done = False
        self.total_rewards = 0

        for step in range(self.max_steps_nr):
            done = self.take_step()
            if done:
                break

    def adjust_parameters(self, episode):
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon)*np.exp(-self.decay_rate*episode) 
        self.rewards.append(self.total_rewards)
        
        episode_count = episode + 1
        if episode_count % 10000 == 0:
            self.q_table_history.append(self.q_table)
            self.score_history.append(sum(self.rewards)/episode_count)

    def run_algorithm(self):
        for episode in range(self.episodes):
            self.run_episode()
            self.adjust_parameters(episode)
        print ("Score over time: " +  str(sum(self.rewards)/self.episodes))
        print(self.q_table)

    def test(self):
        self.env.reset()
        total_test_episodes = 1000
        rewards = []

        for episode in range(total_test_episodes):
            self.state = self.env.reset()
            step = 0
            done = False
            total_rewards = 0

            for step in range(self.max_steps_nr):
                action = np.argmax(self.q_table[self.state,:])
                
                new_state, reward, done, info = self.env.step(action)
                
                total_rewards += reward
                
                if done:
                    rewards.append(total_rewards)
                    print ("Score", total_rewards)
                    print("Steps: ", step)
                    break
                self.state = new_state
        self.env.close()
        #print ("Score over time: " +  str(sum(rewards)/total_test_episodes))

        plt.plot(list(range(0, self.episodes+1, 10000))[1:], self.score_history)
        plt.title("Score vs. number of episodes")
        plt.show()






def main():
    agent = QLearning(episodes=200000, learning_rate=0.8, max_steps_nr = 200, gamma = 0.9, epsilon = 1.0, max_epsilon = 1.0, min_epsilon = 0.001, decay_rate = 0.00005)
    agent.run_algorithm()
    agent.test()

main()