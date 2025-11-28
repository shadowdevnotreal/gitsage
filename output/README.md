# GitSage Output Folder

This folder contains all generated files from GitSage tools.

## Folder Structure

```
output/
├── README/        # Generated README files
├── wiki/          # Generated wiki/documentation files
├── backups/       # Repository backups
└── docs/          # Other documentation files
```

## How It Works

When you use GitSage tools, output files are automatically saved here:

### README Generator
```bash
python readme-generator.py --output output/README/
```
Generated README files will be saved to `output/README/`

### Wiki Generator
```bash
python wiki-generator.py --output output/wiki/
```
Generated wiki files will be saved to `output/wiki/`

### Backup Manager
```bash
python backup-manager.py --backup-dir output/backups/
```
Backups will be saved to `output/backups/`

## Default Behavior

If no output path is specified, GitSage will:
1. Save to current directory (for README)
2. Save to `wiki/` folder (for wiki)
3. Save to `~/.gitsage/backups/` (for backups)

## Centralized Output

This `output/` folder provides a centralized location for all generated files, making it easy to:
- Find your generated content
- Review before committing
- Organize project documentation
- Track changes to generated files

## .gitignore

Add to your `.gitignore` if you don't want to track generated files:
```
output/README/*
output/wiki/*
output/backups/*
!output/*/.gitkeep
```
