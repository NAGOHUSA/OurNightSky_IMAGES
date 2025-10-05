#!/usr/bin/env python3
"""
Auto-generate manifest.json for GitHub image gallery
Simply drop images into the images/ folder and run this script!
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

# ⚠️ CONFIGURE THESE SETTINGS
GITHUB_USERNAME = "NAGOHUSA"  # Replace with your GitHub username
REPO_NAME = "night-sky-images"     # Your repository name
IMAGES_FOLDER = "images"           # Folder containing your images

def get_file_creation_time(filepath):
    """Get the file creation time or use current time as fallback"""
    try:
        # Get file modification time
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    except:
        # Fallback to current time
        return datetime.now(timezone.utc)

def generate_manifest():
    """Generate manifest.json from all images in the images folder"""
    
    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    images = []
    images_path = Path(IMAGES_FOLDER)
    
    # Check if images folder exists
    if not images_path.exists():
        print(f"❌ Error: '{IMAGES_FOLDER}' folder not found!")
        print(f"💡 Please create the folder and add some images.")
        return False
    
    # Scan for image files
    print(f"🔍 Scanning {IMAGES_FOLDER}/ for images...")
    
    for file in sorted(images_path.iterdir()):
        if file.is_file() and file.suffix.lower() in image_extensions:
            # Get file creation/modification time
            file_time = get_file_creation_time(file)
            
            # Build the GitHub raw URL
            url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/main/{IMAGES_FOLDER}/{file.name}"
            
            image_entry = {
                "filename": file.name,
                "url": url,
                "uploadedAt": file_time.isoformat()
            }
            
            images.append(image_entry)
            print(f"  ✓ Found: {file.name}")
    
    if not images:
        print(f"❌ No images found in {IMAGES_FOLDER}/")
        print(f"💡 Add .jpg, .jpeg, or .png files to the {IMAGES_FOLDER}/ folder")
        return False
    
    # Create manifest structure
    manifest = {
        "images": sorted(images, key=lambda x: x['uploadedAt'], reverse=True),
        "lastUpdated": datetime.now(timezone.utc).isoformat()
    }
    
    # Write to manifest.json
    with open('manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ SUCCESS! Generated manifest.json with {len(images)} image(s)")
    print(f"📝 File saved: manifest.json")
    print(f"\n📋 Next steps:")
    print(f"  1. Review the manifest.json file")
    print(f"  2. Commit and push to GitHub:")
    print(f"     git add images/ manifest.json")
    print(f"     git commit -m 'Add new images'")
    print(f"     git push")
    print(f"  3. Your app will automatically load the new images!")
    
    return True

def show_current_manifest():
    """Display current manifest if it exists"""
    if os.path.exists('manifest.json'):
        print("\n📄 Current manifest.json:")
        with open('manifest.json', 'r') as f:
            manifest = json.load(f)
            print(f"  • Total images: {len(manifest.get('images', []))}")
            print(f"  • Last updated: {manifest.get('lastUpdated', 'Unknown')}")
            if manifest.get('images'):
                print(f"  • Latest image: {manifest['images'][0]['filename']}")

if __name__ == "__main__":
    print("=" * 60)
    print("🌌 Our Night Sky - Manifest Generator")
    print("=" * 60)
    
    # Check if username is configured
    if GITHUB_USERNAME == "YOUR_USERNAME":
        print("\n⚠️  WARNING: Please update GITHUB_USERNAME in this script!")
        print("   Open generate_manifest.py and change line 13")
        print("   From: GITHUB_USERNAME = 'YOUR_USERNAME'")
        print("   To:   GITHUB_USERNAME = 'your-actual-username'")
        print()
    
    # Show current manifest if exists
    show_current_manifest()
    
    print()
    
    # Generate new manifest
    success = generate_manifest()
    
    print("=" * 60)
    
    if not success:
        exit(1)
