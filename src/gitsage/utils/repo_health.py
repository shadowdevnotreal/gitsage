#!/usr/bin/env python3
"""
Repository Health Checker
==========================
Analyze repository and teach GitHub best practices.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class RepositoryHealthChecker:
    """Analyze repository health and provide educational feedback"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.checks = {}

    def check_all(self) -> Dict[str, any]:
        """
        Run all health checks

        Returns:
            Dict with overall_score, checks, and recommendations
        """
        results = {
            'overall_score': 0,
            'max_score': 100,
            'checks': {},
            'recommendations': [],
            'quick_wins': [],
            'critical_issues': []
        }

        # Run all checks
        checks = [
            self._check_readme(),
            self._check_license(),
            self._check_contributing(),
            self._check_gitignore(),
            self._check_code_of_conduct(),
            self._check_security_policy(),
            self._check_github_actions(),
            self._check_issues_enabled(),
            self._check_wiki_enabled(),
            self._check_repo_description(),
            self._check_topics(),
            self._check_branch_protection(),
            self._check_documentation(),
        ]

        for check_result in checks:
            name = check_result['name']
            results['checks'][name] = check_result
            results['overall_score'] += check_result['score']

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results['checks'])
        results['quick_wins'] = self._identify_quick_wins(results['checks'])
        results['critical_issues'] = self._identify_critical_issues(results['checks'])

        return results

    def _check_readme(self) -> Dict:
        """Check README.md existence and quality"""
        readme_path = self.repo_path / 'README.md'

        if not readme_path.exists():
            return {
                'name': 'README.md',
                'status': 'missing',
                'score': 0,
                'max_score': 15,
                'message': '❌ Missing - Your project needs a README!',
                'priority': 'critical',
                'fix_time': '10 minutes',
                'learn_url': 'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes'
            }

        # Check README quality
        content = readme_path.read_text()
        score = 5  # Base score for having README

        quality_checks = {
            'has_title': any(line.startswith('# ') for line in content.split('\n')),
            'has_description': len(content) > 100,
            'has_installation': 'install' in content.lower(),
            'has_usage': 'usage' in content.lower() or 'example' in content.lower(),
            'has_badges': 'shields.io' in content or '![' in content,
            'has_toc': 'table of contents' in content.lower() or '## Contents' in content,
        }

        score += sum(2 for check in quality_checks.values() if check)

        return {
            'name': 'README.md',
            'status': 'good' if score >= 12 else 'basic',
            'score': min(score, 15),
            'max_score': 15,
            'message': f'✓ Exists ({score}/15 quality points)',
            'priority': 'normal',
            'quality_checks': quality_checks
        }

    def _check_license(self) -> Dict:
        """Check for LICENSE file"""
        license_files = ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'COPYING']

        for lic in license_files:
            if (self.repo_path / lic).exists():
                return {
                    'name': 'LICENSE',
                    'status': 'good',
                    'score': 10,
                    'max_score': 10,
                    'message': '✓ License file exists',
                    'priority': 'normal'
                }

        return {
            'name': 'LICENSE',
            'status': 'missing',
            'score': 0,
            'max_score': 10,
            'message': '⚠️  Add a license - Learn: choosealicense.com',
            'priority': 'high',
            'fix_time': '2 minutes',
            'learn_url': 'https://choosealicense.com'
        }

    def _check_contributing(self) -> Dict:
        """Check for CONTRIBUTING.md"""
        contrib_path = self.repo_path / 'CONTRIBUTING.md'

        if contrib_path.exists():
            return {
                'name': 'CONTRIBUTING.md',
                'status': 'good',
                'score': 8,
                'max_score': 8,
                'message': '✓ Contributing guidelines exist',
                'priority': 'normal'
            }

        return {
            'name': 'CONTRIBUTING.md',
            'status': 'missing',
            'score': 0,
            'max_score': 8,
            'message': '💡 Optional - Helps contributors understand how to help',
            'priority': 'low',
            'fix_time': '15 minutes',
            'learn_url': 'https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors'
        }

    def _check_gitignore(self) -> Dict:
        """Check for .gitignore"""
        gitignore_path = self.repo_path / '.gitignore'

        if not gitignore_path.exists():
            return {
                'name': '.gitignore',
                'status': 'missing',
                'score': 0,
                'max_score': 10,
                'message': '❌ Critical - Prevents committing secrets & build files',
                'priority': 'critical',
                'fix_time': '3 minutes',
                'learn_url': 'https://git-scm.com/docs/gitignore'
            }

        # Check quality
        content = gitignore_path.read_text()
        has_common_patterns = any(pattern in content for pattern in [
            'node_modules', '__pycache__', '.env', '*.pyc', 'dist/', 'build/'
        ])

        return {
            'name': '.gitignore',
            'status': 'good' if has_common_patterns else 'basic',
            'score': 10 if has_common_patterns else 5,
            'max_score': 10,
            'message': '✓ .gitignore exists' + ('' if has_common_patterns else ' (basic)'),
            'priority': 'normal'
        }

    def _check_code_of_conduct(self) -> Dict:
        """Check for CODE_OF_CONDUCT.md"""
        coc_path = self.repo_path / 'CODE_OF_CONDUCT.md'

        if coc_path.exists():
            return {
                'name': 'CODE_OF_CONDUCT.md',
                'status': 'good',
                'score': 5,
                'max_score': 5,
                'message': '✓ Code of Conduct exists',
                'priority': 'normal'
            }

        return {
            'name': 'CODE_OF_CONDUCT.md',
            'status': 'missing',
            'score': 0,
            'max_score': 5,
            'message': '💡 Optional - Sets community standards',
            'priority': 'low',
            'fix_time': '5 minutes',
            'learn_url': 'https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project'
        }

    def _check_security_policy(self) -> Dict:
        """Check for SECURITY.md"""
        security_path = self.repo_path / 'SECURITY.md'

        if security_path.exists():
            return {
                'name': 'SECURITY.md',
                'status': 'good',
                'score': 5,
                'max_score': 5,
                'message': '✓ Security policy exists',
                'priority': 'normal'
            }

        return {
            'name': 'SECURITY.md',
            'status': 'missing',
            'score': 0,
            'max_score': 5,
            'message': '💡 Optional - Explains how to report vulnerabilities',
            'priority': 'low',
            'fix_time': '10 minutes'
        }

    def _check_github_actions(self) -> Dict:
        """Check for GitHub Actions workflows"""
        workflows_dir = self.repo_path / '.github' / 'workflows'

        if workflows_dir.exists() and list(workflows_dir.glob('*.yml')):
            return {
                'name': 'GitHub Actions',
                'status': 'good',
                'score': 10,
                'max_score': 10,
                'message': '✓ CI/CD workflows configured',
                'priority': 'normal'
            }

        return {
            'name': 'GitHub Actions',
            'status': 'missing',
            'score': 0,
            'max_score': 10,
            'message': '💡 Add CI/CD automation for testing & deployment',
            'priority': 'medium',
            'fix_time': '20 minutes',
            'learn_url': 'https://docs.github.com/en/actions/quickstart'
        }

    def _check_issues_enabled(self) -> Dict:
        """Check if issues are enabled (requires GitHub API or git config)"""
        # This is a placeholder - actual check would need GitHub API
        return {
            'name': 'Issues',
            'status': 'unknown',
            'score': 5,  # Assume enabled
            'max_score': 5,
            'message': '? Enable in Settings → Features → Issues',
            'priority': 'low'
        }

    def _check_wiki_enabled(self) -> Dict:
        """Check if wiki is enabled"""
        # This is a placeholder - actual check would need GitHub API
        return {
            'name': 'Wiki',
            'status': 'unknown',
            'score': 3,  # Assume not enabled
            'max_score': 5,
            'message': '⚠️  Enable in Settings → Features → Wiki',
            'priority': 'low',
            'fix_time': '30 seconds',
            'learn_url': 'https://docs.github.com/en/communities/documenting-your-project-with-wikis'
        }

    def _check_repo_description(self) -> Dict:
        """Check for repository description (placeholder)"""
        return {
            'name': 'Description',
            'status': 'unknown',
            'score': 0,
            'max_score': 3,
            'message': '? Add repository description in GitHub settings',
            'priority': 'medium',
            'fix_time': '1 minute'
        }

    def _check_topics(self) -> Dict:
        """Check for repository topics (placeholder)"""
        return {
            'name': 'Topics',
            'status': 'unknown',
            'score': 0,
            'max_score': 3,
            'message': '? Add 3-5 topics to improve discoverability',
            'priority': 'medium',
            'fix_time': '2 minutes'
        }

    def _check_branch_protection(self) -> Dict:
        """Check for branch protection rules (placeholder)"""
        return {
            'name': 'Branch Protection',
            'status': 'unknown',
            'score': 0,
            'max_score': 5,
            'message': '💡 Protect main branch (require PR reviews)',
            'priority': 'medium',
            'learn_url': 'https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches'
        }

    def _check_documentation(self) -> Dict:
        """Check for additional documentation"""
        docs_dir = self.repo_path / 'docs'
        has_docs = docs_dir.exists() and any(docs_dir.glob('*.md'))

        if has_docs:
            return {
                'name': 'Documentation',
                'status': 'good',
                'score': 6,
                'max_score': 6,
                'message': '✓ Documentation directory exists',
                'priority': 'normal'
            }

        return {
            'name': 'Documentation',
            'status': 'missing',
            'score': 0,
            'max_score': 6,
            'message': '💡 Create docs/ for detailed documentation',
            'priority': 'low',
            'fix_time': '30 minutes'
        }

    def _generate_recommendations(self, checks: Dict) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        for name, check in checks.items():
            if check['status'] in ['missing', 'basic'] and check.get('priority') in ['critical', 'high']:
                rec = f"{check['message']}"
                if 'fix_time' in check:
                    rec += f" ({check['fix_time']})"
                recommendations.append(rec)

        return recommendations

    def _identify_quick_wins(self, checks: Dict) -> List[Dict]:
        """Identify quick improvements (< 5 min)"""
        quick_wins = []

        for name, check in checks.items():
            if check['status'] == 'missing' and check.get('fix_time'):
                # Parse time (rough estimation)
                time_str = check['fix_time']
                if 'minute' in time_str:
                    minutes = int(''.join(filter(str.isdigit, time_str)))
                    if minutes <= 5:
                        quick_wins.append({
                            'name': name,
                            'time': time_str,
                            'points': check['max_score'],
                            'message': check['message']
                        })

        return sorted(quick_wins, key=lambda x: x['points'], reverse=True)

    def _identify_critical_issues(self, checks: Dict) -> List[str]:
        """Identify critical issues that need immediate attention"""
        critical = []

        for name, check in checks.items():
            if check.get('priority') == 'critical' and check['status'] != 'good':
                critical.append(f"{name}: {check['message']}")

        return critical

    def display_health_report(self, console=None):
        """Display comprehensive health report"""
        results = self.check_all()

        if console:
            from rich.panel import Panel
            from rich.table import Table
            from rich.progress import Progress, BarColumn, TextColumn

            # Overall score
            score_percent = (results['overall_score'] / results['max_score']) * 100
            score_color = 'green' if score_percent >= 80 else 'yellow' if score_percent >= 60 else 'red'

            console.print(Panel(
                f"[bold {score_color}]{results['overall_score']}/{results['max_score']} points ({score_percent:.1f}%)[/bold {score_color}]",
                title="🏥 Repository Health Score"
            ))

            # Critical issues
            if results['critical_issues']:
                console.print("\n[bold red]❌ Critical Issues:[/bold red]")
                for issue in results['critical_issues']:
                    console.print(f"  • {issue}")

            # Quick wins
            if results['quick_wins']:
                console.print("\n[bold green]⚡ Quick Wins (< 5 min):[/bold green]")
                for win in results['quick_wins'][:3]:
                    console.print(f"  • {win['name']} ({win['time']}) → +{win['points']} pts")

            # All checks
            console.print("\n[bold cyan]📋 All Checks:[/bold cyan]")
            check_table = Table()
            check_table.add_column("Check", style="cyan")
            check_table.add_column("Status", style="white")
            check_table.add_column("Score", style="green")

            for name, check in results['checks'].items():
                status_icon = {
                    'good': '✓',
                    'basic': '⚠',
                    'missing': '❌',
                    'unknown': '?'
                }.get(check['status'], '?')

                check_table.add_row(
                    name,
                    f"{status_icon} {check['status']}",
                    f"{check['score']}/{check['max_score']}"
                )

            console.print(check_table)

        else:
            # Plain text output
            print("\n" + "="*60)
            print("🏥 REPOSITORY HEALTH REPORT")
            print("="*60)

            score_percent = (results['overall_score'] / results['max_score']) * 100
            print(f"\nOverall Score: {results['overall_score']}/{results['max_score']} ({score_percent:.1f}%)")

            if results['critical_issues']:
                print("\n❌ CRITICAL ISSUES:")
                for issue in results['critical_issues']:
                    print(f"  • {issue}")

            if results['quick_wins']:
                print("\n⚡ QUICK WINS:")
                for win in results['quick_wins'][:3]:
                    print(f"  • {win['name']} ({win['time']}) → +{win['points']} pts")

            print("\n📋 ALL CHECKS:")
            for name, check in results['checks'].items():
                status = check['status']
                score = f"{check['score']}/{check['max_score']}"
                print(f"  {name:20s} [{status:8s}] {score}")

            print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    checker = RepositoryHealthChecker()
    checker.display_health_report()
