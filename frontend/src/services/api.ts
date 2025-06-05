import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface MarketData {
  dates: string[];
  prices: number[];
  volumes: number[];
  sma_20: number[];
  sma_50: number[];
  rsi: number[];
  macd: number[];
  macd_signal: number[];
  macd_hist: number[];
  metadata: {
    symbol: string;
    timeframe: string;
    period: string;
    last_updated: string;
    current_price: number;
    price_change_24h: number;
    volume_24h: number;
  };
}

export interface MarketOverview {
  timestamp: string;
  symbols: {
    [key: string]: {
      current_price: number;
      price_change_24h: number;
      volume_24h: number;
      rsi: number;
      macd: number;
      macd_signal: number;
      macd_hist: number;
    };
  };
}

export interface SentimentResult {
  text: string;
  sentiment: {
    label: 'Positive' | 'Negative' | 'Neutral';
    score: number;
  };
}

export interface Report {
  date: string;
  total_articles: number;
  sources: string[];
  sentiment_distribution: {
    Positive: number;
    Neutral: number;
    Negative: number;
  };
  source_stats: {
    [key: string]: {
      positive: number;
      neutral: number;
      negative: number;
    };
  };
  top_positive: Article[];
  top_negative: Article[];
}

export interface Article {
  title: string;
  summary: string;
  link: string;
  published: string;
  source: string;
  sentiment: {
    label: 'Positive' | 'Negative' | 'Neutral';
    score: number;
  };
}

export const marketApi = {
  getOverview: () => api.get<MarketOverview>('/api/market/overview'),
  getData: (symbol: string, timeframe: string = '1mo', period: string = '1y') =>
    api.get<MarketData>(`/api/market/data/${symbol}`, {
      params: { timeframe, period },
    }),
  getSymbols: () => api.get<{ symbols: string[] }>('/api/market/symbols'),
  getTimeframes: () => api.get<{ timeframes: { [key: string]: string } }>('/api/market/timeframes'),
};

export const sentimentApi = {
  analyzeText: (text: string) =>
    api.post<SentimentResult>('/api/sentiment/analyze', { text }),
  analyzeBatch: (texts: string[]) =>
    api.post<SentimentResult[]>('/api/sentiment/analyze/batch', { texts }),
  getHistory: () => api.get<SentimentResult[]>('/api/sentiment/history'),
  saveResults: (results: SentimentResult[]) =>
    api.post('/api/sentiment/save', { results }),
};

export const reportApi = {
  getReports: () => api.get<{ reports: string[] }>('/api/report/reports'),
  getReport: (date: string) => api.get<Report>(`/api/report/reports/${date}`),
  getPositiveArticles: (date: string) =>
    api.get<{ articles: Article[] }>(`/api/report/reports/${date}/positive`),
  getNegativeArticles: (date: string) =>
    api.get<{ articles: Article[] }>(`/api/report/reports/${date}/negative`),
}; 