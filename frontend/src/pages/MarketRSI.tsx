import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Plot from 'react-plotly.js';
import { marketApi, MarketData } from '../services/api';

const MarketRSI: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const [rsiData, setRsiData] = useState<MarketData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!ticker) return;
      
      try {
        setLoading(true);
        const response = await marketApi.getRSIData(ticker);
        setRsiData(response.data);
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
      <h2 className="mb-4">{ticker} Relative Strength Index (RSI)</h2>
      
      <div className="alert alert-info mb-4">
        <h5>What is RSI?</h5>
        <p>
          The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements.
          RSI values range from 0 to 100. Traditionally, RSI values above 70 indicate overbought conditions,
          while values below 30 suggest oversold conditions. RSI can help identify potential trend reversals
          and overbought/oversold conditions.
        </p>
      </div>

      {rsiData && (
        <Plot
          data={[
            {
              x: rsiData.dates,
              y: rsiData.rsi,
              type: 'scatter',
              mode: 'lines',
              name: 'RSI',
              line: { color: '#007bff' }
            },
            {
              x: rsiData.dates,
              y: Array(rsiData.dates.length).fill(70),
              type: 'scatter',
              mode: 'lines',
              name: 'Overbought',
              line: { color: '#dc3545', dash: 'dash' }
            },
            {
              x: rsiData.dates,
              y: Array(rsiData.dates.length).fill(30),
              type: 'scatter',
              mode: 'lines',
              name: 'Oversold',
              line: { color: '#28a745', dash: 'dash' }
            }
          ]}
          layout={{
            title: { text: 'RSI Chart' },
            xaxis: { title: { text: 'Date' } },
            yaxis: { 
              title: { text: 'RSI Value' },
              range: [0, 100]
            },
            margin: { t: 40 }
          }}
          config={{ responsive: true }}
          style={{ height: '400px' }}
        />
      )}
    </div>
  );
};

export default MarketRSI; 