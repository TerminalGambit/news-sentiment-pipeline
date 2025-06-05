# Sentiment Analysis and Market Data Platform

A full-stack application for sentiment analysis and market data visualization.

## Features

- Sentiment analysis of text and articles
- Market data with technical indicators (SMA, RSI, MACD)
- Report generation and visualization
- Real-time data updates
- Interactive charts and graphs

## Tech Stack

### Backend
- Python 3.11
- Flask
- Transformers (Hugging Face)
- Pandas & NumPy
- yfinance

### Frontend
- React
- TypeScript
- Chart.js
- Tailwind CSS

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sentiment-analysis-platform
```

2. Start the services using Docker Compose:
```bash
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Development

### Backend Development

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
flask run
```

### Frontend Development

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Documentation

### Market Data Endpoints

- `GET /api/market/overview` - Get market overview
- `GET /api/market/data/<symbol>` - Get market data for a symbol
- `GET /api/market/symbols` - Get available symbols
- `GET /api/market/timeframes` - Get available timeframes

### Sentiment Analysis Endpoints

- `POST /api/sentiment/analyze` - Analyze text sentiment
- `POST /api/sentiment/analyze/batch` - Analyze multiple texts
- `GET /api/sentiment/history` - Get analysis history
- `POST /api/sentiment/save` - Save analysis results

### Report Endpoints

- `GET /api/report/reports` - Get available reports
- `GET /api/report/reports/<date>` - Get specific report
- `GET /api/report/reports/<date>/positive` - Get positive articles
- `GET /api/report/reports/<date>/negative` - Get negative articles

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
