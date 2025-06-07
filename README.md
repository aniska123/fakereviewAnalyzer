# Fake Product Review Detection System

A web application to detect AI-generated product reviews using NLP and machine learning.

## Tech Stack
- **Frontend**: React.js
- **Backend**: Flask
- **Database**: MySQL
- **Data Science**: NLP (TF-IDF, Sentiment Analysis), ML (Logistic Regression)

## Setup Instructions
1. **Backend**:
   - `cd backend`
   - `pip install -r requirements.txt`
   - Update `.env` with MySQL credentials
   - `python app.py`

2. **Frontend**:
   - `cd frontend`
   - `npm install`
   - `npm start`

3. **Database**:
   - Run `schema.sql` and `sample_data.sql` in MySQL

## Features
- Classify reviews as real or AI-generated
- Display product credibility scores

## License
MIT
