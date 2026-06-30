"""
Test script for database-driven risk assessment APIs.

This script demonstrates how to use the new API endpoints that
retrieve data from the database instead of requiring full schemas.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_risk_endpoint(endpoint: str, proposal_id: str):
    """Test a single risk assessment endpoint."""
    url = f"{BASE_URL}/api/risk/{endpoint}"
    payload = {"proposal_id": proposal_id}
    
    print(f"\n{'='*70}")
    print(f"Testing: {endpoint.upper()} Risk Assessment")
    print(f"{'='*70}")
    print(f"Request: POST {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS")
            print(f"\nRisk Score: {result.get('risk_score')}/100")
            print(f"Risk Level: {result.get('risk_level')}")
            print(f"Dimension: {result.get('dimension')}")
            
            if result.get('risk_factors'):
                print(f"\nRisk Factors:")
                for factor in result['risk_factors']:
                    print(f"  - {factor}")
            
            if result.get('recommendations'):
                print(f"\nRecommendations:")
                for rec in result['recommendations'][:3]:  # Show first 3
                    print(f"  - {rec}")
        
        elif response.status_code == 404:
            print(f"❌ NOT FOUND: {response.json().get('detail')}")
        
        else:
            print(f"❌ ERROR: {response.json().get('detail')}")
    
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR: Server not running at {BASE_URL}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def test_combined_risk(proposal_id: str):
    """Test combined risk assessment."""
    url = f"{BASE_URL}/api/risk/combined"
    payload = {"proposal_id": proposal_id}
    
    print(f"\n{'='*70}")
    print(f"Testing: COMBINED Risk Assessment (All 7 Dimensions)")
    print(f"{'='*70}")
    print(f"Request: POST {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS")
            print(f"\nOverall Risk Score: {result.get('overall_risk_score')}/100")
            print(f"Risk Level: {result.get('risk_level')}")
            print(f"Underwriting Decision: {result.get('underwriting_decision')}")
            print(f"Premium Loading: {result.get('premium_loading_percentage')}%")
            
            if result.get('dimension_scores'):
                print(f"\nDimension Scores:")
                for dim in result['dimension_scores']:
                    print(f"  - {dim['dimension']:.<20} {dim['score']:>3}/100 (weight: {dim['weight']*100:.0f}%)")
            
            if result.get('top_risk_factors'):
                print(f"\nTop Risk Factors:")
                for factor in result['top_risk_factors'][:5]:
                    print(f"  - {factor}")
        
        elif response.status_code == 404:
            print(f"❌ NOT FOUND: {response.json().get('detail')}")
        
        else:
            print(f"❌ ERROR: {response.json().get('detail')}")
    
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR: Server not running at {BASE_URL}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("DATABASE-DRIVEN RISK ASSESSMENT API TESTS")
    print("="*70)
    
    # Test with a proposal ID (you'll need to insert data first)
    proposal_id = input("\nEnter Proposal ID to test (or press Enter for 'PROP001'): ").strip()
    if not proposal_id:
        proposal_id = "PROP001"
    
    print(f"\nTesting with Proposal ID: {proposal_id}")
    
    # Test individual risk dimensions
    endpoints = [
        "demographic",
        "financial",
        "medical",
        "regional",
        "claims",
        "agent",
        "product"
    ]
    
    for endpoint in endpoints:
        test_risk_endpoint(endpoint, proposal_id)
    
    # Test combined risk
    test_combined_risk(proposal_id)
    
    print(f"\n{'='*70}")
    print("TESTS COMPLETE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
