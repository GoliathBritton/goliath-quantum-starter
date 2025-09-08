#!/usr/bin/env python3
"""
API module for NQBA Quantum Computing Platform

This package contains the FastAPI endpoints and API-related components.
"""

from .recipe_endpoints import router as recipe_router

__all__ = ['recipe_router']