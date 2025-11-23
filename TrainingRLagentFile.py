# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 15:08:02 2025

@author: user
"""

import random
import numpy as np
import matplotlib.pyplot as plt

GRID_SIZE = 7
NUM_EPISODES = 100000
MAX_STEPS = 300

EPSILON_START = 1.0    # start fully exploring
EPSILON_END = 0.05     # minimum exploration rate
EPSILON_DECAY = 0.9995 # decay per episode

ALPHA = 0.1    # Learning rate
GAMMA = 0.9    # Discount factor

# Actions: 0=left, 1=right, 2=up, 3=down, 4=stay
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]

# Q-table: sword_x, sword_y, fruit1_x, fruit1_y, fruit2_x, fruit2_y, bomb_x, bomb_y, action
q_table = np.zeros((GRID_SIZE, GRID_SIZE,
                    GRID_SIZE, GRID_SIZE,
                    GRID_SIZE, GRID_SIZE,
                    GRID_SIZE, GRID_SIZE,
                    len(ACTIONS)))

def move(pos, action_idx):
    dx, dy = ACTIONS[action_idx]
    new_x = min(max(pos[0] + dx, 0), GRID_SIZE - 1)
    new_y = min(max(pos[1] + dy, 0), GRID_SIZE - 1)
    return (new_x, new_y)

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

def get_closest_fruit_dist(sword, fruits):
    return min(dist(sword, f) for f in fruits)

def move_bomb(bomb_pos):
    moves = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1),(0,0)]
    dx, dy = random.choice(moves)
    new_x = min(max(bomb_pos[0] + dx, 0), GRID_SIZE - 1)
    new_y = min(max(bomb_pos[1] + dy, 0), GRID_SIZE - 1)
    return (new_x, new_y)

def get_reward(sword, fruits, bomb, prev_dist):
    if sword == bomb:
        return -50
    for fruit in fruits:
        if sword == fruit:
            return 15
    new_dist = get_closest_fruit_dist(sword, fruits)
    if new_dist < prev_dist:
        return 1
    else:
        return -1

def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.randint(0, len(ACTIONS) - 1)
    return np.argmax(q_table[state])

def get_state(sword, fruit1, fruit2, bomb):
    return (*sword, *fruit1, *fruit2, *bomb)

reward_log = []
epsilon = EPSILON_START

for episode in range(NUM_EPISODES):
    sword = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
    fruit1 = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
    fruit2 = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
    bomb = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
    fruits = [fruit1, fruit2]

    total_reward = 0
    prev_dist = get_closest_fruit_dist(sword, fruits)

    for step in range(MAX_STEPS):
        state = get_state(sword, fruits[0], fruits[1], bomb)
        action = choose_action(state, epsilon)
        next_sword = move(sword, action)

        reward = get_reward(next_sword, fruits, bomb, prev_dist)
        total_reward += reward

        bomb = move_bomb(bomb)

        next_state = get_state(next_sword, fruits[0], fruits[1], bomb)
        best_next_action = np.argmax(q_table[next_state])

        q_table[state][action] += ALPHA * (reward + GAMMA * q_table[next_state][best_next_action] - q_table[state][action])

        sword = next_sword
        prev_dist = get_closest_fruit_dist(sword, fruits)

        if sword in fruits:
            idx = fruits.index(sword)
            fruits[idx] = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
            prev_dist = get_closest_fruit_dist(sword, fruits)
            if reward == 15 or reward == -50:
                break

        if sword == bomb and reward == -50:
            break

    reward_log.append(total_reward)

    # Decay epsilon but keep it >= EPSILON_END
    epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

    if episode % 1000 == 0:
        print(f"Episode {episode}, Reward: {total_reward}")

# Plot training rewards
plt.plot(reward_log)
plt.title("Training Rewards Over Time")
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.grid(True)
plt.savefig("training_rewards.png")
plt.show()


np.save("q_table.npy", q_table)

# Medal based on last episode reward
final_score = reward_log[-1]
if final_score >= 150:
    print("🏅 Gold Medal!")
elif final_score >= 100:
    print("🥈 Silver Medal!")
elif final_score >= 50:
    print("🥉 Bronze Medal!")
else:
    print("💀 Better luck next time!")

# Test the AI
print("\n[AI Test Run]")
sword = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
fruit1 = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
fruit2 = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
bomb = (random.randint(0, GRID_SIZE -1), random.randint(0, GRID_SIZE -1))
fruits = [fruit1, fruit2]

for _ in range(30):
    state = get_state(sword, fruits[0], fruits[1], bomb)
    action = np.argmax(q_table[state])
    sword = move(sword, action)
    bomb = move_bomb(bomb)
    print("Sword:", sword, "Fruits:", fruits, "Bomb:", bomb)
    if sword in fruits:
        print("Sliced a fruit! 🍉")
        break
    elif sword == bomb:
        print("Hit the bomb! 💣")
        break
