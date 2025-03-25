import React, { useState } from 'react';
import axios from 'axios';
import './ReviewAnalyzer.css';

function ReviewAnalyzer() {
  const [review, setReview] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', { review });
      setResult(response.data);
    } catch (error) {
      setResult({ error: 'Error analyzing review' });
    }
    setLoading(false);
  };

  return (
    <div className="analyzer-container">
      <div className="analyzer-box animate-fade-in">
        <h1>Fake Review Detector</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            placeholder="Enter your review here..."
            value={review}
            onChange={(e) => setReview(e.target.value)}
            rows="5"
            required
          />
          <button type="submit" className="analyze-button" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Review'}
          </button>
        </form>
        {result && (
          <div className="result animate-result">
            {result.error ? (
              <p className="error">{result.error}</p>
            ) : (
              <>
                <h3>Result</h3>
                <p>
                  Prediction: {result.prediction} (Confidence:{' '}
                  {(result.confidence * 100).toFixed(2)}%)
                </p>
                <p>Characteristics: {result.rationale.join(', ')}</p>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ReviewAnalyzer;