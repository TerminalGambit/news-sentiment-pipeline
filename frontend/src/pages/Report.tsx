import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { reportApi, Report as ReportType } from '../services/api';

const Report: React.FC = () => {
  const { date } = useParams<{ date: string }>();
  const [report, setReport] = useState<ReportType | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!date) return;
      
      try {
        setLoading(true);
        const response = await reportApi.getReport(date);
        setReport(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [date]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="alert alert-danger">Error: {error}</div>;
  }

  if (!date) {
    return <div className="alert alert-warning">No date specified</div>;
  }

  if (!report) {
    return <div className="alert alert-warning">No report found for this date</div>;
  }

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Market Report for {new Date(date).toLocaleDateString()}</h2>
      
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Summary</h5>
          <p className="card-text">{report.summary}</p>
        </div>
      </div>

      <h3 className="mb-3">Articles</h3>
      <div className="row">
        {report.articles.map((article, index) => (
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
                  <span className={`badge ${article.sentiment === 'positive' ? 'bg-success' : article.sentiment === 'negative' ? 'bg-danger' : 'bg-secondary'}`}>
                    {article.sentiment}
                  </span>
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

export default Report; 