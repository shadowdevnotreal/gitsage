#!/usr/bin/env python3
"""
Automated Backup System for GitSage
Creates backups before destructive operations
"""

import os
import sys
import shutil
import tarfile
import hashlib
import json
from pathlib import Path
from datetime import datetime
import argparse

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None


class BackupManager:
    """Manages repository backups"""

    def __init__(self, backup_root=None):
        self.console = Console() if RICH_AVAILABLE else None
        self.backup_root = Path(backup_root) if backup_root else Path.home() / '.gitsage' / 'backups'
        self.backup_root.mkdir(parents=True, exist_ok=True)
        self.index_file = self.backup_root / 'backup_index.json'
        self.index = self._load_index()

    def _load_index(self):
        """Load backup index"""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {'backups': []}

    def _save_index(self):
        """Save backup index"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def _calculate_checksum(self, filepath):
        """Calculate SHA256 checksum"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _get_repo_size(self, repo_path):
        """Calculate repository size"""
        total = 0
        for dirpath, dirnames, filenames in os.walk(repo_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total += os.path.getsize(filepath)
        return total

    def create_backup(self, repo_path, repo_name=None, operation='manual', metadata=None):
        """
        Create a backup of a repository

        Args:
            repo_path: Path to repository to backup
            repo_name: Name/identifier for the repository
            operation: Type of operation (deletion, reset, etc.)
            metadata: Additional metadata to store

        Returns:
            Backup ID if successful, None otherwise
        """
        repo_path = Path(repo_path)

        if not repo_path.exists():
            self._print_error(f"Repository not found: {repo_path}")
            return None

        # Generate backup ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        repo_name = repo_name or repo_path.name
        safe_name = repo_name.replace('/', '_').replace('\\', '_')
        backup_id = f"{safe_name}_{operation}_{timestamp}"

        # Create backup directory
        backup_dir = self.backup_root / backup_id
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Create tar.gz archive
        archive_path = backup_dir / f"{backup_id}.tar.gz"

        self._print_info(f"Creating backup: {backup_id}")

        try:
            if RICH_AVAILABLE and self.console:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console
                ) as progress:
                    task = progress.add_task("Compressing repository...", total=None)

                    with tarfile.open(archive_path, 'w:gz') as tar:
                        tar.add(repo_path, arcname=repo_path.name)

                    progress.update(task, completed=True)
            else:
                print("Compressing repository...")
                with tarfile.open(archive_path, 'w:gz') as tar:
                    tar.add(repo_path, arcname=repo_path.name)

            # Calculate checksum
            checksum = self._calculate_checksum(archive_path)

            # Get file size
            archive_size = archive_path.stat().st_size
            repo_size = self._get_repo_size(repo_path)

            # Create metadata
            backup_metadata = {
                'backup_id': backup_id,
                'repo_name': repo_name,
                'repo_path': str(repo_path.absolute()),
                'operation': operation,
                'timestamp': timestamp,
                'archive_path': str(archive_path),
                'archive_size': archive_size,
                'repo_size': repo_size,
                'checksum': checksum,
                'metadata': metadata or {}
            }

            # Save metadata
            metadata_path = backup_dir / 'metadata.json'
            with open(metadata_path, 'w') as f:
                json.dump(backup_metadata, f, indent=2)

            # Update index
            self.index['backups'].append(backup_metadata)
            self._save_index()

            self._print_success(f"✓ Backup created: {backup_id}")
            self._print_info(f"  Location: {archive_path}")
            self._print_info(f"  Size: {self._format_size(archive_size)} (compressed from {self._format_size(repo_size)})")
            self._print_info(f"  Checksum: {checksum[:16]}...")

            return backup_id

        except Exception as e:
            self._print_error(f"Backup failed: {e}")
            # Cleanup partial backup
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            return None

    def list_backups(self, repo_name=None, operation=None):
        """List available backups"""
        backups = self.index['backups']

        # Filter
        if repo_name:
            backups = [b for b in backups if repo_name in b['repo_name']]
        if operation:
            backups = [b for b in backups if b['operation'] == operation]

        if not backups:
            self._print_info("No backups found")
            return []

        self._print_info(f"\nAvailable Backups ({len(backups)}):")
        print()

        for backup in backups:
            print(f"ID: {backup['backup_id']}")
            print(f"  Repository: {backup['repo_name']}")
            print(f"  Operation: {backup['operation']}")
            print(f"  Date: {backup['timestamp']}")
            print(f"  Size: {self._format_size(backup['archive_size'])}")
            print(f"  Location: {backup['archive_path']}")
            print()

        return backups

    def restore_backup(self, backup_id, restore_path=None):
        """
        Restore a backup

        Args:
            backup_id: Backup ID to restore
            restore_path: Where to restore (default: original location)
        """
        # Find backup
        backup = None
        for b in self.index['backups']:
            if b['backup_id'] == backup_id:
                backup = b
                break

        if not backup:
            self._print_error(f"Backup not found: {backup_id}")
            return False

        archive_path = Path(backup['archive_path'])

        if not archive_path.exists():
            self._print_error(f"Backup archive not found: {archive_path}")
            return False

        # Verify checksum
        self._print_info("Verifying backup integrity...")
        current_checksum = self._calculate_checksum(archive_path)

        if current_checksum != backup['checksum']:
            self._print_error("Backup integrity check failed! Checksum mismatch.")
            return False

        self._print_success("✓ Backup integrity verified")

        # Determine restore location
        if not restore_path:
            restore_path = Path(backup['repo_path'])
        else:
            restore_path = Path(restore_path)

        # Confirm if directory exists
        if restore_path.exists():
            if RICH_AVAILABLE:
                if not Confirm.ask(f"Directory exists: {restore_path}. Overwrite?"):
                    self._print_info("Restore cancelled")
                    return False
            else:
                response = input(f"Directory exists: {restore_path}. Overwrite? (y/N): ")
                if response.lower() != 'y':
                    self._print_info("Restore cancelled")
                    return False

            # Backup existing directory
            temp_backup = restore_path.parent / f"{restore_path.name}.bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.move(restore_path, temp_backup)
            self._print_info(f"Existing directory moved to: {temp_backup}")

        # Extract archive
        self._print_info(f"Restoring to: {restore_path.parent}")

        try:
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(restore_path.parent)

            self._print_success(f"✓ Backup restored successfully!")
            self._print_info(f"  Location: {restore_path}")

            return True

        except Exception as e:
            self._print_error(f"Restore failed: {e}")
            return False

    def delete_backup(self, backup_id):
        """Delete a backup"""
        # Find backup
        backup = None
        backup_index = None
        for i, b in enumerate(self.index['backups']):
            if b['backup_id'] == backup_id:
                backup = b
                backup_index = i
                break

        if not backup:
            self._print_error(f"Backup not found: {backup_id}")
            return False

        # Delete files
        backup_dir = Path(backup['archive_path']).parent

        if backup_dir.exists():
            shutil.rmtree(backup_dir)
            self._print_success(f"✓ Backup deleted: {backup_id}")

        # Remove from index
        self.index['backups'].pop(backup_index)
        self._save_index()

        return True

    def cleanup_old_backups(self, days=30, keep_count=10):
        """Clean up old backups"""
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days)

        # Group by repository
        repos = {}
        for backup in self.index['backups']:
            repo_name = backup['repo_name']
            if repo_name not in repos:
                repos[repo_name] = []
            repos[repo_name].append(backup)

        deleted_count = 0

        for repo_name, backups in repos.items():
            # Sort by timestamp (newest first)
            backups.sort(key=lambda x: x['timestamp'], reverse=True)

            # Keep specified count of newest backups
            keep_backups = backups[:keep_count]
            old_backups = backups[keep_count:]

            # Delete old backups beyond retention
            for backup in old_backups:
                backup_date = datetime.strptime(backup['timestamp'], '%Y%m%d_%H%M%S')

                if backup_date < cutoff_date:
                    self._print_info(f"Deleting old backup: {backup['backup_id']}")
                    if self.delete_backup(backup['backup_id']):
                        deleted_count += 1

        self._print_success(f"✓ Cleaned up {deleted_count} old backups")
        return deleted_count

    def _format_size(self, bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"

    def _print_info(self, msg):
        if self.console:
            self.console.print(f"[cyan]{msg}[/cyan]")
        else:
            print(msg)

    def _print_success(self, msg):
        if self.console:
            self.console.print(f"[green]{msg}[/green]")
        else:
            print(msg)

    def _print_error(self, msg):
        if self.console:
            self.console.print(f"[red]{msg}[/red]")
        else:
            print(f"ERROR: {msg}", file=sys.stderr)


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(description='GitSage Backup Manager')
    parser.add_argument('--backup-root', help='Backup storage location')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create backup
    create_parser = subparsers.add_parser('create', help='Create a backup')
    create_parser.add_argument('repo_path', help='Repository to backup')
    create_parser.add_argument('--name', help='Repository name')
    create_parser.add_argument('--operation', default='manual', help='Operation type')

    # List backups
    list_parser = subparsers.add_parser('list', help='List backups')
    list_parser.add_argument('--repo', help='Filter by repository name')
    list_parser.add_argument('--operation', help='Filter by operation')

    # Restore backup
    restore_parser = subparsers.add_parser('restore', help='Restore a backup')
    restore_parser.add_argument('backup_id', help='Backup ID to restore')
    restore_parser.add_argument('--path', help='Restore location')

    # Delete backup
    delete_parser = subparsers.add_parser('delete', help='Delete a backup')
    delete_parser.add_argument('backup_id', help='Backup ID to delete')

    # Cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up old backups')
    cleanup_parser.add_argument('--days', type=int, default=30, help='Keep backups from last N days')
    cleanup_parser.add_argument('--keep', type=int, default=10, help='Keep at least N backups per repo')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = BackupManager(backup_root=args.backup_root)

    if args.command == 'create':
        manager.create_backup(args.repo_path, repo_name=args.name, operation=args.operation)

    elif args.command == 'list':
        manager.list_backups(repo_name=args.repo, operation=args.operation)

    elif args.command == 'restore':
        manager.restore_backup(args.backup_id, restore_path=args.path)

    elif args.command == 'delete':
        manager.delete_backup(args.backup_id)

    elif args.command == 'cleanup':
        manager.cleanup_old_backups(days=args.days, keep_count=args.keep)


if __name__ == '__main__':
    main()
