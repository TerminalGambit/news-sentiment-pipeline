import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-md-8 text-center">
          <h1 className="display-4 mb-4">NVIDIA Market Dashboard</h1>
          <p className="lead mb-5">
            Analyze market trends, sentiment, and technical indicators for NVIDIA and related stocks.
          </p>
          <div className="row">
            <div className="col-md-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">Market Overview</h5>
                  <p className="card-text">View real-time market data and technical indicators.</p>
                  <Link to="/market/NVDA" className="btn btn-primary">View Market</Link>
                </div>
              </div>
            </div>
            <div className="col-md-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">Sentiment Analysis</h5>
                  <p className="card-text">Analyze news sentiment and market impact.</p>
                  <Link to="/sentiment" className="btn btn-primary">Analyze Sentiment</Link>
                </div>
              </div>
            </div>
            <div className="col-md-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">Reports</h5>
                  <p className="card-text">Access historical reports and analysis.</p>
                  <Link to="/reports" className="btn btn-primary">View Reports</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 