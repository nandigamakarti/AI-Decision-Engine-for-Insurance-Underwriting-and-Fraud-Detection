from pydantic import BaseModel, Field


class AgentData(BaseModel):
    """Agent/distribution channel risk factors"""
    customer_id: str

    # Agent Info
    agent_id: str
    agent_name: str
    agent_license_number: str
    years_licensed: int = Field(ge=0)

    # Performance
    total_policies_sold: int = Field(ge=0)
    policies_sold_12mo: int = Field(ge=0)
    lapse_rate: float = Field(ge=0, le=100)  # Percentage

    # Compliance
    compliance_violations: int = Field(ge=0)
    active_complaints: int = Field(ge=0)

    # Channel
    distribution_channel: str = Field(..., pattern="^(Direct|Broker|Online|Captive)$")

    # Fraud Risk
    fraud_investigations: int = Field(ge=0)
    fraud_confirmed_cases: int = Field(ge=0)
    agent_risk_score: float = Field(ge=0, le=100)

    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "customer_id": "CUST_001",
                "agent_id": "AGT_5432",
                "agent_name": "Jane Smith",
                "agent_license_number": "AGT-NY-12345",
                "years_licensed": 8,
                "total_policies_sold": 450,
                "policies_sold_12mo": 65,
                "lapse_rate": 8.5,
                "compliance_violations": 0,
                "active_complaints": 0,
                "distribution_channel": "Broker",
                "fraud_investigations": 0,
                "fraud_confirmed_cases": 0,
                "agent_risk_score": 15
            }
        }
