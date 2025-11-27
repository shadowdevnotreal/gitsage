"""GitSage Web Interface - Flask application."""

import os
from pathlib import Path
from typing import Optional

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
try:
    from flask_wtf.csrf import CSRFProtect
    CSRF_AVAILABLE = True
except ImportError:
    CSRF_AVAILABLE = False

from gitsage.__version__ import PROJECT_NAME, __version__
from gitsage.config import get_config
from gitsage.utils import EnvironmentDetector, get_logger

logger = get_logger(__name__)


def create_app(config: Optional[dict] = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    # Load configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["GITSAGE_VERSION"] = __version__
    app.config["PROJECT_NAME"] = PROJECT_NAME

    if config:
        app.config.update(config)

    # Enable CORS
    CORS(app)

    # Enable CSRF protection
    if CSRF_AVAILABLE:
        csrf = CSRFProtect()
        csrf.init_app(app)
        logger.info("CSRF protection enabled")
    else:
        logger.warning("Flask-WTF not installed, CSRF protection disabled. Install with: pip install Flask-WTF")

    # Security headers
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: https:;"
        return response

    # Initialize
    gitsage_config = get_config()

    @app.context_processor
    def inject_globals():
        """Inject global variables into templates."""
        return {
            "version": __version__,
            "project_name": PROJECT_NAME,
        }

    # Routes
    @app.route("/")
    def index():
        """Home page."""
        detector = EnvironmentDetector()
        env_info = detector.detect_all()

        return render_template("index.html", env_info=env_info)

    @app.route("/api/environment")
    def api_environment():
        """API endpoint for environment information."""
        detector = EnvironmentDetector()
        env_info = detector.detect_all()

        return jsonify(
            {
                "success": True,
                "data": env_info,
                "recommendations": [
                    {"priority": rec.priority, "message": rec.message, "action": rec.action}
                    for rec in detector.recommendations
                ],
            }
        )

    @app.route("/api/config")
    def api_config():
        """API endpoint for configuration."""
        config_data = gitsage_config.to_dict()
        return jsonify({"success": True, "data": config_data})

    @app.route("/generators")
    def generators():
        """Generators page."""
        return render_template("generators.html")

    @app.route("/repositories")
    def repositories():
        """Repositories browser page."""
        return render_template("repositories.html")

    @app.route("/backups")
    def backups():
        """Backups page."""
        backup_dir = Path.home() / ".gitsage" / "backups"
        backups = []

        if backup_dir.exists():
            for backup_file in backup_dir.glob("*.tar.gz"):
                backups.append(
                    {
                        "name": backup_file.name,
                        "size": backup_file.stat().st_size,
                        "created": backup_file.stat().st_mtime,
                    }
                )

        return render_template("backups.html", backups=backups)

    @app.route("/settings")
    def settings():
        """Settings page."""
        return render_template("settings.html", config=gitsage_config)

    @app.route("/api/settings", methods=["GET", "POST"])
    def api_settings():
        """API endpoint for settings."""
        if request.method == "POST":
            # Update settings
            data = request.get_json()
            # TODO: Update configuration
            return jsonify({"success": True, "message": "Settings updated"})
        else:
            return jsonify({"success": True, "data": gitsage_config.to_dict()})

    @app.route("/about")
    def about():
        """About page."""
        return render_template("about.html")

    # API Endpoints for Script Generation
    @app.route("/api/generate-script", methods=["POST"])
    def api_generate_script():
        """Generate a script based on template."""
        try:
            data = request.get_json()
            script_type = data.get("scriptType")
            script_name = data.get("scriptName", "generated-script")
            educational = data.get("educationalMode", True)

            # TODO: Implement actual script generation
            script_content = f"""#!/usr/bin/env bash
# Generated Script: {script_name}
# Type: {script_type}
# Generated by GitSage v{__version__}

echo "This is a placeholder for {script_type} script"
echo "Script generation will be fully implemented"
"""

            return jsonify({"success": True, "script": script_content, "name": script_name})
        except Exception as e:
            logger.error(f"Script generation error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # API Endpoints for Repository Browser
    @app.route("/api/repositories")
    def api_repositories():
        """Get list of repositories from GitHub."""
        try:
            import subprocess

            result = subprocess.run(
                [
                    "gh",
                    "repo",
                    "list",
                    "--json",
                    "name,description,url,isPrivate,stargazerCount,forkCount,primaryLanguage,defaultBranchRef,createdAt,updatedAt",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                import json

                repos = json.loads(result.stdout)
                formatted_repos = [
                    {
                        "name": repo.get("name"),
                        "full_name": repo.get("name"),
                        "description": repo.get("description"),
                        "url": repo.get("url"),
                        "private": repo.get("isPrivate", False),
                        "stars": repo.get("stargazerCount", 0),
                        "forks": repo.get("forkCount", 0),
                        "language": (
                            repo.get("primaryLanguage", {}).get("name")
                            if repo.get("primaryLanguage")
                            else None
                        ),
                        "default_branch": (
                            repo.get("defaultBranchRef", {}).get("name")
                            if repo.get("defaultBranchRef")
                            else "main"
                        ),
                        "created": repo.get("createdAt"),
                        "updated": repo.get("updatedAt"),
                        "clone_url": repo.get("url") + ".git" if repo.get("url") else None,
                    }
                    for repo in repos
                ]

                return jsonify({"success": True, "repositories": formatted_repos})
            else:
                return (
                    jsonify({"success": False, "error": "GitHub CLI not authenticated or failed"}),
                    500,
                )

        except Exception as e:
            logger.error(f"Repository fetch error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # API Endpoints for Backup Management
    @app.route("/api/backups")
    def api_backups():
        """Get list of backups."""
        try:
            backup_dir = Path.home() / ".gitsage" / "backups"
            backups = []

            if backup_dir.exists():
                import hashlib

                for i, backup_file in enumerate(backup_dir.glob("*.tar.gz")):
                    # Try to read checksum if exists
                    checksum_file = backup_file.with_suffix(".tar.gz.sha256")
                    checksum = None
                    if checksum_file.exists():
                        checksum = checksum_file.read_text().strip().split()[0]

                    backups.append(
                        {
                            "id": f"backup_{i}",
                            "name": backup_file.name,
                            "path": str(backup_file),
                            "size": backup_file.stat().st_size,
                            "created": backup_file.stat().st_mtime,
                            "checksum": checksum,
                        }
                    )

            return jsonify({"success": True, "backups": backups})
        except Exception as e:
            logger.error(f"Backup list error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/backups/create", methods=["POST"])
    def api_create_backup():
        """Create a new backup."""
        try:
            data = request.get_json()
            # TODO: Implement actual backup creation
            return jsonify(
                {
                    "success": True,
                    "message": "Backup creation will be fully implemented",
                    "backup_id": "temp_id",
                }
            )
        except Exception as e:
            logger.error(f"Backup creation error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/backups/<backup_id>/restore", methods=["POST"])
    def api_restore_backup(backup_id):
        """Restore a backup."""
        try:
            # TODO: Implement actual backup restoration
            return jsonify(
                {"success": True, "message": "Backup restoration will be fully implemented"}
            )
        except Exception as e:
            logger.error(f"Backup restore error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/backups/<backup_id>", methods=["DELETE"])
    def api_delete_backup(backup_id):
        """Delete a backup."""
        try:
            # TODO: Implement actual backup deletion
            return jsonify({"success": True, "message": "Backup deleted"})
        except Exception as e:
            logger.error(f"Backup deletion error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/settings/<category>", methods=["POST"])
    def api_update_settings(category):
        """Update settings for a specific category."""
        try:
            data = request.get_json()
            # TODO: Implement actual settings update
            return jsonify({"success": True, "message": f"{category} settings updated"})
        except Exception as e:
            logger.error(f"Settings update error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # Interactive Tools Routes
    @app.route("/readme-generator")
    def readme_generator():
        """README generator page."""
        return render_template("readme_generator.html")

    @app.route("/wiki-generator")
    def wiki_generator():
        """Wiki generator page."""
        return render_template("wiki_generator.html")

    @app.route("/health-checker")
    def health_checker():
        """Repository health checker page."""
        return render_template("health_checker.html")

    @app.route("/setup-wizard")
    def setup_wizard():
        """Repository setup wizard page."""
        return render_template("setup_wizard.html")

    # Interactive Tools API Endpoints
    @app.route("/api/detect-project", methods=["POST"])
    def api_detect_project():
        """Detect project type and return analysis."""
        try:
            from gitsage.utils import ProjectDetector

            detector = ProjectDetector()
            result = detector.detect()

            return jsonify({"success": True, "data": result})
        except Exception as e:
            logger.error(f"Project detection error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/check-health", methods=["POST"])
    def api_check_health():
        """Check repository health."""
        try:
            from gitsage.utils import RepositoryHealthChecker

            checker = RepositoryHealthChecker()
            result = checker.check_all()

            return jsonify({"success": True, "data": result})
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/beautification-score", methods=["POST"])
    def api_beautification_score():
        """Get beautification score."""
        try:
            from gitsage.utils import BeautificationScorer

            scorer = BeautificationScorer()
            result = scorer.calculate_score()

            return jsonify({"success": True, "data": result})
        except Exception as e:
            logger.error(f"Beautification score error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/generate-readme", methods=["POST"])
    def api_generate_readme():
        """Generate README content."""
        try:
            data = request.get_json()

            # Import README generator logic
            project_name = data.get("projectName", "My Project")
            description = data.get("description", "")
            features = data.get("features", [])
            installation = data.get("installation", "")
            usage = data.get("usage", "")
            license_type = data.get("license", "MIT")

            # Generate README content
            readme_content = f"""# {project_name}

> {description}

## Features

{chr(10).join([f"- {feature}" for feature in features])}

## Installation

```bash
{installation}
```

## Usage

```bash
{usage}
```

## License

{license_type}
"""

            return jsonify({"success": True, "content": readme_content})
        except Exception as e:
            logger.error(f"README generation error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/generate-wiki", methods=["POST"])
    def api_generate_wiki():
        """Generate wiki pages."""
        try:
            data = request.get_json()
            pages = data.get("pages", ["Home", "Installation", "Usage"])

            # Generate wiki pages
            wiki_pages = []
            for page in pages:
                wiki_pages.append(
                    {
                        "name": page,
                        "filename": f"{page}.md",
                        "content": f"# {page}\n\nContent for {page} page.",
                    }
                )

            return jsonify({"success": True, "pages": wiki_pages})
        except Exception as e:
            logger.error(f"Wiki generation error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/setup-wizard/run", methods=["POST"])
    def api_setup_wizard_run():
        """Run complete setup wizard."""
        try:
            from gitsage.utils import (
                BeautificationScorer,
                ProjectDetector,
                RepositoryHealthChecker,
            )

            steps = []

            # Step 1: Detect project
            detector = ProjectDetector()
            detection = detector.detect()
            steps.append(
                {
                    "step": 1,
                    "name": "Project Analysis",
                    "status": "completed",
                    "data": detection,
                }
            )

            # Step 2: Health check
            checker = RepositoryHealthChecker()
            health = checker.check_all()
            steps.append(
                {"step": 2, "name": "Health Check", "status": "completed", "data": health}
            )

            # Step 3: Beautification score
            scorer = BeautificationScorer()
            beauty = scorer.calculate_score()
            steps.append(
                {
                    "step": 3,
                    "name": "Beautification Score",
                    "status": "completed",
                    "data": beauty,
                }
            )

            return jsonify({"success": True, "steps": steps})
        except Exception as e:
            logger.error(f"Setup wizard error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template("error.html", error_code=404, error_message="Page not found"), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return (
            render_template("error.html", error_code=500, error_message="Internal server error"),
            500,
        )

    return app


def main():
    """Run the web interface."""
    app = create_app()

    logger.info(f"Starting {PROJECT_NAME} Web Interface v{__version__}")
    logger.info("Access at: http://localhost:5000")
    logger.info("Press Ctrl+C to stop")

    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
