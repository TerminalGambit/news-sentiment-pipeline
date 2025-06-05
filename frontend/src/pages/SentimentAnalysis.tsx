import React, { useState } from 'react';
import { sentimentApi, SentimentResult } from '../services/api';

const SentimentAnalysis: React.FC = () => {
  const [text, setText] = useState<string>('');
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await sentimentApi.analyzeText(text);
      setResult(response.data);
    } catch (err) {
      setError('Failed to analyze text');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (label: string) => {
    switch (label) {
      case 'Positive':
        return 'text-green-600';
      case 'Negative':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Sentiment Analysis</h2>
        <div className="space-y-4">
          <div>
            <label
              htmlFor="text"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Enter text to analyze
            </label>
            <textarea
              id="text"
              rows={4}
              className="input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type or paste your text here..."
            />
          </div>
          <button
            className="btn btn-primary w-full"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze Sentiment'}
          </button>
        </div>
      </div>

      {error && (
        <div className="card bg-red-50 border border-red-200">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {result && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Analysis Result</h3>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500 mb-1">Sentiment</p>
              <p
                className={`text-xl font-semibold ${getSentimentColor(
                  result.sentiment.label
                )}`}
              >
                {result.sentiment.label}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500 mb-1">Confidence Score</p>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className={`h-2.5 rounded-full ${
                    result.sentiment.label === 'Positive'
                      ? 'bg-green-600'
                      : result.sentiment.label === 'Negative'
                      ? 'bg-red-600'
                      : 'bg-gray-600'
                  }`}
                  style={{
                    width: `${(result.sentiment.score * 100).toFixed(1)}%`,
                  }}
                ></div>
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {(result.sentiment.score * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SentimentAnalysis; 