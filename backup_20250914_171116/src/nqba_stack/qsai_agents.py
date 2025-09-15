"""
QSAI Specialized Agents
=======================

Specialized micro-agents for different decision domains in the QSAI system.
Each agent is responsible for generating action proposals in their specific domain
using quantum-enhanced models and classical fallbacks.
"""

import asyncio
import logging
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .qsai_engine import ActionProposal, ContextVector, AgentType
from .qdllm import qdllm
from .qtransformer import qtransformer
from .qnlp import qnlp
from .dynex_client import get_dynex_client
from .core.ltc_logger import LTCLogger

logger = logging.getLogger(__name__)


class OfferType(Enum):
    """Types of offers that can be proposed"""

    FEATURE_ON_DEMAND = "feature_on_demand"
    SERVICE_PACKAGE = "service_package"
    CHARGING_INCENTIVE = "charging_incentive"
    INSURANCE = "insurance"
    ACCESSORY = "accessory"
    MAINTENANCE = "maintenance"
    SUBSCRIPTION = "subscription"


class ChannelType(Enum):
    """Communication channels for offers"""

    HMI_VOICE = "hmi_voice"
    HMI_CARD = "hmi_card"
    PUSH_NOTIFICATION = "push_notification"
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"


class RiskLevel(Enum):
    """Risk assessment levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class OfferContext:
    """Context for offer generation"""

    user_segment: str
    vehicle_state: Dict[str, Any]
    trip_context: Dict[str, Any]
    market_conditions: Dict[str, Any]
    user_preferences: Dict[str, Any]
    historical_responses: List[Dict[str, Any]]


class OfferAgent:
    """Agent responsible for generating personalized offers"""

    def __init__(self, ltc_logger: LTCLogger):
        self.ltc_logger = ltc_logger
        self.dynex = get_dynex_client()
        self.offer_history: List[Dict[str, Any]] = []
        self.conversion_rates: Dict[str, float] = {}

    def propose_action(self, context: ContextVector) -> Optional[ActionProposal]:
        """Generate personalized offer proposals"""
        logger.info(f"Generating offers for user {context.user_id}")

        try:
            # Build offer context
            offer_context = self._build_offer_context(context)

            # Generate offers using qdLLM (simplified for testing)
            offers = self._generate_offers_sync(offer_context)

            if not offers:
                return None

            # Select best offer using quantum optimization (simplified for testing)
            best_offer = self._select_best_offer_sync(offers, offer_context)

            if not best_offer:
                return None

            # Create action proposal
            proposal = ActionProposal(
                agent_id="offer_agent_v1",
                agent_type=AgentType.OFFER,
                action_id=f"offer_{int(time.time() * 1000)}",
                payload=best_offer,
                estimated_reward=best_offer.get("estimated_revenue", 0.0),
                confidence=best_offer.get("confidence", 0.5),
                required_resources={
                    "hmi_surface": "available",
                    "user_attention": "low",
                },
                safety_impact="low",
                compliance_status="compliant",
                rationale=best_offer.get(
                    "rationale", "Personalized offer based on user context"
                ),
            )

            # Log offer generation
            self.ltc_logger.log_operation(
                "offer_generated",
                {"user_id": context.user_id, "offer_type": best_offer.get("type")},
                "offer_agent",
            )

            return proposal

        except Exception as e:
            logger.error(f"Offer generation failed: {e}")
            return None

    def _build_offer_context(self, context: ContextVector) -> OfferContext:
        """Build offer-specific context from general context"""
        return OfferContext(
            user_segment=context.business_context.get("user_segment", "standard"),
            vehicle_state=context.telemetry,
            trip_context=context.business_context.get("trip_context", {}),
            market_conditions=context.market_signals,
            user_preferences=context.business_context.get("user_preferences", {}),
            historical_responses=self._get_historical_responses(context.user_id),
        )

    def _get_historical_responses(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's historical offer responses"""
        try:
            # Simulate historical data retrieval from database/cache
            # In production, this would query a database or cache service
            historical_data = [
                {
                    "offer_id": f"offer_{user_id}_001",
                    "offer_type": "charging_incentive",
                    "response": "accepted",
                    "timestamp": (datetime.now() - pd.Timedelta(days=7)).isoformat(),
                    "conversion_rate": 0.8,
                    "revenue": 5.0,
                    "channel": "hmi_voice",
                    "context": {"battery_level": 25, "trip_phase": "pre_trip"}
                },
                {
                    "offer_id": f"offer_{user_id}_002",
                    "offer_type": "feature_on_demand",
                    "response": "declined",
                    "timestamp": (datetime.now() - pd.Timedelta(days=3)).isoformat(),
                    "conversion_rate": 0.0,
                    "revenue": 0.0,
                    "channel": "hmi_card",
                    "context": {"speed": 65, "trip_phase": "highway"}
                },
                {
                    "offer_id": f"offer_{user_id}_003",
                    "offer_type": "maintenance",
                    "response": "accepted",
                    "timestamp": (datetime.now() - pd.Timedelta(days=1)).isoformat(),
                    "conversion_rate": 0.4,
                    "revenue": 90.0,
                    "channel": "push_notification",
                    "context": {"maintenance_due": True, "trip_phase": "post_trip"}
                }
            ]
            
            # Filter recent responses (last 30 days)
            cutoff_date = datetime.now() - pd.Timedelta(days=30)
            recent_responses = [
                response for response in historical_data
                if datetime.fromisoformat(response["timestamp"]) > cutoff_date
            ]
            
            logger.info(f"Retrieved {len(recent_responses)} historical responses for user {user_id}")
            return recent_responses
            
        except Exception as e:
            logger.error(f"Failed to retrieve historical responses for user {user_id}: {e}")
            return []

    def _generate_offers_sync(self, context: OfferContext) -> List[Dict[str, Any]]:
        """Generate candidate offers using qdLLM"""
        prompt = f"""
        Generate personalized offers for a connected vehicle user:
        
        User Segment: {context.user_segment}
        Vehicle State: {json.dumps(context.vehicle_state, indent=2)}
        Trip Context: {json.dumps(context.trip_context, indent=2)}
        Market Conditions: {json.dumps(context.market_conditions, indent=2)}
        User Preferences: {json.dumps(context.user_preferences, indent=2)}
        
        Generate 3-5 offers that:
        1. Match the user's current context and preferences
        2. Have high conversion potential
        3. Respect safety and compliance requirements
        4. Maximize revenue while maintaining user satisfaction
        
        For each offer, provide:
        - Type (feature, service, charging, insurance, accessory, maintenance, subscription)
        - Description
        - Price
        - Estimated conversion probability
        - Estimated revenue
        - Rationale
        """

        try:
            # For testing, skip qdLLM call and use fallback offers
            offers = self._generate_fallback_offers(context)

            return offers

        except Exception as e:
            logger.error(f"Failed to generate offers with qdLLM: {e}")
            return self._generate_fallback_offers(context)

    def _parse_offers_response(
        self, response: Dict[str, Any], context: OfferContext
    ) -> List[Dict[str, Any]]:
        """Parse qdLLM response into structured offers"""
        try:
            # Parse qdLLM response content
            content = response.get("content", "")
            if not content:
                logger.warning("Empty response from qdLLM, using fallback offers")
                return self._generate_fallback_offers(context)
            
            # Extract structured offers from response
            # Look for JSON-like structures in the response
            offers = []
            
            # Try to extract offers from structured response
            if "offers" in response:
                raw_offers = response["offers"]
                for raw_offer in raw_offers:
                    offer = self._parse_single_offer(raw_offer, context)
                    if offer:
                        offers.append(offer)
            else:
                # Parse from text content using pattern matching
                offers = self._extract_offers_from_text(content, context)
            
            # Validate and filter offers
            valid_offers = []
            for offer in offers:
                if self._validate_offer(offer):
                    valid_offers.append(offer)
                else:
                    logger.warning(f"Invalid offer filtered out: {offer}")
            
            if not valid_offers:
                logger.warning("No valid offers parsed, using fallback")
                return self._generate_fallback_offers(context)
            
            logger.info(f"Successfully parsed {len(valid_offers)} offers from qdLLM response")
            return valid_offers
            
        except Exception as e:
            logger.error(f"Failed to parse qdLLM offers response: {e}")
            return self._generate_fallback_offers(context)

        offers = []

        # Generate charging incentive if battery is low
        if context.vehicle_state.get("battery_level", 100) < 30:
            offers.append(
                {
                    "type": OfferType.CHARGING_INCENTIVE.value,
                    "description": "20% discount on next charging session",
                    "price": 0.0,
                    "estimated_conversion": 0.8,
                    "estimated_revenue": 5.0,
                    "confidence": 0.9,
                    "rationale": "Low battery detected, high conversion probability",
                }
            )

        # Generate feature-on-demand if user shows interest
        if context.user_preferences.get("feature_interest", False):
            offers.append(
                {
                    "type": OfferType.FEATURE_ON_DEMAND.value,
                    "description": "Premium navigation upgrade - 7-day trial",
                    "price": 0.0,
                    "estimated_conversion": 0.6,
                    "estimated_revenue": 15.0,
                    "confidence": 0.7,
                    "rationale": "User shows interest in premium features",
                }
            )

        # Generate maintenance reminder if due
        if context.vehicle_state.get("maintenance_due", False):
            offers.append(
                {
                    "type": OfferType.MAINTENANCE.value,
                    "description": "Scheduled maintenance package with 10% discount",
                    "price": 90.0,
                    "estimated_conversion": 0.4,
                    "estimated_revenue": 90.0,
                    "confidence": 0.6,
                    "rationale": "Maintenance due, safety-related offer",
                }
            )

        return offers

    def _generate_fallback_offers(self, context: OfferContext) -> List[Dict[str, Any]]:
        """Generate fallback offers when qdLLM fails"""
        return [
            {
                "type": OfferType.CHARGING_INCENTIVE.value,
                "description": "Standard charging discount",
                "price": 0.0,
                "estimated_conversion": 0.5,
                "estimated_revenue": 3.0,
                "confidence": 0.5,
                "rationale": "Fallback offer",
            }
        ]

    def _select_best_offer_sync(
        self, offers: List[Dict[str, Any]], context: OfferContext
    ) -> Optional[Dict[str, Any]]:
        """Select best offer using quantum optimization"""
        if len(offers) == 1:
            return offers[0]

        try:
            # Build QUBO for offer selection
            qubo_matrix = self._build_offer_selection_qubo(offers, context)

            # Submit to quantum solver (simplified for testing)
            qubo_result = self._simulate_qubo_solve(qubo_matrix, len(offers))

            # Parse result
            selected_index = self._parse_offer_selection_result(
                qubo_result, len(offers)
            )

            return offers[selected_index]

        except Exception as e:
            logger.warning(
                f"Quantum offer selection failed, using classical fallback: {e}"
            )
            return self._classical_offer_selection(offers, context)

    def _build_offer_selection_qubo(
        self, offers: List[Dict[str, Any]], context: OfferContext
    ) -> np.ndarray:
        """Build QUBO matrix for offer selection optimization"""
        n_offers = len(offers)
        qubo = np.zeros((n_offers, n_offers))

        # Objective: maximize expected revenue
        for i, offer in enumerate(offers):
            expected_revenue = offer.get("estimated_revenue", 0.0) * offer.get(
                "estimated_conversion", 0.5
            )
            qubo[i, i] = -expected_revenue

        # Constraint: select exactly one offer
        constraint_strength = 100.0
        for i in range(n_offers):
            for j in range(n_offers):
                if i != j:
                    qubo[i, j] += constraint_strength

        return qubo

    def _simulate_qubo_solve(
        self, qubo_matrix: np.ndarray, num_offers: int
    ) -> Dict[str, Any]:
        """Simulate QUBO solve for testing (returns best offer index)"""
        # For testing, just return the first offer
        return {"solution": [0], "energy": -1.0, "num_occurrences": 1}

    def _parse_offer_selection_result(
        self, qubo_result: Dict[str, Any], num_offers: int
    ) -> int:
        """Parse quantum result to get selected offer index"""
        try:
            # Parse Dynex QUBO result format
            if "solution" in qubo_result:
                solution = qubo_result["solution"]
                
                # Handle different solution formats
                if isinstance(solution, list):
                    # Binary solution vector format
                    if len(solution) >= num_offers:
                        # Find the index of the selected offer (value = 1)
                        for i, value in enumerate(solution[:num_offers]):
                            if value == 1:
                                logger.info(f"QUBO selected offer index: {i}")
                                return i
                    
                    # If no clear selection, use first non-zero or default to 0
                    for i, value in enumerate(solution[:num_offers]):
                        if value > 0:
                            return i
                            
                elif isinstance(solution, dict):
                    # Dictionary format with variable names
                    selected_vars = [k for k, v in solution.items() if v == 1]
                    if selected_vars:
                        # Extract index from variable name (e.g., "x_0", "offer_1")
                        for var in selected_vars:
                            try:
                                index = int(var.split('_')[-1])
                                if 0 <= index < num_offers:
                                    logger.info(f"QUBO selected offer index: {index}")
                                    return index
                            except (ValueError, IndexError):
                                continue
            
            # Parse energy-based selection if available
            if "energy" in qubo_result and "num_occurrences" in qubo_result:
                energy = qubo_result["energy"]
                occurrences = qubo_result["num_occurrences"]
                
                # Lower energy indicates better solution
                if energy < 0 and occurrences > 0:
                    # Use energy to influence selection
                    selected_index = abs(int(energy)) % num_offers
                    logger.info(f"Energy-based selection: index {selected_index}")
                    return selected_index
            
            # Fallback: return first offer
            logger.warning("Could not parse QUBO result, defaulting to first offer")
            return 0
            
        except Exception as e:
            logger.error(f"Failed to parse QUBO selection result: {e}")
            return 0

    def _classical_offer_selection(
        self, offers: List[Dict[str, Any]], context: OfferContext
    ) -> Dict[str, Any]:
        """Classical fallback for offer selection"""
        # Simple greedy selection based on expected revenue
        best_offer = max(
            offers,
            key=lambda o: o.get("estimated_revenue", 0.0)
            * o.get("estimated_conversion", 0.5),
        )
        return best_offer

    def _parse_single_offer(self, raw_offer: Dict[str, Any], context: OfferContext) -> Optional[Dict[str, Any]]:
        """Parse a single offer from qdLLM response"""
        try:
            offer = {
                "type": raw_offer.get("type", "unknown"),
                "description": raw_offer.get("description", ""),
                "price": float(raw_offer.get("price", 0.0)),
                "estimated_conversion": float(raw_offer.get("estimated_conversion", 0.5)),
                "estimated_revenue": float(raw_offer.get("estimated_revenue", 0.0)),
                "confidence": float(raw_offer.get("confidence", 0.5)),
                "rationale": raw_offer.get("rationale", "AI-generated offer")
            }
            return offer
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to parse single offer: {e}")
            return None

    def _extract_offers_from_text(self, content: str, context: OfferContext) -> List[Dict[str, Any]]:
        """Extract offers from text content using pattern matching"""
        offers = []
        try:
            # Simple pattern matching for offer extraction
            # Look for structured patterns in the text
            lines = content.split('\n')
            current_offer = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Look for offer type indicators
                if any(offer_type in line.lower() for offer_type in ['charging', 'feature', 'maintenance', 'insurance']):
                    if current_offer:
                        offers.append(current_offer)
                    current_offer = {
                        "type": self._extract_offer_type(line),
                        "description": line,
                        "price": 0.0,
                        "estimated_conversion": 0.5,
                        "estimated_revenue": 0.0,
                        "confidence": 0.6,
                        "rationale": "Extracted from text"
                    }
                
                # Extract price information
                elif '$' in line or 'price' in line.lower():
                    price = self._extract_price(line)
                    if price is not None and current_offer:
                        current_offer["price"] = price
                        current_offer["estimated_revenue"] = price
                
                # Extract conversion probability
                elif '%' in line or 'conversion' in line.lower():
                    conversion = self._extract_percentage(line)
                    if conversion is not None and current_offer:
                        current_offer["estimated_conversion"] = conversion
            
            # Add the last offer
            if current_offer:
                offers.append(current_offer)
                
        except Exception as e:
            logger.error(f"Failed to extract offers from text: {e}")
            
        return offers

    def _extract_offer_type(self, text: str) -> str:
        """Extract offer type from text"""
        text_lower = text.lower()
        if 'charging' in text_lower:
            return OfferType.CHARGING_INCENTIVE.value
        elif 'feature' in text_lower or 'upgrade' in text_lower:
            return OfferType.FEATURE_ON_DEMAND.value
        elif 'maintenance' in text_lower:
            return OfferType.MAINTENANCE.value
        elif 'insurance' in text_lower:
            return OfferType.INSURANCE.value
        else:
            return "unknown"

    def _extract_price(self, text: str) -> Optional[float]:
        """Extract price from text"""
        import re
        try:
            # Look for price patterns like $10.99, $10, 10.99
            price_match = re.search(r'\$?([0-9]+\.?[0-9]*)', text)
            if price_match:
                return float(price_match.group(1))
        except (ValueError, AttributeError):
            pass
        return None

    def _extract_percentage(self, text: str) -> Optional[float]:
        """Extract percentage from text"""
        import re
        try:
            # Look for percentage patterns like 80%, 0.8
            percent_match = re.search(r'([0-9]+\.?[0-9]*)%?', text)
            if percent_match:
                value = float(percent_match.group(1))
                # Convert to decimal if it's a percentage
                if value > 1.0:
                    value = value / 100.0
                return min(value, 1.0)
        except (ValueError, AttributeError):
            pass
        return None

    def _validate_offer(self, offer: Dict[str, Any]) -> bool:
        """Validate offer structure and values"""
        try:
            # Check required fields
            required_fields = ["type", "description", "price", "estimated_conversion", "estimated_revenue"]
            for field in required_fields:
                if field not in offer:
                    return False
            
            # Validate value ranges
            if not (0.0 <= offer["estimated_conversion"] <= 1.0):
                return False
            
            if offer["price"] < 0:
                return False
            
            if offer["estimated_revenue"] < 0:
                return False
            
            # Check offer type is valid
            valid_types = [e.value for e in OfferType]
            if offer["type"] not in valid_types and offer["type"] != "unknown":
                return False
            
            return True
            
        except (KeyError, TypeError, ValueError):
            return False


