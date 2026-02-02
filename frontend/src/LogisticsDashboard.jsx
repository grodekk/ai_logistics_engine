import React, { useState, useEffect } from 'react';
import { Calculator, TrendingUp, Package, DollarSign } from 'lucide-react';

export default function LogisticsDashboard() {
  const [activeTab, setActiveTab] = useState('rates');
  const [routes, setRoutes] = useState([{ route_name: '', monthly_trips: 0 }]);
  const [profitTarget, setProfitTarget] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableRoutes, setAvailableRoutes] = useState([]);
  const [clientScores, setClientScores] = useState([]);

  useEffect(() => {
    fetchAvailableRoutes();
  }, []);

  const fetchAvailableRoutes = async () => {
    try {
      const response = await fetch('http://localhost:8000/routes/available');
      const data = await response.json();
      setAvailableRoutes(data.routes);
    } catch (err) {
      console.error('Failed to fetch routes:', err);
    }
  };

  useEffect(() => {
    if (activeTab === 'scoring') {
      fetchClientScores();
    }
  }, [activeTab]);

  const fetchClientScores = async () => {
    try {
      const response = await fetch('http://localhost:8000/clients/scores');
      const data = await response.json();
      if (!response.ok) {
          setError(data);
          return;
      }
      setClientScores(data);
    } catch (err) {
      setError('Server is unavailable. Please try again later.');
    }
  };

  const addRoute = () => setRoutes([...routes, { route_name: '', monthly_trips: 0 }]);
  const updateRoute = (index, field, value) => {
    const newRoutes = [...routes];
    newRoutes[index][field] = field === 'monthly_trips' ? parseInt(value) || 0 : value;
    setRoutes(newRoutes);
  };
  const removeRoute = (index) => setRoutes(routes.filter((_, i) => i !== index));

  const calculateRates = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(
        `http://localhost:8000/decision/rates?monthly_profit_target=${profitTarget}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(routes.filter(r => r.route_name && r.monthly_trips > 0))
        }
      );

      const data = await response.json();


      if (!response.ok) {
        setError(data);
        return;
      }


      setResult(data);
    } catch (err) {
      setError('Server is unavailable. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 50) return 'text-orange-500';
    return 'text-red-600';
  };

  const getScoreBackground = (score) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 50) return 'bg-orange-100';
    return 'bg-red-100';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center justify-center gap-3">
            <Calculator className="text-indigo-600" size={40} />
            AI Logistics Engine
          </h1>
          <p className="text-gray-600">Optimize your routes and evaluate clients</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-6 justify-center">
          <button
            onClick={() => { setActiveTab('rates'); setError(null); }}
            className={`px-6 py-2 rounded-lg font-semibold transition ${activeTab === 'rates' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
          >
            Calculate Rates
          </button>
          <button
            onClick={() => { setActiveTab('scoring'); setError(null); }}
            className={`px-6 py-2 rounded-lg font-semibold transition ${activeTab === 'scoring' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
          >
            Client Scoring
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            <p>{error.message || error}</p>
            {error.error_id && (
              <p className="text-xs text-gray-600 mt-2">
                Error ID: {error.error_id}
              </p>
            )}
          </div>
        )}


        {/* Calculate Rates Tab */}
        {activeTab === 'rates' && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">Route Configuration</h2>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Monthly Profit Target (€)
              </label>
              <input
                type="number"
                value={profitTarget}
                onChange={(e) => setProfitTarget(parseFloat(e.target.value) || 0)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>

            <div className="space-y-3">
              {routes.map((route, index) => (
                <div key={index} className="flex gap-3 items-center">
                  <select
                    value={route.route_name}
                    onChange={(e) => updateRoute(index, 'route_name', e.target.value)}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">Select a route...</option>
                    {availableRoutes.map((routeName) => (
                      <option key={routeName} value={routeName}>{routeName}</option>
                    ))}
                  </select>
                  <input
                    type="number"
                    placeholder="Trips"
                    value={route.monthly_trips || ''}
                    onChange={(e) => updateRoute(index, 'monthly_trips', e.target.value)}
                    className="w-32 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                  <button
                    onClick={() => removeRoute(index)}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>

            <div className="flex gap-3 mt-4">
              <button
                onClick={addRoute}
                className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition"
              >
                + Add Route
              </button>
              <button
                onClick={calculateRates}
                disabled={loading}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
              >
                {loading ? 'Calculating...' : 'Calculate Rates'}
              </button>
            </div>

            {/* Results */}
            {result && (
              <div className="space-y-6 mt-8">
                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-100 flex justify-between items-center">
                    <div>
                      <p className="text-gray-500 text-sm">Total Trips</p>
                      <p className="text-3xl font-bold text-indigo-600">{result.summary.total_trips}</p>
                    </div>
                    <Package className="text-indigo-600" size={40} />
                  </div>

                  <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-100 flex justify-between items-center">
                    <div>
                      <p className="text-gray-500 text-sm">Total Route Costs</p>
                      <p className="text-3xl font-bold text-green-600">€{result.summary.total_route_costs.toFixed(2)}</p>
                    </div>
                    <DollarSign className="text-green-600" size={40} />
                  </div>

                  <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-100 flex justify-between items-center">
                    <div>
                      <p className="text-gray-500 text-sm">Total Monthly Costs</p>
                      <p className="text-3xl font-bold text-orange-600">€{result.summary.total_monthly_costs.toFixed(2)}</p>
                    </div>
                    <TrendingUp className="text-orange-600" size={40} />
                  </div>
                </div>

                {/* Average Rate */}
                <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg shadow-lg p-6 text-white">
                  <h3 className="text-xl font-semibold mb-1">Average Rate per Trip</h3>
                  <p className="text-4xl font-bold">€{result.average_rate_per_trip.toFixed(2)}</p>
                </div>

                {/* Routes Table */}
                <div className="bg-white rounded-lg shadow-lg border border-gray-100 overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Route</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monthly Trips</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Route Cost</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Required Rate</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {result.routes.map((route, i) => (
                        <tr key={i} className="hover:bg-gray-50 transition">
                          <td className="px-6 py-4 text-sm font-medium text-gray-900">{route.route_name}</td>
                          <td className="px-6 py-4 text-sm text-gray-600">{route.monthly_trips}</td>
                          <td className="px-6 py-4 text-sm text-gray-600">€{route.total_route_cost.toFixed(2)}</td>
                          <td className="px-6 py-4 text-sm font-bold text-indigo-600">€{route.required_rate_per_trip.toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Client Scoring Tab */}
        {activeTab === 'scoring' && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">Client Scoring</h2>
            {clientScores.length === 0 ? (
              <p className="text-gray-500">No client data available.</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Client</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Class</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avg Delay (days)</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Late Payments</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Shipments</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {clientScores.map((client, i) => (
                      <tr key={i} className="hover:bg-gray-50 transition">
                        <td className="px-6 py-4 text-sm font-medium text-gray-900">{client.client_name}</td>
                        <td className="px-6 py-4 text-sm">
                          <span className="px-2 py-1 rounded-full bg-indigo-100 text-indigo-700 text-xs font-semibold">{client.client_class}</span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">{client.avg_payment_delay_days}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{client.late_payment_count}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{client.total_shipments}</td>
                        <td className="px-6 py-4 text-sm">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold ${getScoreColor(client.score)} ${getScoreBackground(client.score)}`}>
                            {client.score}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}