📘 Revenue Prediction System (KNBS Project)
Mission & Problem Statement

This project aims to help Hotels and accomodation facilities estimate tourism accommodation revenue using machine-learning models trained on cleaned KNBS datasets. The system predicts revenue based on occupancy, facility characteristics, and monthly patterns. It provides a public API for real-time predictions and a mobile app interface for easy use.

🌐 Public Prediction API (Swagger UI)

Base URL:
👉 https://revenue-prediction-api.onrender.com
Swagger UI:
👉 https://revenue-prediction-api.onrender.com/docs

This endpoint accepts feature inputs and returns a predicted revenue value using the deployed ML model.

🎥 Demo Videos

👉 https://drive.google.com/drive/folders/1dktOHzYmC5UC7RRAxm1x0ShA382r9L6f?usp=drive_link


📱 How to Run the Mobile App (Flutter)
1. Install Flutter

Follow official installation:
https://docs.flutter.dev/get-started/install

2. Clone the repository
git clone https://github.com/sam-wanjohi/Revenue_prediction.git
cd Revenue_prediction/flutter_app

3. Install dependencies
flutter pub get

4. Update the API URL

Edit this file:

flutter_app/lib/services/api_service.dart


Set:

static const String baseUrl = "https://revenue-prediction-api.onrender.com";

5. Run the app
flutter run


Choose your phone or emulator from the list.