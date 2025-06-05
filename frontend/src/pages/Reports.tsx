import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { reportApi, Report, Article } from '../services/api';

const Reports: React.FC = () => {
  const [reports, setReports] = useState<string[]>([]);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        setLoading(true);
        const response = await reportApi.getReports();
        setReports(response.data.reports);
        if (response.data.reports.length > 0) {
          const reportResponse = await reportApi.getReport(
            response.data.reports[0]
          );
          setSelectedReport(reportResponse.data);
        }
        setError(null);
      } catch (err) {
        setError('Failed to fetch reports');
        console.error(err);
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
      setError(null);
    } catch (err) {
      setError('Failed to fetch report');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const ArticleCard: React.FC<{ article: Article }> = ({ article }) => (
    <div className="card">
      <h4 className="text-lg font-semibold mb-2">{article.title}</h4>
      <p className="text-gray-600 mb-4">{article.summary}</p>
      <div className="flex justify-between items-center">
        <div>
          <span className="text-sm text-gray-500">{article.source}</span>
          <span className="mx-2 text-gray-300">•</span>
          <span className="text-sm text-gray-500">
            {new Date(article.published).toLocaleDateString()}
          </span>
        </div>
        <div
          className={`px-2 py-1 rounded text-sm ${
            article.sentiment.label === 'Positive'
              ? 'bg-green-100 text-green-800'
              : article.sentiment.label === 'Negative'
              ? 'bg-red-100 text-red-800'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {article.sentiment.label}
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600 p-4">
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Report Selection */}
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Reports</h2>
        <div className="flex space-x-4 overflow-x-auto pb-2">
          {reports.map((date) => (
            <button
              key={date}
              className={`btn ${
                selectedReport?.date === date
                  ? 'btn-primary'
                  : 'btn-secondary'
              }`}
              onClick={() => handleReportSelect(date)}
            >
              {new Date(date).toLocaleDateString()}
            </button>
          ))}
        </div>
      </div>

      {selectedReport && (
        <>
          {/* Report Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold mb-2">Total Articles</h3>
              <p className="text-3xl font-bold">
                {selectedReport.total_articles}
              </p>
            </div>
            <div className="card">
              <h3 className="text-lg font-semibold mb-2">Sources</h3>
              <p className="text-3xl font-bold">
                {selectedReport.sources.length}
              </p>
            </div>
            <div className="card">
              <h3 className="text-lg font-semibold mb-2">Sentiment Distribution</h3>
              <div className="space-y-2">
                {Object.entries(selectedReport.sentiment_distribution).map(
                  ([label, count]) => (
                    <div key={label} className="flex justify-between">
                      <span>{label}</span>
                      <span className="font-semibold">{count}</span>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>

          {/* Top Articles */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold">Top Positive Articles</h3>
                <Link
                  to={`/report/${selectedReport.date}/positive`}
                  className="text-primary-600 hover:text-primary-700"
                >
                  See All
                </Link>
              </div>
              <div className="space-y-4">
                {selectedReport.top_positive.map((article) => (
                  <ArticleCard key={article.link} article={article} />
                ))}
              </div>
            </div>
            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold">Top Negative Articles</h3>
                <Link
                  to={`/report/${selectedReport.date}/negative`}
                  className="text-primary-600 hover:text-primary-700"
                >
                  See All
                </Link>
              </div>
              <div className="space-y-4">
                {selectedReport.top_negative.map((article) => (
                  <ArticleCard key={article.link} article={article} />
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Reports; 