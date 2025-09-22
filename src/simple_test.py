#!/usr/bin/env python3
"""Simple test for quantum modules"""

print("🚀 Starting simple quantum test...")

try:
    print("📦 Importing quantum modules...")
    import quantum.reasoning
    print("✅ Reasoning module imported")
    
    import quantum.optimization  
    print("✅ Optimization module imported")
    
    # Test reasoning engine
    from quantum.reasoning import reasoning_engine
    stats = reasoning_engine.get_performance_stats()
    print(f"📊 Reasoning engine stats: {stats}")
    
    # Test optimization engine
    from quantum.optimization import qaoa_engine
    stats = qaoa_engine.get_performance_stats()
    print(f"📊 QAOA engine stats: {stats}")
    
    print("🎉 All quantum modules working correctly!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()