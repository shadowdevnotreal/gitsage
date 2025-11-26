"""GitSage Web Interface - Flask application."""

import os
from pathlib import Path
from typing import Optional

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS

from gitsage.__version__ import __version__, PROJECT_NAME
from gitsage.utils import EnvironmentDetector, get_logger
from gitsage.config import get_config


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
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['GITSAGE_VERSION'] = __version__
    app.config['PROJECT_NAME'] = PROJECT_NAME

    if config:
        app.config.update(config)

    # Enable CORS
    CORS(app)

    # Initialize
    gitsage_config = get_config()

    @app.context_processor
    def inject_globals():
        """Inject global variables into templates."""
        return {
            'version': __version__,
            'project_name': PROJECT_NAME,
        }

    # Routes
    @app.route('/')
    def index():
        """Home page."""
        detector = EnvironmentDetector()
        env_info = detector.detect_all()

        return render_template('index.html', env_info=env_info)

    @app.route('/api/environment')
    def api_environment():
        """API endpoint for environment information."""
        detector = EnvironmentDetector()
        env_info = detector.detect_all()

        return jsonify({
            'success': True,
            'data': env_info,
            'recommendations': [
                {
                    'priority': rec.priority,
                    'message': rec.message,
                    'action': rec.action
                }
                for rec in detector.recommendations
            ]
        })

    @app.route('/api/config')
    def api_config():
        """API endpoint for configuration."""
        config_data = gitsage_config.to_dict()
        return jsonify({
            'success': True,
            'data': config_data
        })

    @app.route('/generators')
    def generators():
        """Generators page."""
        return render_template('generators.html')

    @app.route('/backups')
    def backups():
        """Backups page."""
        backup_dir = Path.home() / '.gitsage' / 'backups'
        backups = []

        if backup_dir.exists():
            for backup_file in backup_dir.glob('*.tar.gz'):
                backups.append({
                    'name': backup_file.name,
                    'size': backup_file.stat().st_size,
                    'created': backup_file.stat().st_mtime
                })

        return render_template('backups.html', backups=backups)

    @app.route('/settings')
    def settings():
        """Settings page."""
        return render_template('settings.html', config=gitsage_config)

    @app.route('/api/settings', methods=['GET', 'POST'])
    def api_settings():
        """API endpoint for settings."""
        if request.method == 'POST':
            # Update settings
            data = request.get_json()
            # TODO: Update configuration
            return jsonify({'success': True, 'message': 'Settings updated'})
        else:
            return jsonify({
                'success': True,
                'data': gitsage_config.to_dict()
            })

    @app.route('/about')
    def about():
        """About page."""
        return render_template('about.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template('error.html', error_code=404, error_message='Page not found'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return render_template('error.html', error_code=500, error_message='Internal server error'), 500

    return app


def main():
    """Run the web interface."""
    app = create_app()

    print(f"Starting {PROJECT_NAME} Web Interface v{__version__}")
    print("Access at: http://localhost:5000")
    print("Press Ctrl+C to stop")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )


if __name__ == '__main__':
    main()
