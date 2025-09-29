#!/usr/bin/env python3
"""
Weekly Batch Analysis System - Research Buddy 2.0

Enhanced institutional-grade batch analysis system that processes training data,
discovers patterns, and generates comprehensive institutional reports.

Features:
- Automated paper processing at scale
- Pattern discovery from human expert data  
- Institutional analytics and reporting
- GitHub integration for continuous learning
- GA performance tracking
- Quality metrics and recommendations
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import sys
import logging

sys.path.insert(0, '/home/todd/py-extractor')
from training_analysis import generate_training_report
from targeted_patterns import ACADEMIC_REFLEXIVITY_PATTERNS
from metadata_extractor import extract_positionality
from github_report_uploader import GitHubReportUploader

class WeeklyBatchProcessor:
    """Enhanced batch processor for institutional-scale analysis"""
    
    def __init__(self, reports_dir="training_reports", batch_dir="batch_papers", output_dir="batch_reports"):
        self.reports_dir = Path(reports_dir)
        self.batch_dir = Path(batch_dir)
        self.output_dir = Path(output_dir)
        
        # Create directories
        self.reports_dir.mkdir(exist_ok=True)
        self.batch_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Initialize GitHub uploader
        self.github_uploader = GitHubReportUploader()
        
        # Analysis thresholds
        self.confidence_threshold = 0.6
        self.pattern_frequency_threshold = 3
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_file = self.output_dir / f"batch_analysis_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_weekly_reports(self, days_back=7):
        """Get all training reports from the past N days"""
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        weekly_reports = []
        
        # Find all JSON training files
        for json_file in self.reports_dir.glob("training_session_*.json"):
            # Extract timestamp from filename
            try:
                # Format: training_session_GA_SESSION_TIMESTAMP.json
                parts = json_file.stem.split('_')
                timestamp_str = '_'.join(parts[-2:])  # Get last two parts
                file_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                if file_date >= cutoff_date:
                    weekly_reports.append(json_file)
                    
            except (ValueError, IndexError):
                print(f"Warning: Could not parse date from {json_file}")
                
        return sorted(weekly_reports)
    
    def combine_training_data(self, report_files):
        """Combine all training data from multiple GA sessions"""
        
        combined_data = []
        ga_stats = defaultdict(lambda: {"papers": 0, "sessions": 0})
        
        for report_file in report_files:
            try:
                with open(report_file, 'r') as f:
                    session_data = json.load(f)
                
                # Extract GA name from filename
                ga_name = report_file.stem.split('_')[2]  # training_session_GA_SESSION_TIMESTAMP
                
                # Add session metadata to each entry
                for entry in session_data:
                    entry["ga_name"] = ga_name
                    entry["session_file"] = str(report_file)
                    combined_data.append(entry)
                
                ga_stats[ga_name]["papers"] += len(session_data)
                ga_stats[ga_name]["sessions"] += 1
                
            except Exception as e:
                print(f"Error processing {report_file}: {e}")
        
        return combined_data, dict(ga_stats)
    
    def analyze_weekly_patterns(self, combined_data):
        """Analyze patterns across all GA training sessions"""
        
        # Overall statistics
        total_papers = len(combined_data)
        judgments = Counter(entry.get("judgment", "unknown") for entry in combined_data)
        
        # Evidence analysis
        positive_entries = [e for e in combined_data 
                          if e.get("judgment", "").startswith("positive")]
        
        evidence_examples = []
        all_pattern_suggestions = []
        
        for entry in positive_entries:
            if entry.get("evidence"):
                evidence_examples.append({
                    "text": entry["evidence"],
                    "filename": entry["filename"],
                    "ga_name": entry["ga_name"],
                    "patterns": entry.get("pattern_types", []),
                    "confidence": entry.get("confidence", 0)
                })
            
            suggestions = entry.get("pattern_suggestions", "").strip()
            if suggestions:
                all_pattern_suggestions.extend([s.strip() for s in suggestions.split(',')])
        
        # Pattern frequency analysis
        suggested_patterns = Counter(all_pattern_suggestions)
        
        # Inter-GA agreement analysis
        filename_judgments = defaultdict(list)
        for entry in combined_data:
            filename = entry["filename"]
            judgment = entry.get("judgment", "unknown")
            ga_name = entry["ga_name"]
            filename_judgments[filename].append((ga_name, judgment))
        
        # Find papers labeled by multiple GAs
        multi_labeled = {filename: judgments for filename, judgments in filename_judgments.items() 
                        if len(judgments) > 1}
        
        return {
            "total_papers": total_papers,
            "judgments": judgments,
            "evidence_examples": evidence_examples,
            "suggested_patterns": suggested_patterns,
            "multi_labeled": multi_labeled
        }
    
    def discover_new_patterns(self, evidence_examples):
        """Discover new regex patterns from GA evidence"""
        
        print("🔍 DISCOVERING NEW PATTERNS FROM GA EVIDENCE")
        print("=" * 60)
        
        # Collect all evidence text
        all_evidence = [example["text"] for example in evidence_examples]
        
        # Look for common phrases that aren't caught by current patterns
        new_pattern_candidates = []
        
        # Pattern 1: Authorial collective positioning
        collective_pattern = r"\b(?:we|our team|the authors?)\s+(?:acknowledge|recognize|position|locate)\s+(?:ourselves?|our)"
        collective_matches = []
        for evidence in all_evidence:
            if re.search(collective_pattern, evidence, re.IGNORECASE):
                collective_matches.append(evidence[:100] + "...")
        
        if collective_matches:
            new_pattern_candidates.append({
                "name": "collective_authorial_positioning",
                "pattern": collective_pattern,
                "examples": collective_matches[:3],
                "count": len(collective_matches)
            })
        
        # Pattern 2: Methodology-embedded reflexivity
        method_pattern = r"\b(?:this\s+study|this\s+research|our\s+methodology)\s+(?:emerged|developed|grew)\s+(?:from|out\s+of)\s+(?:my|our)"
        method_matches = []
        for evidence in all_evidence:
            if re.search(method_pattern, evidence, re.IGNORECASE):
                method_matches.append(evidence[:100] + "...")
        
        if method_matches:
            new_pattern_candidates.append({
                "name": "methodology_embedded_reflexivity", 
                "pattern": method_pattern,
                "examples": method_matches[:3],
                "count": len(method_matches)
            })
        
        # Pattern 3: Cultural/identity intersection
        intersection_pattern = r"\bas\s+a\s+\w+\s+(?:and|who\s+is\s+also|with)\s+\w+\s+(?:researcher|scholar|person)"
        intersection_matches = []
        for evidence in all_evidence:
            if re.search(intersection_pattern, evidence, re.IGNORECASE):
                intersection_matches.append(evidence[:100] + "...")
        
        if intersection_matches:
            new_pattern_candidates.append({
                "name": "intersectional_identity_disclosure",
                "pattern": intersection_pattern, 
                "examples": intersection_matches[:3],
                "count": len(intersection_matches)
            })
        
        return new_pattern_candidates
    
    def analyze_ga_performance(self, combined_data, ga_stats):
        """Comprehensive GA performance analysis"""
        self.logger.info("📊 Analyzing GA performance...")
        
        ga_performance = {}
        
        for ga_name, stats in ga_stats.items():
            ga_entries = [e for e in combined_data if e.get("ga_name") == ga_name]
            
            if len(ga_entries) >= 3:  # Minimum for meaningful analysis
                judgments = [e.get("judgment", "unknown") for e in ga_entries]
                confidences = [e.get("confidence", 0) for e in ga_entries if e.get("confidence")]
                evidence_entries = [e for e in ga_entries if e.get("evidence", "").strip()]
                
                ga_performance[ga_name] = {
                    "papers_labeled": len(ga_entries),
                    "sessions": stats["sessions"],
                    "positive_rate": len([j for j in judgments if j.startswith("positive")]) / len(judgments),
                    "explicit_rate": len([j for j in judgments if j == "positive_explicit"]) / len(judgments),
                    "average_confidence": sum(confidences) / len(confidences) if confidences else 0,
                    "evidence_rate": len(evidence_entries) / len(ga_entries),
                    "avg_evidence_length": sum(len(e["evidence"]) for e in evidence_entries) / len(evidence_entries) if evidence_entries else 0
                }
                
        return ga_performance
    
    def calculate_quality_metrics(self, combined_data, ga_performance):
        """Calculate institutional quality metrics"""
        self.logger.info("📈 Calculating quality metrics...")
        
        # Inter-GA agreement estimation
        filename_judgments = defaultdict(list)
        for entry in combined_data:
            filename = entry["filename"]
            judgment = entry.get("judgment", "unknown")
            filename_judgments[filename].append(judgment)
        
        # Find papers with multiple judgments
        agreement_cases = 0
        total_multi_cases = 0
        
        for filename, judgments in filename_judgments.items():
            if len(judgments) > 1:
                total_multi_cases += 1
                if len(set(judgments)) == 1:  # All GAs agreed
                    agreement_cases += 1
                    
        inter_ga_agreement = agreement_cases / total_multi_cases if total_multi_cases > 0 else 0
        
        # Overall system quality metrics
        all_confidences = [e.get("confidence", 0) for e in combined_data if e.get("confidence")]
        avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0
        
        evidence_rate = len([e for e in combined_data if e.get("evidence", "").strip()]) / len(combined_data)
        
        # GA productivity variance (consistency indicator)
        if ga_performance:
            productivities = [perf["papers_labeled"] for perf in ga_performance.values()]
            avg_productivity = sum(productivities) / len(productivities)
            productivity_variance = sum((p - avg_productivity)**2 for p in productivities) / len(productivities)
        else:
            avg_productivity = 0
            productivity_variance = 0
            
        return {
            "inter_ga_agreement": inter_ga_agreement,
            "average_confidence": avg_confidence,
            "evidence_collection_rate": evidence_rate,
            "ga_productivity_avg": avg_productivity,
            "ga_productivity_variance": productivity_variance,
            "total_multi_labeled": total_multi_cases,
            "high_confidence_rate": len([c for c in all_confidences if c >= 4]) / len(all_confidences) if all_confidences else 0
        }
    
    def generate_institutional_report(self, combined_data, ga_stats, analysis, new_patterns, ga_performance, quality_metrics):
        """Generate comprehensive institutional report"""
        self.logger.info("📋 Generating institutional report...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create comprehensive institutional report
        institutional_report = {
            "report_date": datetime.now().isoformat(),
            "analysis_period": "weekly",
            "summary": {
                "total_papers_labeled": len(combined_data),
                "total_gas_active": len(ga_stats),
                "total_sessions": sum(stats["sessions"] for stats in ga_stats.values()),
                "new_patterns_discovered": len(new_patterns)
            },
            "judgment_distribution": dict(analysis['judgments']),
            "ga_performance": ga_performance,
            "quality_metrics": quality_metrics,
            "pattern_discoveries": new_patterns,
            "recommendations": self.generate_recommendations(quality_metrics, ga_performance, analysis)
        }
        
        # Save detailed JSON report
        json_report_path = self.output_dir / f"institutional_report_{timestamp}.json"
        with open(json_report_path, 'w') as f:
            json.dump(institutional_report, f, indent=2)
            
        # Generate executive markdown summary
        md_report_path = self.generate_executive_summary(institutional_report, timestamp)
        
        return {
            "json_report": json_report_path,
            "md_report": md_report_path,
            "report_data": institutional_report
        }
    
    def generate_recommendations(self, quality_metrics, ga_performance, analysis):
        """Generate actionable institutional recommendations"""
        recommendations = []
        
        # Agreement recommendations
        if quality_metrics["inter_ga_agreement"] < 0.7:
            recommendations.append({
                "category": "Training",
                "priority": "High",
                "recommendation": "Inter-GA agreement below 70% - consider additional training or clearer guidelines",
                "metric": f"Current agreement: {quality_metrics['inter_ga_agreement']:.1%}"
            })
            
        # Confidence recommendations
        if quality_metrics["average_confidence"] < 3.5:
            recommendations.append({
                "category": "Training", 
                "priority": "Medium",
                "recommendation": "Average confidence below 3.5 - GAs may need more practice or clearer examples",
                "metric": f"Current average: {quality_metrics['average_confidence']:.2f}/5"
            })
            
        # Evidence collection recommendations
        if quality_metrics["evidence_collection_rate"] < 0.7:
            recommendations.append({
                "category": "Process",
                "priority": "Medium", 
                "recommendation": "Evidence collection rate below 70% - emphasize importance of citing specific text",
                "metric": f"Current rate: {quality_metrics['evidence_collection_rate']:.1%}"
            })
            
        # GA recruitment recommendations
        if len(ga_performance) < 3:
            recommendations.append({
                "category": "Staffing",
                "priority": "Medium",
                "recommendation": "Consider recruiting additional GAs for better coverage and reliability",
                "metric": f"Current GAs: {len(ga_performance)}"
            })
            
        # High performers recognition
        high_performers = [ga for ga, perf in ga_performance.items() 
                         if perf["average_confidence"] > 4.0 and perf["evidence_rate"] > 0.8]
        if high_performers:
            recommendations.append({
                "category": "Recognition",
                "priority": "Low",
                "recommendation": f"Recognize high-performing GAs: {', '.join(high_performers)}",
                "metric": "High confidence + evidence collection"
            })
            
        return recommendations
    
    def generate_executive_summary(self, report_data, timestamp):
        """Generate executive summary in markdown"""
        summary = f"""# 📊 Research Buddy Weekly Institutional Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Analysis Period:** Weekly  
