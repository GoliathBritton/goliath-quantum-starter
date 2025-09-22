"""Simple test to verify video processing system components."""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all components can be imported."""
    print("Testing imports...")
    
    try:
        from video_processing.video_processor import VideoProcessor
        print("✓ VideoProcessor imported")
        
        from video_processing.content_analyzer import ContentAnalyzer
        print("✓ ContentAnalyzer imported")
        
        from video_processing.categorization import tag_manager, categorizer
        print("✓ Categorization system imported")
        
        from video_processing.database import VideoDatabase
        print("✓ Database system imported")
        
        from video_processing.models import VideoMetadata, VideoAnalysis
        print("✓ Database models imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_categorization():
    """Test categorization system."""
    print("\nTesting categorization...")
    
    try:
        from video_processing.categorization import tag_manager
        
        result = tag_manager.generate_comprehensive_tags(
            "Quantum Computing Basics",
            "Introduction to qubits and quantum gates",
            "Quantum Channel"
        )
        
        print(f"✓ Primary category: {result['primary_category']}")
        print(f"✓ Technical level: {result['technical_level']}")
        print(f"✓ Content type: {result['content_type']}")
        print(f"✓ Generated {len(result['tags'])} tags")
        
        return True
    except Exception as e:
        print(f"❌ Categorization failed: {e}")
        return False

def test_video_processor():
    """Test video processor initialization."""
    print("\nTesting video processor...")
    
    try:
        from video_processing.video_processor import VideoProcessor
        
        # Test without database
        processor = VideoProcessor(use_database=False)
        print("✓ VideoProcessor initialized (no database)")
        
        # Test video ID extraction
        test_url = "https://www.youtube.com/watch?v=JhHMJCUmq28"
        video_id = processor.extract_video_id(test_url)
        print(f"✓ Video ID extracted: {video_id}")
        
        return True
    except Exception as e:
        print(f"❌ Video processor failed: {e}")
        return False

def main():
    """Run simple tests."""
    print("=== Simple Video Processing System Test ===")
    
    tests = [
        ("Import Test", test_imports),
        ("Categorization Test", test_categorization),
        ("Video Processor Test", test_video_processor)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        success = test_func()
        results.append((test_name, success))
    
    print("\n=== Test Results ===")
    all_passed = True
    for test_name, success in results:
        status = "✓ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Video processing system is working.")
    else:
        print("\n❌ Some tests failed.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    print(f"\nTest completed with {'success' if success else 'failures'}.")