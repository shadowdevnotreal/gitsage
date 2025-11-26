#!/usr/bin/env python3
"""
Smart Project Type Detector
============================
Auto-detect project type from codebase analysis.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ProjectDetector:
    """Intelligently detect project type from codebase"""

    PROJECT_TYPES = {
        'npm-package': {
            'files': ['package.json'],
            'optional': ['tsconfig.json', 'webpack.config.js'],
            'indicators': {'package.json': ['main', 'module', 'types']}
        },
        'python-library': {
            'files': ['setup.py', 'pyproject.toml'],
            'optional': ['setup.cfg', 'MANIFEST.in'],
            'indicators': {'setup.py': ['setup('], 'pyproject.toml': ['[project]']}
        },
        'cli-tool': {
            'files': ['main.py', 'cli.py', '__main__.py'],
            'optional': ['argparse', 'click', 'typer'],
            'indicators': {'*.py': ['argparse', 'click.command', '@click.', 'typer.Typer']}
        },
        'web-application': {
            'files': ['app.py', 'server.py', 'wsgi.py'],
            'optional': ['requirements.txt', 'Procfile'],
            'indicators': {'*.py': ['Flask', 'FastAPI', 'Django', 'app.route']}
        },
        'data-science': {
            'files': ['*.ipynb'],
            'optional': ['requirements.txt', 'environment.yml'],
            'indicators': {'*.py': ['pandas', 'numpy', 'sklearn', 'tensorflow', 'torch']}
        },
        'mobile-app': {
            'files': ['android/', 'ios/', 'app.json'],
            'optional': ['package.json', 'metro.config.js'],
            'indicators': {'package.json': ['react-native', 'expo']}
        },
        'wordpress-plugin': {
            'files': ['*.php'],
            'optional': ['readme.txt', 'composer.json'],
            'indicators': {'*.php': ['Plugin Name:', 'add_action', 'add_filter']}
        },
        'blockchain': {
            'files': ['contracts/', 'truffle-config.js', 'hardhat.config.js'],
            'optional': ['migrations/', 'test/'],
            'indicators': {'*.sol': ['pragma solidity', 'contract ']}
        },
        'docker-app': {
            'files': ['Dockerfile', 'docker-compose.yml'],
            'optional': ['.dockerignore', 'docker-compose.yaml'],
            'indicators': {}
        }
    }

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)

    def detect(self) -> Dict[str, any]:
        """
        Detect project type and return comprehensive analysis

        Returns:
            Dict with detected_type, confidence, technologies, and suggestions
        """
        results = {
            'detected_type': None,
            'confidence': 0.0,
            'technologies': [],
            'languages': {},
            'frameworks': [],
            'suggestions': []
        }

        # Detect languages
        results['languages'] = self._detect_languages()

        # Detect project type
        type_scores = {}
        for ptype, criteria in self.PROJECT_TYPES.items():
            score = self._score_project_type(ptype, criteria)
            if score > 0:
                type_scores[ptype] = score

        if type_scores:
            best_type = max(type_scores, key=type_scores.get)
            results['detected_type'] = best_type
            results['confidence'] = min(type_scores[best_type] / 10.0, 1.0)

        # Detect frameworks and technologies
        results['frameworks'] = self._detect_frameworks()
        results['technologies'] = self._detect_technologies()

        # Generate suggestions
        results['suggestions'] = self._generate_suggestions(results)

        return results

    def _detect_languages(self) -> Dict[str, int]:
        """Detect programming languages and count files"""
        extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React/TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.sol': 'Solidity'
        }

        language_counts = {}

        for ext, lang in extensions.items():
            files = list(self.repo_path.rglob(f'*{ext}'))
            # Exclude common directories
            files = [f for f in files if not any(
                part.startswith('.') or part in ['node_modules', 'venv', 'build', 'dist']
                for part in f.parts
            )]

            if files:
                language_counts[lang] = len(files)

        return dict(sorted(language_counts.items(), key=lambda x: x[1], reverse=True))

    def _score_project_type(self, ptype: str, criteria: Dict) -> int:
        """Score how well the project matches a type"""
        score = 0

        # Check required files
        for file_pattern in criteria.get('files', []):
            if self._find_files(file_pattern):
                score += 5

        # Check optional files
        for file_pattern in criteria.get('optional', []):
            if self._find_files(file_pattern):
                score += 2

        # Check indicators in file content
        for file_pattern, keywords in criteria.get('indicators', {}).items():
            files = self._find_files(file_pattern)
            for file in files[:5]:  # Check first 5 matching files
                try:
                    content = file.read_text(encoding='utf-8', errors='ignore')
                    for keyword in keywords:
                        if keyword in content:
                            score += 3
                            break
                except Exception:
                    pass

        return score

    def _find_files(self, pattern: str) -> List[Path]:
        """Find files matching pattern"""
        if pattern.endswith('/'):
            # Directory pattern
            return [p for p in self.repo_path.rglob('*') if p.is_dir() and p.name == pattern.rstrip('/')]
        elif '*' in pattern:
            # Glob pattern
            return list(self.repo_path.rglob(pattern))
        else:
            # Exact filename
            file_path = self.repo_path / pattern
            return [file_path] if file_path.exists() else []

    def _detect_frameworks(self) -> List[str]:
        """Detect frameworks used in the project"""
        frameworks = []

        # Check package.json for JS frameworks
        package_json = self.repo_path / 'package.json'
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

                framework_map = {
                    'react': 'React',
                    'vue': 'Vue.js',
                    'angular': 'Angular',
                    'next': 'Next.js',
                    'express': 'Express.js',
                    'nestjs': 'NestJS',
                    'svelte': 'Svelte'
                }

                for pkg, fw in framework_map.items():
                    if any(pkg in dep.lower() for dep in deps.keys()):
                        frameworks.append(fw)
            except Exception:
                pass

        # Check requirements.txt / pyproject.toml for Python frameworks
        req_files = ['requirements.txt', 'pyproject.toml', 'setup.py']
        for req_file in req_files:
            req_path = self.repo_path / req_file
            if req_path.exists():
                try:
                    content = req_path.read_text().lower()

                    framework_map = {
                        'django': 'Django',
                        'flask': 'Flask',
                        'fastapi': 'FastAPI',
                        'pyramid': 'Pyramid',
                        'tornado': 'Tornado',
                        'streamlit': 'Streamlit',
                        'tensorflow': 'TensorFlow',
                        'pytorch': 'PyTorch',
                        'scikit-learn': 'scikit-learn'
                    }

                    for pkg, fw in framework_map.items():
                        if pkg in content and fw not in frameworks:
                            frameworks.append(fw)
                except Exception:
                    pass

        return frameworks

    def _detect_technologies(self) -> List[str]:
        """Detect technologies and tools"""
        technologies = []

        tech_files = {
            'Docker': ['Dockerfile', 'docker-compose.yml'],
            'Kubernetes': ['k8s/', 'kubernetes/'],
            'GitHub Actions': ['.github/workflows/'],
            'CircleCI': ['.circleci/'],
            'Travis CI': ['.travis.yml'],
            'Jest': ['jest.config.js'],
            'Pytest': ['pytest.ini', 'pyproject.toml'],
            'Webpack': ['webpack.config.js'],
            'Vite': ['vite.config.js'],
            'TypeScript': ['tsconfig.json'],
            'ESLint': ['.eslintrc.js', '.eslintrc.json'],
            'Prettier': ['.prettierrc'],
            'GitBook': ['book.json', 'SUMMARY.md'],
            'Sphinx': ['conf.py', 'docs/conf.py'],
            'MkDocs': ['mkdocs.yml']
        }

        for tech, files in tech_files.items():
            for file_pattern in files:
                if self._find_files(file_pattern):
                    technologies.append(tech)
                    break

        return technologies

    def _generate_suggestions(self, results: Dict) -> List[str]:
        """Generate helpful suggestions based on detection"""
        suggestions = []

        detected_type = results.get('detected_type')

        if detected_type == 'python-library':
            if not self._find_files('setup.py') and not self._find_files('pyproject.toml'):
                suggestions.append("Add setup.py or pyproject.toml for package distribution")
            if not self._find_files('tests/'):
                suggestions.append("Create tests/ directory with pytest or unittest")

        elif detected_type == 'npm-package':
            package_json = self.repo_path / 'package.json'
            if package_json.exists():
                try:
                    data = json.loads(package_json.read_text())
                    if 'main' not in data:
                        suggestions.append("Add 'main' field to package.json")
                    if 'types' not in data and 'TypeScript' in results.get('technologies', []):
                        suggestions.append("Add 'types' field for TypeScript definitions")
                except Exception:
                    pass

        elif detected_type == 'web-application':
            if 'Docker' not in results.get('technologies', []):
                suggestions.append("Consider adding Dockerfile for deployment")
            if not any('CI' in tech for tech in results.get('technologies', [])):
                suggestions.append("Setup CI/CD with GitHub Actions or similar")

        # General suggestions
        if not self._find_files('README.md'):
            suggestions.append("Create README.md with project documentation")

        if not self._find_files('LICENSE'):
            suggestions.append("Add LICENSE file (MIT, Apache 2.0, etc.)")

        if not self._find_files('.gitignore'):
            suggestions.append("Add .gitignore to prevent committing unwanted files")

        return suggestions

    def get_template_recommendation(self) -> str:
        """Get recommended template based on detection"""
        detection = self.detect()
        detected_type = detection.get('detected_type')

        # Map detected types to template types
        template_map = {
            'npm-package': 'npm-package',
            'python-library': 'python-library',
            'cli-tool': 'cli-tool',
            'web-application': 'web-application',
            'data-science': 'data-science',
            'mobile-app': 'mobile-app',
            'wordpress-plugin': 'wordpress-plugin',
            'blockchain': 'blockchain'
        }

        return template_map.get(detected_type, 'cli-tool')  # Default to cli-tool

    def display_detection_results(self, console=None):
        """Display detection results in a nice format"""
        results = self.detect()

        if console:
            from rich.table import Table
            from rich.panel import Panel

            # Languages table
            if results['languages']:
                lang_table = Table(title="📝 Detected Languages")
                lang_table.add_column("Language", style="cyan")
                lang_table.add_column("Files", style="green")

                for lang, count in results['languages'].items():
                    lang_table.add_row(lang, str(count))

                console.print(lang_table)

            # Project type
            if results['detected_type']:
                console.print(Panel(
                    f"[bold green]{results['detected_type']}[/bold green]\n"
                    f"Confidence: {results['confidence']*100:.1f}%",
                    title="🎯 Detected Project Type"
                ))

            # Technologies
            if results['frameworks'] or results['technologies']:
                tech_list = results['frameworks'] + results['technologies']
                console.print(f"\n[bold cyan]🔧 Technologies:[/bold cyan] {', '.join(tech_list)}")

            # Suggestions
            if results['suggestions']:
                console.print("\n[bold yellow]💡 Suggestions:[/bold yellow]")
                for suggestion in results['suggestions']:
                    console.print(f"  • {suggestion}")
        else:
            # Plain text output
            print("\n" + "="*60)
            print("📝 PROJECT ANALYSIS")
            print("="*60)

            if results['languages']:
                print("\nDetected Languages:")
                for lang, count in results['languages'].items():
                    print(f"  • {lang}: {count} files")

            if results['detected_type']:
                print(f"\n🎯 Project Type: {results['detected_type']}")
                print(f"   Confidence: {results['confidence']*100:.1f}%")

            if results['frameworks']:
                print(f"\n🔧 Frameworks: {', '.join(results['frameworks'])}")

            if results['technologies']:
                print(f"\n🛠️  Technologies: {', '.join(results['technologies'])}")

            if results['suggestions']:
                print("\n💡 Suggestions:")
                for suggestion in results['suggestions']:
                    print(f"  • {suggestion}")

            print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    detector = ProjectDetector()
    detector.display_detection_results()