**System:** Research Buddy 2.0

## 🎯 Executive Summary

### Training Program Performance
- **Papers Labeled:** {report_data['summary']['total_papers_labeled']}
- **Active GAs:** {report_data['summary']['total_gas_active']}
- **Training Sessions:** {report_data['summary']['total_sessions']}
- **New Patterns Discovered:** {report_data['summary']['new_patterns_discovered']}

### Quality Indicators
| Metric | Score | Target | Status |
|--------|-------|---------|---------|
| Inter-GA Agreement | {report_data['quality_metrics']['inter_ga_agreement']:.1%} | >70% | {'✅' if report_data['quality_metrics']['inter_ga_agreement'] > 0.7 else '⚠️'} |
| Average Confidence | {report_data['quality_metrics']['average_confidence']:.2f}/5 | >3.5 | {'✅' if report_data['quality_metrics']['average_confidence'] > 3.5 else '⚠️'} |
| Evidence Collection | {report_data['quality_metrics']['evidence_collection_rate']:.1%} | >70% | {'✅' if report_data['quality_metrics']['evidence_collection_rate'] > 0.7 else '⚠️'} |
| High Confidence Rate | {report_data['quality_metrics']['high_confidence_rate']:.1%} | >40% | {'✅' if report_data['quality_metrics']['high_confidence_rate'] > 0.4 else '⚠️'} |

