#!/usr/bin/env python3
"""
Fact-Check Auditor Script
Reads project_specs.txt and validates against expected values.
Generates an audit report with MATCH/MISMATCH/DATA MISSING status.
Maintains persistent audit history log.
Includes CRITICAL WARNING for elevated risk levels.
"""

from pathlib import Path
from datetime import datetime
import re


class FactCheckAuditor:
    """A strict fact-checker that validates file content against expected values."""
    
    def __init__(self):
        """Initialize with expected values."""
        self.expected_values = {
            'Deadline': 'January 15th',
            'Lead': 'Sarah Chen',
            'Budget': '$50,000',
            'Risk Level': 'Low'
        }
        self.source_file = Path('project_specs.txt')
        self.report_file = Path('audit_report.txt')
        self.history_log = Path('audit_history.log')
        self.content = None
    
    def load_file(self):
        """Load the content from project_specs.txt."""
        try:
            if not self.source_file.exists():
                print(f"Error: File '{self.source_file}' does not exist.")
                return False
            
            with open(self.source_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
            
            print(f"✓ Loaded: {self.source_file}")
            print(f"Content: {self.content}\n")
            return True
        
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def extract_value(self, category):
        """Extract a specific value from the content."""
        if not self.content:
            return None
        
        content_lower = self.content.lower()
        
        # Search patterns for each category
        if category == 'Deadline':
            # Look for deadline date pattern
            match = re.search(r'deadline is ([^.]+)', content_lower)
            if match:
                return match.group(1).strip()
        
        elif category == 'Lead':
            # Look for lead engineer name
            match = re.search(r'lead engineer is ([^.]+)', content_lower)
            if match:
                return match.group(1).strip()
        
        elif category == 'Budget':
            # Look for budget amount
            match = re.search(r'budget is ([^.]+)', content_lower)
            if match:
                return match.group(1).strip()
        
        elif category == 'Risk Level':
            # Look for risk level
            match = re.search(r'risk level:\s*([^.]+)', content_lower)
            if match:
                return match.group(1).strip()
        
        return None
    
    def audit(self):
        """Perform the audit and generate report."""
        results = []
        
        print("=" * 60)
        print("AUDIT IN PROGRESS")
        print("=" * 60)
        
        for category, expected in self.expected_values.items():
            actual = self.extract_value(category)
            
            if actual is None:
                status = 'DATA MISSING'
                print(f"{category}: {status}")
            elif actual.lower() == expected.lower():
                status = 'MATCH'
                print(f"{category}: {status} ({expected})")
            else:
                status = 'MISMATCH'
                
                # Check for CRITICAL WARNING on Risk Level
                if category == 'Risk Level' and actual.lower() in ['medium', 'high']:
                    status = 'CRITICAL WARNING'
                    print(f"{category}: {status} (Expected: {expected}, Found: {actual.upper()})")
                else:
                    print(f"{category}: {status} (Expected: {expected}, Found: {actual})")
            
            results.append({
                'category': category,
                'expected': expected,
                'actual': actual,
                'status': status
            })
        
        print("=" * 60)
        return results
    
    def generate_report(self, results):
        """Generate the audit_report.txt file."""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("FACT-CHECK AUDIT REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Source File: {self.source_file}")
        report_lines.append(f"Report Generated: {Path(__file__).name}")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # Check for critical warnings
        critical_warnings = [r for r in results if r['status'] == 'CRITICAL WARNING']
        if critical_warnings:
            report_lines.append("!!! CRITICAL WARNINGS DETECTED !!!")
            report_lines.append("=" * 60)
            for warning in critical_warnings:
                report_lines.append(f"⚠️  {warning['category']}: {warning['actual'].upper()}")
                report_lines.append(f"    Expected: {warning['expected']}")
            report_lines.append("=" * 60)
            report_lines.append("")
        
        report_lines.append("VALIDATION RESULTS:")
        report_lines.append("-" * 60)
        
        for result in results:
            report_lines.append(f"\nCategory: {result['category']}")
            report_lines.append(f"Expected Value: {result['expected']}")
            
            if result['actual'] is not None:
                report_lines.append(f"Actual Value: {result['actual']}")
            else:
                report_lines.append(f"Actual Value: NOT FOUND")
            
            report_lines.append(f"Status: {result['status']}")
            report_lines.append("-" * 60)
        
        report_lines.append("")
        report_lines.append("SUMMARY:")
        matches = sum(1 for r in results if r['status'] == 'MATCH')
        mismatches = sum(1 for r in results if r['status'] == 'MISMATCH')
        missing = sum(1 for r in results if r['status'] == 'DATA MISSING')
        critical = sum(1 for r in results if r['status'] == 'CRITICAL WARNING')
        
        report_lines.append(f"  MATCH: {matches}")
        report_lines.append(f"  MISMATCH: {mismatches}")
        report_lines.append(f"  CRITICAL WARNING: {critical}")
        report_lines.append(f"  DATA MISSING: {missing}")
        report_lines.append("")
        report_lines.append("=" * 60)
        
        report_content = '\n'.join(report_lines)
        
        try:
            with open(self.report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"\n✓ Report generated: {self.report_file}")
            return True
        except Exception as e:
            print(f"\nError generating report: {e}")
            return False
    
    def log_to_history(self, results):
        """Append audit results to persistent history log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate summary
        matches = sum(1 for r in results if r['status'] == 'MATCH')
        mismatches = [r for r in results if r['status'] == 'MISMATCH']
        missing = [r for r in results if r['status'] == 'DATA MISSING']
        critical_warnings = [r for r in results if r['status'] == 'CRITICAL WARNING']
        
        # Build log entry
        log_entry = []
        log_entry.append("-" * 60)
        log_entry.append(f"AUDIT RUN: {timestamp}")
        log_entry.append(f"Total Matches: {matches}")
        
        # Log critical warnings first
        if critical_warnings:
            log_entry.append(f"⚠️  CRITICAL WARNINGS: {len(critical_warnings)}")
            for c in critical_warnings:
                log_entry.append(f"  - {c['category']}: Expected '{c['expected']}', Found '{c['actual'].upper()}'")
        
        if mismatches:
            log_entry.append(f"Mismatches Found: {len(mismatches)}")
            for m in mismatches:
                log_entry.append(f"  - {m['category']}: Expected '{m['expected']}', Found '{m['actual']}'")
        else:
            if not critical_warnings:
                log_entry.append("Mismatches Found: None")
        
        if missing:
            log_entry.append(f"Data Missing: {len(missing)}")
            for m in missing:
                log_entry.append(f"  - {m['category']}: {m['expected']}")
        
        log_entry.append("-" * 60)
        log_entry.append("")
        
        log_content = '\n'.join(log_entry)
        
        try:
            # Append to history log (create if doesn't exist)
            mode = 'a' if self.history_log.exists() else 'w'
            with open(self.history_log, mode, encoding='utf-8') as f:
                if mode == 'w':
                    f.write("=" * 60 + "\n")
                    f.write("AUDIT HISTORY LOG\n")
                    f.write("=" * 60 + "\n\n")
                f.write(log_content)
            
            print(f"✓ History logged: {self.history_log}")
            return True
        except Exception as e:
            print(f"Error logging to history: {e}")
            return False
    
    def run(self):
        """Execute the full audit process."""
        print("\n" + "=" * 60)
        print("FACT-CHECK AUDITOR")
        print("=" * 60 + "\n")
        
        if not self.load_file():
            return False
        
        results = self.audit()
        
        self.generate_report(results)
        self.log_to_history(results)
        
        print("\nAudit complete!")
        return True


def main():
    """Main function to run the fact-check auditor."""
    auditor = FactCheckAuditor()
    auditor.run()


if __name__ == "__main__":
    main()
