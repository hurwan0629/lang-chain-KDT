from maze_env import MazeEnv
import random
import pickle
# import torch
# from torch import nn
# from torch.distributions import Categorical

SEED=2026

random.seed(SEED)
# torch.manual_seed(SEED)
# if torch.cuda.is_available():
#   torch.cuda.manual_seed(SEED)

# DTYPE = torch.float32
# DEVICE = torch.device(
#   "cuda" if torch.cuda.is_available() else "cpu"
# )

env = MazeEnv()

# q table
#   UP, DOWN, LEFT, RIGHT 
table: dict[tuple[int, int], list[float]] = {
  c: [0, 0, 0, 0]
  for c
  in env.walkable_cells()
}

best_state = None
best_reward = float("-inf")

EPISODE = 200
MAX_STEPS = 40

ALPHA = 0.05
GAMMA=0.95
EPSILON_START = 1.0
EPSILON_DECAY = 0.992
EPSILON_MIN = 0.05
LOG_EVERY = 100
epsilon = EPSILON_START
reward_history = []

for epi in range(1, EPISODE+1):
  pos = env.reset()
  total_reward = 0
  for t in range(MAX_STEPS):
    if random.random() < epsilon:
      action = random.randint(0, 3)
    else:
      action = max(range(len(table[pos])), key=lambda i: table[pos][i])

    # 다음 상태
    next_pos, reward, end = env.step(action)

    total_reward += reward

    
    # 다음 상태에서 argmax로 움직일 경우의 움직임
    next_value = max(table[next_pos])

    table.get(pos)[action] += ALPHA * (reward + GAMMA * next_value * (0 if end else 1) - table[pos][action])
    if end:
      break

    pos = next_pos

    epsilon = max(epsilon*EPSILON_DECAY, EPSILON_MIN)

  reward_history.append(total_reward)

  if best_reward < total_reward:
    best_state = table
    best_reward = total_reward
  if epi % LOG_EVERY == 0:
    print(f"episode - {epi}: {total_reward}")

with open("./maze/class_200epi_best_q_table.pkl", "wb") as f:
  pickle.dump(best_state, f)

with open("./maze/class_200epi_last_q_table.pkl", "wb") as f:
  pickle.dump(table, f)

print("ended")