## 📈 GA Performance Summary

"""
        
        # GA performance table
        if report_data['ga_performance']:
            summary += "| GA Name | Papers | Confidence Avg | Evidence Rate | Positive Rate |\n"
            summary += "|---------|---------|----------------|---------------|---------------|\n"
            
            for ga_name, perf in report_data['ga_performance'].items():
                summary += f"| {ga_name} | {perf['papers_labeled']} | {perf['average_confidence']:.2f} | {perf['evidence_rate']:.1%} | {perf['positive_rate']:.1%} |\n"
        
        summary += "\n## 🔍 Pattern Discoveries\n\n"
        
        if report_data['pattern_discoveries']:
            for pattern in report_data['pattern_discoveries']:
                summary += f"**{pattern['name']}** - {pattern['count']} matches found\n"
        else:
            summary += "No new patterns discovered this week.\n"
            
        summary += "\n## 💡 Recommendations\n\n"
        
        for i, rec in enumerate(report_data['recommendations'], 1):
            priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(rec['priority'], "⚪")
            summary += f"{i}. {priority_emoji} **{rec['category']}**: {rec['recommendation']}\n"
            summary += f"   *{rec['metric']}*\n\n"
            
        summary += "---\n*Generated by Research Buddy 2.0 Institutional Analytics*"
        
        # Save summary
        summary_path = self.output_dir / f"executive_summary_{timestamp}.md"
        with open(summary_path, 'w') as f:
            f.write(summary)
            
        return summary_path
    
    def process_batch_papers(self):
        """Process any papers in the batch directory"""
        self.logger.info("📄 Processing batch papers...")
        
        pdf_files = list(self.batch_dir.glob("*.pdf"))
        if not pdf_files:
            return {"processed": 0, "results": []}
            
        results = []
        for pdf_file in pdf_files:
            try:
                # Run enhanced detection
                result = extract_positionality(str(pdf_file))
                
                results.append({
                    "filename": pdf_file.name,
                    "positionality_score": result["positionality_score"],
                    "patterns_found": result["positionality_tests"],
                    "evidence_count": len(result["positionality_snippets"])
                })
                
                # Move to processed folder
                processed_dir = self.batch_dir / "processed"
                processed_dir.mkdir(exist_ok=True)
                pdf_file.rename(processed_dir / pdf_file.name)
                
            except Exception as e:
                self.logger.error(f"Error processing {pdf_file}: {e}")
                
        return {"processed": len(results), "results": results}
    
    def generate_weekly_report(self, combined_data, ga_stats, analysis, new_patterns):
        """Generate comprehensive weekly analysis report"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# Weekly Training Analysis Report
