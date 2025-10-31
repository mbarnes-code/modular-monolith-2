#!/usr/bin/env python3
"""
Performance Regression Detection Script - T138
Automated detection of constitutional performance regressions
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


class PerformanceRegressionDetector:
    """Detect performance regressions against constitutional thresholds"""
    
    CONSTITUTIONAL_THRESHOLDS = {
        'Security': 1000,        # <1s - threat analysis criticality
        'Productivity': 2000,    # <2s - task management workflows
        'MTG': 3000,            # <3s - game analysis complexity
        'Infrastructure': 5000,  # <5s - system operations tolerance
        'UI': 200               # <200ms - executive function support
    }
    
    REGRESSION_TOLERANCE = 0.1  # 10% tolerance for minor variations
    
    def __init__(self, results_file='performance_test_results.json'):
        self.results_file = results_file
        self.baseline_dir = Path('performance-baselines')
        self.baseline_dir.mkdir(exist_ok=True)
    
    def load_current_results(self):
        """Load current performance test results"""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Results file not found: {self.results_file}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in results file: {e}")
            return None
    
    def load_baseline(self):
        """Load the most recent performance baseline"""
        baseline_files = list(self.baseline_dir.glob('baseline_*.json'))
        
        if not baseline_files:
            print("⚠️ No performance baseline found - creating initial")
            return None
        
        # Get most recent baseline
        latest_baseline = max(baseline_files, key=lambda f: f.stat().st_mtime)
        
        try:
            with open(latest_baseline, 'r') as f:
                baseline = json.load(f)
                print(f"📊 Loaded baseline from: {latest_baseline.name}")
                return baseline
        except Exception as e:
            print(f"❌ Error loading baseline: {e}")
            return None
    
    def detect_constitutional_violations(self, results):
        """Detect violations of constitutional performance requirements"""
        violations = []
        
        for result in results.get('results', []):
            domain = result.get('domain', 'Unknown')
            avg_time = result.get('avg_response_time', 0)
            threshold = self.CONSTITUTIONAL_THRESHOLDS.get(
                domain, float('inf'))
            
            if avg_time > threshold:
                violations.append({
                    'domain': domain,
                    'avg_response_time': avg_time,
                    'constitutional_threshold': threshold,
                    'violation_factor': avg_time / threshold,
                    'severity': 'critical' if avg_time > threshold * 1.5 else 'major'
                })
        
        return violations
    
    def detect_performance_regressions(self, current_results, baseline):
        """Detect regressions compared to baseline"""
        if not baseline or 'domain_baselines' not in baseline:
            return []
        
        regressions = []
        baseline_metrics = baseline['domain_baselines']
        
        for result in current_results.get('results', []):
            domain = result.get('domain', 'Unknown')
            current_avg = result.get('avg_response_time', 0)
            
            if domain in baseline_metrics:
                baseline_avg = baseline_metrics[domain]['avg_response_time']
                regression_factor = current_avg / baseline_avg
                
                # Check for significant regression (> 10% increase)
                if regression_factor > (1 + self.REGRESSION_TOLERANCE):
                    regressions.append({
                        'domain': domain,
                        'current_avg': current_avg,
                        'baseline_avg': baseline_avg,
                        'regression_factor': regression_factor,
                        'regression_percent': (regression_factor - 1) * 100,
                        'severity': 'critical' if regression_factor > 1.5 else 'major'
                    })
        
        return regressions
    
    def create_baseline(self, results):
        """Create a new performance baseline"""
        baseline = {
            'timestamp': datetime.now().isoformat(),
            'commit_sha': os.getenv('GITHUB_SHA', 'unknown'),
            'branch': os.getenv('GITHUB_REF_NAME', 'main'),
            'constitutional_compliance': True,
            'domain_baselines': {}
        }
        
        # Extract baseline metrics from compliant results
        for result in results.get('results', []):
            domain = result.get('domain', 'Unknown')
            avg_time = result.get('avg_response_time', 0)
            threshold = self.CONSTITUTIONAL_THRESHOLDS.get(domain, float('inf'))
            
            # Only include compliant results in baseline
            if avg_time <= threshold:
                baseline['domain_baselines'][domain] = {
                    'avg_response_time': avg_time,
                    'max_response_time': result.get('max_response_time', avg_time),
                    'threshold': threshold,
                    'compliance_margin': (threshold - avg_time) / threshold
                }
        
        # Save baseline
        timestamp = int(datetime.now().timestamp())
        baseline_file = self.baseline_dir / f'baseline_{timestamp}.json'
        
        with open(baseline_file, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        print(f"✅ Created new performance baseline: {baseline_file.name}")
        return baseline
    
    def generate_regression_report(self, violations, regressions, results):
        """Generate comprehensive regression report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'commit_sha': os.getenv('GITHUB_SHA', 'unknown'),
            'branch': os.getenv('GITHUB_REF_NAME', 'unknown'),
            'constitutional_violations': violations,
            'performance_regressions': regressions,
            'summary': {
                'total_violations': len(violations),
                'total_regressions': len(regressions),
                'critical_issues': len([
                    v for v in violations + regressions 
                    if v.get('severity') == 'critical'
                ]),
                'compliance_rate': results.get('summary', {}).get('compliance_rate', 0),
                'overall_status': 'FAIL' if violations or regressions else 'PASS'
            },
            'constitutional_requirements': self.CONSTITUTIONAL_THRESHOLDS
        }
        
        # Save report
        with open('regression_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def print_report(self, violations, regressions, results):
        """Print human-readable regression report"""
        print("\n🎯 CONSTITUTIONAL PERFORMANCE REGRESSION ANALYSIS")
        print("=" * 60)
        
        # Constitutional violations
        if violations:
            print(f"\n❌ CONSTITUTIONAL VIOLATIONS ({len(violations)})")
            for v in violations:
                print(f"  {v['domain']}: {v['avg_response_time']:.1f}ms > "
                      f"{v['constitutional_threshold']}ms "
                      f"({v['violation_factor']:.2f}x threshold)")
        
        # Performance regressions
        if regressions:
            print(f"\n📉 PERFORMANCE REGRESSIONS ({len(regressions)})")
            for r in regressions:
                print(f"  {r['domain']}: {r['current_avg']:.1f}ms vs "
                      f"{r['baseline_avg']:.1f}ms baseline "
                      f"(+{r['regression_percent']:.1f}%)")
        
        # Summary
        compliance_rate = results.get('summary', {}).get('compliance_rate', 0)
        print(f"\n📊 SUMMARY")
        print(f"Constitutional Compliance: {compliance_rate:.1%}")
        print(f"Violations: {len(violations)}")
        print(f"Regressions: {len(regressions)}")
        
        if not violations and not regressions:
            print("✅ All constitutional performance requirements met!")
        else:
            print("❌ Performance issues detected - see details above")
    
    def run_analysis(self):
        """Run complete regression analysis"""
        print("🔍 Starting Performance Regression Analysis")
        
        # Load current results
        current_results = self.load_current_results()
        if not current_results:
            return 1
        
        # Load baseline
        baseline = self.load_baseline()
        
        # Detect constitutional violations
        violations = self.detect_constitutional_violations(current_results)
        
        # Detect regressions against baseline
        regressions = self.detect_performance_regressions(current_results, baseline)
        
        # Generate and save report
        report = self.generate_regression_report(violations, regressions, current_results)
        
        # Print results
        self.print_report(violations, regressions, current_results)
        
        # Create baseline if none exists and results are clean
        if not baseline and not violations:
            self.create_baseline(current_results)
        
        # Return exit code
        return 1 if violations or regressions else 0


def main():
    """Main CLI entry point"""
    detector = PerformanceRegressionDetector()
    exit_code = detector.run_analysis()
    
    if exit_code == 0:
        print("\n🎉 Performance validation passed!")
    else:
        print("\n💥 Performance validation failed!")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()