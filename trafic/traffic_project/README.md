# Traffic Volume Prediction Web Application

This project is a Django web application designed to predict traffic volume based on user inputs such as hour of the day, day of the week, and whether it is a holiday. The application utilizes a pre-trained machine learning model to provide accurate predictions.

## Project Structure

```
traffic_project/
├── traffic_project/          # Main Django project directory
│   ├── __init__.py
│   ├── settings.py           # Configuration settings for the Django project
│   ├── urls.py               # URL routing for the project
│   └── wsgi.py               # WSGI entry point for the application
├── predictor/                # Django app for traffic prediction
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Admin site configuration
│   ├── apps.py               # App configuration
│   ├── models.py             # Data models (currently empty)
│   ├── views.py              # View functions for handling requests
│   ├── urls.py               # URL routing for the predictor app
│   ├── forms.py              # Forms for user input
│   └── templates/            # HTML templates for the app
│       └── predictor/
│           ├── index.html    # Main input form page
│           └── prediction.html # Page to display prediction results
├── static/                   # Static files (CSS, JS, etc.)
│   └── css/
│       └── style.css         # Custom styles for the application
├── ml_models/                # Directory for machine learning models
│   └── traffic_model.pkl     # Pre-trained traffic prediction model
├── manage.py                 # Command-line utility for Django
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd traffic_project
   ```

2. **Create a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```
   python manage.py runserver
   ```

6. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:8000/` to access the traffic prediction application.

## Usage

- On the main page, enter the hour of the day, select the day of the week, and indicate if it is a holiday.
- Submit the form to receive a prediction of the traffic volume for the specified inputs.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.