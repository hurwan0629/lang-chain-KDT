"""Tuned online (1-step) Actor-Critic for Gymnasium LunarLander-v3.

The episode/step loop and best_model.pth / last-episode.pth layout
follow the original experiment. This is an experiment, not a guarantee
of solving the environment.
"""

from pathlib import Path

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
from torch.distributions import Categorical
from torch.optim.lr_scheduler import LambdaLR

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DTYPE = torch.float32


class ActorCriticNet(nn.Module):
    """Independent policy and value networks: no shared-gradient conflict."""

    def __init__(self, obs_dim=8, n_actions=4):
        super().__init__()

        self.actor = nn.Sequential(
            nn.Linear(obs_dim, 128),
            nn.Tanh(),
            nn.Linear(128, 128),
            nn.Tanh(),
            nn.Linear(128, n_actions),
        )
        self.critic = nn.Sequential(
            nn.Linear(obs_dim, 128),
            nn.Tanh(),
            nn.Linear(128, 128),
            nn.Tanh(),
            nn.Linear(128, 1),
        )

        # Small initial actor logits; independently initialized value head.
        for network in (self.actor, self.critic):
            for layer in network:
                if isinstance(layer, nn.Linear):
                    # 직교초기화
                    # 가중치 행렬의 행 또는 열이 서로 직교하도록 초기화하는 방식
                    # 이를 통해서 초기 신호와 gradient의 크기가 층을 통과하면서 지나치게 커지거나 작아지는 현상 완화
                    nn.init.orthogonal_(layer.weight, gain=nn.init.calculate_gain("tanh"))
                    nn.init.zeros_(layer.bias)
        nn.init.orthogonal_(self.actor[-1].weight, gain=0.01)
        nn.init.orthogonal_(self.critic[-1].weight, gain=1.0)

    def forward(self, x):
        return self.actor(x), self.critic(x).squeeze(-1)


@torch.no_grad()
def evaluate_policy(model, episodes=10, max_step=1500, seed=10_000, greedy=True):
    """Independent, fixed-seed evaluation; no optimizer updates."""
    env = gym.make("LunarLander-v3")
    old_mode = model.training
    model.eval()
    device = next(model.parameters()).device
    scores = []
    try:
        for k in range(episodes):
            obs, _ = env.reset(seed=seed + k)
            total = 0.0
            for _ in range(max_step):
                x = torch.as_tensor(obs, dtype=DTYPE, device=device)
                logits, _ = model(x)
                if greedy:
                    action = int(torch.argmax(logits).item())
                else:
                    action = int(Categorical(logits=logits).sample().item())
                obs, reward, terminated, truncated, _ = env.step(action)
                total += float(reward)
                if terminated or truncated:
                    break
            scores.append(total)
    finally:
        model.train(old_mode)
        env.close()
    return float(np.mean(scores)), float(np.std(scores))


