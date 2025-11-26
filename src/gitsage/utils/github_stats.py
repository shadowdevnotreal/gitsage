#!/usr/bin/env python3
"""
GitHub Stats Integration
========================
Generate badges, stats, and visual repository statistics.
"""

from pathlib import Path
from typing import Dict, List, Optional
import subprocess


class GitHubStatsGenerator:
    """Generate GitHub badges, stats, and visualizations"""

    BADGE_STYLES = ['flat', 'flat-square', 'plastic', 'for-the-badge', 'social']

    def __init__(self, username: str = None, repo: str = None, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.username = username or self._detect_github_username()
        self.repo = repo or self._detect_repo_name()

    def _detect_github_username(self) -> str:
        """Detect GitHub username from git remote"""
        try:
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            url = result.stdout.strip()

            # Parse GitHub URL
            if 'github.com' in url:
                # https://github.com/username/repo.git
                # git@github.com:username/repo.git
                parts = url.replace('.git', '').split('/')
                if len(parts) >= 2:
                    username = parts[-2].split(':')[-1]
                    return username
        except Exception:
            pass

        return 'username'

    def _detect_repo_name(self) -> str:
        """Detect repository name from git remote"""
        try:
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            url = result.stdout.strip()

            # Parse repo name
            if 'github.com' in url:
                parts = url.replace('.git', '').split('/')
                if parts:
                    return parts[-1]
        except Exception:
            pass

        return self.repo_path.name

    def generate_badge(self, badge_type: str, style: str = 'flat', **kwargs) -> str:
        """
        Generate shields.io badge markdown

        Args:
            badge_type: Type of badge (license, version, build, etc.)
            style: Badge style (flat, flat-square, etc.)
            **kwargs: Additional parameters (label, message, color, etc.)

        Returns:
            Markdown string for badge
        """
        base_url = "https://img.shields.io"

        badge_templates = {
            'license': f"github/license/{self.username}/{self.repo}",
            'version': f"github/v/release/{self.username}/{self.repo}",
            'release-date': f"github/release-date/{self.username}/{self.repo}",
            'stars': f"github/stars/{self.username}/{self.repo}",
            'forks': f"github/forks/{self.username}/{self.repo}",
            'issues': f"github/issues/{self.username}/{self.repo}",
            'issues-closed': f"github/issues-closed/{self.username}/{self.repo}",
            'prs': f"github/issues-pr/{self.username}/{self.repo}",
            'prs-closed': f"github/issues-pr-closed/{self.username}/{self.repo}",
            'contributors': f"github/contributors/{self.username}/{self.repo}",
            'commit-activity': f"github/commit-activity/m/{self.username}/{self.repo}",
            'last-commit': f"github/last-commit/{self.username}/{self.repo}",
            'code-size': f"github/languages/code-size/{self.username}/{self.repo}",
            'repo-size': f"github/repo-size/{self.username}/{self.repo}",
            'downloads': f"github/downloads/{self.username}/{self.repo}/total",
            'top-language': f"github/languages/top/{self.username}/{self.repo}",
        }

        # Custom badges
        if badge_type == 'custom':
            label = kwargs.get('label', 'badge')
            message = kwargs.get('message', 'message')
            color = kwargs.get('color', 'blue')
            badge_url = f"{base_url}/badge/{label}-{message}-{color}?style={style}"
        elif badge_type == 'maintained':
            badge_url = f"{base_url}/badge/Maintained%3F-yes-green.svg?style={style}"
        elif badge_type == 'pr-welcome':
            badge_url = f"{base_url}/badge/PRs-welcome-brightgreen.svg?style={style}"
        elif badge_type in badge_templates:
            badge_url = f"{base_url}/{badge_templates[badge_type]}?style={style}"
        else:
            return ""

        # Create markdown
        alt_text = badge_type.replace('-', ' ').title()
        return f"![{alt_text}]({badge_url})"

    def generate_badge_set(self, badges: List[str], style: str = 'flat') -> str:
        """
        Generate a set of badges

        Args:
            badges: List of badge types to include
            style: Badge style

        Returns:
            Markdown string with all badges
        """
        badge_lines = []

        for badge_type in badges:
            badge_md = self.generate_badge(badge_type, style)
            if badge_md:
                badge_lines.append(badge_md)

        return '\n'.join(badge_lines)

    def generate_stats_section(self) -> str:
        """Generate comprehensive stats section for README"""
        stats_md = f"""## 📊 Repository Stats

![Contributors](https://img.shields.io/github/contributors/{self.username}/{self.repo})
![Last Commit](https://img.shields.io/github/last-commit/{self.username}/{self.repo})
![Commit Activity](https://img.shields.io/github/commit-activity/m/{self.username}/{self.repo})
![Code Size](https://img.shields.io/github/languages/code-size/{self.username}/{self.repo})
![Top Language](https://img.shields.io/github/languages/top/{self.username}/{self.repo})

"""
        return stats_md

    def generate_profile_stats_card(self) -> str:
        """Generate GitHub Stats card using github-readme-stats"""
        return f"""[![{self.username}'s GitHub Stats](https://github-readme-stats.vercel.app/api?username={self.username}&show_icons=true&theme=default)](https://github.com/{self.username})
"""

    def generate_language_stats_card(self) -> str:
        """Generate language stats card"""
        return f"""[![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={self.username}&layout=compact)](https://github.com/{self.username}/{self.repo})
"""

    def generate_trophy_section(self) -> str:
        """Generate GitHub trophy section"""
        return f"""## 🏆 GitHub Trophies

[![trophy](https://github-profile-trophy.vercel.app/?username={self.username}&theme=onedark&no-frame=true&no-bg=true&margin-w=4)](https://github.com/{self.username})
"""

    def generate_contribution_graph(self) -> str:
        """Generate contribution activity graph"""
        return f"""## 📈 Contribution Activity

[![{self.username}'s Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username={self.username}&theme=react-dark)](https://github.com/{self.username}/{self.repo})
"""

    def generate_standard_badges(self) -> str:
        """Generate standard badge set for most projects"""
        badges = [
            'license',
            'version',
            'stars',
            'forks',
            'issues',
            'last-commit',
            'maintained',
            'pr-welcome'
        ]

        badge_md = []
        for badge_type in badges:
            badge = self.generate_badge(badge_type, style='flat-square')
            if badge:
                badge_md.append(badge)

        return ' '.join(badge_md)

    def generate_social_badges(self) -> str:
        """Generate social media style badges"""
        badges = ['stars', 'forks', 'watchers']
        badge_md = []

        for badge_type in badges:
            badge = self.generate_badge(badge_type, style='social')
            if badge:
                badge_md.append(badge)

        return ' '.join(badge_md)

    def generate_quality_badges(self, ci_service: str = None) -> str:
        """
        Generate quality/CI badges

        Args:
            ci_service: CI service (github-actions, travis, circleci)
        """
        badges = []

        # CI/CD badge
        if ci_service == 'github-actions':
            badges.append(
                f"![CI](https://github.com/{self.username}/{self.repo}/workflows/CI/badge.svg)"
            )
        elif ci_service == 'travis':
            badges.append(
                f"![Build](https://travis-ci.org/{self.username}/{self.repo}.svg?branch=main)"
            )
        elif ci_service == 'circleci':
            badges.append(
                f"![CircleCI](https://circleci.com/gh/{self.username}/{self.repo}.svg?style=svg)"
            )

        # Coverage badge (placeholder)
        badges.append(
            f"![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg?style=flat-square)"
        )

        # Code quality badge (placeholder)
        badges.append(
            f"![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen.svg?style=flat-square)"
        )

        return ' '.join(badges)

    def generate_comprehensive_stats_readme(self, include_graphs: bool = True) -> str:
        """Generate a comprehensive stats section for README"""
        content = []

        # Standard badges
        content.append("<!-- Badges -->")
        content.append(self.generate_standard_badges())
        content.append("")

        # Stats section
        if include_graphs:
            content.append(self.generate_stats_section())
            content.append("")

            # GitHub stats cards
            content.append("### GitHub Stats")
            content.append("")
            content.append(self.generate_profile_stats_card())
            content.append("")

            # Language stats
            content.append("### Most Used Languages")
            content.append("")
            content.append(self.generate_language_stats_card())
            content.append("")

        return '\n'.join(content)

    def get_repo_info(self) -> Dict[str, str]:
        """Get detected repository information"""
        return {
            'username': self.username,
            'repo': self.repo,
            'github_url': f"https://github.com/{self.username}/{self.repo}",
            'wiki_url': f"https://github.com/{self.username}/{self.repo}/wiki",
            'issues_url': f"https://github.com/{self.username}/{self.repo}/issues"
        }


if __name__ == "__main__":
    # Example usage
    stats = GitHubStatsGenerator()
    info = stats.get_repo_info()

    print("Repository Info:")
    print(f"  Username: {info['username']}")
    print(f"  Repo: {info['repo']}")
    print(f"  URL: {info['github_url']}")
    print("\nGenerated Badges:")
    print(stats.generate_standard_badges())
