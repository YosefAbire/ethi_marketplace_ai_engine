import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface FraudAlert {
  id: string;
  type: string;
  risk_level: string;
  risk_score: number;
  title: string;
  description: string;
  evidence: any;
  affected_entities: string[];
  recommended_actions: string[];
  confidence: number;
  status: string;
  ethiopian_context?: string;
  created_at: string;
  updated_at: string;
}

interface FraudStatistics {
  period_days: number;
  total_alerts: number;
  critical_alerts: number;
  high_risk_alerts: number;
  confirmed_fraud: number;
  false_positives: number;
  accuracy_rate: number;
  false_positive_rate: number;
  fraud_types: { [key: string]: number };
}

interface FraudDetectionDashboardProps {
  onTabChange: (tab: any) => void;
}

export const FraudDetectionDashboard: React.FC<FraudDetectionDashboardProps> = ({ onTabChange }) => {
  const [alerts, setAlerts] = useState<FraudAlert[]>([]);
  const [statistics, setStatistics] = useState<FraudStatistics | null>(null);
  const [loading, setLoading] = useState(false);
  const [scanLoading, setScanLoading] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState<FraudAlert | null>(null);
  const [scanResults, setScanResults] = useState<any>(null);

  useEffect(() => {
    loadFraudData();
  }, []);

  const loadFraudData = async () => {
    setLoading(true);
    try {
      // Load alerts and statistics in parallel
      const [alertsResponse, statsResponse] = await Promise.all([
        fetch('/api/fraud/alerts'),
        fetch('/api/fraud/statistics')
      ]);

      if (alertsResponse.ok) {
        const alertsData = await alertsResponse.json();
        setAlerts(alertsData.alerts || []);
      }

      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStatistics(statsData.statistics || null);
      }
    } catch (error) {
      console.error('Error loading fraud data:', error);
    } finally {
      setLoading(false);
    }
  };

  const runFraudScan = async (scanType: string = 'full') => {
    setScanLoading(true);
    try {
      const response = await fetch('/api/fraud/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ scan_type: scanType }),
      });

      if (response.ok) {
        const result = await response.json();
        setScanResults(result);
        // Reload alerts after scan
        await loadFraudData();
      }
    } catch (error) {
      console.error('Error running fraud scan:', error);
    } finally {
      setScanLoading(false);
    }
  };

  const updateAlertStatus = async (alertId: string, status: string, notes?: string) => {
    try {
      const response = await fetch(`/api/fraud/alerts/${alertId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          status,
          resolved_by: 'admin',
          notes,
        }),
      });

      if (response.ok) {
        // Reload alerts
        await loadFraudData();
        setSelectedAlert(null);
      }
    } catch (error) {
      console.error('Error updating alert status:', error);
    }
  };

  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel.toLowerCase()) {
      case 'critical':
        return 'text-red-600 bg-red-100';
      case 'high':
        return 'text-orange-600 bg-orange-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'low':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getFraudTypeIcon = (fraudType: string) => {
    switch (fraudType) {
      case 'pricing_manipulation':
        return 'fa-chart-line';
      case 'transaction_fraud':
        return 'fa-exchange-alt';
      case 'inventory_fraud':
        return 'fa-boxes';
      case 'account_fraud':
        return 'fa-user-shield';
      case 'coordinated_attack':
        return 'fa-network-wired';
      default:
        return 'fa-exclamation-triangle';
    }
  };

  if (loading) {
    return (
      <div className="p-8 h-full flex items-center justify-center">
        <div className="text-center">
          <i className="fas fa-spinner fa-spin text-4xl text-ethiGreen mb-4"></i>
          <p className="text-slate-600">Loading fraud detection data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 h-full overflow-y-auto custom-scrollbar">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-800 mb-2">
              Fraud Detection • ማጭበርበር ማወቂያ
            </h1>
            <p className="text-slate-600">
              AI-powered security monitoring for the Ethiopian marketplace
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => runFraudScan('full')}
              disabled={scanLoading}
              className="bg-ethiGreen text-white px-6 py-3 rounded-xl font-semibold hover:bg-ethiGreen/90 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {scanLoading ? (
                <>
                  <i className="fas fa-spinner fa-spin"></i>
                  Scanning...
                </>
              ) : (
                <>
                  <i className="fas fa-search"></i>
                  Run Full Scan
                </>
              )}
            </button>
            <button
              onClick={loadFraudData}
              className="bg-white border border-slate-200 text-slate-700 px-6 py-3 rounded-xl font-semibold hover:bg-slate-50 transition-colors flex items-center gap-2"
            >
              <i className="fas fa-sync-alt"></i>
              Refresh
            </button>
          </div>
        </div>

        {/* Statistics Cards */}
        {statistics && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Total Alerts"
              value={statistics.total_alerts.toString()}
              icon="fa-shield-alt"
              color="text-blue-600"
              subtitle={`${statistics.period_days} days`}
            />
            <StatCard
              title="Critical Alerts"
              value={statistics.critical_alerts.toString()}
              icon="fa-exclamation-triangle"
              color="text-red-600"
              subtitle="Immediate action required"
            />
            <StatCard
              title="Accuracy Rate"
              value={`${statistics.accuracy_rate.toFixed(1)}%`}
              icon="fa-bullseye"
              color="text-green-600"
              subtitle="Detection accuracy"
            />
            <StatCard
              title="False Positives"
              value={`${statistics.false_positive_rate.toFixed(1)}%`}
              icon="fa-times-circle"
              color="text-orange-600"
              subtitle="False alarm rate"
            />
          </div>
        )}

        {/* Scan Results */}
        {scanResults && (
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm mb-8">
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <i className="fas fa-search text-ethiGreen"></i>
              Latest Scan Results
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="text-center p-4 bg-slate-50 rounded-xl">
                <div className="text-2xl font-bold text-slate-800">
                  {scanResults.alerts_found || 0}
                </div>
                <div className="text-sm text-slate-600">Alerts Found</div>
              </div>
              <div className="text-center p-4 bg-red-50 rounded-xl">
                <div className="text-2xl font-bold text-red-600">
                  {scanResults.critical_alerts || 0}
                </div>
                <div className="text-sm text-slate-600">Critical</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-xl">
                <div className="text-2xl font-bold text-orange-600">
                  {scanResults.high_risk_alerts || 0}
                </div>
                <div className="text-sm text-slate-600">High Risk</div>
              </div>
            </div>
            {scanResults.summary && (
              <div className="bg-slate-50 p-4 rounded-xl">
                <p className="text-slate-700">{scanResults.summary}</p>
              </div>
            )}
          </div>
        )}

        {/* Active Alerts */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
          <h3 className="font-bold text-lg mb-6 flex items-center gap-2">
            <i className="fas fa-exclamation-triangle text-ethiYellow"></i>
            Active Fraud Alerts
            <span className="ml-auto text-xs font-medium text-slate-400 bg-slate-100 px-2 py-1 rounded-lg">
              {alerts.length} alerts
            </span>
          </h3>

          {alerts.length === 0 ? (
            <div className="text-center py-12">
              <i className="fas fa-shield-alt text-6xl text-green-200 mb-4"></i>
              <h4 className="text-xl font-bold text-slate-800 mb-2">All Clear!</h4>
              <p className="text-slate-600">No active fraud alerts detected. The marketplace is secure.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  className="border border-slate-200 rounded-2xl p-6 hover:border-slate-300 transition-colors cursor-pointer"
                  onClick={() => setSelectedAlert(alert)}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center">
                        <i className={`fas ${getFraudTypeIcon(alert.type)} text-slate-600`}></i>
                      </div>
                      <div>
                        <h4 className="font-bold text-slate-800">{alert.title}</h4>
                        <p className="text-sm text-slate-600">{alert.type.replace('_', ' ')}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${getRiskLevelColor(alert.risk_level)}`}>
                        {alert.risk_level}
                      </span>
                      <div className="text-right">
                        <div className="text-lg font-bold text-slate-800">{alert.risk_score}/100</div>
                        <div className="text-xs text-slate-500">Risk Score</div>
                      </div>
                    </div>
                  </div>
                  
                  <p className="text-slate-700 mb-4">{alert.description}</p>
                  
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-4">
                      <span className="text-slate-500">
                        Confidence: {(alert.confidence * 100).toFixed(0)}%
                      </span>
                      <span className="text-slate-500">
                        Entities: {alert.affected_entities.length}
                      </span>
                    </div>
                    <div className="text-slate-500">
                      {new Date(alert.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  
                  {alert.ethiopian_context && (
                    <div className="mt-4 p-3 bg-ethiGreen/5 border border-ethiGreen/20 rounded-xl">
                      <div className="flex items-center gap-2 mb-1">
                        <i className="fas fa-globe-africa text-ethiGreen text-sm"></i>
                        <span className="text-sm font-semibold text-ethiGreen">Ethiopian Context</span>
                      </div>
                      <p className="text-sm text-slate-700">{alert.ethiopian_context}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Alert Detail Modal */}
        {selectedAlert && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-slate-200">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold text-slate-800">Alert Details</h3>
                  <button
                    onClick={() => setSelectedAlert(null)}
                    className="w-8 h-8 rounded-lg bg-slate-100 text-slate-400 hover:bg-slate-200 transition-colors"
                  >
                    <i className="fas fa-times"></i>
                  </button>
                </div>
              </div>
              
              <div className="p-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 bg-slate-100 rounded-xl flex items-center justify-center">
                    <i className={`fas ${getFraudTypeIcon(selectedAlert.type)} text-slate-600`}></i>
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-slate-800">{selectedAlert.title}</h4>
                    <p className="text-slate-600">{selectedAlert.type.replace('_', ' ')}</p>
                  </div>
                  <span className={`ml-auto px-3 py-1 rounded-full text-xs font-bold uppercase ${getRiskLevelColor(selectedAlert.risk_level)}`}>
                    {selectedAlert.risk_level}
                  </span>
                </div>

                <div className="space-y-6">
                  <div>
                    <h5 className="font-semibold text-slate-800 mb-2">Description</h5>
                    <p className="text-slate-700">{selectedAlert.description}</p>
                  </div>

                  <div>
                    <h5 className="font-semibold text-slate-800 mb-2">Evidence</h5>
                    <div className="bg-slate-50 p-4 rounded-xl">
                      <pre className="text-sm text-slate-700 whitespace-pre-wrap">
                        {JSON.stringify(selectedAlert.evidence, null, 2)}
                      </pre>
                    </div>
                  </div>

                  <div>
                    <h5 className="font-semibold text-slate-800 mb-2">Recommended Actions</h5>
                    <ul className="space-y-2">
                      {selectedAlert.recommended_actions.map((action, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <i className="fas fa-check-circle text-ethiGreen mt-1"></i>
                          <span className="text-slate-700">{action}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="flex gap-3 pt-4 border-t border-slate-200">
                    <button
                      onClick={() => updateAlertStatus(selectedAlert.id, 'investigating')}
                      className="flex-1 bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
                    >
                      Start Investigation
                    </button>
                    <button
                      onClick={() => updateAlertStatus(selectedAlert.id, 'false_positive', 'Marked as false positive')}
                      className="flex-1 bg-orange-600 text-white py-3 rounded-xl font-semibold hover:bg-orange-700 transition-colors"
                    >
                      False Positive
                    </button>
                    <button
                      onClick={() => updateAlertStatus(selectedAlert.id, 'resolved', 'Alert resolved')}
                      className="flex-1 bg-green-600 text-white py-3 rounded-xl font-semibold hover:bg-green-700 transition-colors"
                    >
                      Resolve
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const StatCard = ({ title, value, icon, color, subtitle }: any) => (
  <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
    <div className={`w-10 h-10 ${color} bg-opacity-10 rounded-xl flex items-center justify-center mb-4`}>
      <i className={`fas ${icon} ${color}`}></i>
    </div>
    <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">{title}</p>
    <p className="text-2xl font-black text-slate-800 tracking-tighter mb-1">{value}</p>
    {subtitle && <p className="text-xs text-slate-500">{subtitle}</p>}
  </div>
);