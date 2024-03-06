import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simulate_games_with_loss_streaks(base_bet, X, num_games, initial_amount=2000, win_chance=0.495):
    balance = initial_amount
    bet = base_bet
    loss_streak = 0
    results = []
    loss_streaks = []  #store the end of loss streaks and their length

    for i in range(num_games):
        win = np.random.rand() >= (1 - win_chance)
        if win:
            if loss_streak >= 11:  #track if loss streak is more than 11
                loss_streaks.append((i, loss_streak))
            balance += bet
            bet = base_bet
            loss_streak = 0
        else:
            balance -= bet
            loss_streak += 1
            if loss_streak >= 2:
                bet = min(bet * 2, balance)  #ensure bet does not exceed balance
            if loss_streak > X or balance < bet:
                if loss_streak >= 11:  #include the final streak if it's significant
                    loss_streaks.append((i, loss_streak))
                break
        results.append(balance)

    return results, loss_streaks


def analyze_results(results, base_bet):
    profits = [result[-1] - 2000 for result in results if result[-1] > 2000]
    losses = [2000 - result[-1] for result in results if result[-1] < 2000]
    num_profit = len(profits)
    num_loss = len(losses)
    avg_profit = np.mean(profits) if profits else 0
    avg_loss = np.mean(losses) if losses else 0
    best_case = max(results, key=lambda x: x[-1])[-1]
    lost_everything = len([result for result in results if result[-1] < base_bet])

    return num_profit, num_loss, avg_profit, avg_loss, best_case, lost_everything


modes = [
    {'base_bet': 0.05, 'X': 15, 'num_games': 100000},
    {'base_bet': 0.1, 'X': 12, 'num_games': 100000},
    {'base_bet': 0.5, 'X': 99, 'num_games': 100000},
     {'base_bet': 0.1, 'X': 5, 'num_games': 100000},
]

all_results = []

for mode in modes:
    results_with_streaks = [simulate_games_with_loss_streaks(**mode) for _ in range(1000)]
    results = [result for result, _ in results_with_streaks]
    all_results.append(results)
    num_profit, num_loss, avg_profit, avg_loss, best_case, lost_everything = analyze_results(results, mode['base_bet'])
    chance_to_profit = (num_profit / 1000) * 100 
    
    print(f"Mode {modes.index(mode)+1} stats:")
    print(f"  Number of players with profit: {num_profit}")
    print(f"  Number of players with loss: {num_loss}")
    print(f"  Average profit (for those who profited): ${avg_profit:.2f}")
    print(f"  Average loss (for those who lost): ${avg_loss:.2f}")
    print(f"  Best case scenario (highest balance): ${best_case:.2f}")
    print(f"  Chance to profit using this case: {chance_to_profit:.2f}%")
    print(f"  Number of players who lost everything: {lost_everything}")
    print("--------------------------------------------------")



def plot_results(results, mode_index):
    plt.figure(figsize=(10, 6))
    for result in results[:100]:  #plot first 100 players to keep the graph readable
        plt.plot(result, alpha=0.5)
    plt.title(f"Player Balances Over Time - Mode {mode_index+1}")
    plt.xlabel("Number of Games")
    plt.ylabel("Balance")
    plt.show()

for index, results in enumerate(all_results):
    plot_results(results, index)
