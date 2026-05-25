from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np

# Load clean data
laps = pd.read_csv('clean_laps.csv')

# Convert Compound to numbers since ML can't read text
laps['CompoundEncoded'] = laps['Compound'].map({
    'SOFT': 1,
    'MEDIUM': 2,
    'HARD': 3
})

laps = laps.dropna(subset=['CompoundEncoded', 'LapTimeSeconds', 'FuelCorrectedTime'])

# Define features and target
X = laps[['CompoundEncoded', 'FuelCorrectedTime']]
y = laps['LapTimeSeconds']

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Test the model
predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)

print(f"Model trained successfully")
print(f"Average prediction error: {error:.3f} seconds")

# ---- BETTING ODDS & TRADING SIGNALS ----

odds = {
    'Red Bull Racing': 1.25,
    'Ferrari': 5.00,
    'Mercedes': 8.00,
    'Aston Martin': 15.00,
    'McLaren': 20.00,
    'Alpine': 50.00,
    'Haas F1 Team': 100.00,
    'AlphaTauri': 100.00,
    'Alfa Romeo': 100.00,
    'Williams': 200.00
}

# Convert odds to implied probabilities
market = {team: 1/odd for team, odd in odds.items()}

# Get each team's single fastest lap from qualifying
team_pace = laps.groupby('Team')['LapTimeSeconds'].min()

# Calculate gap from fastest team
fastest = team_pace.min()
performance_gap = team_pace - fastest

# Exponential scaling - bigger gap = lower probability
raw_scores = np.exp(-performance_gap * 2)
model_prob = raw_scores / raw_scores.sum()

# Generate signals
print("\n--- PITWALL QUANT TRADING SIGNALS ---\n")
print(f"{'Team':<25} {'Market Odds':>12} {'Market Prob':>12} {'Model Prob':>12} {'Signal':>8}")
print("-" * 75)

for team in odds:
    if team in model_prob.index:
        mkt = market[team]
        mdl = model_prob[team]
        diff = mdl - mkt
        signal = "BUY" if diff > 0.02 else "SELL" if diff < -0.02 else "HOLD"
        print(f"{team:<25} {odds[team]:>12.2f} {mkt:>11.1%} {mdl:>11.1%} {signal:>8}")