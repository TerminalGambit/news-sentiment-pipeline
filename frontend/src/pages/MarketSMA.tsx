import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Plot from 'react-plotly.js';
import { marketApi, MarketData } from '../services/api';

const MarketSMA: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const [smaData, setSmaData] = useState<MarketData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!ticker) return;
      
      try {
        setLoading(true);
        const response = await marketApi.getSMAData(ticker);
        setSmaData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
      <h2 className="mb-4">{ticker} Simple Moving Averages</h2>
      
      <div className="alert alert-info mb-4">
        <h5>What is SMA?</h5>
        <p>
          Simple Moving Average (SMA) is a technical indicator that helps identify trends by smoothing out price data.
          The 20-day SMA shows short-term trends, while the 50-day SMA indicates medium-term trends.
          When the price crosses above the SMA, it may signal an uptrend, and when it crosses below, it may indicate a downtrend.
        </p>
      </div>

      {smaData && (
        <Plot
          data={[
            {
              x: smaData.dates,
              y: smaData.prices,
              type: 'scatter',
              mode: 'lines',
              name: 'Close Price',
              line: { color: '#007bff' }
            },
            {
              x: smaData.dates,
              y: smaData.sma20,
              type: 'scatter',
              mode: 'lines',
              name: 'SMA 20',
              line: { color: '#28a745', dash: 'dot' }
            },
            {
              x: smaData.dates,
              y: smaData.sma50,
              type: 'scatter',
              mode: 'lines',
              name: 'SMA 50',
              line: { color: '#dc3545', dash: 'dash' }
            }
          ]}
          layout={{
            title: { text: 'Close Price with 20 & 50 Day SMA' },
            xaxis: { title: { text: 'Date' } },
            yaxis: { title: { text: 'Price (USD)' } },
            margin: { t: 40 }
          }}
          config={{ responsive: true }}
          style={{ height: '400px' }}
        />
      )}
    </div>
  );
};

export default MarketSMA; 