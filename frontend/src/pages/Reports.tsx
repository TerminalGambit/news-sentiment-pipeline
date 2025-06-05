import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { reportApi, Report as ReportType, Article } from '../services/api';

const ArticleCard: React.FC<{ article: Article }> = ({ article }) => (
  <div className="bg-white rounded shadow p-4 mb-4">
    <h4 className="font-bold text-lg mb-1">{article.title}</h4>
    <div className="flex items-center text-sm text-gray-500 mb-2">
      <span>{article.source}</span>
      <span className="mx-2 text-gray-300">•</span>
      <span className="text-sm text-gray-500">
        {new Date(article.publishedAt).toLocaleDateString()}
      </span>
    </div>
    <div
      className={`px-2 py-1 rounded text-sm ${
        article.sentiment === 'positive'
          ? 'bg-green-100 text-green-800'
          : article.sentiment === 'negative'
          ? 'bg-red-100 text-red-800'
          : 'bg-gray-100 text-gray-800'
      }`}
    >
      {article.sentiment}
    </div>
    <p className="mt-2 text-gray-700">{article.summary}</p>
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-block mt-2 text-blue-600 hover:underline"
    >
      Read More
    </a>
  </div>
);

const Reports: React.FC = () => {
  const [reports, setReports] = useState<ReportType[]>([]);
  const [selectedReport, setSelectedReport] = useState<ReportType | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        setLoading(true);
        const response = await reportApi.getReports();
        setReports(response.data);
        if (response.data.length > 0) {
          const reportResponse = await reportApi.getReport(response.data[0].date);
          setSelectedReport(reportResponse.data);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, []);

  const handleReportSelect = async (date: string) => {
    try {
      setLoading(true);
      const response = await reportApi.getReport(date);
      setSelectedReport(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="alert alert-danger">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Sentiment Reports</h2>
      <div className="mb-4 flex flex-wrap gap-2">
        {reports.map((report) => (
          <button
            key={report.date}
            className={`px-4 py-2 rounded ${
              selectedReport && selectedReport.date === report.date
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800'
            }`}
            onClick={() => handleReportSelect(report.date)}
          >
            {new Date(report.date).toLocaleDateString()}
          </button>
        ))}
      </div>
      {selectedReport && (
        <div>
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Summary</h5>
              <p className="card-text">{selectedReport.summary}</p>
            </div>
          </div>
          <h3 className="mb-3">Articles</h3>
          <div className="row">
            {selectedReport.articles.map((article, index) => (
              <div key={index} className="col-md-6 mb-4">
                <ArticleCard article={article} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports; 