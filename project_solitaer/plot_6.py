import Q_Agent
import SimWorld
import numpy as np
import matplotlib.pyplot as plt
import copy
import time


def calc_epsilon_decay(epsilon, epsilon_end):
    return (epsilon_end/epsilon)**(1/float(EPISODES))                               # auf 1 setzen für keinen decay
    # return 1

def calc_alpha_decay(alpha, alpha_end):
    # return (alpha_end/alpha)**(1/float(EPISODES))                                 # auf 1 setzen für keinen decay
    return 1


EPISODES = 10000
"""
    Plot Name: 
    Board(X)                    # z.b Dreieck(6)
    alpha wert oder range       # z.b 1
    epsilon wert oder range     # z.b 0.1-0.2
    initial Q-values            # z.b 0
    reward function/parameters  # z.b normal
    averaging parameter         # z.b 100
"""
NAME = "Dreieck(6) 1 0.1-0.2 0 normal 100 %d Episodes" % EPISODES
AVERAGE = 100

alpha = 1                                                           # startwert lernrate
gamma = 1                                                           # startwert discount faktor
epsilon_start = [0.1, 0.12, 0.14, 0.16, 0.18, 0.20]
epsilon_end = 0.0005                                                # endwert wenn decay eingestellt
alpha_end = 0.0005                                                  # endwert wenn decay eingestellt

"""
Spielbrett aufsetzten
"""

Brett1 = SimWorld.Triangular(6)
Brett1.populate_board()
# Brett1.board_array[3][3].set_value(1)
# Brett1.board_array[3][4].set_value(0)
# Brett1.board_array[3][5].set_value(0)
Brett1.board_array[0][0].set_value(0)
Brett1.set_neighbor_pairs()
start_board = Brett1.get_board_copy()

"""
Agent aufsetzen
"""
episode_counter = 0
list_of_results = [[]]
episode_rewards = [[]]
total_rewards = [[]]
start_time = time.time()
moving_avg = [[]]
moving_avg_2 = [[]]
for i in range(6):
    AgentP = Q_Agent.QLearner(alpha, gamma, epsilon_start[i], calc_epsilon_decay(epsilon_start[i], epsilon_end), calc_alpha_decay(alpha, alpha_end), NAME+str(i))
    list_of_results.append([])
    episode_rewards.append([])
    total_rewards.append([])
    moving_avg.append([])
    moving_avg_2.append([])
    for element in range(EPISODES):
        if Q_Agent.goal_reached is True:
            Q_Agent.update_learner()
        episode_counter += 1
        immediate_reward = []
        while not Brett1.in_final_state():
            agent_action = AgentP.get_next_action(Brett1.get_board_view(), Brett1.get_actions())
            Brett1.take_action(agent_action)
            AgentP.train_agent(Brett1.get_board_view(), Brett1.get_actions(), agent_action, Brett1.get_previous_state(), Brett1.in_final_state())
            immediate_reward.append(Q_Agent.get_reward(Brett1.get_board_view(), Brett1.in_final_state()))
        result = np.sum(Brett1.get_board_view())
        list_of_results[i].append(result)
        AgentP.update_epsilon()     # apply epsilon decay
        episode_rewards[i].append(Q_Agent.get_reward(Brett1.get_board_view(), Brett1.in_final_state()))
        total_rewards[i].append(sum(immediate_reward))
        if Brett1.in_final_state():
            Brett1.set_board_array(copy.deepcopy(start_board))
    print("done")

    moving_avg[i] = np.convolve(list_of_results[i], np.ones((AVERAGE,)) / AVERAGE, mode="valid")
    moving_avg_2[i] = np.convolve(total_rewards[i], np.ones((AVERAGE,)) / AVERAGE, mode="valid")

plt.figure(0)
x = [i for i in range(len(moving_avg[1]))]

plt.plot(x, moving_avg[0], color='red', label='epsilon_start = '+str(epsilon_start[0]))
plt.plot(x, moving_avg[1], color='blue', label='epsilon_start = '+str(epsilon_start[1]))
plt.plot(x, moving_avg[2], color='green', label='epsilon_start = '+str(epsilon_start[2]))
plt.plot(x, moving_avg[3], color='purple', label='epsilon_start = '+str(epsilon_start[3]))
plt.plot(x, moving_avg[4], color='brown', label='epsilon_start = '+str(epsilon_start[4]))
plt.plot(x, moving_avg[5], color='orange', label='epsilon_start = '+str(epsilon_start[5]))

plt.legend()
plt.ylim(1, 9)
plt.title(NAME)
plt.ylabel('Remaining Pins')
plt.xlabel('Games played')
plt.grid()
plt.savefig(NAME+".pdf", dpi=300)


plt.figure(1)
x2 = [i for i in range(len(moving_avg_2[1]))]

plt.plot(x2, moving_avg_2[0], color='red', label='epsilon_start = '+str(epsilon_start[0]))
plt.plot(x2, moving_avg_2[1], color='blue', label='epsilon_start = '+str(epsilon_start[1]))
plt.plot(x2, moving_avg_2[2], color='green', label='epsilon_start = '+str(epsilon_start[2]))
plt.plot(x2, moving_avg_2[3], color='purple', label='epsilon_start = '+str(epsilon_start[3]))
plt.plot(x2, moving_avg_2[4], color='brown', label='epsilon_start = '+str(epsilon_start[4]))
plt.plot(x2, moving_avg_2[5], color='orange', label='epsilon_start = '+str(epsilon_start[5]))
plt.legend()
plt.ylabel('Total Reward over Episode')
plt.xlabel('Games played')
plt.grid()
plt.savefig(NAME+" Reward.pdf", dpi=300)
print("--- %s seconds ---" % (time.time() - start_time))