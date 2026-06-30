"""
Agent data extractor.

Extracts agent/distribution channel information from database tables:
- AgentDetails: agent profile, channel
- AgentRiskScores: pre-calculated risk metrics
- AnnualClubPerformance: performance indicators
"""

from sqlalchemy.orm import Session
from datetime import datetime
from db.models import AgentDetails, AgentRiskScores, AnnualClubPerformance, ProposalDetails
from data.schemas.agent_schema import AgentData


def parse_percentage(value: str) -> float:
    """Parse percentage string to float (e.g., '80%' -> 80.0)"""
    try:
        return float(value.replace('%', '').strip())
    except:
        return 0.0


def extract_agent_data(db: Session, proposal_id: str) -> AgentData:
    """
    Extract agent data from database for a given proposal.
    
    Args:
        db: Database session
        proposal_id: Unique proposal identifier
        
    Returns:
        AgentData object populated from database
        
    Raises:
        ValueError: If proposal or agent not found
    """
    # Get proposal
    proposal = db.query(ProposalDetails).filter(
        ProposalDetails.proposal_num == proposal_id
    ).first()
    
    if not proposal:
        raise ValueError(f"Proposal {proposal_id} not found")
    
    if not proposal.agent_code:
        raise ValueError(f"No agent code found for proposal {proposal_id}")
    
    # Get agent details
    agent = db.query(AgentDetails).filter(
        AgentDetails.agent_code == proposal.agent_code
    ).first()
    
    if not agent:
        raise ValueError(f"Agent {proposal.agent_code} not found")
    
    # Get agent risk scores
    risk_scores = db.query(AgentRiskScores).filter(
        AgentRiskScores.agent_code == proposal.agent_code
    ).first()
    
    # Get agent performance
    performance = db.query(AnnualClubPerformance).filter(
        AnnualClubPerformance.agent_code == proposal.agent_code
    ).first()
    
    # Calculate years licensed
    years_licensed = 5  # Default
    if agent.created_on:
        years_licensed = (datetime.now() - agent.created_on).days // 365
    
    # Get loss ratio and lapse rate
    loss_ratio = 50.0  # Default
    lapse_rate = 10.0  # Default
    
    if risk_scores:
        if risk_scores.loss_ratio:
            loss_ratio = float(risk_scores.loss_ratio)
        if risk_scores.lapse_rate:
            lapse_rate = float(risk_scores.lapse_rate)
    elif performance and performance.loss_ratio:
        loss_ratio = parse_percentage(performance.loss_ratio)
    
    # Map channel to valid distribution_channel values
    channel_map = {
        "Direct": "Direct",
        "Agency": "Broker",  # Map Agency to Broker
        "Broker": "Broker",
        "Online": "Online",
        "Captive": "Captive",
        "Digital": "Online",
        "Partner": "Broker"
    }
    distribution_channel = channel_map.get(agent.channel, "Broker") if agent.channel else "Broker"
    
    # Get performance metrics
    total_policies_sold = 100  # Default, not in DB
    policies_sold_12mo = 20  # Default, not in DB
    
    if performance:
        # Try to extract from performance data if available
        total_policies_sold = 100  # Still default as not directly in DB
        policies_sold_12mo = 20
    
    # Calculate agent risk score (0-100)
    agent_risk_score = 20.0  # Default low risk
    if risk_scores and risk_scores.risk_category:
        risk_map = {"Low": 15.0, "Medium": 50.0, "High": 85.0}
        agent_risk_score = risk_map.get(risk_scores.risk_category, 20.0)
    
    # Build AgentData object
    return AgentData(
        customer_id=f"CUST_{proposal_id}",
        agent_id=agent.agent_code,
        agent_name=agent.agent_code,  # Name not in DB, use code
        agent_license_number=agent.agent_code,  # License not in DB, use code
        years_licensed=max(years_licensed, 1),
        total_policies_sold=total_policies_sold,
        policies_sold_12mo=policies_sold_12mo,
        lapse_rate=lapse_rate,
        compliance_violations=0,  # Not in DB, assume none
        active_complaints=0,  # Not in DB, assume none
        distribution_channel=distribution_channel,
        fraud_investigations=0,  # Not in DB, assume none
        fraud_confirmed_cases=0,  # Not in DB, assume none
        agent_risk_score=agent_risk_score
    )
