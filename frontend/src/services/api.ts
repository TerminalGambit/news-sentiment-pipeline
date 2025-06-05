import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Market Data Types
export interface MarketData {
  dates: string[];
  prices: number[];
  sma20?: number[];
  sma50?: number[];
  rsi?: number[];
  macd?: number[];
  signal?: number[];
  histogram?: number[];
}

export interface MarketOverview {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap: number;
  peRatio: number;
  eps: number;
  dividend: number;
  dividendYield: number;
}

// Sentiment Types
export interface SentimentResult {
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  score: number;
  confidence: number;
}

// Report Types
export interface Report {
  date: string;
  summary: string;
  articles: Article[];
}

export interface Article {
  title: string;
  summary: string;
  source: string;
  url: string;
  publishedAt: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  score: number;
}

// API Services
export const marketApi = {
  getOverview: (symbol: string) => 
    axios.get<MarketOverview>(`${API_BASE_URL}/market/overview/${symbol}`),
  
  getData: (symbol: string, timeframe: string = '1d', period: string = '1mo') => 
    axios.get<MarketData>(`${API_BASE_URL}/market/data/${symbol}`, {
      params: { timeframe, period }
    }),
  
  getSMAData: (symbol: string) => 
    axios.get<MarketData>(`${API_BASE_URL}/market/sma/${symbol}`),
  
  getRSIData: (symbol: string) => 
    axios.get<MarketData>(`${API_BASE_URL}/market/rsi/${symbol}`),
  
  getMACDData: (symbol: string) => 
    axios.get<MarketData>(`${API_BASE_URL}/market/macd/${symbol}`),
  
  getSymbols: () => 
    axios.get<string[]>(`${API_BASE_URL}/market/symbols`),
  
  getTimeframes: () => 
    axios.get<string[]>(`${API_BASE_URL}/market/timeframes`)
};

export const sentimentApi = {
  analyzeText: (text: string) => 
    axios.post<SentimentResult>(`${API_BASE_URL}/sentiment/analyze`, { text }),
  
  analyzeBatch: (texts: string[]) => 
    axios.post<SentimentResult[]>(`${API_BASE_URL}/sentiment/analyze/batch`, { texts }),
  
  getHistory: () => 
    axios.get<SentimentResult[]>(`${API_BASE_URL}/sentiment/history`),
  
  saveResults: (results: SentimentResult[]) => 
    axios.post(`${API_BASE_URL}/sentiment/save`, { results }),
  
  getPositiveArticles: () => 
    axios.get<Article[]>(`${API_BASE_URL}/sentiment/articles/positive`),
  
  getNegativeArticles: () => 
    axios.get<Article[]>(`${API_BASE_URL}/sentiment/articles/negative`)
};

export const reportApi = {
  getReports: () => 
    axios.get<Report[]>(`${API_BASE_URL}/reports`),
  
  getReport: (date: string) => 
    axios.get<Report>(`${API_BASE_URL}/reports/${date}`),
  
  generateReport: () => 
    axios.post<Report>(`${API_BASE_URL}/reports/generate`)
}; 