def train_ac_lunar_lander(
    episode=2000,
    gamma=0.99,
    lr=8e-5,              # Actor LR
    critic_lr=3e-4,
    seed=42,
    max_step=1500,
    dtype=DTYPE,
    reward_scale=0.1,
    entropy_start=0.02,
    entropy_end=0.002,
    eval_every=50,
    eval_episodes=10,
):
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    env = gym.make("LunarLander-v3")
    # New directory deliberately avoids overwriting previous experiments.
    save_dir = Path("./ac_lunar_results/tuned_online_ac")
    save_dir.mkdir(parents=True, exist_ok=True)

    ac = ActorCriticNet(8, 4).to(DEVICE)
    device = next(ac.parameters()).device
    optimizer = optim.Adam([
        {"params": ac.actor.parameters(), "lr": lr, "name": "actor"},
        {"params": ac.critic.parameters(), "lr": critic_lr, "name": "critic"},
    ], eps=1e-5)

    # Episode-wise learning-rate decay; both groups retain their LR ratio.
    scheduler = LambdaLR(
        optimizer,
        lr_lambda=lambda ep: max(0.2, 1.0 - 0.8 * ep / max(1, episode)),
    )

    config = {
        "env": "LunarLander-v3",
        "episode": episode,
        "max_step": max_step,
        "gamma": gamma,
        "lr": "\n".join(f"{g['name']}: lr = {g['lr']:.6f}" for g in optimizer.param_groups),
        "actor_lr": lr,
        "critic_lr": critic_lr,
        "reward_scale": reward_scale,
        "entropy_start": entropy_start,
        "entropy_end": entropy_end,
        "eval_every": eval_every,
        "eval_episodes": eval_episodes,
        "seed": f"{seed} + episode",
        "model": str(ac),
        "architecture_version": "separate_128x128_ortho_v1",
    }
    model_architecture = "\n".join(f"{name}: {module}" for name, module in ac.named_modules())
    reward_history = []
    evaluation_history = []
    best_reward = float("-inf")  # Best EVALUATION MEAN, not single-episode maximum.
    best_single_reward = float("-inf")
    td_rms_sq = 1.0

    try:
        for epi in range(1, episode + 1):
            ac.train()
            state, _ = env.reset(seed=seed + epi)
            total_reward = 0.0
            entropies = []
            critic_losses = []
            action_counts = np.zeros(4, dtype=np.int64)
            entropy_coef = entropy_start + (entropy_end - entropy_start) * (epi - 1) / max(1, episode - 1)

            for t in range(max_step):
                x = torch.as_tensor(state, dtype=dtype, device=device)
                logits, value = ac(x)
                dist = Categorical(logits=logits)
                action = dist.sample()
                next_state, reward, terminated, truncated, _ = env.step(int(action.item()))
                total_reward += float(reward)  # Report ORIGINAL, unscaled Gymnasium return.

                with torch.no_grad():
                    next_x = torch.as_tensor(next_state, dtype=dtype, device=device)
                    _, next_value = ac(next_x)
                    td_target = reward_scale * reward + gamma * (1.0 - float(terminated)) * next_value

                delta = td_target - value
                # RMS scale only for policy gradient. Preserve the sign of advantage.
                td_rms_sq = 0.99 * td_rms_sq + 0.01 * float(delta.detach().square().item())
                advantage = (delta.detach() / max(1.0, td_rms_sq ** 0.5)).clamp(-5.0, 5.0)

                actor_loss = -dist.log_prob(action) * advantage - entropy_coef * dist.entropy()
                critic_loss = F.mse_loss(value, td_target)
                loss = actor_loss + 0.5 * critic_loss

                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                # Independent norms preserve the separate networks' different scales.
                torch.nn.utils.clip_grad_norm_(ac.actor.parameters(), max_norm=0.5)
                torch.nn.utils.clip_grad_norm_(ac.critic.parameters(), max_norm=1.0)
                optimizer.step()

                entropies.append(float(dist.entropy().detach().item()))
                critic_losses.append(float(critic_loss.detach().item()))
                action_counts[int(action.item())] += 1
                state = next_state
                if terminated or truncated:
                    break

            reward_history.append(total_reward)
            best_single_reward = max(best_single_reward, total_reward)
            scheduler.step()

            if epi % eval_every == 0 or epi == episode:
                eval_mean, eval_std = evaluate_policy(
                    ac, episodes=eval_episodes, max_step=max_step,
                    seed=10_000, greedy=True,
                )
                evaluation_history.append({"episode": epi, "mean": eval_mean, "std": eval_std})
                print(
                    f"episode {epi:4d} | train(last 50): {np.mean(reward_history[-50:]):8.2f} "
                    f"| greedy eval: {eval_mean:8.2f} +/- {eval_std:6.2f} "
                    f"| entropy: {np.mean(entropies):.3f} "
                    f"| critic MSE: {np.mean(critic_losses):.3f} "
                    f"| actions: {(action_counts / max(1, action_counts.sum())).round(2)}"
                )

                if eval_mean > best_reward:
                    best_reward = eval_mean
                    torch.save({
                        "episode": epi,
                        "evaluation_mean": eval_mean,
                        "evaluation_std": eval_std,
                        "model_architecture": model_architecture,
                        "state_dict": ac.state_dict(),
                        "model_config": config,
                        "optimizer_state_dict": optimizer.state_dict(),
                        "scheduler_state_dict": scheduler.state_dict(),
                    }, save_dir / "best_model.pth")
                    print(f"best reward model saved - episode: {epi} / eval mean: {eval_mean:.2f}")

                torch.save({
                    "episode": epi,
                    "model_architecture": model_architecture,
                    "state_dict": ac.state_dict(),
                    "config": config,
                    "optimizer_state_dict": optimizer.state_dict(),
                    "scheduler_state_dict": scheduler.state_dict(),
                }, save_dir / "last-episode.pth")
    finally:
        env.close()

    return {
        "model": ac,
        "reward_history": reward_history,
        "evaluation_history": evaluation_history,
        "config": config,
        "best_eval_mean": best_reward,
        "best_single_episode_reward": best_single_reward,
    }


if __name__ == "__main__":
    result = train_ac_lunar_lander(
        gamma=0.99, lr=8e-5, critic_lr=3e-4,
        episode=2000, max_step=1500,
    )
    print("Best 10-episode greedy eval mean:", result["best_eval_mean"])
