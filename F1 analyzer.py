import fastf1
from fastf1 import plotting
import pandas as pd
from matplotlib import pyplot as plt

# FEATURES
# 1. Load race
# 2. Print race result
# 3. Show fastest lap of chosen driver and fastest lap overall
# 4. Show graph comparing top 3 drivers
# 5. Show biggest gainer and loser (Race only)

plotting.setup_mpl(
    mpl_timedelta_support=True,
    color_scheme='fastf1'
)

fastf1.Cache.enable_cache(r'C:\Users\HP\F1')

getting_year_user_prefers = int(input("Input a given year: \n"))
getting_location_user_prefers = input("Input a race location: \n")
getting_session_type_user_prefers = input(
    "Enter session type (FP1, FP2, FP3, Q, SQ, R): \n"
).upper()

print(
"Driver Abbreviations:\n"
"Kimi Antonelli = ANT\n"
"Oscar Piastri = PIA\n"
"Lewis Hamilton = HAM\n"
"Max Verstappen = VER\n"
"Charles Leclerc = LEC\n"
"George Russell = RUS\n"
"Sergio Perez = PER\n"
"Carlos Sainz = SAI\n"
"Fernando Alonso = ALO\n"
"Valtteri Bottas = BOT\n"
"Pierre Gasly = GAS\n"
"Lando Norris = NOR\n"
"Isack Hadjar = HAD\n"
"Franco Colapinto = COL\n"
"Ollie Bearman = BEA\n"
"Esteban Ocon = OCO\n"
"Gabriel Bortoleto = BOR\n"
"Nico Hulkenberg = HUL\n"
"Lance Stroll = STR\n"
"Alex Albon = ALB\n"
"Liam Lawson = LAW\n"
"Arvid Lindblad = LIN\n"
)

fastest_driver = input(
    "Enter the abbreviation of the driver you want to see the fastest lap for: "
).upper()

print(f"\nLoading data for {getting_year_user_prefers} {getting_location_user_prefers} - Session: {getting_session_type_user_prefers}\n")
print(f"Loading fastest lap for {fastest_driver}...\n")

session = fastf1.get_session(
    getting_year_user_prefers,
    getting_location_user_prefers,
    getting_session_type_user_prefers
)

session.load()

# ==========================
# TOP 3 GRAPH
# ==========================

top3 = session.results.head(3)

for row in top3.itertuples():

    driver = row.DriverNumber
    abbreviation = row.Abbreviation

    driver_laps = (
        session.laps
        .pick_drivers(driver)
        .pick_quicklaps()
    )

    if not driver_laps.empty:

        plt.plot(
            driver_laps["LapNumber"],
            driver_laps["LapTime"].dt.total_seconds(),
            label=abbreviation
        )

# ==========================
# RESULTS TABLE
# ==========================

results = session.results[
    ["Position", "Abbreviation", "TeamName", "Status", "GridPosition"]
].copy()

results["Position"] = pd.to_numeric(
    results["Position"],
    errors="coerce"
)

results["GridPosition"] = pd.to_numeric(
    results["GridPosition"],
    errors="coerce"
)

# Race-only statistics
if getting_session_type_user_prefers == "R":

    results["Positions Gained"] = (
        results["GridPosition"] -
        results["Position"]
    )

    valid = results.dropna(subset=["Positions Gained"])

    if not valid.empty:
        biggest_gain = valid.loc[
            valid["Positions Gained"].idxmax()
        ]

        worst_gain = valid.loc[
            valid["Positions Gained"].idxmin()
        ]

# ==========================
# FASTEST LAPS
# ==========================

laps = session.laps

fastest = laps.pick_fastest()

driver_laps = laps.pick_drivers(fastest_driver)

if driver_laps.empty:
    fastest_lap = None
else:
    fastest_lap = driver_laps.pick_fastest()

# ==========================
# TERMINAL OUTPUT
# ==========================

print("Data loaded successfully! Your result is ready for viewing\n")

print(results.to_string(index=False))

print("\n")

print(f"Total laps: {len(laps)}")

print("\n")

if fastest_lap is None:
    print(f"{fastest_driver} did not participate in this session.")
else:
    print("Fastest lap for selected driver:\n")
    print(fastest_lap)

print("\n")

print("Fastest lap of the session:\n")
print(fastest)

print("\n")

if getting_session_type_user_prefers == "R":

    print(
        f"🏆 Biggest Gainer: "
        f"{biggest_gain['Abbreviation']} "
        f"(+{int(biggest_gain['Positions Gained'])} places)"
    )

    print()

    print(
        f"📉 Biggest Loser: "
        f"{worst_gain['Abbreviation']} "
        f"({int(worst_gain['Positions Gained'])} places)"
    )

else:

    print("Positions gained/lost is only available for Race sessions.")

# ==========================
# GRAPH
# ==========================

plt.xlabel("Lap Number")
plt.ylabel("Lap Time (s)")
plt.title(
    f"{getting_year_user_prefers} {getting_location_user_prefers} "
    f"{getting_session_type_user_prefers} - Top 3 Driver Comparison"
)
plt.legend()
plt.grid(True)
plt.show()