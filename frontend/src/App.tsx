import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
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

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/market/:ticker" element={<MarketOverview />} />
              <Route path="/market/:ticker/sma" element={<MarketSMA />} />
              <Route path="/market/:ticker/rsi" element={<MarketRSI />} />
              <Route path="/market/:ticker/macd" element={<MarketMACD />} />
              <Route path="/report/:date" element={<Report />} />
              <Route path="/report/:date/positive" element={<PositiveArticles />} />
              <Route path="/report/:date/negative" element={<NegativeArticles />} />
            </Routes>
          </Layout>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App; 