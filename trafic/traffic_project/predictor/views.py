from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import joblib
import numpy as np
import os
import json

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

def map_view(request):
    """Display traffic map for Kigali city"""
 
    model = get_model()
    
   
    kigali_center = {
        'lat': -1.9536,
        'lng': 30.0605
    }
    
    
    streets = [
        {
            'name': 'KN 2 Road (Main Highway)',
            'lat': -1.9520,
            'lng': 30.0650,
            'traffic_density': 85,  # High traffic
            'roads': [
                [-1.9500, 30.0630],
                [-1.9520, 30.0650],
                [-1.9540, 30.0670]
            ]
        },
        {
            'name': 'Kigali City Center',
            'lat': -1.9536,
            'lng': 30.0605,
            'traffic_density': 90,  # Very High traffic
            'roads': [
                [-1.9520, 30.0590],
                [-1.9536, 30.0605],
                [-1.9550, 30.0620]
            ]
        },
        {
            'name': 'Nyamirambo Area',
            'lat': -1.9600,
            'lng': 30.0500,
            'traffic_density': 60,  # Medium traffic
            'roads': [
                [-1.9580, 30.0480],
                [-1.9600, 30.0500],
                [-1.9620, 30.0520]
            ]
        },
        {
            'name': 'Kacyiru District',
            'lat': -1.9450,
            'lng': 30.0800,
            'traffic_density': 70,  # High traffic
            'roads': [
                [-1.9430, 30.0780],
                [-1.9450, 30.0800],
                [-1.9470, 30.0820]
            ]
        },
        {
            'name': 'Gisozi Area',
            'lat': -1.9400,
            'lng': 30.0550,
            'traffic_density': 50,  # Medium traffic
            'roads': [
                [-1.9380, 30.0530],
                [-1.9400, 30.0550],
                [-1.9420, 30.0570]
            ]
        },
        {
            'name': 'Kimihurura District',
            'lat': -1.9350,
            'lng': 30.0900,
            'traffic_density': 65,  # Medium-High traffic
            'roads': [
                [-1.9330, 30.0880],
                [-1.9350, 30.0900],
                [-1.9370, 30.0920]
            ]
        }
    ]
    
    context = {
        'kigali_center': kigali_center,
        'streets': streets,
    }
    
    return render(request, 'predictor/map.html', context)

def get_traffic_data(request):
    """API endpoint to get traffic predictions for specific time"""
    model = get_model()
    if model is None:
        return JsonResponse({'error': 'Model not available'}, status=500)
    
    hour = int(request.GET.get('hour', 12))
    day = int(request.GET.get('day', 0))
    is_holiday = int(request.GET.get('is_holiday', 0))
    
    # Major streets and areas in Kigali
    streets = [
        {'name': 'KN 2 Road', 'lat': -1.9520, 'lng': 30.0650},
        {'name': 'City Center', 'lat': -1.9536, 'lng': 30.0605},
        {'name': 'Nyamirambo', 'lat': -1.9600, 'lng': 30.0500},
        {'name': 'Kacyiru', 'lat': -1.9450, 'lng': 30.0800},
        {'name': 'Gisozi', 'lat': -1.9400, 'lng': 30.0550},
        {'name': 'Kimihurura', 'lat': -1.9350, 'lng': 30.0900},
    ]
    
    predictions = []
    for street in streets:
        # Get traffic prediction
        input_data = np.array([[hour, day, is_holiday]])
        base_prediction = model.predict(input_data)[0]
        
        # Add some variation based on location
        variation = np.random.randint(-50, 50)
        traffic_volume = max(100, int(base_prediction + variation))
        
        # Calculate traffic density (0-100)
        traffic_density = min(100, int((traffic_volume / 2000) * 100))
        
        predictions.append({
            'name': street['name'],
            'lat': street['lat'],
            'lng': street['lng'],
            'traffic_volume': traffic_volume,
            'traffic_density': traffic_density,
            'status': 'Heavy' if traffic_density > 75 else 'Moderate' if traffic_density > 50 else 'Light'
        })
    
    return JsonResponse({'data': predictions})

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