
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib


np.random.seed(42)

print("Generating synthetic traffic data...")

# Create features (hour, day_of_week, is_holiday)
hours = []
days = []
holidays = []
volumes = []

# Generate data for different scenarios
for hour in range(24):
    for day in range(7):
        for holiday in range(2):
            hours.append(hour)
            days.append(day)
            holidays.append(holiday)
            base_volume = 1000
            # Hour-based pattern (rush hours)
            if 7 <= hour < 10 or 17 <= hour < 20:
                base_volume += 500
            # Night-time less traffic
            if 22 <= hour or hour < 6:
                base_volume -= 300
            
            # Weekday vs weekend
            if day < 5:  # Weekday
                base_volume *= 1.2
            else:  # Weekend
                base_volume *= 0.8
            
            # Holiday effect
            if holiday:
                base_volume *= 0.7
            
            # Add some random noise
            noise = np.random.normal(0, 100)
            final_volume = max(100, base_volume + noise)
            
            volumes.append(final_volume)

# Convert to numpy arrays
X = np.array([hours, days, holidays]).T
y = np.array(volumes)

print(f"Training data shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Train the model
print("Training Random Forest model...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

# Evaluate on training data
train_score = model.score(X, y)
print(f"Training R² score: {train_score:.4f}")

# Save the model
model_path = os.path.join(os.path.dirname(__file__), 'ml_models', 'traffic_model.pkl')
os.makedirs(os.path.dirname(model_path), exist_ok=True)

print(f"Saving model to {model_path}...")
joblib.dump(model, model_path)

print("Model training completed successfully!")


print("\nTesting model with sample predictions:")
test_cases = [
    (8, 0, 0, "Monday 8:00 AM, Regular day"),
    (18, 4, 0, "Friday 6:00 PM, Regular day"),
    (12, 5, 1, "Saturday 12:00 PM, Holiday"),
    (3, 2, 0, "Wednesday 3:00 AM, Regular day"),
]

for hour, day, holiday, description in test_cases:
    prediction = model.predict([[hour, day, holiday]])[0]
    print(f"  {description}: {prediction:.0f} cars")
