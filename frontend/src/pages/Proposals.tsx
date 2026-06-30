import React, { useState } from 'react';
import { ProposalSummary } from '../types';
import { Search, Filter, Check, X, ShieldAlert } from 'lucide-react';

interface ProposalsProps {
  proposals: ProposalSummary[];
  setCurrentPage: (page: string) => void;
  setSelectedProposalId: (id: string) => void;
}

export const Proposals: React.FC<ProposalsProps> = ({
  proposals,
  setCurrentPage,
  setSelectedProposalId
}) => {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('all');

  // Filter and search logic
  const filteredProposals = proposals.filter(p => {
    const searchLower = search.toLowerCase();
    const matchesSearch = 
      p.proposal_num.toLowerCase().includes(searchLower) ||
      (p.product_name && p.product_name.toLowerCase().includes(searchLower)) ||
      (p.lead_city && p.lead_city.toLowerCase().includes(searchLower)) ||
      (p.lead_state && p.lead_state.toLowerCase().includes(searchLower));

    if (!matchesSearch) return false;

    if (filter === 'all') return true;
    if (filter === 'chronic') return p.has_chronic_disease_data;
    if (filter === 'claims') return p.has_claims_data;
    if (filter === 'kyc-alert') return p.kyc_status === 'High Risk Flags';
    if (filter === 'clean') return !p.has_chronic_disease_data && !p.has_claims_data;
    return true;
  });

  const handleAudit = (proposalNum: string) => {
    setSelectedProposalId(proposalNum);
    setCurrentPage('detail');
  };

  const renderCheck = (val: boolean) => {
    return val ? (
      <Check size={16} style={{ color: 'var(--color-low)' }} />
    ) : (
      <X size={16} style={{ color: 'var(--text-muted)', opacity: 0.5 }} />
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px 0' }}>
      
      {/* Search and Filters Bar */}
      <div className="glass-panel" style={{ padding: '16px', display: 'flex', gap: '16px', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap' }}>
        
        {/* Search Input */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', position: 'relative', flex: 1, minWidth: '250px' }}>
          <Search size={18} style={{ position: 'absolute', left: '14px', color: 'var(--text-muted)' }} />
          <input 
            type="text" 
            placeholder="Search proposals by number, city, or product plan..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: '100%', paddingLeft: '44px' }}
          />
        </div>

        {/* Filter Selection */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
            <Filter size={16} />
            <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>Category:</span>
          </div>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            style={{ minWidth: '180px' }}
          >
            <option value="all">All Applications</option>
            <option value="chronic">Pre-Existing Diseases (PED)</option>
            <option value="claims">Historical Claim Holders</option>
            <option value="kyc-alert">KYC Fraud/Risk Alerts</option>
            <option value="clean">Clean Profile Applications</option>
          </select>
        </div>

      </div>

      {/* Main Grid */}
      <div className="glass-panel" style={{ padding: '24px', overflow: 'hidden' }}>
        <div style={{ overflowX: 'auto' }}>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Product Plan</th>
                <th>Age/Gender</th>
                <th>Sum Insured</th>
                <th style={{ textAlign: 'center' }}>Member</th>
                <th style={{ textAlign: 'center' }}>KYC</th>
                <th style={{ textAlign: 'center' }}>Claims</th>
                <th style={{ textAlign: 'center' }}>Agent</th>
                <th style={{ textAlign: 'center' }}>Geo</th>
                <th>Underwrite</th>
              </tr>
            </thead>
            <tbody>
              {filteredProposals.length > 0 ? (
                filteredProposals.map(proposal => (
                  <tr key={proposal.proposal_num}>
                    <td style={{ fontWeight: 600 }}>{proposal.proposal_num}</td>
                    <td>
                      <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <span style={{ fontWeight: 500 }}>{proposal.product_name || `ID: ${proposal.product_id}`}</span>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          Income: ${proposal.annual_income?.toLocaleString()}/yr
                        </span>
                      </div>
                    </td>
                    <td style={{ fontSize: '0.92rem' }}>
                      {proposal.member_age}Y ({proposal.member_gender})
                    </td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem' }}>
                      ${proposal.sum_insured?.toLocaleString()}
                    </td>
                    <td style={{ textAlign: 'center' }}>{renderCheck(proposal.has_member_data)}</td>
                    <td style={{ textAlign: 'center' }}>
                      {proposal.kyc_status === 'High Risk Flags' ? (
                        <ShieldAlert size={16} style={{ color: 'var(--color-critical)', margin: '0 auto' }} />
                      ) : (
                        renderCheck(proposal.has_kyc_data)
                      )}
                    </td>
                    <td style={{ textAlign: 'center' }}>{renderCheck(proposal.has_claims_data)}</td>
                    <td style={{ textAlign: 'center' }}>{renderCheck(proposal.has_agent_data)}</td>
                    <td style={{ textAlign: 'center' }}>{renderCheck(proposal.has_lead_data)}</td>
                    <td>
                      <button
                        onClick={() => handleAudit(proposal.proposal_num)}
                        style={{
                          background: 'rgba(99, 102, 241, 0.15)',
                          color: 'var(--color-primary)',
                          border: '1px solid rgba(99, 102, 241, 0.3)',
                          padding: '6px 14px',
                          borderRadius: '6px',
                          fontSize: '0.82rem',
                          fontWeight: 600
                        }}
                        className="glass-panel-interactive"
                      >
                        Assess
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={10} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '40px' }}>
                    No proposals matched your search/filter parameters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
