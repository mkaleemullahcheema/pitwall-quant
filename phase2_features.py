import pandas as pd

# Load cleaned qualifying data
laps = pd.read_csv('clean_laps.csv')
print("Data loaded successfully")
print(laps.shape)
print(laps.head())

# ---- FUEL CORRECTION ----
def fuel_correct(lap_time, lap_number, fuel_effect=0.03):
    correction = (lap_number - 1) * fuel_effect
    return lap_time + correction

laps['FuelCorrectedTime'] = laps.apply(
    lambda row: fuel_correct(row['LapTimeSeconds'], row['LapNumber']),
    axis=1
)

print("\nFuel corrected times added")
print(laps[['Driver', 'Team', 'LapNumber', 'LapTimeSeconds', 'FuelCorrectedTime']].head(10))

laps.to_csv('clean_laps.csv', index=False)
print("Updated data saved")