class TimingAgent:
    """Agent responsible for determining optimal timing for actions"""

    def __init__(self, ltc_logger: LTCLogger):
        self.ltc_logger = ltc_logger
        self.timing_history: List[Dict[str, Any]] = []

    def propose_action(self, context: ContextVector) -> Optional[ActionProposal]:
        """Generate timing recommendations for actions"""
        logger.info(f"Generating timing recommendations for user {context.user_id}")

        try:
            # Analyze context for timing decisions
            timing_analysis = self._analyze_timing_context(context)

            # Generate timing recommendation using qdLLM (simplified for testing)
            timing_recommendation = self._generate_timing_recommendation_sync(
                timing_analysis
            )

            if not timing_recommendation:
                return None

            # Create action proposal
            proposal = ActionProposal(
                agent_id="timing_agent_v1",
                agent_type=AgentType.TIMING,
                action_id=f"timing_{int(time.time() * 1000)}",
                payload=timing_recommendation,
                estimated_reward=timing_recommendation.get("timing_boost", 0.0),
                confidence=timing_recommendation.get("confidence", 0.5),
                required_resources={"timing_engine": "available"},
                safety_impact="low",
                compliance_status="compliant",
                rationale=timing_recommendation.get(
                    "rationale", "Optimal timing based on context analysis"
                ),
            )

            return proposal

        except Exception as e:
            logger.error(f"Timing recommendation failed: {e}")
            return None

    def _analyze_timing_context(self, context: ContextVector) -> Dict[str, Any]:
        """Analyze context for timing decisions"""
        analysis = {
            "current_time": datetime.now().isoformat(),  # Convert to ISO string for JSON serialization
            "trip_phase": self._determine_trip_phase(context),
            "driver_workload": self._estimate_driver_workload(context),
            "urgency_level": self._assess_urgency(context),
            "optimal_windows": self._identify_optimal_windows(context),
        }

        return analysis

    def _determine_trip_phase(self, context: ContextVector) -> str:
        """Determine current trip phase"""
        telemetry = context.telemetry

        if telemetry.get("speed", 0) == 0:
            return "parked"
        elif telemetry.get("speed", 0) < 10:
            return "low_speed"
        elif telemetry.get("speed", 0) > 80:
            return "highway"
        else:
            return "city_driving"

    def _estimate_driver_workload(self, context: ContextVector) -> float:
        """Estimate current driver workload (0.0 to 1.0)"""
        telemetry = context.telemetry

        # Factors: speed, acceleration, steering, navigation activity
        speed_factor = min(telemetry.get("speed", 0) / 120.0, 1.0)
        accel_factor = abs(telemetry.get("acceleration", 0)) / 10.0
        steering_factor = abs(telemetry.get("steering_angle", 0)) / 45.0

        workload = (speed_factor + accel_factor + steering_factor) / 3.0
        return min(workload, 1.0)

    def _assess_urgency(self, context: ContextVector) -> str:
        """Assess urgency level of potential actions"""
        telemetry = context.telemetry
        business_context = context.business_context

        # Check for urgent conditions
        if telemetry.get("battery_level", 100) < 20:
            return "critical"
        elif telemetry.get("maintenance_due", False):
            return "high"
        elif business_context.get("subscription_expiring", False):
            return "medium"
        else:
            return "low"

    def _identify_optimal_windows(self, context: ContextVector) -> List[Dict[str, Any]]:
        """Identify optimal timing windows for actions"""
        windows = []

        # Pre-trip window
        windows.append(
            {
                "type": "pre_trip",
                "description": "Before starting trip",
                "optimal_duration": 300,  # 5 minutes
                "conditions": ["parked", "low_workload"],
            }
        )

        # Post-trip window
        windows.append(
            {
                "type": "post_trip",
                "description": "After completing trip",
                "optimal_duration": 600,  # 10 minutes
                "conditions": ["parked", "low_workload"],
            }
        )

        # Low-workload driving window
        windows.append(
            {
                "type": "low_workload",
                "description": "During low-workload driving",
                "optimal_duration": 120,  # 2 minutes
                "conditions": ["city_driving", "low_workload"],
            }
        )

        return windows

    def _generate_timing_recommendation_sync(
        self, timing_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Generate timing recommendation using qdLLM"""
        prompt = f"""
        Generate optimal timing recommendations for connected vehicle actions:
        
        Timing Analysis: {json.dumps(timing_analysis, indent=2)}
        
        Provide recommendations for:
        1. When to show offers (immediate, deferred, post-trip)
        2. Optimal duration for user interaction
        3. Conditions that would make timing better
        4. Expected boost in conversion rate
        5. Rationale for timing choice
        """

        try:
            # For testing, skip qdLLM call and use fallback timing
            recommendation = self._generate_fallback_timing(timing_analysis)

            return recommendation

        except Exception as e:
            logger.error(f"Failed to generate timing recommendation: {e}")
            return self._generate_fallback_timing(timing_analysis)

    def _parse_timing_response(
        self, response: Dict[str, Any], timing_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse qdLLM response into timing recommendation"""
        try:
            # Parse qdLLM response content
            content = response.get("content", "")
            
            # Initialize default values
            timing = "post_trip"
            duration = 600
            timing_boost = 0.1
            confidence = 0.5
            rationale = "Default timing recommendation"
            
            # Try to extract structured timing data from response
            if "timing" in response:
                timing_data = response["timing"]
                timing = timing_data.get("when", timing)
                duration = timing_data.get("duration", duration)
                timing_boost = timing_data.get("boost", timing_boost)
                confidence = timing_data.get("confidence", confidence)
                rationale = timing_data.get("rationale", rationale)
            else:
                # Parse from text content
                timing_info = self._extract_timing_from_text(content)
                if timing_info:
                    timing = timing_info.get("timing", timing)
                    duration = timing_info.get("duration", duration)
                    timing_boost = timing_info.get("timing_boost", timing_boost)
                    confidence = timing_info.get("confidence", confidence)
                    rationale = timing_info.get("rationale", rationale)
            
            # Apply context-based adjustments
            trip_phase = timing_analysis["trip_phase"]
            driver_workload = timing_analysis["driver_workload"]
            urgency = timing_analysis["urgency_level"]
            
            # Override based on critical conditions
            if urgency == "critical":
                timing = "immediate"
                duration = 60
                timing_boost = max(timing_boost, 0.3)
                rationale = f"Critical urgency override: {rationale}"
            elif trip_phase == "parked" and driver_workload < 0.3:
                timing = "immediate"
                duration = min(duration, 300)
                timing_boost = max(timing_boost, 0.2)
            
            # Validate and constrain values
            timing_boost = max(0.0, min(1.0, timing_boost))
            confidence = max(0.0, min(1.0, confidence))
            duration = max(30, min(1800, duration))  # 30 seconds to 30 minutes
            
            return {
                "timing": timing,
                "duration": duration,
                "timing_boost": timing_boost,
                "confidence": confidence,
                "rationale": rationale,
            }
            
        except Exception as e:
            logger.error(f"Failed to parse timing response: {e}")
            return self._generate_fallback_timing(timing_analysis)

        trip_phase = timing_analysis["trip_phase"]
        driver_workload = timing_analysis["driver_workload"]
        urgency = timing_analysis["urgency_level"]

        if urgency == "critical":
            timing = "immediate"
            duration = 60
            timing_boost = 0.3
        elif trip_phase == "parked" and driver_workload < 0.3:
            timing = "immediate"
            duration = 300
            timing_boost = 0.2
        elif trip_phase == "post_trip":
            timing = "deferred"
            duration = 600
            timing_boost = 0.15
        else:
            timing = "post_trip"
            duration = 600
            timing_boost = 0.1

        return {
            "timing": timing,
            "duration": duration,
            "timing_boost": timing_boost,
            "confidence": 0.8,
            "rationale": f"Optimal timing based on {trip_phase} phase and {urgency} urgency",
        }

    def _generate_fallback_timing(
        self, timing_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate fallback timing recommendation"""
        return {
            "timing": "post_trip",
            "duration": 600,
            "timing_boost": 0.05,
            "confidence": 0.5,
            "rationale": "Fallback timing recommendation",
        }


class ChannelAgent:
    """Agent responsible for selecting optimal communication channels"""

    def __init__(self, ltc_logger: LTCLogger):
        self.ltc_logger = ltc_logger
        self.channel_history: List[Dict[str, Any]] = []
        self.channel_performance: Dict[str, float] = {}

    def propose_action(self, context: ContextVector) -> Optional[ActionProposal]:
        """Generate channel recommendations for actions"""
        logger.info(f"Generating channel recommendations for user {context.user_id}")

        try:
            # Analyze context for channel selection
            channel_analysis = self._analyze_channel_context(context)

            # Generate channel recommendation using qdLLM (simplified for testing)
            channel_recommendation = self._generate_channel_recommendation_sync(
                channel_analysis
            )

            if not channel_recommendation:
                return None

            # Create action proposal
            proposal = ActionProposal(
                agent_id="channel_agent_v1",
                agent_type=AgentType.CHANNEL,
                action_id=f"channel_{int(time.time() * 1000)}",
                payload=channel_recommendation,
                estimated_reward=channel_recommendation.get("conversion_boost", 0.0),
                confidence=channel_recommendation.get("confidence", 0.5),
                required_resources={"channel_availability": "check"},
                safety_impact="low",
                compliance_status="compliant",
                rationale=channel_recommendation.get(
                    "rationale", "Optimal channel based on context analysis"
                ),
            )

            return proposal

        except Exception as e:
            logger.error(f"Channel recommendation failed: {e}")
            return None

    def _analyze_channel_context(self, context: ContextVector) -> Dict[str, Any]:
        """Analyze context for channel selection"""
        analysis = {
            "driver_workload": self._estimate_driver_workload(context),
            "vehicle_speed": context.telemetry.get("speed", 0),
            "hmi_availability": self._check_hmi_availability(context),
            "user_preferences": context.business_context.get("channel_preferences", {}),
            "historical_performance": self._get_channel_performance(context.user_id),
        }

        return analysis

    def _estimate_driver_workload(self, context: ContextVector) -> float:
        """Estimate current driver workload (0.0 to 1.0)"""
        # Similar to TimingAgent implementation
        telemetry = context.telemetry

        speed_factor = min(telemetry.get("speed", 0) / 120.0, 1.0)
        accel_factor = abs(telemetry.get("acceleration", 0)) / 10.0
        steering_factor = abs(telemetry.get("steering_angle", 0)) / 45.0

        workload = (speed_factor + accel_factor + steering_factor) / 3.0
        return min(workload, 1.0)

    def _check_hmi_availability(self, context: ContextVector) -> Dict[str, bool]:
        """Check availability of different HMI surfaces"""
        telemetry = context.telemetry
        business_context = context.business_context

        return {
            "voice": True,  # Always available
            "visual": telemetry.get("speed", 0) < 80,  # Limited at high speeds
            "touch": telemetry.get("speed", 0) < 60,  # Limited at moderate+ speeds
            "gesture": telemetry.get("speed", 0) < 40,  # Limited at higher speeds
        }

    def _get_channel_performance(self, user_id: str) -> Dict[str, float]:
        """Get historical channel performance for user"""
        try:
            # Simulate performance data retrieval from analytics database
            # In production, this would query historical conversion rates by channel
            
            # Base performance metrics (industry averages)
            base_performance = {
                "hmi_voice": 0.65,
                "hmi_card": 0.55,
                "push_notification": 0.35,
                "email": 0.25,
                "sms": 0.15,
            }
            
            # Simulate user-specific performance variations
            import hashlib
            user_hash = int(hashlib.md5(user_id.encode()).hexdigest()[:8], 16)
            
            # Generate consistent but varied performance for each user
            user_performance = {}
            for channel, base_rate in base_performance.items():
                # Add user-specific variation (-0.2 to +0.3)
                variation = ((user_hash % 100) / 100.0 - 0.5) * 0.5
                user_rate = max(0.05, min(0.95, base_rate + variation))
                user_performance[channel] = round(user_rate, 3)
            
            # Simulate recent performance trends
            recent_interactions = self._get_recent_channel_interactions(user_id)
            for interaction in recent_interactions:
                channel = interaction.get("channel")
                success = interaction.get("converted", False)
                
                if channel in user_performance:
                    # Adjust performance based on recent interactions
                    if success:
                        user_performance[channel] = min(0.95, user_performance[channel] + 0.05)
                    else:
                        user_performance[channel] = max(0.05, user_performance[channel] - 0.02)
            
            logger.info(f"Retrieved channel performance for user {user_id}: {user_performance}")
            return user_performance
            
        except Exception as e:
            logger.error(f"Failed to retrieve channel performance for user {user_id}: {e}")
            return {
                "hmi_voice": 0.7,
                "hmi_card": 0.6,
                "push_notification": 0.4,
                "email": 0.3,
                "sms": 0.2,
            }
    
    def _get_recent_channel_interactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get recent channel interaction history for performance calculation"""
        try:
            # Simulate recent channel interactions
            interactions = [
                {
                    "channel": "hmi_voice",
                    "timestamp": (datetime.now() - pd.Timedelta(days=2)).isoformat(),
                    "converted": True,
                    "offer_type": "charging_incentive"
                },
                {
                    "channel": "hmi_card",
                    "timestamp": (datetime.now() - pd.Timedelta(days=5)).isoformat(),
                    "converted": False,
                    "offer_type": "feature_on_demand"
                },
                {
                    "channel": "push_notification",
                    "timestamp": (datetime.now() - pd.Timedelta(days=1)).isoformat(),
                    "converted": True,
                    "offer_type": "maintenance"
                }
            ]
            
            # Filter to last 14 days
            cutoff_date = datetime.now() - pd.Timedelta(days=14)
            recent_interactions = [
                interaction for interaction in interactions
                if datetime.fromisoformat(interaction["timestamp"]) > cutoff_date
            ]
            
            return recent_interactions
            
        except Exception as e:
            logger.error(f"Failed to retrieve recent channel interactions: {e}")
            return []

    def _generate_channel_recommendation_sync(
        self, channel_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Generate channel recommendation using qdLLM"""
        prompt = f"""
        Generate optimal channel recommendations for connected vehicle communications:
        
        Channel Analysis: {json.dumps(channel_analysis, indent=2)}
        
        Provide recommendations for:
        1. Primary channel (HMI voice, HMI card, push, email, SMS)
        2. Fallback channels if primary unavailable
        3. Expected conversion rate improvement
        4. Safety considerations
        5. Rationale for channel choice
        """

        try:
            # For testing, skip qdLLM call and use fallback channel
            recommendation = self._generate_fallback_channel(channel_analysis)

            return recommendation

        except Exception as e:
            logger.error(f"Failed to generate channel recommendation: {e}")
            return self._generate_fallback_channel(channel_analysis)

    def _parse_channel_response(
        self, response: Dict[str, Any], channel_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse qdLLM response into channel recommendation"""
        try:
            # Parse qdLLM response content
            content = response.get("content", "")
            
            # Initialize default values
            primary_channel = "push_notification"
            fallback_channels = ["email"]
            conversion_boost = 0.05
            confidence = 0.5
            rationale = "Default channel recommendation"
            
            # Try to extract structured channel data from response
            if "channel" in response:
                channel_data = response["channel"]
                primary_channel = channel_data.get("primary", primary_channel)
                fallback_channels = channel_data.get("fallback", fallback_channels)
                conversion_boost = channel_data.get("boost", conversion_boost)
                confidence = channel_data.get("confidence", confidence)
                rationale = channel_data.get("rationale", rationale)
            else:
                # Parse from text content
                channel_info = self._extract_channel_from_text(content)
                if channel_info:
                    primary_channel = channel_info.get("primary_channel", primary_channel)
                    fallback_channels = channel_info.get("fallback_channels", fallback_channels)
                    conversion_boost = channel_info.get("conversion_boost", conversion_boost)
                    confidence = channel_info.get("confidence", confidence)
                    rationale = channel_info.get("rationale", rationale)
            
            # Apply context-based adjustments
            driver_workload = channel_analysis["driver_workload"]
            vehicle_speed = channel_analysis["vehicle_speed"]
            hmi_availability = channel_analysis["hmi_availability"]
            
            # Override based on safety and availability
            if driver_workload > 0.7 or vehicle_speed > 80:
                # High workload or speed - use non-visual channels
                if primary_channel in ["hmi_card", "touch", "gesture"]:
                    primary_channel = "hmi_voice"
                    rationale = f"Safety override due to high workload/speed: {rationale}"
            elif not hmi_availability.get(primary_channel.split('_')[-1], True):
                # Channel not available - use fallback
                available_channels = [ch for ch, avail in hmi_availability.items() if avail]
                if available_channels:
                    primary_channel = f"hmi_{available_channels[0]}"
                    rationale = f"Availability override: {rationale}"
            
            # Validate and constrain values
            conversion_boost = max(0.0, min(1.0, conversion_boost))
            confidence = max(0.0, min(1.0, confidence))
            
            # Ensure fallback channels are valid
            valid_channels = ["hmi_voice", "hmi_card", "push_notification", "email", "sms"]
            fallback_channels = [ch for ch in fallback_channels if ch in valid_channels]
            if not fallback_channels:
                fallback_channels = ["email", "sms"]
            
            return {
                "primary_channel": primary_channel,
                "fallback_channels": fallback_channels,
                "conversion_boost": conversion_boost,
                "confidence": confidence,
                "rationale": rationale,
            }
            
        except Exception as e:
            logger.error(f"Failed to parse channel response: {e}")
            return self._generate_fallback_channel(channel_analysis)

        driver_workload = channel_analysis["driver_workload"]
        vehicle_speed = channel_analysis["vehicle_speed"]
        hmi_availability = channel_analysis["hmi_availability"]

        if driver_workload < 0.3 and vehicle_speed < 40:
            primary_channel = "hmi_card"
            conversion_boost = 0.2
        elif driver_workload < 0.5 and vehicle_speed < 80:
            primary_channel = "hmi_voice"
            conversion_boost = 0.15
        else:
            primary_channel = "push_notification"
            conversion_boost = 0.05

        return {
            "primary_channel": primary_channel,
            "fallback_channels": ["email", "sms"],
            "conversion_boost": conversion_boost,
            "confidence": 0.8,
            "rationale": f"Channel selected based on workload ({driver_workload:.2f}) and speed ({vehicle_speed})",
        }

    def _generate_fallback_channel(
        self, channel_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate fallback channel recommendation"""
        return {
            "primary_channel": "push_notification",
            "fallback_channels": ["email"],
            "conversion_boost": 0.02,
            "confidence": 0.5,
            "rationale": "Fallback channel recommendation",
        }


class RiskAgent:
    """Agent responsible for risk assessment and fraud detection"""

    def __init__(self, ltc_logger: LTCLogger):
        self.ltc_logger = ltc_logger
        self.risk_history: List[Dict[str, Any]] = []
        self.risk_thresholds: Dict[str, float] = {}

    def propose_action(self, context: ContextVector) -> Optional[ActionProposal]:
        """Generate risk assessment and recommendations"""
        logger.info(f"Generating risk assessment for user {context.user_id}")

        try:
            # Analyze risk context
            risk_analysis = self._analyze_risk_context(context)

            # Generate risk recommendation using qdLLM (simplified for testing)
            risk_recommendation = self._generate_risk_recommendation_sync(risk_analysis)

            if not risk_recommendation:
                return None

            # Create action proposal
            proposal = ActionProposal(
                agent_id="risk_agent_v1",
                agent_type=AgentType.RISK,
                action_id=f"risk_{int(time.time() * 1000)}",
                payload=risk_recommendation,
                estimated_reward=risk_recommendation.get("risk_reduction", 0.0),
                confidence=risk_recommendation.get("confidence", 0.5),
                required_resources={"risk_engine": "available"},
                safety_impact="medium",
                compliance_status="compliant",
                rationale=risk_recommendation.get(
                    "rationale", "Risk assessment and mitigation"
                ),
            )

            return proposal

        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return None

    def _analyze_risk_context(self, context: ContextVector) -> Dict[str, Any]:
        """Analyze context for risk assessment"""
        analysis = {
            "user_risk_profile": self._assess_user_risk(context),
            "transaction_risk": self._assess_transaction_risk(context),
            "fraud_indicators": self._detect_fraud_indicators(context),
            "compliance_risks": self._assess_compliance_risks(context),
            "safety_risks": self._assess_safety_risks(context),
        }

        return analysis

    def _assess_user_risk(self, context: ContextVector) -> Dict[str, Any]:
        """Assess user's risk profile"""
        business_context = context.business_context

        return {
            "risk_score": business_context.get("risk_score", 0.5),
            "credit_score": business_context.get("credit_score", 700),
            "payment_history": business_context.get("payment_history", "good"),
            "account_age": business_context.get("account_age_days", 365),
        }

    def _assess_transaction_risk(self, context: ContextVector) -> Dict[str, Any]:
        """Assess risk of current transaction"""
        business_context = context.business_context
        telemetry = context.telemetry

        return {
            "amount": business_context.get("transaction_amount", 0.0),
            "location": telemetry.get("location", "unknown"),
            "time_of_day": datetime.now().hour,
            "device_consistency": business_context.get("device_consistency", True),
        }

    def _detect_fraud_indicators(self, context: ContextVector) -> List[str]:
        """Detect potential fraud indicators"""
        indicators = []
        business_context = context.business_context
        telemetry = context.telemetry

        # Check for suspicious patterns
        if business_context.get("multiple_devices", False):
            indicators.append("multiple_devices")

        if telemetry.get("location", "unknown") == "unknown":
            indicators.append("location_unknown")

        if business_context.get("unusual_activity", False):
            indicators.append("unusual_activity")

        return indicators

    def _assess_compliance_risks(self, context: ContextVector) -> List[str]:
        """Assess compliance-related risks"""
        risks = []
        business_context = context.business_context

        # Check for compliance issues
        if not business_context.get("gdpr_consent", False):
            risks.append("gdpr_consent_missing")

        if not business_context.get("age_verification", False):
            risks.append("age_verification_missing")

        return risks

    def _assess_safety_risks(self, context: ContextVector) -> List[str]:
        """Assess safety-related risks"""
        risks = []
        telemetry = context.telemetry

        # Check for safety issues
        if telemetry.get("battery_level", 100) < 10:
            risks.append("critical_battery")

        if telemetry.get("maintenance_overdue", False):
            risks.append("maintenance_overdue")

        return risks

    def _generate_risk_recommendation_sync(
        self, risk_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Generate risk recommendation using qdLLM (simplified for testing)"""
        try:
            # For testing, skip qdLLM call and use fallback risk
            recommendation = self._generate_fallback_risk(risk_analysis)

            return recommendation

        except Exception as e:
            logger.error(f"Failed to generate risk recommendation: {e}")
            return self._generate_fallback_risk(risk_analysis)

    async def _generate_risk_recommendation(
        self, risk_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Generate risk recommendation using qdLLM"""
        prompt = f"""
        Generate risk assessment and mitigation recommendations:
        
        Risk Analysis: {json.dumps(risk_analysis, indent=2)}
        
        Provide recommendations for:
        1. Overall risk level (low, medium, high, critical)
        2. Specific risk factors to address
        3. Mitigation strategies
        4. Expected risk reduction
        5. Compliance requirements
        """

        try:
            response = await qdllm.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=512,
                use_quantum_enhancement=True,
            )

            # Parse response into risk recommendation
            recommendation = self._parse_risk_response(response, risk_analysis)

            return recommendation

        except Exception as e:
            logger.error(f"Failed to generate risk recommendation: {e}")
            return self._generate_fallback_risk(risk_analysis)

    def _parse_risk_response(
        self, response: Dict[str, Any], risk_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse qdLLM response into risk recommendation"""
        try:
            # Parse qdLLM response content
            content = response.get("content", "")
            
            # Initialize default values
            risk_level = "medium"
            risk_score = 0.5
            risk_factors = []
            mitigation_strategies = ["standard_verification"]
            risk_reduction = 0.1
            confidence = 0.5
            rationale = "Default risk assessment"
            
            # Try to extract structured risk data from response
            if "risk" in response:
                risk_data = response["risk"]
                risk_level = risk_data.get("level", risk_level)
                risk_score = risk_data.get("score", risk_score)
                risk_factors = risk_data.get("factors", risk_factors)
                mitigation_strategies = risk_data.get("mitigation", mitigation_strategies)
                risk_reduction = risk_data.get("reduction", risk_reduction)
                confidence = risk_data.get("confidence", confidence)
                rationale = risk_data.get("rationale", rationale)
            else:
                # Parse from text content
                risk_info = self._extract_risk_from_text(content)
                if risk_info:
                    risk_level = risk_info.get("risk_level", risk_level)
                    risk_score = risk_info.get("risk_score", risk_score)
                    risk_factors = risk_info.get("risk_factors", risk_factors)
                    mitigation_strategies = risk_info.get("mitigation_strategies", mitigation_strategies)
                    risk_reduction = risk_info.get("risk_reduction", risk_reduction)
                    confidence = risk_info.get("confidence", confidence)
                    rationale = risk_info.get("rationale", rationale)
            
            # Apply context-based adjustments
            user_risk = risk_analysis["user_risk_profile"]["risk_score"]
            fraud_indicators = len(risk_analysis["fraud_indicators"])
            compliance_risks = len(risk_analysis["compliance_risks"])
            safety_risks = len(risk_analysis["safety_risks"])
            
            # Calculate comprehensive risk score
            calculated_risk = (
                user_risk
                + fraud_indicators * 0.2
                + compliance_risks * 0.3
                + safety_risks * 0.4
            )
            
            # Override risk level based on calculated score
            if calculated_risk > 0.8:
                risk_level = "critical"
                risk_reduction = max(risk_reduction, 0.4)
            elif calculated_risk > 0.6:
                risk_level = "high"
                risk_reduction = max(risk_reduction, 0.3)
            elif calculated_risk > 0.4:
                risk_level = "medium"
                risk_reduction = max(risk_reduction, 0.2)
            else:
                risk_level = "low"
                risk_reduction = max(risk_reduction, 0.1)
            
            # Use calculated risk score if higher than parsed
            risk_score = max(risk_score, calculated_risk)
            
            # Combine risk factors from analysis
            all_risk_factors = list(set(
                risk_factors +
                risk_analysis["fraud_indicators"] +
                risk_analysis["compliance_risks"] +
                risk_analysis["safety_risks"]
            ))
            
            # Validate and constrain values
            risk_score = max(0.0, min(1.0, risk_score))
            risk_reduction = max(0.0, min(1.0, risk_reduction))
            confidence = max(0.0, min(1.0, confidence))
            
            # Ensure valid risk level
            valid_levels = ["low", "medium", "high", "critical"]
            if risk_level not in valid_levels:
                risk_level = "medium"
            
            return {
                "risk_level": risk_level,
                "risk_score": risk_score,
                "risk_factors": all_risk_factors,
                "mitigation_strategies": mitigation_strategies,
                "risk_reduction": risk_reduction,
                "confidence": confidence,
                "rationale": f"Risk assessment: {len(fraud_indicators)} fraud indicators, {len(compliance_risks)} compliance risks, {len(safety_risks)} safety risks. {rationale}",
            }
            
        except Exception as e:
            logger.error(f"Failed to parse risk response: {e}")
            return self._generate_fallback_risk(risk_analysis)

        # Calculate overall risk score
        user_risk = risk_analysis["user_risk_profile"]["risk_score"]
        fraud_indicators = len(risk_analysis["fraud_indicators"])
        compliance_risks = len(risk_analysis["compliance_risks"])
        safety_risks = len(risk_analysis["safety_risks"])

        total_risk = (
            user_risk
            + fraud_indicators * 0.2
            + compliance_risks * 0.3
            + safety_risks * 0.4
        )

        if total_risk > 0.8:
            risk_level = "critical"
            risk_reduction = 0.4
        elif total_risk > 0.6:
            risk_level = "high"
            risk_reduction = 0.3
        elif total_risk > 0.4:
            risk_level = "medium"
            risk_reduction = 0.2
        else:
            risk_level = "low"
            risk_reduction = 0.1

        return {
            "risk_level": risk_level,
            "risk_score": total_risk,
            "risk_factors": risk_analysis["fraud_indicators"]
            + risk_analysis["compliance_risks"]
            + risk_analysis["safety_risks"],
            "mitigation_strategies": [
                "enhanced_verification",
                "fraud_monitoring",
                "compliance_checks",
            ],
            "risk_reduction": risk_reduction,
            "confidence": 0.8,
            "rationale": f"Risk assessment based on {len(risk_analysis['fraud_indicators'])} fraud indicators, {len(risk_analysis['compliance_risks'])} compliance risks, {len(risk_analysis['safety_risks'])} safety risks",
        }

    def _generate_fallback_risk(self, risk_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback risk recommendation"""
        return {
            "risk_level": "medium",
            "risk_score": 0.5,
            "risk_factors": ["fallback_assessment"],
            "mitigation_strategies": ["standard_verification"],
            "risk_reduction": 0.1,
            "confidence": 0.5,
            "rationale": "Fallback risk assessment",
        }
    
    def _extract_timing_from_text(self, text: str) -> Dict[str, Any]:
        """Extract timing information from text content"""
        timing_data = {}
        
        try:
            import re
            
            # Extract delay values
            delay_patterns = [
                r"delay[:\s]+([0-9.]+)\s*(?:seconds?|s)",
                r"wait[:\s]+([0-9.]+)\s*(?:seconds?|s)",
                r"([0-9.]+)\s*(?:second|s)\s*delay"
            ]
            
            for pattern in delay_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    timing_data["delay_seconds"] = float(match.group(1))
                    break
            
            # Extract confidence values
            confidence_patterns = [
                r"confidence[:\s]+([0-9.]+)",
                r"certainty[:\s]+([0-9.]+)",
                r"([0-9.]+)%\s*confident"
            ]
            
            for pattern in confidence_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    conf_val = float(match.group(1))
                    # Normalize to 0-1 range if it looks like a percentage
                    if conf_val > 1:
                        conf_val = conf_val / 100.0
                    timing_data["confidence"] = min(1.0, max(0.0, conf_val))
                    break
            
            # Extract urgency indicators
            if re.search(r"\b(urgent|critical|immediate|asap)\b", text, re.IGNORECASE):
                timing_data["urgency"] = "high"
            elif re.search(r"\b(normal|standard|regular)\b", text, re.IGNORECASE):
                timing_data["urgency"] = "medium"
            elif re.search(r"\b(low|defer|later|when convenient)\b", text, re.IGNORECASE):
                timing_data["urgency"] = "low"
            
            return timing_data
            
        except Exception as e:
            logger.error(f"Error extracting timing from text: {e}")
            return {}
    
    def _extract_channel_from_text(self, text: str) -> Dict[str, Any]:
        """Extract channel information from text content"""
        channel_data = {}
        
        try:
            import re
            
            # Extract channel recommendations
            channel_patterns = {
                "hmi_voice": r"\b(voice|audio|speak|announce|verbal)\b",
                "hmi_card": r"\b(display|screen|visual|card|show)\b",
                "push_notification": r"\b(notification|push|alert|popup)\b",
                "email": r"\b(email|mail|message)\b",
                "sms": r"\b(sms|text|message)\b"
            }
            
            channel_scores = {}
            for channel, pattern in channel_patterns.items():
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                if matches > 0:
                    channel_scores[channel] = matches
            
            if channel_scores:
                # Recommend the most mentioned channel
                best_channel = max(channel_scores, key=channel_scores.get)
                channel_data["recommended_channel"] = best_channel
            
            # Extract confidence values
            confidence_patterns = [
                r"confidence[:\s]+([0-9.]+)",
                r"certainty[:\s]+([0-9.]+)",
                r"([0-9.]+)%\s*confident"
            ]
            
            for pattern in confidence_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    conf_val = float(match.group(1))
                    # Normalize to 0-1 range if it looks like a percentage
                    if conf_val > 1:
                        conf_val = conf_val / 100.0
                    channel_data["confidence"] = min(1.0, max(0.0, conf_val))
                    break
            
            # Extract priority indicators
            if re.search(r"\b(high priority|urgent|critical)\b", text, re.IGNORECASE):
                channel_data["priority"] = "high"
            elif re.search(r"\b(medium priority|normal|standard)\b", text, re.IGNORECASE):
                channel_data["priority"] = "medium"
            elif re.search(r"\b(low priority|defer|background)\b", text, re.IGNORECASE):
                channel_data["priority"] = "low"
            
            return channel_data
            
        except Exception as e:
            logger.error(f"Error extracting channel from text: {e}")
            return {}
    
    def _extract_risk_from_text(self, text: str) -> Dict[str, Any]:
        """Extract risk information from text content"""
        risk_data = {}
        
        try:
            import re
            
            # Extract risk level
            risk_patterns = {
                "high": r"\b(high|critical|severe|dangerous|unsafe)\s*risk\b",
                "medium": r"\b(medium|moderate|normal|standard)\s*risk\b",
                "low": r"\b(low|minimal|safe|secure)\s*risk\b"
            }
            
            for level, pattern in risk_patterns.items():
                if re.search(pattern, text, re.IGNORECASE):
                    risk_data["risk_level"] = level
                    break
            
            # Extract confidence values
            confidence_patterns = [
                r"confidence[:\s]+([0-9.]+)",
                r"certainty[:\s]+([0-9.]+)",
                r"([0-9.]+)%\s*confident"
            ]
            
            for pattern in confidence_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    conf_val = float(match.group(1))
                    # Normalize to 0-1 range if it looks like a percentage
                    if conf_val > 1:
                        conf_val = conf_val / 100.0
                    risk_data["confidence"] = min(1.0, max(0.0, conf_val))
                    break
            
            # Extract risk factors
            risk_factors = []
            factor_patterns = [
                r"fraud[:\s]*([^.\n]+)",
                r"compliance[:\s]*([^.\n]+)",
                r"safety[:\s]*([^.\n]+)",
                r"security[:\s]*([^.\n]+)"
            ]
            
            for pattern in factor_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                risk_factors.extend([match.strip() for match in matches if match.strip()])
            
            if risk_factors:
                risk_data["risk_factors"] = risk_factors[:5]  # Limit to 5 factors
            
            # Extract recommendation
            if re.search(r"\b(approve|allow|proceed|safe)\b", text, re.IGNORECASE):
                risk_data["recommendation"] = "approve"
            elif re.search(r"\b(deny|block|reject|unsafe)\b", text, re.IGNORECASE):
                risk_data["recommendation"] = "deny"
            elif re.search(r"\b(review|investigate|manual|human)\b", text, re.IGNORECASE):
                risk_data["recommendation"] = "review"
            
            return risk_data
            
        except Exception as e:
            logger.error(f"Error extracting risk from text: {e}")
            return {}


# Agent factory for easy instantiation
class AgentFactory:
    """Factory for creating specialized agents"""

    @staticmethod
    def create_agent(agent_type: AgentType, ltc_logger: LTCLogger):
        """Create agent instance based on type"""
        if agent_type == AgentType.OFFER:
            return OfferAgent(ltc_logger)
        elif agent_type == AgentType.TIMING:
            return TimingAgent(ltc_logger)
        elif agent_type == AgentType.CHANNEL:
            return ChannelAgent(ltc_logger)
        elif agent_type == AgentType.RISK:
            return RiskAgent(ltc_logger)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
