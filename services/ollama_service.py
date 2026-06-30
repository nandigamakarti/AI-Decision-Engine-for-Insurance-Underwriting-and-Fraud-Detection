"""
Ollama Integration Service - Handles communication with Ollama AI model.
Generates dynamic risk assessments using structured prompting.
"""

import json
import logging
from typing import Optional, Dict, Any
import requests
from pydantic import BaseModel

from config import settings
from api.models import CustomerDataInput, RiskAssessmentOutput, RiskFactor

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for interacting with Ollama AI model for risk assessment."""

    def __init__(self):
        """Initialize the Ollama service."""
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.temperature = settings.OLLAMA_TEMPERATURE
        self.top_p = settings.OLLAMA_TOP_P
        self.timeout = settings.OLLAMA_TIMEOUT

    def health_check(self) -> bool:
        """
        Check if Ollama service is running and accessible.

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama health check failed: {str(e)}")
            return False

    def assess_risk(self, customer_data: CustomerDataInput) -> RiskAssessmentOutput:
        """
        Use Ollama to generate dynamic risk assessment.

        Args:
            customer_data: Customer information for risk assessment

        Returns:
            RiskAssessmentOutput with AI-generated risk factors and scores
        """
        try:
            # Build the prompt for risk assessment
            prompt = self._build_risk_assessment_prompt(customer_data)

            # Call Ollama to generate risk assessment
            response = self._call_ollama(prompt)

            # Parse the response
            risk_assessment = self._parse_risk_assessment(response, customer_data)

            return risk_assessment

        except Exception as e:
            logger.error(f"Error in Ollama risk assessment: {str(e)}")
            raise

    def _build_risk_assessment_prompt(self, customer_data: CustomerDataInput) -> str:
        """
        Build a structured prompt for Ollama to assess customer risk.

        Args:
            customer_data: Customer data to assess

        Returns:
            Prompt string for Ollama
        """
        customer_json = customer_data.model_dump_json(indent=2)

        prompt = f"""You are an expert insurance underwriter assistant. Analyze the following customer data and provide a comprehensive risk assessment in JSON format.

CUSTOMER DATA:
{customer_json}

Based on the customer data above, provide a detailed risk assessment in the following JSON format (IMPORTANT: respond ONLY with valid JSON, no additional text):

{{
    "overall_risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "overall_risk_score": <number 0-100>,
    "risk_factors": [
        {{
            "factor_name": "<name of the risk factor>",
            "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
            "score": <number 0-100>,
            "description": "<detailed explanation of why this is a risk>"
        }}
    ],
    "recommendations": [
        "<underwriting recommendation 1>",
        "<underwriting recommendation 2>"
    ],
    "additional_notes": "<any additional insights or observations>"
}}

Guidelines for assessment:
1. Analyze health factors (conditions, smoking, BMI, medications)
2. Consider financial stability (income, credit score, debt levels)
3. Review claims history patterns
4. Assess lifestyle and age-related risks
5. Flag any inconsistencies or red flags in the data
6. Provide actionable underwriting recommendations
7. Ensure all risk scores and levels are justified by the data

IMPORTANT: Return ONLY valid JSON. Do not include any markdown formatting, code blocks, or explanatory text."""

        return prompt

    def _call_ollama(self, prompt: str) -> str:
        """
        Call the Ollama API with the given prompt.

        Args:
            prompt: The prompt to send to Ollama

        Returns:
            The model's response as a string
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except requests.exceptions.Timeout:
            raise Exception(
                f"Ollama request timed out after {self.timeout} seconds. "
                "Consider increasing OLLAMA_TIMEOUT."
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to communicate with Ollama: {str(e)}")

    def _parse_risk_assessment(
        self, response_text: str, customer_data: CustomerDataInput
    ) -> RiskAssessmentOutput:
        """
        Parse the Ollama response and convert to RiskAssessmentOutput.

        Args:
            response_text: Raw text response from Ollama
            customer_data: Original customer data

        Returns:
            Parsed RiskAssessmentOutput object
        """
        try:
            # Try to extract JSON from the response
            json_str = self._extract_json(response_text)

            # Parse the JSON
            assessment_data = json.loads(json_str)

            # Convert risk factors
            risk_factors = [
                RiskFactor(
                    factor_name=factor.get("factor_name", "Unknown"),
                    risk_level=factor.get("risk_level", "MEDIUM").upper(),
                    score=float(factor.get("score", 50)),
                    description=factor.get("description", "")
                )
                for factor in assessment_data.get("risk_factors", [])
            ]

            # Create output
            output = RiskAssessmentOutput(
                customer_id=customer_data.customer_id,
                overall_risk_level=assessment_data.get("overall_risk_level", "MEDIUM").upper(),
                overall_risk_score=float(assessment_data.get("overall_risk_score", 50)),
                risk_factors=risk_factors,
                recommendations=assessment_data.get("recommendations", []),
                assessment_date=assessment_data.get(
                    "assessment_date",
                    ""
                ) or self._get_current_timestamp(),
                additional_notes=assessment_data.get(
                    "additional_notes",
                    "Risk assessment completed using Ollama AI model"
                )
            )

            return output

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from Ollama: {str(e)}")
            logger.error(f"Response text: {response_text}")
            raise Exception(f"Invalid JSON response from Ollama: {str(e)}")

    def _extract_json(self, text: str) -> str:
        """
        Extract valid JSON from text that may contain extra content.

        Args:
            text: Text potentially containing JSON

        Returns:
            Extracted JSON string

        Raises:
            Exception: If no valid JSON can be extracted
        """
        # Try to find JSON object in the text
        start_idx = text.find("{")
        if start_idx == -1:
            raise Exception("No JSON object found in response")

        # Find the matching closing brace
        brace_count = 0
        for i in range(start_idx, len(text)):
            if text[i] == "{":
                brace_count += 1
            elif text[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    return text[start_idx : i + 1]

        raise Exception("Could not find matching closing brace for JSON object")

    @staticmethod
    def _get_current_timestamp() -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()


# Global instance
ollama_service = OllamaService()
