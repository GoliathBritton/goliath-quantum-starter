"""
NQBA Business Units API Router

Provides REST API endpoints for all business units in the NQBA ecosystem.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import logging
from pydantic import BaseModel, Field

from ..business_integration import business_unit_manager, BusinessUnitType

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models for request/response validation


class EnergyOptimizationRequest(BaseModel):
    customer_type: str = Field(
        ..., description="Type of customer (residential, commercial, industrial)"
    )
    current_consumption: float = Field(
        ..., description="Current energy consumption in kW"
    )
    optimization_level: str = Field(
        default="standard", description="Optimization level (standard, maximum)"
    )


class ConsumptionAnalysisRequest(BaseModel):
    customer_type: str = Field(..., description="Type of customer")
    time_period: str = Field(default="24h", description="Analysis time period")


class EnergyForecastRequest(BaseModel):
    forecast_hours: int = Field(default=24, description="Number of hours to forecast")
    customer_type: str = Field(..., description="Type of customer")


class EnergyMixRequest(BaseModel):
    total_demand: float = Field(..., description="Total energy demand in kW")
    available_sources: List[str] = Field(
        default=[], description="Available energy sources"
    )


class CarbonFootprintRequest(BaseModel):
    energy_consumption: float = Field(..., description="Energy consumption in kWh")
    energy_mix: Dict[str, float] = Field(
        ..., description="Energy source mix percentages"
    )


class GridLoadRequest(BaseModel):
    grid_load: float = Field(..., description="Current grid load in MW")
    available_capacity: float = Field(..., description="Available grid capacity in MW")
    renewable_generation: float = Field(..., description="Renewable generation in MW")


class BusinessUnitResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    quantum_advantage: Optional[float] = None
    timestamp: float


# FLYFOX AI API Endpoints


@router.get("/flyfox-ai", response_model=Dict[str, Any])
async def get_flyfox_ai_info():
    """Get FLYFOX AI business unit information"""
    try:
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )

        if not flyfox_units:
            raise HTTPException(
                status_code=404, detail="FLYFOX AI business unit not found"
            )

        flyfox_unit = flyfox_units[0]
        capabilities = await flyfox_unit.get_capabilities()

        return {
            "success": True,
            "business_unit": "FLYFOX AI",
            "capabilities": capabilities,
            "status": flyfox_unit.status.value,
            "endpoints": [
                "/api/v1/flyfox-ai/optimize-energy",
                "/api/v1/flyfox-ai/analyze-consumption",
                "/api/v1/flyfox-ai/forecast-demand",
                "/api/v1/flyfox-ai/optimize-mix",
                "/api/v1/flyfox-ai/carbon-footprint",
                "/api/v1/flyfox-ai/grid-balancing",
            ],
        }

    except Exception as e:
        logger.error(f"Error getting FLYFOX AI info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flyfox-ai/optimize-energy", response_model=BusinessUnitResponse)
async def optimize_energy_consumption(request: EnergyOptimizationRequest):
    """Optimize energy consumption patterns"""
    try:
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )

        if not flyfox_units:
            raise HTTPException(
                status_code=404, detail="FLYFOX AI business unit not found"
            )

        flyfox_unit = flyfox_units[0]

        # Execute energy optimization
        result = await flyfox_unit.execute_operation(
            "optimize_energy_consumption", request.dict()
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=400, detail=result.get("error", "Optimization failed")
            )

        return BusinessUnitResponse(
            success=True,
            message="Energy consumption optimized successfully",
            data=result,
            quantum_advantage=result.get("quantum_advantage"),
            timestamp=result.get("timestamp", 0),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in energy optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flyfox-ai/analyze-consumption", response_model=BusinessUnitResponse)
async def analyze_consumption_patterns(request: ConsumptionAnalysisRequest):
    """Analyze energy consumption patterns"""
    try:
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )

        if not flyfox_units:
            raise HTTPException(
                status_code=404, detail="FLYFOX AI business unit not found"
            )

        flyfox_unit = flyfox_units[0]

        # Execute consumption analysis
        result = await flyfox_unit.execute_operation(
            "analyze_consumption_patterns", request.dict()
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=400, detail=result.get("error", "Analysis failed")
            )

        return BusinessUnitResponse(
            success=True,
            message="Consumption patterns analyzed successfully",
            data=result,
            quantum_advantage=result.get("quantum_advantage"),
            timestamp=result.get("timestamp", 0),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in consumption analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flyfox-ai/forecast-demand", response_model=BusinessUnitResponse)
async def forecast_energy_demand(request: EnergyForecastRequest):
    """Forecast energy demand"""
    try:
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )

        if not flyfox_units:
            raise HTTPException(
                status_code=404, detail="FLYFOX AI business unit not found"
            )

        flyfox_unit = flyfox_units[0]

        # Execute demand forecasting
        result = await flyfox_unit.execute_operation(
            "forecast_energy_demand", request.dict()
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=400, detail=result.get("error", "Forecasting failed")
            )

        return BusinessUnitResponse(
            success=True,
            message="Energy demand forecasted successfully",
            data=result,
            quantum_advantage=result.get("quantum_advantage"),
            timestamp=result.get("timestamp", 0),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in demand forecasting: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flyfox-ai/optimize-mix", response_model=BusinessUnitResponse)
async def optimize_energy_mix(request: EnergyMixRequest):
    """Optimize energy source mix"""
    try:
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )

        if not flyfox_units:
            raise HTTPException(
                status_code=404, detail="FLYFOX AI business unit not found"
            )

        flyfox_unit = flyfox_units[0]

        # Execute energy mix optimization
        result = await flyfox_unit.execute_operation(
            "optimize_energy_mix", request.dict()
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=400, detail=result.get("error", "Mix optimization failed")
            )

        return BusinessUnitResponse(
            success=True,
            message="Energy mix optimized successfully",
            data=result,
            quantum_advantage=result.get("quantum_advantage"),
            timestamp=result.get("timestamp", 0),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in energy mix optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flyfox-ai/carbon-footprint", response_model=BusinessUnitResponse)
async def calculate_carbon_footprint(request: CarbonFootprintRequest):
    """Calculate carbon footprint"""
    try:
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )

        if not flyfox_units:
            raise HTTPException(
                status_code=404, detail="FLYFOX AI business unit not found"
            )

        flyfox_unit = flyfox_units[0]

        # Execute carbon footprint calculation
        result = await flyfox_unit.execute_operation(
            "calculate_carbon_footprint", request.dict()
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=400, detail=result.get("error", "Calculation failed")
            )

        return BusinessUnitResponse(
            success=True,
            message="Carbon footprint calculated successfully",
            data=result,
            quantum_advantage=result.get("quantum_advantage"),
            timestamp=result.get("timestamp", 0),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in carbon footprint calculation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flyfox-ai/grid-balancing", response_model=BusinessUnitResponse)
async def grid_load_balancing(request: GridLoadRequest):
    """Grid load balancing optimization"""
    try:
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )

        if not flyfox_units:
            raise HTTPException(
                status_code=404, detail="FLYFOX AI business unit not found"
            )

        flyfox_unit = flyfox_units[0]

        # Execute grid load balancing
        result = await flyfox_unit.execute_operation(
            "grid_load_balancing", request.dict()
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=400, detail=result.get("error", "Grid balancing failed")
            )

        return BusinessUnitResponse(
            success=True,
            message="Grid load balancing completed successfully",
            data=result,
            quantum_advantage=result.get("quantum_advantage"),
            timestamp=result.get("timestamp", 0),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in grid load balancing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flyfox-ai/insights", response_model=Dict[str, Any])
async def get_flyfox_ai_insights():
    """Get FLYFOX AI insights and analytics"""
    try:
        flyfox_units = await business_unit_manager.get_business_units_by_type(
            BusinessUnitType.FLYFOX_AI
        )

        if not flyfox_units:
            raise HTTPException(
                status_code=404, detail="FLYFOX AI business unit not found"
            )

        flyfox_unit = flyfox_units[0]
        insights = await flyfox_unit.get_energy_insights()

        return {
            "success": True,
            "business_unit": "FLYFOX AI",
            "insights": insights,
            "status": flyfox_unit.status.value,
        }

    except Exception as e:
        logger.error(f"Error getting FLYFOX AI insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Business Unit Management Endpoints


@router.get("/business-units", response_model=Dict[str, Any])
async def get_all_business_units():
    """Get all registered business units"""
    try:
        all_units = await business_unit_manager.get_all_business_units()

        business_units_info = []
        for unit in all_units:
            status_report = await unit.get_status_report()
            business_units_info.append(status_report)

        return {
            "success": True,
            "total_business_units": len(all_units),
            "business_units": business_units_info,
        }

    except Exception as e:
        logger.error(f"Error getting business units: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/business-units/{unit_id}", response_model=Dict[str, Any])
async def get_business_unit(unit_id: str):
    """Get specific business unit by ID"""
    try:
        unit = await business_unit_manager.get_business_unit(unit_id)

        if not unit:
            raise HTTPException(
                status_code=404, detail=f"Business unit {unit_id} not found"
            )

        status_report = await unit.get_status_report()

        return {"success": True, "business_unit": status_report}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting business unit {unit_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ecosystem/status", response_model=Dict[str, Any])
async def get_ecosystem_status():
    """Get overall ecosystem status"""
    try:
        ecosystem_status = await business_unit_manager.get_ecosystem_status()

        return {"success": True, "ecosystem_status": ecosystem_status}

    except Exception as e:
        logger.error(f"Error getting ecosystem status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ecosystem/cross-unit-operation", response_model=Dict[str, Any])
async def execute_cross_unit_operation(operation_type: str, parameters: Dict[str, Any]):
    """Execute operation involving multiple business units"""
    try:
        result = await business_unit_manager.execute_cross_unit_operation(
            operation_type, parameters
        )

        return {"success": True, "cross_unit_operation": result}

    except Exception as e:
        logger.error(f"Error in cross-unit operation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