Generated: {timestamp}

## 📊 Weekly Summary

### Participation
- **Total Papers Analyzed**: {analysis['total_papers']}
- **Active GAs**: {len(ga_stats)}
- **Total Sessions**: {sum(stats['sessions'] for stats in ga_stats.values())}

### GA Performance
"""
        
        for ga_name, stats in sorted(ga_stats.items()):
            report += f"- **{ga_name}**: {stats['papers']} papers across {stats['sessions']} sessions\n"
        
        report += f"""
### Judgment Distribution
"""
        
        for judgment, count in analysis['judgments'].most_common():
            percentage = (count / analysis['total_papers']) * 100
            report += f"- **{judgment}**: {count} papers ({percentage:.1f}%)\n"
        
        report += f"""
## 🎯 Pattern Analysis

### Top Evidence Examples
"""
        
        # Show best evidence examples (high confidence, clear patterns)
        high_confidence = [e for e in analysis['evidence_examples'] if e['confidence'] >= 4]
        high_confidence.sort(key=lambda x: x['confidence'], reverse=True)
        
        for i, example in enumerate(high_confidence[:5], 1):
            report += f"""
#### Example {i} (Confidence: {example['confidence']}/5)
- **GA**: {example['ga_name']}
- **File**: {example['filename']}
- **Patterns**: {', '.join(example['patterns']) if example['patterns'] else 'None'}
- **Text**: "{example['text'][:200]}{'...' if len(example['text']) > 200 else ''}"
"""
        
        report += f"""
