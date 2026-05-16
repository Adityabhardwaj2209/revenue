import React, { useState, useEffect } from 'react';
import { Activity, BarChart2, PieChart, ShieldAlert, LayoutDashboard, Settings } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, LineChart, Line } from 'recharts';
import axios from 'axios';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [scores, setScores] = useState([]);
  const [summary, setSummary] = useState({});
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [scoresRes, summaryRes, anomaliesRes] = await Promise.all([
          axios.get('http://localhost:8000/api/health-scores'),
          axios.get('http://localhost:8000/api/summary'),
          axios.get('http://localhost:8000/api/anomalies')
        ]);
        setScores(scoresRes.data);
        setSummary(summaryRes.data);
        setAnomalies(anomaliesRes.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const renderDashboard = () => (
    <div className="grid-layout">
      {/* Top Stat Cards */}
      <div className="col-span-3 glass-card animate-in" style={{animationDelay: '0.1s'}}>
        <div className="stat-label">Total Companies</div>
        <div className="stat-value">{summary.total_companies}</div>
      </div>
      <div className="col-span-3 glass-card animate-in" style={{animationDelay: '0.2s'}}>
        <div className="stat-label">Excellent Health</div>
        <div className="stat-value" style={{color: '#2ECC71'}}>{summary.excellent_health}</div>
      </div>
      <div className="col-span-3 glass-card animate-in" style={{animationDelay: '0.3s'}}>
        <div className="stat-label">Needs Attention</div>
        <div className="stat-value" style={{color: '#E74C3C'}}>{summary.needs_attention}</div>
      </div>
      <div className="col-span-3 glass-card animate-in" style={{animationDelay: '0.4s'}}>
        <div className="stat-label">Avg Market ROE</div>
        <div className="stat-value">{summary.avg_market_roe}%</div>
      </div>

      {/* Chart Section */}
      <div className="col-span-8 glass-card animate-in" style={{animationDelay: '0.5s', height: '400px'}}>
        <h3 style={{marginBottom: '1rem', color: 'white', fontWeight: 600}}>ML Health Scores Distribution</h3>
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={scores.slice(0, 20)} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
            <XAxis dataKey="company" stroke="#94a3b8" tick={{fill: '#94a3b8'}} />
            <YAxis stroke="#94a3b8" tick={{fill: '#94a3b8'}} />
            <Tooltip 
              contentStyle={{backgroundColor: 'rgba(15, 17, 26, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: 'white'}}
              itemStyle={{color: 'white'}}
            />
            <Bar dataKey="score" radius={[4, 4, 0, 0]}>
              {scores.slice(0, 20).map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* List Section */}
      <div className="col-span-4 glass-card animate-in" style={{animationDelay: '0.6s', height: '400px', overflowY: 'auto'}}>
        <h3 style={{marginBottom: '1rem', color: 'white', fontWeight: 600}}>Top Rankings</h3>
        <table className="table-container">
          <thead>
            <tr>
              <th>Company</th>
              <th>Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {scores.slice(0, 10).map((s, i) => (
              <tr key={i}>
                <td style={{fontWeight: 500, color: 'white'}}>{s.company}</td>
                <td>{s.score}</td>
                <td>
                  <span className="health-badge" style={{backgroundColor: `${s.color}20`, color: s.color}}>
                    {s.label}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderMLScores = () => (
    <div className="glass-card animate-in" style={{height: 'calc(100vh - 150px)', overflowY: 'auto'}}>
      <h3 style={{marginBottom: '1rem', color: 'white', fontWeight: 600}}>Complete ML Health Scores</h3>
      <table className="table-container">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Company</th>
            <th>Overall Score</th>
            <th>Status</th>
            <th>ROE %</th>
          </tr>
        </thead>
        <tbody>
          {scores.map((s, i) => (
            <tr key={i}>
              <td style={{color: '#94a3b8'}}>{i + 1}</td>
              <td style={{fontWeight: 500, color: 'white'}}>{s.company}</td>
              <td>{s.score}</td>
              <td>
                <span className="health-badge" style={{backgroundColor: `${s.color}20`, color: s.color}}>
                  {s.label}
                </span>
              </td>
              <td>{s.roe}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  const renderAnomalies = () => (
    <div className="glass-card animate-in" style={{height: 'calc(100vh - 150px)', overflowY: 'auto'}}>
      <h3 style={{marginBottom: '1rem', color: 'white', fontWeight: 600}}>Detected Anomalies</h3>
      {anomalies.length > 0 ? (
        <table className="table-container">
          <thead>
            <tr>
              <th>Company</th>
              <th>Year</th>
              <th>Metric</th>
              <th>Severity</th>
            </tr>
          </thead>
          <tbody>
            {anomalies.map((a, i) => (
              <tr key={i}>
                <td style={{fontWeight: 500, color: 'white'}}>{a.company}</td>
                <td>{a.year}</td>
                <td>{a.metric}</td>
                <td>
                  <span className="health-badge" style={{
                    backgroundColor: a.severity === 'High' ? 'rgba(231, 76, 60, 0.2)' : 'rgba(240, 165, 0, 0.2)', 
                    color: a.severity === 'High' ? '#E74C3C' : '#F0A500'
                  }}>
                    {a.severity}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div style={{color: '#94a3b8', padding: '2rem', textAlign: 'center'}}>
          No anomalies detected at this time.
        </div>
      )}
    </div>
  );

  const renderContent = () => {
    switch(activeTab) {
      case 'dashboard': return renderDashboard();
      case 'ml_scores': return renderMLScores();
      case 'anomalies': return renderAnomalies();
      default: return (
        <div className="glass-card animate-in" style={{color: '#94a3b8', padding: '2rem', textAlign: 'center'}}>
          This view is under construction.
        </div>
      );
    }
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <Activity className="logo-icon" size={28} />
          Nifty 100 Engine
        </div>
        <nav className="nav-links mt-8">
          <a className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
            <LayoutDashboard size={20} /> Dashboard
          </a>
          <a className={`nav-item ${activeTab === 'ml_scores' ? 'active' : ''}`} onClick={() => setActiveTab('ml_scores')}>
            <BarChart2 size={20} /> ML Scores
          </a>
          <a className={`nav-item ${activeTab === 'anomalies' ? 'active' : ''}`} onClick={() => setActiveTab('anomalies')}>
            <ShieldAlert size={20} /> Anomalies
          </a>
          <a className={`nav-item ${activeTab === 'sectors' ? 'active' : ''}`} onClick={() => setActiveTab('sectors')}>
            <PieChart size={20} /> Sectors
          </a>
          <a className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`} onClick={() => setActiveTab('settings')}>
            <Settings size={20} /> Settings
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="header animate-in">
          <h1>Financial Intelligence Overview</h1>
        </div>

        {loading ? (
          <div style={{color: 'white', padding: '2rem', textAlign: 'center'}}>Loading ML Models...</div>
        ) : (
          renderContent()
        )}
      </main>
    </div>
  );
}

export default App;
