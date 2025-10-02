"""
GitHub Pages Deployment Script
=============================
Prepares the Blancosy Financials dashboard for GitHub Pages deployment
"""

import os
import shutil
from pathlib import Path

def clean_for_deployment():
    """Clean up files not needed for GitHub Pages"""
    
    # Files to keep for GitHub Pages
    keep_files = {
        'index.html',           # Main dashboard
        'README.md',            # Documentation
        '.gitignore',           # Git configuration
        'requirements.txt',     # Python dependencies
        'generate_static_dashboard.py',  # Dashboard generator
        'official_data_processor.py',   # Data processor
        'deploy.py'             # This script
    }
    
    # Directories to keep
    keep_dirs = {
        'docs',                 # Documentation
        '.git'                  # Git repository (if exists)
    }
    
    print("🧹 Cleaning up files for GitHub Pages deployment...")
    
    current_dir = Path('.')
    removed_count = 0
    
    for item in current_dir.iterdir():
        if item.name.startswith('.') and item.name != '.gitignore':
            continue  # Skip hidden files except .gitignore
            
        if item.is_file():
            if item.name not in keep_files:
                try:
                    item.unlink()
                    print(f"   ❌ Removed: {item.name}")
                    removed_count += 1
                except Exception as e:
                    print(f"   ⚠️ Could not remove {item.name}: {e}")
        
        elif item.is_dir():
            if item.name not in keep_dirs and not item.name.startswith('.'):
                try:
                    shutil.rmtree(item)
                    print(f"   ❌ Removed directory: {item.name}")
                    removed_count += 1
                except Exception as e:
                    print(f"   ⚠️ Could not remove directory {item.name}: {e}")
    
    print(f"✅ Cleanup complete! Removed {removed_count} items")
    return removed_count

def verify_deployment_files():
    """Verify all required files are present"""
    
    required_files = [
        'index.html',
        'README.md',
        '.gitignore'
    ]
    
    print("\n🔍 Verifying deployment files...")
    
    all_present = True
    for file in required_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            print(f"   ❌ Missing: {file}")
            all_present = False
    
    # Check docs directory
    docs_dir = Path('docs')
    if docs_dir.exists():
        doc_files = list(docs_dir.glob('*.md'))
        print(f"   ✅ docs/ directory ({len(doc_files)} files)")
        for doc_file in doc_files:
            print(f"      📄 {doc_file.name}")
    else:
        print("   ⚠️ docs/ directory not found")
    
    return all_present

def show_deployment_instructions():
    """Show final deployment instructions"""
    
    print("\n" + "="*60)
    print("🚀 GITHUB PAGES DEPLOYMENT READY!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Create a new GitHub repository")
    print("2. Upload these files to your repository:")
    print("   • index.html (main dashboard)")
    print("   • README.md (documentation)")
    print("   • .gitignore (git configuration)")
    print("   • docs/ folder (additional documentation)")
    
    print("\n3. Enable GitHub Pages:")
    print("   • Go to repository Settings → Pages")
    print("   • Select 'Deploy from a branch'")
    print("   • Choose 'main' branch and '/ (root)' folder")
    
    print("\n4. Access your dashboard:")
    print("   • https://yourusername.github.io/repository-name/")
    
    print("\n🎯 Your dashboard features:")
    print("   ✅ Official 2024 P&L data (KES 3,389,075.35 net profit)")
    print("   ✅ Interactive charts and visualizations")
    print("   ✅ Responsive design (mobile-friendly)")
    print("   ✅ Professional business presentation")
    
    print("\n📖 For detailed instructions, see:")
    print("   • README.md - Overview and features")
    print("   • docs/deployment-guide.md - Step-by-step guide")
    print("   • docs/data-sources.md - Data documentation")
    
    print("\n" + "="*60)

def main():
    """Main deployment preparation function"""
    
    print("🏢 BLANCOSY FINANCIALS - GITHUB PAGES DEPLOYMENT")
    print("="*60)
    
    # Check if index.html exists
    if not Path('index.html').exists():
        print("❌ index.html not found!")
        print("💡 Run 'python generate_static_dashboard.py' first")
        return
    
    # Clean up unnecessary files
    removed = clean_for_deployment()
    
    # Verify required files
    if verify_deployment_files():
        show_deployment_instructions()
    else:
        print("\n❌ Some required files are missing!")
        print("💡 Please ensure all files are generated correctly")

if __name__ == "__main__":
    main()
