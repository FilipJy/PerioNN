import React, { useState } from 'react';
import './App.css';

function PredictForm() {
  const [name, setName] = useState('');
  const [year, setYear] = useState(0);
  const [issue, setIssue] = useState(0);
  const [publisher, setPublisher] = useState('');
  const [correctedPages, setCorrectedPages] = useState(0);
  const [prediction, setPrediction] = useState(null);

  const handlePredictSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://0.0.0.0:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `name=${name}&year=${year}&issue=${issue}&publisher=${publisher}`,
      });
      const data = await response.json();
      const predictedPages = data['Predicted Pages'];
      
      setPrediction(Math.floor(predictedPages));
    } catch (error) {
      console.error('Error predicting pages:', error);
    }
  };

  const handleCorrectSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://0.0.0.0:8000/correct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `corrected_pages=${correctedPages}`,
      });
      const data = await response.json();
      console.log(data['message']);
    } catch (error) {
      console.error('Error correcting and retraining:', error);
    }
  };

  return (
    <div className="everything">
      <h2>Predict Pages</h2>
      <form onSubmit={handlePredictSubmit}>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="number" placeholder="Year" value={year} onChange={(e) => setYear(e.target.value)} required />
        <input type="number" placeholder="Issue" value={issue} onChange={(e) => setIssue(e.target.value)} required />
        <input type="text" placeholder="Publisher" value={publisher} onChange={(e) => setPublisher(e.target.value)} required />
        <button type="submit">Predict</button>
      </form>
      {prediction && <p>Predicted Pages: {prediction}</p>}

      <h2>Correct and Retrain</h2>
      <form onSubmit={handleCorrectSubmit}>
        <input
          type="number"
          placeholder="Corrected Pages"
          value={correctedPages}
          onChange={(e) => setCorrectedPages(e.target.value)}
          required
        />
        <button type="submit">Correct and Retrain</button>
      </form>
    </div>
  );
}

export default PredictForm;
