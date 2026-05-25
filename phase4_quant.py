import pandas as pd
import numpy as np

def kelly_criterion(odds, model_prob):
    b = odds - 1
    p = model_prob
    q = 1 - p
    f = (b * p - q) / b
    return max(f, 0)  # Never bet negative

# Starting bankroll
bankroll = 1000

# Signals from Phase 3
signals = {
    'Ferrari': {'odds': 5.00, 'model_prob': 0.227, 'signal': 'BUY'},
    'Aston Martin': {'odds': 15.00, 'model_prob': 0.116, 'signal': 'BUY'},
    'Haas F1 Team': {'odds': 100.00, 'model_prob': 0.045, 'signal': 'BUY'},
}

print(f"Starting Bankroll: ${bankroll}")
print(f"\n{'Team':<25} {'Kelly %':>10} {'Bet Amount':>12} {'Signal':>8}")
print("-" * 60)

total_bet = 0
for team, data in signals.items():
    if data['signal'] == 'BUY':
        f = kelly_criterion(data['odds'], data['model_prob'])
        bet = round(bankroll * f, 2)
        total_bet += bet
        print(f"{team:<25} {f:>9.1%} {f'${bet}':>12} {'BUY':>8}")

print(f"\nTotal capital deployed: ${round(total_bet, 2)}")
print(f"Capital held back: ${round(bankroll - total_bet, 2)}")