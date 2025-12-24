import React, { useState } from 'react';
import { AlertCircle, CheckCircle, TrendingUp, Image, Smartphone, Zap, Globe } from 'lucide-react';

export default function ShopifyScanner() {
  const [storeUrl, setStoreUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = 'https://127.0.0.1:8000'; // Replace after deploying backend

  const handleScan = async () => {
    if (!storeUrl) return;
    
    setLoading(true);
    setError(null);
    setReport(null);

    try {
      const response = await fetch(`${API_URL}/scan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ store_url: storeUrl }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Scan failed');
      }

      const data = await response.json();
      setReport(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 85) return 'bg-green-100';
    if (score >= 70) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Shopify Store Health Scanner
          </h1>
          <p className="text-gray-600">
            Free SEO, Performance & Mobile Analysis • Built by Ruchita
          </p>
        </div>

        {/* Scan Input */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Enter Shopify Store URL
            </label>
            <input
              type="url"
              value={storeUrl}
              onChange={(e) => setStoreUrl(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleScan()}
              placeholder="https://example.myshopify.com"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={handleScan}
            disabled={loading || !storeUrl}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
          >
            {loading ? 'Scanning...' : 'Scan Store (Free)'}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
              <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* Report */}
        {report && (
          <div className="space-y-6">
            {/* Overall Score */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-center">
                <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full ${getScoreBg(report.overall_score)} mb-4`}>
                  <span className={`text-5xl font-bold ${getScoreColor(report.overall_score)}`}>
                    {report.overall_score}
                  </span>
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Overall Health Score
                </h2>
                <p className="text-gray-600">
                  {report.overall_score >= 85 && "Excellent! Your store is well-optimized."}
                  {report.overall_score >= 70 && report.overall_score < 85 && "Good, but there's room for improvement."}
                  {report.overall_score < 70 && "Critical issues found - these may be costing you sales."}
                </p>
              </div>
            </div>

            {/* Score Breakdown */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <ScoreCard
                icon={<Globe size={24} />}
                title="SEO"
                score={report.seo_score}
              />
              <ScoreCard
                icon={<Zap size={24} />}
                title="Performance"
                score={report.performance_score}
              />
              <ScoreCard
                icon={<Image size={24} />}
                title="Images"
                score={report.image_score}
              />
              <ScoreCard
                icon={<Smartphone size={24} />}
                title="Mobile"
                score={report.mobile_score}
              />
            </div>

            {/* Recommendations */}
            {report.recommendations.length > 0 && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                  <TrendingUp size={20} className="text-blue-600" />
                  Recommendations
                </h3>
                <ul className="space-y-2">
                  {report.recommendations.map((rec, i) => (
                    <li key={i} className="text-gray-700 text-sm flex items-start gap-2">
                      <span>•</span>
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Issues */}
            {report.issues.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <AlertCircle size={20} className="text-red-600" />
                  Issues Found ({report.issues.length})
                </h3>
                <ul className="space-y-3">
                  {report.issues.map((issue, i) => (
                    <li key={i} className="text-gray-700 text-sm border-l-4 border-red-400 pl-4 py-2 bg-red-50">
                      {issue}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Details */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="font-bold text-gray-900 mb-4">Store Details</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Total Images:</span>
                  <span className="ml-2 font-semibold">{report.details.images.total_images}</span>
                </div>
                <div>
                  <span className="text-gray-600">Missing Alt Text:</span>
                  <span className="ml-2 font-semibold">{report.details.images.missing_alt}</span>
                </div>
                <div>
                  <span className="text-gray-600">HTML Size:</span>
                  <span className="ml-2 font-semibold">{report.details.performance.html_size_kb}KB</span>
                </div>
                <div>
                  <span className="text-gray-600">Scripts:</span>
                  <span className="ml-2 font-semibold">{report.details.performance.script_count}</span>
                </div>
              </div>
            </div>

            {/* CTA */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-8 text-center text-white">
              <h3 className="text-2xl font-bold mb-2">Need Help Fixing These Issues?</h3>
              <p className="mb-4 opacity-90">
                I can optimize your store and fix all issues found in this report.
              </p>
              <a
                href="mailto:ruchitabhalala.ca@gmail.com?subject=Fix My Shopify Store Issues"
                className="inline-block bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Get a Free Quote
              </a>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-8 pb-8 text-gray-600 text-sm">
          <p>Built by Ruchita Bhalala • Backend Engineer specializing in E-commerce</p>
          <p className="mt-1">
            <a href="mailto:ruchitabhalala.ca@gmail.com" className="text-blue-600 hover:underline">
              ruchitabhalala.ca@gmail.com
            </a>
            {' • '}
            <a href="https://linkedin.com/in/ruchitagelani" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
              LinkedIn
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

function ScoreCard({ icon, title, score }) {
  const getColor = (s) => {
    if (s >= 85) return 'text-green-600 bg-green-50 border-green-200';
    if (s >= 70) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  return (
    <div className={`bg-white rounded-lg shadow p-4 border-2 ${getColor(score).split(' ').slice(1).join(' ')}`}>
      <div className={`${getColor(score).split(' ')[0]} mb-2`}>
        {icon}
      </div>
      <div className="text-2xl font-bold text-gray-900">{score}</div>
      <div className="text-sm text-gray-600">{title}</div>
    </div>
  );
}