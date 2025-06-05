import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { marketApi, MarketOverview as MarketOverviewData, MarketData } from '../services/api';
import Plot from 'react-plotly.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MarketOverview: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const [overview, setOverview] = useState<MarketOverviewData | null>(null);
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!ticker) return;
      
      try {
        setLoading(true);
        const [overviewResponse, marketDataResponse] = await Promise.all([
          marketApi.getOverview(ticker),
          marketApi.getData(ticker)
        ]);
        setOverview(overviewResponse.data);
        setMarketData(marketDataResponse.data);
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
      <h2 className="mb-4">{ticker} Market Overview</h2>
      
      <div className="row">
        <div className="col-md-8">
          {marketData && (
            <Plot
              data={[
                {
                  x: marketData.dates,
                  y: marketData.prices,
                  type: 'scatter',
                  mode: 'lines',
                  name: 'Price',
                  line: { color: '#007bff' }
                }
              ]}
              layout={{
                title: { text: 'Price History' },
                xaxis: { title: { text: 'Date' } },
                yaxis: { title: { text: 'Price (USD)' } },
                margin: { t: 40 }
              }}
              config={{ responsive: true }}
              style={{ height: '400px' }}
            />
          )}
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Market Information</h5>
              {overview && (
                <div>
                  <p><strong>Name:</strong> {overview.name}</p>
                  <p><strong>Symbol:</strong> {overview.symbol}</p>
                  <p><strong>Price:</strong> ${overview.price.toFixed(2)}</p>
                  <p><strong>Change:</strong> {overview.change.toFixed(2)} ({overview.changePercent.toFixed(2)}%)</p>
                  <p><strong>Volume:</strong> {overview.volume.toLocaleString()}</p>
                  <p><strong>Market Cap:</strong> ${(overview.marketCap / 1e9).toFixed(2)}B</p>
                  <p><strong>P/E Ratio:</strong> {overview.peRatio.toFixed(2)}</p>
                  <p><strong>EPS:</strong> ${overview.eps.toFixed(2)}</p>
                  <p><strong>Dividend:</strong> ${overview.dividend.toFixed(2)}</p>
                  <p><strong>Dividend Yield:</strong> {overview.dividendYield.toFixed(2)}%</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketOverview; 