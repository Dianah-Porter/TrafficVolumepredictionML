
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import sys


print(" Loading Dataset...")

cli_mode = len(sys.argv) >= 3

data = pd.read_csv('traffic_smart_city.csv')

X = data[['Hour', 'DayOfWeek', 'IsHoliday']]
y = data['TrafficVolume']
print(f"   Data Loaded: {len(data)} rows.")
print("   Features: Hour, DayOfWeek, IsHoliday")


print("\n Training the Artificial Intelligence...")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("   Model Training Complete!")


print("\n Checking Accuracy...")
y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred)
error_margin = mean_absolute_error(y_test, y_pred)

print(f"    Model Accuracy: {accuracy * 100:.2f}%")
print("    Average Error: +/- {int(error_margin)} cars")
print("   (This high accuracy proves the model understands the city's patterns)")
if not cli_mode:
    plt.figure(figsize=(14, 5))

    plt.subplot(1, 2, 1)
    plt.plot(y_test.values[:50], label='Actual Traffic', marker='o', color='blue', alpha=0.5)
    plt.plot(y_pred[:50], label='AI Prediction', linestyle='--', color='red', linewidth=2)
    plt.title('AI Prediction vs Reality (First 50 Samples)')
    plt.xlabel('Time Steps')
    plt.ylabel('Number of Cars')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    importance = model.feature_importances_
    features = ['Hour of Day', 'Day of Week', 'Is Holiday?']
    sns.barplot(x=importance, y=features, palette='magma')
    plt.title('What Drives Traffic in the City?')
    plt.xlabel('Importance Score')

    plt.tight_layout()
    plt.show()

    print("\n" + "="*40)
    print("   🚦 LIVE SCENARIO SIMULATION   ")
    print("="*40)

def predict_scenario(hour, day_name, is_holiday):
    days = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
    day_num = days[day_name]
    prediction = model.predict([[hour, day_num, is_holiday]])[0]
    status = "Regular Day" if is_holiday == 0 else "HOLIDAY "
    print(f"Time: {hour}:00 | Day: {day_name} | {status}")
    print(f"🚗 Predicted Traffic: {int(prediction)} cars")
    print("-" * 30)

if not cli_mode:
    print("Comparison 1: Does the AI know Friday is busier?")
    predict_scenario(18, 'Tue', 0)
    predict_scenario(18, 'Fri', 0)

    print("\nComparison 2: Does the AI respect Holidays?")
    predict_scenario(8, 'Mon', 0)
    predict_scenario(8, 'Mon', 1)

def _normalize_day(inp: str) -> str:
    inp = inp.strip().lower()
    names = {
        'mon': 'Mon', 'monday': 'Mon',
        'tue': 'Tue', 'tues': 'Tue', 'tuesday': 'Tue',
        'wed': 'Wed', 'wednesday': 'Wed',
        'thu': 'Thu', 'thursday': 'Thu',
        'fri': 'Fri', 'friday': 'Fri',
        'sat': 'Sat', 'saturday': 'Sat',
        'sun': 'Sun', 'sunday': 'Sun'
    }
    return names.get(inp, '')


if __name__ == '__main__':
    try:
        if cli_mode:
           
            day_in = sys.argv[1]
            hour_in = sys.argv[2]
            hol_in = sys.argv[3] if len(sys.argv) > 3 else 'n'

            day_abbr = _normalize_day(day_in)
            if not day_abbr:
                print("Invalid day. Use Mon,Tue,Wed,Thu,Fri,Sat,Sun or full name.")
            else:
                try:
                    hour = int(hour_in)
                    if hour < 0 or hour > 23:
                        raise ValueError()
                except ValueError:
                    print("Invalid hour. Must be integer 0-23.")
                    hour = None

                is_holiday = 1 if str(hol_in).strip().lower() in ('y', 'yes', '1', 'true') else 0

                if hour is not None:
                    predict_scenario(hour, day_abbr, is_holiday)
        else:
            print("\n--- Interactive Prediction ---")
            day_in = input("Enter day (Mon/Tue/... or Monday): ")
            day_abbr = _normalize_day(day_in)
            if not day_abbr:
                print("Invalid day. Use Mon,Tue,Wed,Thu,Fri,Sat,Sun or full name.")
            else:
                hour_in = input("Enter hour (0-23): ")
                try:
                    hour = int(hour_in)
                    if hour < 0 or hour > 23:
                        raise ValueError()
                except ValueError:
                    print("Invalid hour. Must be integer 0-23.")
                    hour = None

                hol_in = input("Is it a holiday? (y/n): ")
                is_holiday = 1 if hol_in.strip().lower() in ('y', 'yes', '1', 'true') else 0

                if hour is not None:
                    print("\nResult:")
                    predict_scenario(hour, day_abbr, is_holiday)
    except KeyboardInterrupt:
        print("\nExiting interactive mode.")

