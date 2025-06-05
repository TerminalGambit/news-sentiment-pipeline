import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { HomeIcon, ChartBarIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import theme from './styles/theme';
import Layout from './components/Layout';
import Home from './pages/Home';
import MarketOverview from './pages/MarketOverview';
import MarketSMA from './pages/MarketSMA';
import MarketRSI from './pages/MarketRSI';
import MarketMACD from './pages/MarketMACD';
import Report from './pages/Report';
import PositiveArticles from './pages/PositiveArticles';
import NegativeArticles from './pages/NegativeArticles';
import SentimentAnalysis from './pages/SentimentAnalysis';
import Reports from './pages/Reports';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const navigation = [
  { name: 'Market Overview', href: '/', icon: HomeIcon },
  { name: 'Sentiment Analysis', href: '/sentiment', icon: ChartBarIcon },
  { name: 'Reports', href: '/reports', icon: DocumentTextIcon },
];

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <div className="min-h-screen bg-gray-100">
            {/* Navigation */}
            <nav className="bg-white shadow-sm">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                  <div className="flex">
                    <div className="flex-shrink-0 flex items-center">
                      <span className="text-2xl font-bold text-primary-600">
                        Sentiment Analysis
                      </span>
                    </div>
                    <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                      {navigation.map((item) => (
                        <Link
                          key={item.name}
                          to={item.href}
                          className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-primary-600"
                        >
                          <item.icon className="h-5 w-5 mr-2" />
                          {item.name}
                        </Link>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </nav>

            {/* Main content */}
            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/market/:ticker" element={<MarketOverview />} />
                <Route path="/market/:ticker/sma" element={<MarketSMA />} />
                <Route path="/market/:ticker/rsi" element={<MarketRSI />} />
                <Route path="/market/:ticker/macd" element={<MarketMACD />} />
                <Route path="/report/:date" element={<Report />} />
                <Route path="/report/:date/positive" element={<PositiveArticles />} />
                <Route path="/report/:date/negative" element={<NegativeArticles />} />
                <Route path="/sentiment" element={<SentimentAnalysis />} />
                <Route path="/reports" element={<Reports />} />
              </Routes>
            </main>
          </div>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App; 