### Pattern Suggestions from GAs
"""
        
        for pattern, count in analysis['suggested_patterns'].most_common(10):
            report += f"- **{pattern}** (suggested {count}x)\n"
        
        report += f"""
## 🔍 New Pattern Discovery

### Discovered Patterns
"""
        
        if new_patterns:
            for pattern in new_patterns:
                report += f"""
#### {pattern['name']}
- **Pattern**: `{pattern['pattern']}`
- **Matches Found**: {pattern['count']}
- **Examples**:
"""
                for example in pattern['examples']:
                    report += f"  - \"{example}\"\n"
        else:
            report += "No new patterns discovered this week.\n"
        
        report += f"""
## 🤝 Inter-GA Agreement

### Papers Labeled by Multiple GAs
"""
        
        if analysis['multi_labeled']:
            for filename, judgments in list(analysis['multi_labeled'].items())[:5]:
                report += f"- **{filename}**: "
                judgment_summary = Counter(j[1] for j in judgments)
                report += ", ".join(f"{j} ({c})" for j, c in judgment_summary.items())
                report += "\n"
        else:
            report += "No papers were labeled by multiple GAs this week.\n"
        
        report += f"""
## 🚀 Recommended Actions

### Immediate Improvements
"""
        
        if new_patterns:
            report += "1. **Integrate new patterns** into detection system\n"
            report += "2. **Test patterns** on validation dataset\n"
            report += "3. **Measure performance improvement**\n"
        
        positive_rate = analysis['judgments'].get('positive_explicit', 0) + analysis['judgments'].get('positive_subtle', 0)
        positive_pct = (positive_rate / analysis['total_papers']) * 100
        
        if positive_pct < 20:
            report += "4. **Seek more papers with positionality statements** for balanced training\n"
        elif positive_pct > 80:
            report += "4. **Include more papers without positionality** for balanced training\n"
        
        report += f"""
### Next Week's Focus
- Continue systematic labeling
- Test discovered patterns on new papers
- Focus on {', '.join([j for j, c in analysis['judgments'].most_common()[-2:]])} cases for better coverage

