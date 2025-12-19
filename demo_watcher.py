"""Demo script for file watcher functionality."""
import time
import os
from pathlib import Path

def demo_file_watcher():
    """
    Demo: File Watcher
    
    This script demonstrates the file watcher functionality.
    
    Instructions:
    1. Run this script in one terminal
    2. In another terminal, run: .\fast-search.bat watch "d:\fast-search\test_dir"
    3. Watch as files are created, modified, and deleted
    4. The watcher will detect changes in real-time!
    """
    
    print("=" * 60)
    print("FILE WATCHER DEMO")
    print("=" * 60)
    
    # Create test directory
    test_dir = Path("d:/fast-search/test_dir")
    test_dir.mkdir(exist_ok=True)
    
    print(f"\n✓ Created test directory: {test_dir}")
    print(f"\nNow run in another terminal:")
    print(f"  .\\fast-search.bat watch \"{test_dir}\"")
    print(f"\nPress Enter when watcher is running...")
    input()
    
    print("\n" + "=" * 60)
    print("Starting file operations...")
    print("=" * 60)
    
    # Test 1: Create files
    print("\n1. Creating test files...")
    for i in range(3):
        file_path = test_dir / f"test_file_{i}.txt"
        file_path.write_text(f"Test content {i}")
        print(f"   Created: {file_path.name}")
        time.sleep(1)
    
    time.sleep(2)
    
    # Test 2: Modify files
    print("\n2. Modifying files...")
    for i in range(3):
        file_path = test_dir / f"test_file_{i}.txt"
        file_path.write_text(f"Modified content {i}")
        print(f"   Modified: {file_path.name}")
        time.sleep(1)
    
    time.sleep(2)
    
    # Test 3: Rename file
    print("\n3. Renaming file...")
    old_path = test_dir / "test_file_0.txt"
    new_path = test_dir / "renamed_file.txt"
    old_path.rename(new_path)
    print(f"   Renamed: test_file_0.txt -> renamed_file.txt")
    time.sleep(2)
    
    # Test 4: Delete files
    print("\n4. Deleting files...")
    for file in test_dir.glob("*.txt"):
        file.unlink()
        print(f"   Deleted: {file.name}")
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("✓ Demo complete!")
    print("=" * 60)
    print("\nCheck the watcher terminal - you should see all events logged!")
    print("Press Ctrl+C in the watcher terminal to stop.")
    
    # Cleanup
    test_dir.rmdir()
    print(f"\n✓ Cleaned up test directory")


if __name__ == '__main__':
    demo_file_watcher()
