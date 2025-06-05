import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { marketApi, MarketData, MarketOverview } from '../services/api';

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
  const [overview, setOverview] = useState<MarketOverview | null>(null);
  const [selectedSymbol, setSelectedSymbol] = useState<string>('BTC-USD');
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [timeframe, setTimeframe] = useState<string>('1mo');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [overviewRes, dataRes] = await Promise.all([
          marketApi.getOverview(),
          marketApi.getData(selectedSymbol, timeframe),
        ]);
        setOverview(overviewRes.data);
        setMarketData(dataRes.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch market data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedSymbol, timeframe]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600 p-4">
        <p>{error}</p>
      </div>
    );
  }

  const priceChartData = {
    labels: marketData?.dates || [],
    datasets: [
      {
        label: 'Price',
        data: marketData?.prices || [],
        borderColor: 'rgb(14, 165, 233)',
        tension: 0.1,
      },
      {
        label: 'SMA 20',
        data: marketData?.sma_20 || [],
        borderColor: 'rgb(234, 179, 8)',
        tension: 0.1,
      },
      {
        label: 'SMA 50',
        data: marketData?.sma_50 || [],
        borderColor: 'rgb(239, 68, 68)',
        tension: 0.1,
      },
    ],
  };

  const rsiChartData = {
    labels: marketData?.dates || [],
    datasets: [
      {
        label: 'RSI',
        data: marketData?.rsi || [],
        borderColor: 'rgb(14, 165, 233)',
        tension: 0.1,
      },
    ],
  };

  const macdChartData = {
    labels: marketData?.dates || [],
    datasets: [
      {
        label: 'MACD',
        data: marketData?.macd || [],
        borderColor: 'rgb(14, 165, 233)',
        tension: 0.1,
      },
      {
        label: 'Signal',
        data: marketData?.macd_signal || [],
        borderColor: 'rgb(234, 179, 8)',
        tension: 0.1,
      },
      {
        label: 'Histogram',
        data: marketData?.macd_hist || [],
        borderColor: 'rgb(239, 68, 68)',
        tension: 0.1,
      },
    ],
  };

  return (
    <div className="space-y-6">
      {/* Market Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {overview?.symbols &&
          Object.entries(overview.symbols).map(([symbol, data]) => (
            <div key={symbol} className="card">
              <h3 className="text-lg font-semibold mb-2">{symbol}</h3>
              <div className="space-y-2">
                <p className="text-2xl font-bold">
                  ${data.current_price.toLocaleString()}
                </p>
                <p
                  className={`text-sm ${
                    data.price_change_24h >= 0
                      ? 'text-green-600'
                      : 'text-red-600'
                  }`}
                >
                  {data.price_change_24h >= 0 ? '+' : ''}
                  {data.price_change_24h.toFixed(2)}%
                </p>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-500">RSI</p>
                    <p>{data.rsi.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">MACD</p>
                    <p>{data.macd.toFixed(2)}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Price Chart</h3>
          <Line data={priceChartData} />
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">RSI</h3>
          <Line data={rsiChartData} />
        </div>
        <div className="card lg:col-span-2">
          <h3 className="text-lg font-semibold mb-4">MACD</h3>
          <Line data={macdChartData} />
        </div>
      </div>
    </div>
  );
};

export default MarketOverview; 