# student-monitoring-system

# Real-Time Student Monitoring & Engagement System

This project is a real-time AI-powered student monitoring system designed to support **exam integrity** and **student engagement analysis**.  
It consists of two interfaces:

1. **Student Portal** – Captures webcam video and streams frames in real time  
2. **Teacher Dashboard** – Displays live engagement status and proctoring alerts  

The system emphasizes **confusion detection** using explainable computer vision logic.

# steps to execute code

# install requirement from requiremennts.txt
cd backend
pip install -r requirements.txt

# Start the backend server:
uvicorn main:app --reload

-- then you have to open student.html in web browser
-- give camera permission 
-- then open techer.html 