---
*Report generated automatically from GA training sessions*
"""
        
        return report
    
    def run_weekly_analysis(self, days_back=7):
        """Run comprehensive institutional weekly analysis pipeline"""
        
        self.logger.info(f"� Starting comprehensive weekly analysis ({days_back} days)")
        
        # Step 1: Process any batch papers
        batch_results = self.process_batch_papers()
        if batch_results["processed"] > 0:
            self.logger.info(f"📄 Processed {batch_results['processed']} batch papers")
        
        # Step 2: Get and combine training reports
        report_files = self.get_weekly_reports(days_back)
        
        if not report_files:
            self.logger.warning("❌ No training reports found for the specified period")
            return None
        
        self.logger.info(f"📁 Found {len(report_files)} training session files")
        
        # Step 3: Combine all training data
        combined_data, ga_stats = self.combine_training_data(report_files)
        self.logger.info(f"📊 Combined {len(combined_data)} total paper analyses from {len(ga_stats)} GAs")
        
        # Step 4: Run comprehensive analysis
        analysis = self.analyze_weekly_patterns(combined_data)
        ga_performance = self.analyze_ga_performance(combined_data, ga_stats)
        quality_metrics = self.calculate_quality_metrics(combined_data, ga_performance)
        
        # Step 5: Discover new patterns
        new_patterns = self.discover_new_patterns(analysis['evidence_examples'])
        self.logger.info(f"🔍 Discovered {len(new_patterns)} new patterns")
        
        # Step 6: Generate institutional report
        institutional_report = self.generate_institutional_report(
            combined_data, ga_stats, analysis, new_patterns, ga_performance, quality_metrics
        )
        
        self.logger.info("✅ Comprehensive weekly analysis complete!")
        
        return {
            'institutional_report': institutional_report,
            'combined_data': combined_data,
            'ga_performance': ga_performance,
            'quality_metrics': quality_metrics,
            'new_patterns': new_patterns,
            'batch_results': batch_results
        }

def main():
    """Run comprehensive weekly institutional analysis"""
    
    processor = WeeklyBatchProcessor()
    result = processor.run_weekly_analysis(days_back=7)
    
    if result:
        print(f"\n📋 INSTITUTIONAL ANALYSIS SUMMARY")
        print("=" * 50)
        
        # Basic stats
        institutional_data = result['institutional_report']['report_data']
        summary = institutional_data['summary']
        
        print(f"📊 Papers Labeled: {summary['total_papers_labeled']}")
        print(f"👥 Active GAs: {summary['total_gas_active']}")
        print(f"🎯 Training Sessions: {summary['total_sessions']}")
        print(f"🔍 New Patterns: {summary['new_patterns_discovered']}")
        
        # Quality metrics
        print(f"\n📈 QUALITY METRICS")
        quality = result['quality_metrics']
        print(f"🤝 Inter-GA Agreement: {quality['inter_ga_agreement']:.1%}")
        print(f"📊 Average Confidence: {quality['average_confidence']:.2f}/5")
        print(f"📄 Evidence Collection: {quality['evidence_collection_rate']:.1%}")
        print(f"⭐ High Confidence Rate: {quality['high_confidence_rate']:.1%}")
        
        # Reports generated
        print(f"\n📁 REPORTS GENERATED")
        reports = result['institutional_report']
        print(f"📋 Executive Summary: {reports['md_report'].name}")
        print(f"📊 Detailed Report: {reports['json_report'].name}")
        
        # Recommendations
        recommendations = institutional_data['recommendations']
        if recommendations:
            print(f"\n💡 KEY RECOMMENDATIONS ({len(recommendations)})")
            for i, rec in enumerate(recommendations[:3], 1):  # Show top 3
                priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(rec['priority'], "⚪")
                print(f"{i}. {priority_emoji} {rec['recommendation']}")
        
        # Pattern discoveries
        if result['new_patterns']:
            print(f"\n🔍 NEW PATTERNS TO INTEGRATE:")
            for pattern in result['new_patterns'][:3]:  # Show top 3
                print(f"  - {pattern['name']}: {pattern['count']} matches")
                
        print(f"\n✅ Research Buddy 2.0 institutional analysis complete!")
        
    else:
        print("❌ No analysis data available - ensure training reports exist")

if __name__ == "__main__":
    main()