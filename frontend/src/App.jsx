import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { motion, AnimatePresence } from 'framer-motion'
import {
  HeartPulse,
  Database,
  BrainCircuit,
  Activity,
  Watch,
  ChevronLeft,
  Sparkles,
  AlertTriangle,
  CheckCircle2,
  Stethoscope,
  BookOpen,
  ArrowRight
} from 'lucide-react'

function App() {
  const [userData, setUserData] = useState({
    age: '',
    bmi: '',
    bp: '',
    sugar: '',
    lifestyle: 'Sedentary'
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('input')

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value })
  }

  const syncWearable = () => {
    // Simulate sophisticated wearable sync
    setLoading(true)
    setTimeout(() => {
      setUserData({
        age: 45,
        bmi: 28.5,
        bp: 135,
        sugar: 110,
        lifestyle: 'Moderate'
      })
      setLoading(false)
    }, 1500)
  }

  const analyzeHealth = async () => {
    setLoading(true)
    setResult(null)
    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_data: {
            ...userData,
            age: Number(userData.age),
            bmi: Number(userData.bmi),
            bp: Number(userData.bp),
            sugar: Number(userData.sugar)
          }
        })
      })
      const data = await response.json()
      setResult(data)
      setActiveTab('results')
    } catch (error) {
      console.error("Error connecting to AI Agents:", error)
      alert("AI Service is currently offline. Please ensure the backend server is running.")
    }
    setLoading(false)
  }

  return (
    <div className="container">
      <header>
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1>PreventiveCare <span style={{ fontWeight: 300, color: 'var(--text-dim)' }}>AI</span></h1>
          <p className="subtitle">
            Next-generation multi-agent intelligence for proactive health orchestration and personalized care.
          </p>
        </motion.div>
      </header>

      <main>
        <AnimatePresence mode="wait">
          {activeTab === 'input' ? (
            <motion.div
              key="input"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.4 }}
              className="glass-card"
              style={{ maxWidth: '700px', margin: '0 auto' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <div className="agent-icon" style={{ background: 'rgba(6, 182, 212, 0.1)' }}>
                    <Database className="primary" size={24} color="var(--primary)" />
                  </div>
                  <h2 style={{ fontSize: '1.5rem' }}>Biometric Profile</h2>
                </div>
                <button className="btn btn-secondary" onClick={syncWearable} disabled={loading} style={{ width: 'auto' }}>
                  <Watch size={18} />
                  {loading ? 'Syncing...' : 'Sync Wearable'}
                </button>
              </div>

              <div className="grid-form" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                <div className="form-group">
                  <label>Biological Age</label>
                  <input name="age" type="number" value={userData.age} onChange={handleChange} placeholder="e.g. 35" />
                </div>
                <div className="form-group">
                  <label>BMI Index</label>
                  <input name="bmi" type="number" value={userData.bmi} onChange={handleChange} placeholder="e.g. 24.2" />
                </div>
                <div className="form-group">
                  <label>Systolic Pressure (mmHg)</label>
                  <input name="bp" type="number" value={userData.bp} onChange={handleChange} placeholder="e.g. 120" />
                </div>
                <div className="form-group">
                  <label>Fasting Glucose (mg/dL)</label>
                  <input name="sugar" type="number" value={userData.sugar} onChange={handleChange} placeholder="e.g. 95" />
                </div>
                <div className="form-group" style={{ gridColumn: '1 / -1' }}>
                  <label>Lifestyle Factor</label>
                  <select name="lifestyle" value={userData.lifestyle} onChange={handleChange}>
                    <option value="Sedentary">Sedentary (Low Activity)</option>
                    <option value="Moderate">Moderate (Active 2-3x/week)</option>
                    <option value="Active">Athletic (Daily Training)</option>
                  </select>
                </div>
              </div>

              <div style={{ marginTop: '2.5rem' }}>
                <button
                  className="btn btn-primary"
                  onClick={analyzeHealth}
                  disabled={loading || !userData.age}
                >
                  {loading ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                    >
                      <Activity size={24} />
                    </motion.div>
                  ) : (
                    <>
                      <BrainCircuit size={24} />
                      Run Clinical Analysis
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="results-view"
            >
              <div className="results-header">
                <button className="btn btn-secondary" onClick={() => setActiveTab('input')}>
                  <ChevronLeft size={20} />
                  Refine Data
                </button>
                <div className="breadcrumb-divider"></div>
                <h2>Analysis Report</h2>
              </div>

              <div className="dashboard">
                {/* Risk Agent Output */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.1 }}
                  className="glass-card agent-card"
                  style={{ borderLeft: `4px solid ${result.risk_analysis.risk_level === 'High' ? 'var(--danger)' : 'var(--primary)'}` }}
                >
                  <div className="agent-header">
                    <div className="agent-icon">
                      <Stethoscope color={result.risk_analysis.risk_level === 'High' ? 'var(--danger)' : 'var(--primary)'} />
                    </div>
                    <div className="agent-info">
                      <h3>Risk Prediction Agent</h3>
                      <p>Predictive ML Diagnostics</p>
                    </div>
                    <span className={`badge ${result.risk_analysis.risk_level === 'High' ? 'risk-high' : 'risk-low'}`}>
                      {result.risk_analysis.risk_level}
                    </span>
                  </div>
                  <div className="markdown-content">
                    <ReactMarkdown>{result.risk_analysis.explanation}</ReactMarkdown>
                  </div>
                </motion.div>

                {/* RAG Agent Output */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="glass-card agent-card"
                >
                  <div className="agent-header">
                    <div className="agent-icon">
                      <BookOpen color="var(--secondary)" />
                    </div>
                    <div className="agent-info">
                      <h3>Medical Knowledge (RAG)</h3>
                      <p>Evidence-Based Guidelines</p>
                    </div>
                  </div>
                  <div className="markdown-content">
                    {result.guidelines.map((g, i) => (
                      <div key={i}><ReactMarkdown>{g}</ReactMarkdown></div>
                    ))}
                  </div>
                </motion.div>

                {/* Recommendation Agent Output */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="glass-card full-width"
                  style={{ background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.9) 100%)' }}
                >
                  <div className="agent-header">
                    <div className="agent-icon" style={{ background: 'rgba(139, 92, 246, 0.1)' }}>
                      <Sparkles color="var(--secondary)" />
                    </div>
                    <div className="agent-info">
                      <h3 style={{ fontSize: '1.3rem' }}>Orchestrated Care Strategy</h3>
                      <p>Synthesized Intelligence Recommendation</p>
                    </div>
                  </div>
                  <div className="markdown-content" style={{ color: 'var(--text-main)', fontSize: '1.05rem' }}>
                    <ReactMarkdown>{result.recommendation}</ReactMarkdown>
                  </div>

                  <div style={{ marginTop: '2rem', paddingTop: '2rem', borderTop: '1px solid var(--glass-border)', display: 'flex', gap: '1rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--success)' }}>
                      <CheckCircle2 size={16} /> Verified Protocol
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--primary)' }}>
                      <Sparkles size={16} /> AI Enhanced
                    </div>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <footer style={{ marginTop: '4rem', paddingBottom: '2rem', textAlign: 'center', color: 'var(--text-dim)', fontSize: '0.8rem' }}>
        <p>&copy; 2026 PreventiveCare AI Systems &bull; High-End Multi-Agent Orchestration</p>
      </footer>
    </div>
  )
}

export default App
