#!/usr/bin/env python3
"""Quick test for video processing."""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

print("Starting video processing test...")

try:
    from video_processing import VideoProcessor
    print("✅ Video processing module imported successfully")
    
    # Initialize processor
    processor = VideoProcessor()
    print("✅ Video processor initialized")
    
    # Test video ID extraction
    test_url = "https://www.youtube.com/watch?v=0S1EiFxhyO4"
    video_id = processor.extractor.extract_video_id(test_url)
    print(f"✅ Video ID extracted: {video_id}")
    
    # Test basic processing
    result = processor.process_video_url(test_url)
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"✅ Video processed successfully")
        print(f"   Video ID: {result['metadata']['video_id']}")
        print(f"   Title: {result['metadata'].get('title', 'N/A')}")
        print(f"   Quantum relevance: {result['analysis']['quantum_relevance_score']:.2f}")
    
    print("\n🎯 Video processing test completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()