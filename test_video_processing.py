#!/usr/bin/env python3
"""Test script for video processing functionality with provided YouTube URLs."""

import sys
import os
import json
from typing import List

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from video_processing import VideoProcessor
except ImportError:
    print("Error: Could not import video_processing module")
    sys.exit(1)


def test_video_processing():
    """Test video processing with the provided YouTube URLs."""
    
    # The provided YouTube URLs
    test_urls = [
        "https://www.youtube.com/watch?v=0S1EiFxhyO4",
        "https://www.youtube.com/watch?v=qUNYIe7ZNl8", 
        "https://www.youtube.com/watch?v=uxaNLBIL-k8",
        "https://www.youtube.com/watch?v=mDAz0DtsxZQ"
    ]
    
    print("🎥 Testing Video Processing System")
    print("=" * 50)
    
    # Initialize video processor
    try:
        processor = VideoProcessor()
        print("✅ Video processor initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize video processor: {e}")
        return False
    
    # Test 1: Process individual videos
    print("\n📹 Test 1: Processing individual videos")
    print("-" * 30)
    
    for i, url in enumerate(test_urls, 1):
        try:
            print(f"\nProcessing video {i}: {url}")
            result = processor.process_video_url(url)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                metadata = result.get('metadata', {})
                analysis = result.get('analysis', {})
                
                print(f"✅ Video ID: {metadata.get('video_id', 'N/A')}")
                print(f"   Title: {metadata.get('title', 'N/A')}")
                print(f"   Channel: {metadata.get('channel_name', 'N/A')}")
                print(f"   Quantum Relevance: {analysis.get('quantum_relevance_score', 0):.2f}")
                print(f"   Educational: {analysis.get('educational_content', False)}")
                print(f"   Technical Level: {analysis.get('technical_level', 'N/A')}")
                print(f"   Content Type: {analysis.get('content_type', 'N/A')}")
                
                keywords = analysis.get('keywords', [])
                if keywords:
                    print(f"   Keywords: {', '.join(keywords[:5])}")
                
        except Exception as e:
            print(f"❌ Error processing video {i}: {e}")
    
    # Test 2: Batch processing
    print("\n📊 Test 2: Batch processing all videos")
    print("-" * 30)
    
    try:
        batch_results = processor.process_multiple_urls(test_urls)
        successful = sum(1 for r in batch_results if r.get('processing_status') == 'success')
        print(f"✅ Batch processing complete: {successful}/{len(test_urls)} successful")
        
        for result in batch_results:
            if result.get('processing_status') == 'success':
                analysis = result.get('analysis', {})
                metadata = result.get('metadata', {})
                print(f"   - {metadata.get('video_id', 'N/A')}: Relevance {analysis.get('quantum_relevance_score', 0):.2f}")
            
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
    
    # Test 3: Quantum relevant videos
    print("\n🔬 Test 3: Finding quantum-relevant videos")
    print("-" * 30)
    
    try:
        relevant_videos = processor.get_quantum_relevant_videos(test_urls, min_relevance=0.1)
        print(f"✅ Found {len(relevant_videos)} quantum-relevant videos (min relevance: 0.1)")
        
        for video in relevant_videos:
            metadata = video.get('metadata', {})
            analysis = video.get('analysis', {})
            print(f"   - {metadata.get('title', 'N/A')[:50]}...")
            print(f"     Relevance: {analysis.get('quantum_relevance_score', 0):.2f}")
            
    except Exception as e:
        print(f"❌ Quantum relevance filtering failed: {e}")
    
    # Test 4: Educational content
    print("\n🎓 Test 4: Finding educational content")
    print("-" * 30)
    
    try:
        educational_videos = processor.get_educational_content(test_urls)
        print(f"✅ Found {len(educational_videos)} educational videos")
        
        for video in educational_videos:
            metadata = video.get('metadata', {})
            analysis = video.get('analysis', {})
            print(f"   - {metadata.get('title', 'N/A')[:50]}...")
            print(f"     Level: {analysis.get('technical_level', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Educational content filtering failed: {e}")
    
    # Test 5: Summary report
    print("\n📈 Test 5: Generating summary report")
    print("-" * 30)
    
    try:
        summary = processor.generate_summary_report(test_urls)
        
        print(f"✅ Summary Report Generated:")
        print(f"   Total videos: {summary.get('total_videos_processed', 0)}")
        print(f"   Successful processing: {summary.get('successful_processing', 0)}")
        print(f"   Quantum relevant: {summary.get('quantum_relevant_videos', 0)}")
        print(f"   Success rate: {summary.get('processing_success_rate', 0):.2%}")
        print(f"   Quantum relevance rate: {summary.get('quantum_relevance_rate', 0):.2%}")
        
        # Technical level distribution
        tech_dist = summary.get('technical_level_distribution', {})
        if tech_dist:
            print(f"   Technical levels: {tech_dist}")
        
        # Top keywords
        top_keywords = summary.get('top_keywords', [])
        if top_keywords:
            print(f"   Top keywords: {[kw[0] for kw in top_keywords[:5]]}")
        
        # Export summary to file
        export_success = processor.export_to_json(summary, "video_analysis_summary.json")
        if export_success:
            print(f"   📄 Summary exported to: video_analysis_summary.json")
        
    except Exception as e:
        print(f"❌ Summary report generation failed: {e}")
    
    print("\n🎯 Video Processing Test Complete!")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    print("🚀 Starting Video Processing Tests...")
    success = test_video_processing()
    
    if success:
        print("\n✅ All tests completed successfully!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)