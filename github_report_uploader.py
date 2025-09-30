#!/usr/bin/env python3
"""
Enhanced Training Interface with Auto-Upload

This enhanced version automatically uploads training reports to GitHub
and generates markdown reports for batch analysis.
"""

import json
import os
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
        
    def load_config(self):
        """Load configuration from interface_settings.json"""
        config_file = Path("interface_settings.json")
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
    
    def save_local_report(self, training_data, ga_name, session_id):
        """Save report locally first"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON data
        json_filename = f"training_session_{ga_name}_{session_id}_{timestamp}.json"
        json_path = self.reports_dir / json_filename
        
        with open(json_path, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        # Save markdown report
        md_content = self.create_training_report(training_data, ga_name, session_id)
        md_filename = f"training_report_{ga_name}_{session_id}_{timestamp}.md"
        md_path = self.reports_dir / md_filename
        
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        return json_path, md_path
    
    def upload_to_github(self, json_path, md_path, ga_name, session_id):
        """Upload reports to GitHub repository"""
        
        try:
            # Check if git is configured
            result = subprocess.run(['git', 'status'], 
                                  capture_output=True, text=True, cwd='.')
            
            if result.returncode != 0:
                return False, "Not in a git repository"
            
            # Add files to git
            subprocess.run(['git', 'add', str(json_path)], cwd='.')
            subprocess.run(['git', 'add', str(md_path)], cwd='.')
            
            # Commit with descriptive message
            commit_msg = f"Training session: {ga_name} - {session_id}"
            result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                  capture_output=True, text=True, cwd='.')
            
            if result.returncode != 0:
                return False, f"Git commit failed: {result.stderr}"
            
            # Push to remote
            result = subprocess.run(['git', 'push'], 
                                  capture_output=True, text=True, cwd='.')
            
            if result.returncode != 0:
                return False, f"Git push failed: {result.stderr}"
            
            return True, "Successfully uploaded to GitHub"
            
        except Exception as e:
            return False, f"Upload error: {str(e)}"
    
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