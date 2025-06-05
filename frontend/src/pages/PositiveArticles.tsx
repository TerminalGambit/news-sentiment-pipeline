import React, { useEffect, useState } from 'react';
import { sentimentApi, Article } from '../services/api';

const PositiveArticles: React.FC = () => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await sentimentApi.getPositiveArticles();
        setArticles(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="alert alert-danger">Error: {error}</div>;
  }

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Positive Sentiment Articles</h2>
      
      <div className="row">
        {articles.map((article, index) => (
          <div key={index} className="col-md-6 mb-4">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">{article.title}</h5>
                <h6 className="card-subtitle mb-2 text-muted">{article.source}</h6>
                <p className="card-text">{article.summary}</p>
                <div className="d-flex justify-content-between align-items-center">
                  <small className="text-muted">
                    {new Date(article.publishedAt).toLocaleDateString()}
                  </small>
                  <span className="badge bg-success">positive</span>
                </div>
                <a href={article.url} target="_blank" rel="noopener noreferrer" className="btn btn-primary mt-3">
                  Read More
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PositiveArticles; 