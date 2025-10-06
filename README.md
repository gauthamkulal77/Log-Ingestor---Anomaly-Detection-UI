# Log-Ingestor  & Anomaly Detection UI

A full-stack log ingestor with a React UI and Python backend. This tool uses a mock AI model to classify logs as "normal" or "anomaly" and stores them in MongoDB. The interface allows for dynamic, real-time filtering and searching of all log data.
Log Ingestor & Query Interface

A full-stack log management system to ingest, search, filter, and analyze logs with AI-powered anomaly detection.
Built with React (frontend), Flask (backend), and MongoDB Atlas (database).

Live Webpage : https://log-ingestor-project-123-e0d04.web.app/


Features

  * Filter logs by level, message, resourceId, traceId, spanId, commit, parentResourceId
  * Start / End date filters for time-based log queries  
  * Prediction badge (Anomaly / Normal)  
  * Logs displayed in a responsive, styled table  
  * Reset button to clear all filters
  * Deployable on Firebase (frontend) and Google App Engine (backend)

Tech Stack

  Frontend: React, Axios, CSS, Firebase Hosting                                                                                                                                           
  Backend: Python, Flask, Gunicorn, Google App Engine                                                                                                                                     
  Database: MongoDB Atlas                                                                                                                                                                 
  Deployment: Firebase Hosting + Google App Engine                                                                                                                                        

Getting Started
  1. Clone the Repository
     git clone https://github.com/gauthamkulal77/log-ingestor.git
     cd log-ingestor

  2. Backend Setup (Flask API)
    
    Navigate to the backend folder:
    cd backend

  Create a virtual environment (recommended):
    
    python -m venv venv
    source venv/bin/activate   # Mac/Linux
    venv\Scripts\activate      # Windows


  Install dependencies:

    pip install -r requirements.txt

  Create a .env file in backend/ and add:

    MONGO_URI=your-mongodb-connection-string
    PORT=5000

  Start the backend:

    python app.py
    Runs at: http://localhost:5000

3. Frontend Setup (React)

  pen a new terminal and go to the frontend folder:
  
    cd frontend

  Install dependencies:

    npm install

  Update App.js API URL for local dev:

    const API_URL = "http://localhost:5000";  // Local backend


  In production, replace with your App Engine URL.

Start the frontend:

    npm start

Runs at: http://localhost:3000

Deployment
  Frontend (Firebase Hosting)

  Build production files:

    npm run build


  Deploy to Firebase:

    firebase deploy

Backend (Google App Engine – Flask)

  Deploy to App Engine:

    gcloud app deploy

  View live logs:

    gcloud app logs tail -s default

SCREENSHOTS:
<img width="1360" height="684" alt="image" src="https://github.com/user-attachments/assets/4ad23f6f-2670-4351-b7cc-d2618731d478" />



Requirements.txt (Backend)                                                                                                                                                                
Flask==2.3.2                                                                                                                                                                              
pymongo==4.5.0                                                                                                                                                                            
dnspython==2.4.2                                                                                                                                                                          
python-dotenv==1.0.0                                                                                                                                                                      
gunicorn==21.2.0

