import fastf1
import pandas as pd

fastf1.Cache.enable_cache('cache')

print("Loading session... this may take a minute on first run")
session = fastf1.get_session(2023, 'Bahrain', 'Q')
session.load()

laps = session.laps

# Qualifying doesn't have TrackStatus so we use fewer columns
columns = ['Driver', 'Team', 'LapTime', 'LapNumber', 'Compound']
laps = laps[columns].copy()

print("Raw data loaded:")
print(laps.shape)
print(laps.head(10))

# ---- DATA CLEANING ----

# Remove missing lap times
laps = laps.dropna(subset=['LapTime'])

# Convert to seconds
laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

# Remove outliers per driver
median_times = laps.groupby('Driver')['LapTimeSeconds'].transform('median')
laps = laps[laps['LapTimeSeconds'] <= median_times * 1.1]

print(f"\nClean laps remaining: {len(laps)}")
print(laps.sort_values('LapTimeSeconds').head(10))

laps.to_csv('clean_laps.csv', index=False)
print("Clean data saved to clean_laps.csv")