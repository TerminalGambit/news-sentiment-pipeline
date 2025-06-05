import React, { useState } from 'react';
import { sentimentApi } from '../services/api';

interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral';
  score: number;
}

const SentimentAnalysis: React.FC = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter some text.');
      return;
    }
    setError(null);
    setLoading(true);
    setResult(null);
    try {
      const response = await sentimentApi.analyzeText(text);
      setResult(response.data);
    } catch (err) {
      setError('Failed to analyze sentiment.');
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'text-green-600';
      case 'negative':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Sentiment Analysis</h2>
      <textarea
        className="form-control mb-3"
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to analyze..."
      />
      <button className="btn btn-primary mb-3" onClick={handleAnalyze} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
      {error && <div className="alert alert-danger">{error}</div>}
      {result && (
        <div className="mt-4">
          <p className={`text-xl font-semibold ${getSentimentColor(result.sentiment)}`}>{result.sentiment}</p>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div
              className={`h-2.5 rounded-full ${
                result.sentiment === 'positive'
                  ? 'bg-green-600'
                  : result.sentiment === 'negative'
                  ? 'bg-red-600'
                  : 'bg-gray-600'
              }`}
              style={{ width: `${(result.score * 100).toFixed(1)}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 mt-1">{(result.score * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  );
};

export default SentimentAnalysis; 