#!/usr/bin/env python3
"""
Repository Beautification Scorer
=================================
Gamify GitHub best practices with scoring and leveling system.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple
from .repo_health import RepositoryHealthChecker


class BeautificationScorer:
    """Gamify repository aesthetics with levels, achievements, and scores"""

    LEVELS = {
        'beginner': (0, 29, '🌱', 'Just Getting Started'),
        'intermediate': (30, 59, '🌿', 'Building Momentum'),
        'advanced': (60, 79, '🌳', 'Looking Professional'),
        'expert': (80, 94, '🌟', 'Production Ready'),
        'master': (95, 100, '💎', 'Open Source Champion')
    }

    ACHIEVEMENTS = {
        'first_readme': {'name': 'First Steps', 'desc': 'Created README.md', 'points': 5},
        'licensed': {'name': 'Licensed to Code', 'desc': 'Added LICENSE file', 'points': 5},
        'professional_docs': {'name': 'Documentation Master', 'desc': 'Complete documentation', 'points': 10},
        'ci_cd_setup': {'name': 'Automation Engineer', 'desc': 'Setup CI/CD pipeline', 'points': 10},
        'community_ready': {'name': 'Community Builder', 'desc': 'Contributing + CoC', 'points': 8},
        'security_conscious': {'name': 'Security First', 'desc': 'Added SECURITY.md', 'points': 5},
        'well_branded': {'name': 'Well Branded', 'desc': 'Description + topics + badges', 'points': 8},
        'wiki_master': {'name': 'Wiki Master', 'desc': 'Created comprehensive wiki', 'points': 10},
        'perfectionist': {'name': 'Perfectionist', 'desc': 'Achieved 100% score', 'points': 20}
    }

    CATEGORIES = {
        'documentation': {
            'name': 'Documentation',
            'emoji': '📚',
            'checks': ['README.md', 'Documentation', 'Wiki'],
            'max_points': 26
        },
        'community': {
            'name': 'Community',
            'emoji': '👥',
            'checks': ['CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'LICENSE'],
            'max_points': 23
        },
        'automation': {
            'name': 'Automation',
            'emoji': '🤖',
            'checks': ['GitHub Actions', 'Branch Protection'],
            'max_points': 15
        },
        'security': {
            'name': 'Security',
            'emoji': '🔒',
            'checks': ['SECURITY.md', '.gitignore'],
            'max_points': 15
        },
        'discoverability': {
            'name': 'Discoverability',
            'emoji': '🔍',
            'checks': ['Description', 'Topics'],
            'max_points': 6
        },
        'engagement': {
            'name': 'Engagement',
            'emoji': '💬',
            'checks': ['Issues'],
            'max_points': 5
        }
    }

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.health_checker = RepositoryHealthChecker(repo_path)

    def calculate_score(self) -> Dict:
        """
        Calculate comprehensive beautification score

        Returns:
            Dict with score, level, achievements, category_scores, and recommendations
        """
        health_results = self.health_checker.check_all()

        results = {
            'total_score': health_results['overall_score'],
            'max_score': health_results['max_score'],
            'percentage': (health_results['overall_score'] / health_results['max_score']) * 100,
            'level': None,
            'level_info': {},
            'achievements': [],
            'category_scores': {},
            'improvements': [],
            'next_milestone': None
        }

        # Determine level
        results['level'], results['level_info'] = self._get_level(results['percentage'])

        # Check achievements
        results['achievements'] = self._check_achievements(health_results['checks'])

        # Calculate category scores
        results['category_scores'] = self._calculate_category_scores(health_results['checks'])

        # Generate improvement suggestions
        results['improvements'] = self._generate_improvements(
            health_results['checks'],
            results['category_scores']
        )

        # Next milestone
        results['next_milestone'] = self._get_next_milestone(results['percentage'])

        return results

    def _get_level(self, percentage: float) -> Tuple[str, Dict]:
        """Determine level based on percentage score"""
        for level_name, (min_score, max_score, emoji, description) in self.LEVELS.items():
            if min_score <= percentage <= max_score:
                return level_name, {
                    'name': level_name,
                    'min': min_score,
                    'max': max_score,
                    'emoji': emoji,
                    'description': description
                }
        return 'beginner', self.LEVELS['beginner']

    def _check_achievements(self, checks: Dict) -> List[Dict]:
        """Check which achievements have been unlocked"""
        unlocked = []

        # First README
        if checks.get('README.md', {}).get('status') in ['good', 'basic']:
            unlocked.append(self.ACHIEVEMENTS['first_readme'])

        # Licensed
        if checks.get('LICENSE', {}).get('status') == 'good':
            unlocked.append(self.ACHIEVEMENTS['licensed'])

        # Professional docs
        readme_good = checks.get('README.md', {}).get('status') == 'good'
        docs_good = checks.get('Documentation', {}).get('status') == 'good'
        if readme_good and docs_good:
            unlocked.append(self.ACHIEVEMENTS['professional_docs'])

        # CI/CD
        if checks.get('GitHub Actions', {}).get('status') == 'good':
            unlocked.append(self.ACHIEVEMENTS['ci_cd_setup'])

        # Community ready
        contrib_good = checks.get('CONTRIBUTING.md', {}).get('status') == 'good'
        coc_good = checks.get('CODE_OF_CONDUCT.md', {}).get('status') == 'good'
        if contrib_good and coc_good:
            unlocked.append(self.ACHIEVEMENTS['community_ready'])

        # Security conscious
        if checks.get('SECURITY.md', {}).get('status') == 'good':
            unlocked.append(self.ACHIEVEMENTS['security_conscious'])

        return unlocked

    def _calculate_category_scores(self, checks: Dict) -> Dict[str, Dict]:
        """Calculate score for each category"""
        category_results = {}

        for cat_id, cat_info in self.CATEGORIES.items():
            total = 0
            max_total = 0

            for check_name in cat_info['checks']:
                if check_name in checks:
                    total += checks[check_name]['score']
                    max_total += checks[check_name]['max_score']

            percentage = (total / max_total * 100) if max_total > 0 else 0

            category_results[cat_id] = {
                'name': cat_info['name'],
                'emoji': cat_info['emoji'],
                'score': total,
                'max_score': max_total,
                'percentage': percentage,
                'status': self._get_category_status(percentage)
            }

        return category_results

    def _get_category_status(self, percentage: float) -> str:
        """Get status emoji for category"""
        if percentage >= 90:
            return '✅'
        elif percentage >= 70:
            return '⚠️'
        elif percentage >= 40:
            return '🔶'
        else:
            return '❌'

    def _generate_improvements(self, checks: Dict, category_scores: Dict) -> List[Dict]:
        """Generate prioritized improvement suggestions"""
        improvements = []

        # Find weakest categories
        weak_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1]['percentage']
        )[:3]

        for cat_id, cat_data in weak_categories:
            if cat_data['percentage'] < 80:
                improvement = {
                    'category': cat_data['name'],
                    'emoji': cat_data['emoji'],
                    'current': f"{cat_data['percentage']:.0f}%",
                    'suggestions': []
                }

                # Find missing checks in this category
                cat_info = self.CATEGORIES[cat_id]
                for check_name in cat_info['checks']:
                    if check_name in checks and checks[check_name]['status'] != 'good':
                        improvement['suggestions'].append({
                            'name': check_name,
                            'message': checks[check_name]['message'],
                            'points': checks[check_name]['max_score'],
                            'time': checks[check_name].get('fix_time', 'Unknown')
                        })

                if improvement['suggestions']:
                    improvements.append(improvement)

        return improvements

    def _get_next_milestone(self, current_percentage: float) -> Dict:
        """Get next level milestone and how to reach it"""
        for level_name, (min_score, max_score, emoji, description) in self.LEVELS.items():
            if max_score > current_percentage:
                points_needed = max_score - current_percentage
                return {
                    'level': level_name,
                    'emoji': emoji,
                    'description': description,
                    'target': max_score,
                    'points_needed': f"{points_needed:.1f}",
                    'percentage_needed': f"{points_needed:.0f}%"
                }

        return None

    def display_beautification_report(self, console=None):
        """Display gamified beautification report"""
        results = self.calculate_score()

        if console:
            from rich.panel import Panel
            from rich.table import Table
            from rich.progress import Progress, BarColumn, TextColumn
            from rich import box

            # Main score panel
            level_info = results['level_info']
            console.print(Panel(
                f"[bold cyan]{level_info['emoji']} {level_info['name'].upper()}[/bold cyan]\n"
                f"[italic]{level_info['description']}[/italic]\n\n"
                f"Score: [bold green]{results['total_score']}/{results['max_score']}[/bold green] "
                f"([bold yellow]{results['percentage']:.1f}%[/bold yellow])",
                title="🌟 Repository Beautification Score",
                border_style="cyan"
            ))

            # Achievements
            if results['achievements']:
                console.print("\n[bold yellow]🏆 Achievements Unlocked:[/bold yellow]")
                for achievement in results['achievements']:
                    console.print(
                        f"  • [green]{achievement['name']}[/green]: {achievement['desc']} "
                        f"[dim](+{achievement['points']} pts)[/dim]"
                    )

            # Category scores
            console.print("\n[bold cyan]📊 Category Breakdown:[/bold cyan]")
            cat_table = Table(show_header=True, box=box.ROUNDED)
            cat_table.add_column("Category", style="cyan")
            cat_table.add_column("Status", justify="center")
            cat_table.add_column("Score", justify="right")
            cat_table.add_column("Progress", justify="right")

            for cat_id, cat_data in results['category_scores'].items():
                cat_table.add_row(
                    f"{cat_data['emoji']} {cat_data['name']}",
                    cat_data['status'],
                    f"{cat_data['score']}/{cat_data['max_score']}",
                    f"{cat_data['percentage']:.0f}%"
                )

            console.print(cat_table)

            # Improvements
            if results['improvements']:
                console.print("\n[bold yellow]💡 Top Improvements:[/bold yellow]")
                for imp in results['improvements'][:2]:
                    console.print(f"\n  {imp['emoji']} [cyan]{imp['category']}[/cyan] ({imp['current']})")
                    for sug in imp['suggestions'][:2]:
                        console.print(
                            f"    • {sug['name']}: {sug['message']} "
                            f"[dim](+{sug['points']} pts, ~{sug['time']})[/dim]"
                        )

            # Next milestone
            if results['next_milestone']:
                milestone = results['next_milestone']
                console.print(Panel(
                    f"Next Level: [bold green]{milestone['emoji']} {milestone['level'].upper()}[/bold green]\n"
                    f"{milestone['description']}\n\n"
                    f"Need: [yellow]{milestone['percentage_needed']}%[/yellow] more points",
                    title="🎯 Next Milestone",
                    border_style="yellow"
                ))

        else:
            # Plain text output
            print("\n" + "="*60)
            print("🌟 REPOSITORY BEAUTIFICATION SCORE")
            print("="*60)

            level_info = results['level_info']
            print(f"\n{level_info['emoji']} Level: {level_info['name'].upper()}")
            print(f"   {level_info['description']}")
            print(f"\nScore: {results['total_score']}/{results['max_score']} ({results['percentage']:.1f}%)")

            if results['achievements']:
                print("\n🏆 ACHIEVEMENTS:")
                for achievement in results['achievements']:
                    print(f"  • {achievement['name']}: {achievement['desc']} (+{achievement['points']} pts)")

            print("\n📊 CATEGORY BREAKDOWN:")
            for cat_id, cat_data in results['category_scores'].items():
                print(
                    f"  {cat_data['status']} {cat_data['emoji']} {cat_data['name']}: "
                    f"{cat_data['score']}/{cat_data['max_score']} ({cat_data['percentage']:.0f}%)"
                )

            if results['improvements']:
                print("\n💡 TOP IMPROVEMENTS:")
                for imp in results['improvements'][:2]:
                    print(f"\n  {imp['emoji']} {imp['category']} ({imp['current']})")
                    for sug in imp['suggestions'][:2]:
                        print(f"    • {sug['name']}: +{sug['points']} pts (~{sug['time']})")

            if results['next_milestone']:
                milestone = results['next_milestone']
                print(f"\n🎯 NEXT MILESTONE: {milestone['emoji']} {milestone['level'].upper()}")
                print(f"   {milestone['description']}")
                print(f"   Need: {milestone['percentage_needed']}% more points")

            print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    scorer = BeautificationScorer()
    scorer.display_beautification_report()
