import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Plot from 'react-plotly.js';
import { marketApi, MarketData } from '../services/api';

interface MACDData {
  dates: string[];
  macd?: number[];
  signal?: number[];
  histogram?: number[];
}

const MarketMACD: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const [macdData, setMACDData] = useState<MACDData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMACD = async () => {
      if (!ticker) return;
      
      try {
        setLoading(true);
        const response = await marketApi.getMACDData(ticker);
        setMACDData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchMACD();
  }, [ticker]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="alert alert-danger">Error: {error}</div>;
  }

  if (!ticker) {
    return <div className="alert alert-warning">No ticker specified</div>;
  }

  return (
    <div className="container mt-4">
      <h2 className="mb-4">MACD Analysis</h2>
      
      <div className="alert alert-info mb-4">
        <h5>What is MACD?</h5>
        <p>
          The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows
          the relationship between two moving averages of a security's price. The MACD line is calculated by
          subtracting the 26-period EMA from the 12-period EMA. The signal line is a 9-period EMA of the MACD line.
          The histogram represents the difference between the MACD line and the signal line.
        </p>
      </div>

      {macdData && (
        <Plot
          data={[
            {
              x: macdData.dates,
              y: macdData.macd || [],
              type: 'scatter',
              mode: 'lines',
              name: 'MACD Line',
              line: { color: '#007bff' }
            },
            {
              x: macdData.dates,
              y: macdData.signal || [],
              type: 'scatter',
              mode: 'lines',
              name: 'Signal Line',
              line: { color: '#28a745' }
            },
            {
              x: macdData.dates,
              y: macdData.histogram || [],
              type: 'bar',
              name: 'Histogram',
              marker: {
                color: (macdData.histogram || []).map(value => value >= 0 ? '#28a745' : '#dc3545')
              }
            }
          ]}
          layout={{
            title: { text: 'MACD Chart' },
            xaxis: { title: { text: 'Date' } },
            yaxis: { title: { text: 'Value' } },
            margin: { t: 40 }
          }}
          config={{ responsive: true }}
          style={{ height: '400px' }}
        />
      )}
    </div>
  );
};

export default MarketMACD; 