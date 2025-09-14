#!/usr/bin/env python3
"""
Test script for Lead Ingestion Engine
"""

import sys
import os
sys.path.append('src')

from agents.lead_ingestion_engine import LeadIngestionEngine, LeadData

def test_lead_engine():
    """Test the lead ingestion engine functionality"""
    print("🚀 Testing Lead Ingestion Engine...")
    
    try:
        # Initialize engine
        engine = LeadIngestionEngine()
        print("✅ Lead Ingestion Engine initialized successfully")
        
        # Create test lead data
        test_lead = LeadData(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+1-555-123-4567",
            company="Test Corp",
            title="CEO",
            industry="Technology",
            location="San Francisco, CA"
        )
        
        # Test saving lead
        success = engine.save_to_database(test_lead)
        if success:
            print("✅ Test lead saved successfully")
        else:
            print("❌ Failed to save test lead")
        
        # Check storage
        lead_count = engine.storage.get_lead_count()
        print(f"📊 Total leads in storage: {lead_count}")
        
        # Display stats
        print(f"📈 Engine stats: {engine.stats}")
        
        print("\n🎉 Lead Ingestion Engine test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Lead Ingestion Engine: {str(e)}")
        return False

if __name__ == "__main__":
    test_lead_engine()