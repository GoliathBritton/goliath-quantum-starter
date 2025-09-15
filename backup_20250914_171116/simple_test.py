#!/usr/bin/env python3
"""
Simple test for Quantum AI Division components
"""

import sys
import os
sys.path.append('src')

try:
    from agents.lead_ingestion_engine import LeadData, LeadStorage
    print("✅ LeadData and LeadStorage imported successfully")
    
    # Test storage
    storage = LeadStorage()
    test_lead = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'company': 'Test Corp'
    }
    
    storage.add_lead(test_lead)
    print(f"✅ Lead added to storage. Total leads: {storage.get_lead_count()}")
    
    # Test LeadData
    lead_data = LeadData(
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        company="Demo Inc"
    )
    print(f"✅ LeadData created: {lead_data.first_name} {lead_data.last_name}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n🎉 Basic component test completed!")