from django.shortcuts import render
from django.http import HttpResponse
import joblib
import numpy as np
import os

# Global variable to cache the model
_model = None

def get_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'traffic_model.pkl')
        try:
            _model = joblib.load(model_path)
        except Exception as e:
            print(f"Warning: Could not load model from {model_path}: {e}")
            _model = None
    return _model

def index(request):
    return render(request, 'predictor/index.html')

def predict(request):
    if request.method == 'POST':
        model = get_model()
        if model is None:
            return HttpResponse("Model not available. Please train the model first.", status=500)
        
        hour = int(request.POST['hour'])
        day_name = request.POST.get('day', '')
        is_holiday = int(request.POST['is_holiday'])
        
        # Convert day name to day of week number (0-6, where 0 is Monday)
        day_mapping = {
            'Mon': 0, 'Monday': 0,
            'Tue': 1, 'Tuesday': 1,
            'Wed': 2, 'Wednesday': 2,
            'Thu': 3, 'Thursday': 3,
            'Fri': 4, 'Friday': 4,
            'Sat': 5, 'Saturday': 5,
            'Sun': 6, 'Sunday': 6,
        }
        day_of_week = day_mapping.get(day_name, 0)

        # Prepare input for the model
        input_data = np.array([[hour, day_of_week, is_holiday]])
        prediction = model.predict(input_data)[0]

        return render(request, 'predictor/prediction.html', {
            'prediction': int(prediction),
            'hour': hour,
            'day_name': day_name,
            'is_holiday': 'Yes' if is_holiday else 'No'
        })

    return HttpResponse("Invalid request method.")