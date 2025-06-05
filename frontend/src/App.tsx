import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
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

const App: React.FC = () => {
  return (
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
            <Route path="/positive-articles" element={<PositiveArticles />} />
            <Route path="/negative-articles" element={<NegativeArticles />} />
            <Route path="/sentiment" element={<SentimentAnalysis />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
};

export default App; 