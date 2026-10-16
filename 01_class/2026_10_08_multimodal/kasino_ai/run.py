import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from agent import Player
from machine import MachineFactory
from strategy.epsilon_greedy import EpsilonGreedy
from strategy.greedy import Greedy
from strategy.random_strategy import RandomStrategy


STRATEGIES = {
    "random": RandomStrategy(),
    "greedy-1": Greedy(),
    "greedy-2": Greedy(),
    "greedy-3": Greedy(),
    "epsilon_greedy_0.1": EpsilonGreedy(epsilon=0.1),
    "epsilon_greedy_0.01": EpsilonGreedy(epsilon=0.01),
}
SPINS = 1000
OUTPUT_DIR = Path(__file__).resolve().parent / "run"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone(timedelta(hours=9))).strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    for name, strategy in STRATEGIES.items():
        # 실험마다 새 플레이어를 만들어 이전 전략의 학습 기록을 분리합니다.
        player = Player(left_spin=SPINS)
        for machine in MachineFactory.create_machines():
            player.append_choice(machine)
        player.set_strategy(strategy)

        steps = []
        while player.left_spin > 0:
            before = {
                machine: record.copy()
                for machine, record in player.status.items()
            }
            result = player.play()
            index = result["idx"]
            steps.append({
                "spin": len(steps) + 1,
                "idx": index,
                "machine_number": index + 1,
                "p": player.choice[index].p,
                "reward": player.rewards[-1],
                "total_reward": player.total_reward,
                "status_before": before[player.choice[index]],
                # 참조 대신 복사본을 저장해야 이후 학습에도 과거 기록이 유지됩니다.
                "status_after": result["status"].copy(),
            })

        final_status = [
            {
                "idx": index,
                "machine_number": index + 1,
                "p": machine.p,
                **player.status[machine],
            }
            for index, machine in enumerate(player.choice)
        ]
        most_selected = max(final_status, key=lambda record: record["spin_count"])
        summary = {
            "final_status": final_status,
            "most_selected_machine": most_selected["machine_number"],
            "rewards": player.rewards,
        }
        experiment = {
            "strategy": name,
            "epsilon": strategy.epsilon if isinstance(strategy, EpsilonGreedy) else None,
            "total_spins": len(steps),
            "total_reward": player.total_reward,
            "summary": summary,
            "steps": steps,
        }

        output_path = OUTPUT_DIR / f"{run_id}_{name}.json"
        with output_path.open("x", encoding="utf-8") as output_file:
            json.dump(experiment, output_file, ensure_ascii=False, indent=2)

        print(f"\n전략: {name}")
        print(f"총 실행: {len(steps)}, 누적 보상: {player.total_reward}")
        print(f"가장 많이 선택한 머신: {most_selected['machine_number']}번")
        for record in final_status:
            print(
                f"  머신 {record['machine_number']}번 "
                f"(idx={record['idx']}, p={record['p']}): "
                f"선택 {record['spin_count']}회, 보상 {record['score']}, "
                f"추정 당첨률 {record['q']:.4f}"
            )
        print(f"JSON 저장: {output_path}")


if __name__ == "__main__":
    main()
