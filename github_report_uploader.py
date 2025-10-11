#!/usr/bin/env python3
"""
Enhanced Training Interface with Auto-Upload

This enhanced version automatically uploads training reports to GitHub
and generates markdown reports for batch analysis.
"""

import json
import os
import shutil
import subprocess
import requests
from datetime import datetime
from pathlib import Path

class GitHubReportUploader:
    """Handle automatic upload of training reports to GitHub"""
    
    def __init__(self):
        """Initialize the GitHub uploader with configuration from environment variables and settings file."""
        from configuration_dialog import load_configuration
        
        # Load configuration using the new secure method
        self.config = load_configuration()
        
        # Get sensitive data from environment variables
        self.token = os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "")
        
        # Get repository settings from config file
        self.owner = self.config.get("github_owner", "")
        self.repo = self.config.get("github_repo", "")
        
        if not self.token:
            print("⚠️  GitHub token not found in RESEARCH_BUDDY_GITHUB_TOKEN environment variable")
        
        if not self.owner or not self.repo:
            print("⚠️  GitHub repository settings not configured. Please run configuration dialog.")
            
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Initialize reports directory in user's home directory (writable location)
        # This is critical for .app bundles which are read-only
        self.reports_dir = Path.home() / ".research_buddy" / "training_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def load_config(self):
        """Load configuration from user's config directory"""
        config_dir = Path.home() / ".research_buddy"
        config_file = config_dir / "interface_settings.json"
        default_config = {
            "github_owner": "OhioMathTeacher",
            "github_repo": "research-buddy", 
            "github_token": ""
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                print(f"Warning: Could not load configuration: {e}")
                
        return default_config
        
    def create_training_report(self, training_data, ga_name, session_id):
        """Create a markdown report from training data"""
        
        timestamp = datetime.now().isoformat()
        
        # Count judgments
        judgments = {}
        for entry in training_data:
            judgment = entry.get("judgment", "unknown")
            judgments[judgment] = judgments.get(judgment, 0) + 1
        
        # Extract evidence examples
        positive_examples = []
        for entry in training_data:
            if entry.get("judgment", "").startswith("positive") and entry.get("evidence"):
                positive_examples.append({
                    "filename": entry["filename"],
                    "evidence": entry["evidence"][:200] + ("..." if len(entry["evidence"]) > 200 else ""),
                    "patterns": entry.get("pattern_types", []),
                    "confidence": entry.get("confidence", 0)
                })
        
        # Generate markdown report
        report_content = f"# Training Session Report\n\n"
        report_content += f"## Session Information\n"
        report_content += f"- **GA Name**: {ga_name}\n"
        report_content += f"- **Session ID**: {session_id}\n"
        report_content += f"- **Timestamp**: {timestamp}\n"
        report_content += f"- **Papers Analyzed**: {len(training_data)}\n\n"
        report_content += f"## Summary Statistics\n\n"
        report_content += f"### Judgment Distribution\n"
        
        for judgment, count in judgments.items():
            percentage = (count / len(training_data)) * 100
            report_content += f"- **{judgment}**: {count} papers ({percentage:.1f}%)\n"
        
        report_content += f"\n### Pattern Analysis\n"
        report_content += f"- **Total Evidence Quotes**: {len(positive_examples)}\n"
        avg_confidence = sum(e['confidence'] for e in positive_examples) / len(positive_examples) if positive_examples else 0
        report_content += f"- **Average Confidence**: {avg_confidence:.1f}/5\n\n"
        report_content += f"## Evidence Examples\n\n"
        
        for i, example in enumerate(positive_examples[:5], 1):
            report_content += f"\n### Example {i}: {example['filename']}\n"
            report_content += f"- **Confidence**: {example['confidence']}/5\n"
            patterns_str = ', '.join(example['patterns']) if example['patterns'] else 'None specified'
            report_content += f"- **Patterns**: {patterns_str}\n"
            report_content += f"- **Evidence**: \"{example['evidence']}\"\n\n"
        
        report_content += f"## Pattern Suggestions\n\n"
        pattern_suggestions = []
        for entry in training_data:
            suggestions = entry.get("pattern_suggestions", "").strip()
            if suggestions:
                pattern_suggestions.extend([s.strip() for s in suggestions.split(',')])
        
        if pattern_suggestions:
            from collections import Counter
            suggestion_counts = Counter(pattern_suggestions)
            for suggestion, count in suggestion_counts.most_common(10):
                report_content += f"- **{suggestion}** ({count}x)\n"
        else:
            report_content += "No pattern suggestions provided.\n"
        
        report_content += f"""
## Next Steps for Analysis

1. **Pattern Discovery**: Analyze evidence quotes for new regex patterns
2. **False Negative Review**: Check papers marked negative for missed statements  
3. **Validation Testing**: Test discovered patterns on validation set
4. **System Integration**: Add successful patterns to detection engine

## Raw Data

```json
{json.dumps(training_data, indent=2)}
```
"""
        
        return report_content
    
    def sanitize_name(self, name):
        """Clean name for use in filename (remove spaces, special chars)"""
        import re
        # Remove spaces and special characters, keep only alphanumeric and hyphens
        clean = re.sub(r'[^\w\-]', '', name.replace(' ', ''))
        return clean[:50]  # Limit length
    
    def extract_author_from_filename(self, filename):
        """Extract author name from PDF filename (assumes Author-Title format)"""
        # Remove .pdf extension
        name = filename.replace('.pdf', '').replace('.PDF', '')
        # If hyphen exists, take first part as author
        if '-' in name:
            author = name.split('-')[0]
        else:
            # Otherwise use the whole filename
            author = name
        return self.sanitize_name(author)
    
    def get_primary_judgment(self, training_data):
        """Get the most common judgment from training data"""
        if not training_data:
            return "unknown"
        judgments = [entry.get("judgment", "unknown") for entry in training_data]
        from collections import Counter
        most_common = Counter(judgments).most_common(1)
        if most_common:
            judgment = most_common[0][0]
            # Simplify judgment names: "positive_subtle" -> "positive"
            return judgment.split('_')[0] if '_' in judgment else judgment
        return "unknown"
    
    def save_local_report(self, training_data, ga_name, session_id):
        """Save report locally first with improved filenames"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Clean GA name for filename
        clean_ga_name = self.sanitize_name(ga_name)
        
        # Extract paper info if available
        if training_data and len(training_data) > 0:
            # Get the first paper's filename as representative
            paper_filename = training_data[0].get("filename", "unknown")
            paper_author = self.extract_author_from_filename(paper_filename)
            primary_judgment = self.get_primary_judgment(training_data)
        else:
            paper_author = "unknown"
            primary_judgment = "unknown"
        
        # New filename format: reviewer_author_judgment_timestamp.ext
        # Example: ToddEdwards_Armstrong_positive_20251010_144437.json
        base_filename = f"{clean_ga_name}_{paper_author}_{primary_judgment}_{timestamp}"
        
        # Save JSON data
        json_filename = f"{base_filename}.json"
        json_path = self.reports_dir / json_filename
        
        with open(json_path, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        # Save markdown report
        md_content = self.create_training_report(training_data, ga_name, session_id)
        md_filename = f"{base_filename}.md"
        md_path = self.reports_dir / md_filename
        
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        return json_path, md_path
    
    def upload_to_github(self, json_path, md_path, ga_name, session_id):
        """Upload reports to GitHub repository using GitHub API"""
        
        try:
            # Check if we have the necessary credentials
            if not self.token or not self.owner or not self.repo:
                return False, "GitHub credentials not configured. Please check Settings."
            
            # Read the file contents
            with open(json_path, 'r') as f:
                json_content = f.read()
            
            with open(md_path, 'r') as f:
                md_content = f.read()
            
            # Upload JSON file via GitHub API
            json_upload_url = f"{self.base_url}/contents/training_reports/{json_path.name}"
            json_data = {
                "message": f"Training: {ga_name} reviewed {json_path.stem}",
                "content": self._encode_content(json_content),
                "branch": "main"
            }
            
            json_response = requests.put(json_upload_url, headers=self.headers, json=json_data)
            
            if json_response.status_code not in [200, 201]:
                return False, f"Failed to upload JSON: {json_response.status_code} - {json_response.text}"
            
            # Upload MD file via GitHub API
            md_upload_url = f"{self.base_url}/contents/training_reports/{md_path.name}"
            md_data = {
                "message": f"Training report: {ga_name} - {md_path.stem}",
                "content": self._encode_content(md_content),
                "branch": "main"
            }
            
            md_response = requests.put(md_upload_url, headers=self.headers, json=md_data)
            
            if md_response.status_code not in [200, 201]:
                return False, f"Failed to upload MD: {md_response.status_code} - {md_response.text}"
            
            return True, f"Successfully uploaded to GitHub: {json_path.name}"
            
        except Exception as e:
            return False, f"Upload error: {str(e)}"
    
    def _encode_content(self, content):
        """Encode content to base64 for GitHub API"""
        import base64
        return base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    def process_training_session(self, training_data, ga_name):
        """Complete processing pipeline for a training session"""
        
        session_id = datetime.now().strftime("%Y%m%d_%H%M")
        
        # Save locally
        json_path, md_path = self.save_local_report(training_data, ga_name, session_id)
        
        # Upload to GitHub
        success, message = self.upload_to_github(json_path, md_path, ga_name, session_id)
        
        return {
            'success': success,
            'message': message,
            'json_file': str(json_path),
            'md_file': str(md_path),
            'session_id': session_id
        }

# Integration with existing training interface
def add_auto_upload_to_training_interface():
    """
    Instructions for integrating auto-upload into enhanced_training_interface.py
    """
    integration_code = '''
# Add to enhanced_training_interface.py

from github_report_uploader import GitHubReportUploader

class EnhancedTrainingInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... existing code ...
        self.uploader = GitHubReportUploader()
        
        # Add GA name input
        self.ga_name_input = QLineEdit()
        self.ga_name_input.setPlaceholderText("Enter GA name (e.g., 'sarah_m')")
        
        # Modify export button to include auto-upload
        export_btn = QPushButton("📤 Export & Upload")
        export_btn.clicked.connect(self.export_and_upload)
    
    def export_and_upload(self):
        """Enhanced export with auto-upload to GitHub"""
        if not self.training_data:
            QMessageBox.information(self, "No Data", "No training data to export.")
            return
        
        ga_name = self.ga_name_input.text().strip()
        if not ga_name:
            QMessageBox.warning(self, "Missing Info", "Please enter GA name.")
            return
        
        # Process the training session
        result = self.uploader.process_training_session(self.training_data, ga_name)
        
        if result['success']:
            QMessageBox.information(
                self, "✅ Success", 
                f"Training session uploaded successfully!\\n\\n"
                f"Session ID: {result['session_id']}\\n"
                f"Files created:\\n"
                f"- {result['md_file']}\\n"
                f"- {result['json_file']}\\n\\n"
                f"Data is now available for batch analysis."
            )
        else:
            QMessageBox.critical(
                self, "❌ Upload Failed", 
                f"Could not upload to GitHub:\\n{result['message']}\\n\\n"
                f"Files saved locally:\\n"
                f"- {result['md_file']}\\n"
                f"- {result['json_file']}"
            )
    '''
    
    return integration_code

if __name__ == "__main__":
    # Example usage
    sample_training_data = [
        {
            "filename": "example_paper.pdf",
            "timestamp": "2025-09-29T10:30:00",
            "judgment": "positive_explicit",
            "evidence": "I acknowledge my position as a White researcher working in communities of color.",
            "pattern_types": ["first_person_reflexivity", "identity_disclosure"],
            "confidence": 4,
            "pattern_suggestions": "privilege acknowledgment, racial positioning"
        }
    ]
    
    uploader = GitHubReportUploader()
    result = uploader.process_training_session(sample_training_data, "test_user")
    print(f"Test result: {result}")