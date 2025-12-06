"""
Post-build script to generate file hash and update documentation
Run this after building the .exe
"""
import os
import hashlib

def get_file_hash(filepath):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read file in chunks for memory efficiency
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_file_size(filepath):
    """Get file size in MB"""
    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb

if __name__ == "__main__":
    exe_path = "dist/LeagueWinPredictor.exe"
    
    if not os.path.exists(exe_path):
        print("Error: LeagueWinPredictor.exe not found in dist/ folder")
        print("Please run 'python build_exe.py' first")
        exit(1)
    
    print("=" * 80)
    print("Post-Build Information")
    print("=" * 80)
    print()
    
    # Calculate hash
    print("⏳ Calculating SHA256 hash...")
    file_hash = get_file_hash(exe_path)
    
    # Get size
    file_size = get_file_size(exe_path)
    
    print("✅ Done!\n")
    print("=" * 80)
    print("DISTRIBUTION INFORMATION")
    print("=" * 80)
    print(f"\nFile: {exe_path}")
    print(f"Size: {file_size:.2f} MB")
    print(f"SHA256: {file_hash}")
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("1. UPDATE DOWNLOAD_INSTRUCTIONS.md:")
    print(f"   Replace [PASTE HASH HERE] with:")
    print(f"   {file_hash}")
    print()
    print("2. TEST THE EXECUTABLE:")
    print(f"   dist\\LeagueWinPredictor.exe")
    print()
    print("3. SUBMIT TO WINDOWS DEFENDER (recommended):")
    print("   https://www.microsoft.com/wdsi/filesubmission")
    print()
    print("4. SCAN WITH VIRUSTOTAL (optional):")
    print("   https://www.virustotal.com/")
    print()
    print("5. CREATE GITHUB RELEASE:")
    print("   - Tag: v1.0.0")
    print(f"   - Upload: {exe_path}")
    print(f"   - Size: {file_size:.2f} MB")
    print(f"   - Hash: {file_hash}")
    print()
    print("=" * 80)
    
    # Save to file for easy reference (append mode to keep history)
    from datetime import datetime
    
    # Check if file exists to determine if we need a separator
    file_exists = os.path.exists("build_info.txt")
    
    with open("build_info.txt", "a") as f:
        # Add separator if file already has content
        if file_exists:
            f.write("\n" + "=" * 80 + "\n\n")
        
        f.write(f"Build Information\n")
        f.write(f"=================\n\n")
        f.write(f"Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"File: {exe_path}\n")
        f.write(f"Size: {file_size:.2f} MB\n")
        f.write(f"SHA256: {file_hash}\n")
        f.write(f"File Created: {datetime.fromtimestamp(os.path.getctime(exe_path)).strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("Build info saved to: build_info.txt")
    print()
