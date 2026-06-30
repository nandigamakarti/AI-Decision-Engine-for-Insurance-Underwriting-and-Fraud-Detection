import { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { Proposals } from './pages/Proposals';
import { ProposalDetail } from './pages/ProposalDetail';
import { Simulator } from './pages/Simulator';
import { System } from './pages/System';
import { Reports } from './pages/Reports';
import { AuditLogs } from './pages/AuditLogs';
import { Settings } from './pages/Settings';
import { fetchProposals, fetchSystemHealth, getMockMode, setMockMode } from './apiClient';
import { ProposalSummary, SystemHealth } from './types';
import { ShieldAlert } from 'lucide-react';

function App() {
  const [currentPage, setCurrentPage] = useState<string>('dashboard');
  const [selectedProposalId, setSelectedProposalId] = useState<string>('PROP001');
  const [proposals, setProposals] = useState<ProposalSummary[]>([]);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [mockMode, setMockState] = useState<boolean>(getMockMode());
  const [loading, setLoading] = useState(true);
  const [healthLoading, setHealthLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchProposals();
      setProposals(data);
    } catch (err) {
      console.error('Failed to load proposals', err);
    } finally {
      setLoading(false);
    }
  };

  const loadHealth = async () => {
    setHealthLoading(true);
    try {
      const health = await fetchSystemHealth();
      setSystemHealth(health);
      // Sync mock state in case API client auto-switched to mock mode
      setMockState(getMockMode());
    } catch (err) {
      console.error('Failed to load health status', err);
    } finally {
      setHealthLoading(false);
    }
  };

  useEffect(() => {
    // Initial diagnostics run and data loader
    const init = async () => {
      await loadHealth();
      await loadData();
    };
    init();

    // Background polling for health status diagnostics every 30 seconds
    const intervalId = setInterval(() => {
      loadHealth();
    }, 30000);

    return () => clearInterval(intervalId);
  }, []);

  const handleSetMockMode = (mode: boolean) => {
    setMockMode(mode);
    setMockState(mode);
    // Reload database metrics and proposals for correct mode
    loadData();
    loadHealth();
  };

  const renderPageContent = () => {
    if (loading && proposals.length === 0) {
      return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', padding: '80px 0', alignItems: 'center' }}>
          <div className="skeleton" style={{ width: '80px', height: '80px', borderRadius: '50%' }} />
          <div className="skeleton" style={{ width: '250px', height: '20px' }} />
          <div className="skeleton" style={{ width: '150px', height: '14px' }} />
        </div>
      );
    }

    switch (currentPage) {
      case 'dashboard':
        return (
          <Dashboard
            proposals={proposals}
            systemHealth={systemHealth}
            setCurrentPage={setCurrentPage}
            setSelectedProposalId={setSelectedProposalId}
          />
        );
      case 'proposals':
        return (
          <Proposals
            proposals={proposals}
            setCurrentPage={setCurrentPage}
            setSelectedProposalId={setSelectedProposalId}
          />
        );
      case 'detail':
        return (
          <ProposalDetail
            proposalId={selectedProposalId}
            proposals={proposals}
            setCurrentPage={setCurrentPage}
            setSelectedProposalId={setSelectedProposalId}
          />
        );
      case 'simulator':
        return <Simulator />;
      case 'reports':
        return <Reports />;
      case 'logs':
        return <AuditLogs />;
      case 'settings':
        return (
          <Settings
            systemHealth={systemHealth}
            loading={healthLoading}
            refreshHealth={loadHealth}
            mockMode={mockMode}
          />
        );
      case 'system':
        return (
          <System
            systemHealth={systemHealth}
            loading={healthLoading}
            refreshHealth={loadHealth}
            mockMode={mockMode}
            setMockMode={handleSetMockMode}
          />
        );
      default:
        return (
          <div style={{ padding: '40px', textAlign: 'center' }}>
            <ShieldAlert size={40} style={{ color: 'var(--color-critical)' }} />
            <h3>Page Not Found</h3>
          </div>
        );
    }
  };

  return (
    <div style={{
      display: 'flex',
      minHeight: '100vh',
      background: 'var(--bg-primary)',
      color: 'var(--text-primary)',
      width: '100vw',
      overflowX: 'hidden'
    }}>
      {/* Sidebar */}
      <Sidebar 
        currentPage={currentPage} 
        setCurrentPage={(page) => {
          setCurrentPage(page);
          setSidebarOpen(false); // Auto-close drawer on navigation in mobile views
        }} 
        mockMode={mockMode}
        setMockMode={handleSetMockMode}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Content Area */}
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        padding: '0 16px 16px 16px',
        minWidth: 0 // Prevents grid layout overflow issues
      }}>
        {/* Header */}
        <Header 
          currentPage={currentPage} 
          systemHealth={systemHealth} 
          mockMode={mockMode}
          onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        {/* Dynamic Subpage */}
        <main style={{ flex: 1, padding: '0 8px 32px 0' }}>
          {renderPageContent()}
        </main>
      </div>
    </div>
  );
}

export default App;
