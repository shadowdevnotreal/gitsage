# GitHub Actions - Deep Dive Tutorial

> Master CI/CD with GitHub Actions - From basics to advanced workflows

## 📚 Table of Contents

1. [Introduction to GitHub Actions](#introduction)
2. [Core Concepts](#core-concepts)
3. [Your First Workflow](#first-workflow)
4. [Workflow Syntax Deep Dive](#workflow-syntax)
5. [Common Use Cases](#common-use-cases)
6. [Advanced Patterns](#advanced-patterns)
7. [Secrets & Security](#secrets-security)
8. [Optimization & Best Practices](#optimization)
9. [Troubleshooting](#troubleshooting)

---

## Introduction to GitHub Actions

### What are GitHub Actions?

**Simple explanation:** GitHub Actions is GitHub's built-in CI/CD platform that automates your software workflows.

**CI/CD = Continuous Integration / Continuous Deployment:**
- **CI**: Automatically test code when you push
- **CD**: Automatically deploy code when tests pass

**Analogy:** Like having a robot assistant that tests and deploys your code every time you make changes.

### Why Use GitHub Actions?

✅ **Built into GitHub** - No external service needed
✅ **Free for public repos** - 2,000 minutes/month for private
✅ **Matrix builds** - Test multiple versions simultaneously
✅ **Huge marketplace** - Thousands of pre-built actions
✅ **Event-driven** - Trigger on push, PR, issues, schedule, etc.

### Common Use Cases

- 🧪 Run tests automatically on every push
- 📦 Build and package your application
- 🚀 Deploy to production when merging to main
- 📊 Generate documentation
- 🔒 Security scanning and dependency updates
- 🏷️ Create releases automatically
- 📧 Send notifications on build failures

---

## Core Concepts

### Workflows

**Definition:** Automated process defined in YAML file.

**Location:** `.github/workflows/*.yml`

```yaml
# .github/workflows/ci.yml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm test
```

### Events

**Triggers** that start workflows:

```yaml
# Single event
on: push

# Multiple events
on: [push, pull_request]

# Specific branches
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# Scheduled (cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

# Manual trigger
on: workflow_dispatch
```

### Jobs

**Units of work** that run in parallel (by default):

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing"

  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building"

  # This job waits for test and build
  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying"
```

### Steps

**Individual tasks** within a job:

```yaml
steps:
  # Use a pre-built action
  - uses: actions/checkout@v3

  # Run a command
  - run: npm install

  # Run multiple commands
  - run: |
      npm run build
      npm run test

  # Named step
  - name: Upload artifact
    uses: actions/upload-artifact@v3
    with:
      name: build
      path: dist/
```

### Runners

**Machines** that execute jobs:

```yaml
# GitHub-hosted runners (free)
runs-on: ubuntu-latest    # Ubuntu Linux
runs-on: windows-latest   # Windows
runs-on: macos-latest     # macOS

# Self-hosted runner
runs-on: self-hosted
```

### Actions

**Reusable units** from marketplace or custom:

```yaml
# Official GitHub action
- uses: actions/checkout@v3

# Community action
- uses: docker/build-push-action@v4

# Local action in your repo
- uses: ./.github/actions/my-action
```

---

## Your First Workflow

### Step 1: Create Workflow File

```bash
# In your repository
mkdir -p .github/workflows
touch .github/workflows/hello-world.yml
```

### Step 2: Write Simple Workflow

```yaml
# .github/workflows/hello-world.yml
name: Hello World

# Trigger on push to any branch
on: push

jobs:
  greet:
    runs-on: ubuntu-latest

    steps:
      # Print greeting
      - name: Say hello
        run: echo "Hello, GitHub Actions!"

      # Print current date
      - name: Show date
        run: date

      # Print environment
      - name: Show environment
        run: |
          echo "Runner OS: $RUNNER_OS"
          echo "GitHub Actor: $GITHUB_ACTOR"
          echo "Repository: $GITHUB_REPOSITORY"
```

### Step 3: Commit and Push

```bash
git add .github/workflows/hello-world.yml
git commit -m "Add GitHub Actions workflow"
git push
```

### Step 4: View Results

1. Go to your GitHub repository
2. Click "Actions" tab
3. See your workflow running!
4. Click on the workflow run to see logs

---

## Workflow Syntax Deep Dive

### Complete Workflow Example

```yaml
name: Complete CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    paths-ignore:
      - '**.md'
      - 'docs/**'
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM
  workflow_dispatch:  # Manual trigger

env:
  NODE_VERSION: '18'
  CACHE_KEY: npm-cache

jobs:
  test:
    name: Test on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [16, 18, 20]
      fail-fast: false

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: matrix.os == 'ubuntu-latest' && matrix.node == 18

  build:
    name: Build Application
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}

      - run: npm ci
      - run: npm run build

      - name: Upload build artifact
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
          retention-days: 7

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production

    steps:
      - uses: actions/checkout@v3

      - name: Download build artifact
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/

      - name: Deploy to server
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          echo "Deploying to production..."
          # Deployment commands here
```

### Workflow Syntax Elements

#### Conditional Execution

```yaml
steps:
  # Run only on main branch
  - name: Deploy
    if: github.ref == 'refs/heads/main'
    run: ./deploy.sh

  # Run only on pull requests
  - name: Check PR
    if: github.event_name == 'pull_request'
    run: echo "This is a PR"

  # Run only on success
  - name: Cleanup
    if: success()
    run: echo "Tests passed!"

  # Run only on failure
  - name: Notify failure
    if: failure()
    run: echo "Tests failed!"

  # Run always (even if previous steps failed)
  - name: Always run
    if: always()
    run: echo "This always runs"
```

#### Matrix Strategy

```yaml
# Test multiple combinations
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [16, 18, 20]
    include:
      # Add specific combination
      - os: macos-latest
        node: 18
    exclude:
      # Remove specific combination
      - os: windows-latest
        node: 16

# Creates jobs for all combinations (except excluded)
```

#### Outputs

```yaml
jobs:
  build:
    outputs:
      version: ${{ steps.get_version.outputs.version }}

    steps:
      - id: get_version
        run: echo "version=1.2.3" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    steps:
      - run: echo "Deploying version ${{ needs.build.outputs.version }}"
```

---

## Common Use Cases

### 1. Node.js CI/CD

```yaml
name: Node.js CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [16, 18, 20]

    steps:
      - uses: actions/checkout@v3

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - run: npm ci
      - run: npm run build --if-present
      - run: npm test

      - name: Upload coverage
        if: matrix.node-version == 18
        uses: codecov/codecov-action@v3
```

### 2. Python Testing

```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### 3. Docker Build and Push

```yaml
name: Docker Build

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: myorg/myapp

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 4. Deploy to GitHub Pages

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - run: npm ci
      - run: npm run build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./dist

  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

### 5. Automated Releases

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Build project
        run: |
          npm ci
          npm run build

      - name: Create Release
        uses: ncipollo/release-action@v1
        with:
          artifacts: "dist/*.zip"
          generateReleaseNotes: true
          token: ${{ secrets.GITHUB_TOKEN }}
```

### 6. Scheduled Jobs

```yaml
name: Nightly Build

on:
  schedule:
    # Every day at 2 AM UTC
    - cron: '0 2 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run nightly tests
        run: npm run test:integration

      - name: Notify on failure
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Nightly build failed',
              body: 'The nightly build failed. Please investigate.'
            })
```

---

## Advanced Patterns

### Reusable Workflows

**Define once, use many times:**

```yaml
# .github/workflows/reusable-tests.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      npm-token:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}

      - run: npm ci
      - run: npm test
```

**Use it:**

```yaml
# .github/workflows/ci.yml
name: CI

on: [push]

jobs:
  test-node-16:
    uses: ./.github/workflows/reusable-tests.yml
    with:
      node-version: '16'

  test-node-18:
    uses: ./.github/workflows/reusable-tests.yml
    with:
      node-version: '18'
```

### Composite Actions

**Create custom actions:**

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Install dependencies and setup environment'

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '18'

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: ${{ inputs.node-version }}

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: node_modules
        key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}

    - name: Install dependencies
      run: npm ci
      shell: bash
```

**Use it:**

```yaml
steps:
  - uses: actions/checkout@v3
  - uses: ./.github/actions/setup-project
    with:
      node-version: '18'
  - run: npm test
```

### Caching Dependencies

```yaml
# NPM cache
- uses: actions/setup-node@v3
  with:
    node-version: '18'
    cache: 'npm'

# Manual cache
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Python pip cache
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'
    cache: 'pip'

# Docker layer cache
- name: Build with cache
  uses: docker/build-push-action@v4
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Artifacts

```yaml
# Upload artifact
- name: Upload build
  uses: actions/upload-artifact@v3
  with:
    name: build-artifacts
    path: |
      dist/
      *.log
    retention-days: 5

# Download artifact (different job)
- name: Download build
  uses: actions/download-artifact@v3
  with:
    name: build-artifacts
    path: build/
```

---

## Secrets & Security

### Adding Secrets

1. Go to repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value
4. Use in workflow: `${{ secrets.SECRET_NAME }}`

### Using Secrets

```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
    run: ./deploy.sh

  # Never echo secrets!
  # ❌ DON'T: run: echo ${{ secrets.API_KEY }}
```

### Environment Secrets

```yaml
jobs:
  deploy:
    environment: production  # Uses production environment secrets
    steps:
      - run: echo "Deploying with ${{ secrets.PROD_API_KEY }}"
```

### Security Best Practices

```yaml
# 1. Limit permissions
permissions:
  contents: read
  pull-requests: write

# 2. Pin action versions (use SHA instead of tag)
- uses: actions/checkout@8e5e7e5ab8b370d6c329ec480221332ada57f0ab  # v3.5.2

# 3. Use secrets, not hardcoded values
# ❌ BAD
- run: curl -H "Authorization: Bearer abc123"

# ✅ GOOD
- run: curl -H "Authorization: Bearer ${{ secrets.API_TOKEN }}"

# 4. Limit token scope
- uses: actions/checkout@v3
  with:
    token: ${{ secrets.LIMITED_SCOPE_TOKEN }}

# 5. Use environments for deployment protection
environment:
  name: production
  url: https://example.com
```

---

## Optimization & Best Practices

### Speed Up Workflows

```yaml
# 1. Use caching
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ hashFiles('package-lock.json') }}

# 2. Run jobs in parallel
jobs:
  test-frontend:
    ...
  test-backend:
    ...  # Runs at same time as frontend

# 3. Use matrix for concurrent testing
strategy:
  matrix:
    version: [16, 18, 20]  # All run in parallel

# 4. Skip unnecessary runs
on:
  push:
    paths-ignore:
      - 'docs/**'
      - '**.md'

# 5. Cancel outdated runs
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Cost Optimization

```yaml
# 1. Use cheaper runners when possible
runs-on: ubuntu-latest  # Cheapest

# 2. Limit matrix size
strategy:
  matrix:
    os: [ubuntu-latest]  # Don't test on all OS unless needed

# 3. Set timeouts
jobs:
  test:
    timeout-minutes: 10

# 4. Use paths filters
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
```

### Workflow Organization

```yaml
# Use descriptive names
name: "CI: Test and Build"

jobs:
  test:
    name: "Test on Node ${{ matrix.node }}"

  # Group related steps
  - name: Setup environment
    run: |
      npm ci
      npm run setup

  # Use if conditions wisely
  - name: Deploy
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

---

## Troubleshooting

### Common Issues

#### 1. Workflow Not Triggering

```yaml
# Check:
# - Is the YAML file in .github/workflows/?
# - Is the filename .yml or .yaml?
# - Is the trigger event correct?

on:
  push:
    branches: [main]  # Only triggers on main, not other branches
```

#### 2. Secrets Not Working

```bash
# Secrets are case-sensitive!
# ❌ ${{ secrets.api_key }}
# ✅ ${{ secrets.API_KEY }}

# Check secret is set: Repo → Settings → Secrets
```

#### 3. Cache Not Working

```yaml
# Cache key must be unique and deterministic
# ❌ BAD
key: my-cache  # Same key always

# ✅ GOOD
key: ${{ runner.os }}-${{ hashFiles('package-lock.json') }}
```

#### 4. Permission Denied

```yaml
# Add required permissions
permissions:
  contents: write  # For creating releases
  packages: write  # For publishing packages
```

### Debug Workflows

```yaml
# 1. Enable debug logging
# In repo settings, set secrets:
# ACTIONS_STEP_DEBUG = true
# ACTIONS_RUNNER_DEBUG = true

# 2. Add debug steps
- name: Debug
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "Actor: ${{ github.actor }}"
    env  # Print all environment variables

# 3. Use tmate for SSH debugging
- name: Setup tmate session
  uses: mxschmitt/action-tmate@v3
  if: failure()  # Only on failure
```

### View Logs

1. Go to Actions tab
2. Click on workflow run
3. Click on job
4. Click on step to see logs
5. Download logs (top right) for offline viewing

---

## Quick Reference

### Trigger Events

```yaml
on:
  push:                    # On every push
  pull_request:           # On PR
  release:                # On release
  schedule:               # Cron schedule
    - cron: '0 0 * * *'
  workflow_dispatch:      # Manual trigger
  repository_dispatch:    # External API trigger
```

### Context Variables

```yaml
# Common context variables
${{ github.repository }}      # owner/repo
${{ github.ref }}            # refs/heads/main
${{ github.sha }}            # Commit SHA
${{ github.actor }}          # Username who triggered
${{ github.event_name }}     # push, pull_request, etc.
${{ runner.os }}             # Linux, Windows, macOS
${{ secrets.SECRET_NAME }}   # Access secrets
${{ env.MY_VAR }}            # Environment variable
```

### Useful Actions

```yaml
# Checkout code
- uses: actions/checkout@v3

# Setup languages
- uses: actions/setup-node@v3
- uses: actions/setup-python@v4
- uses: actions/setup-go@v4
- uses: actions/setup-java@v3

# Caching
- uses: actions/cache@v3

# Artifacts
- uses: actions/upload-artifact@v3
- uses: actions/download-artifact@v3

# GitHub Script
- uses: actions/github-script@v6

# Docker
- uses: docker/setup-buildx-action@v2
- uses: docker/login-action@v2
- uses: docker/build-push-action@v4
```

---

## Practice Exercises

### Exercise 1: Basic CI

Create a workflow that:
1. Runs on push and PR
2. Tests on Node 18
3. Runs `npm test`

<details>
<summary>Solution</summary>

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
```
</details>

### Exercise 2: Matrix Testing

Test on Node 16, 18, 20 and Ubuntu, Windows.

<details>
<summary>Solution</summary>

```yaml
name: Matrix Test

on: push

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [16, 18, 20]

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```
</details>

### Exercise 3: Deploy on Main

Deploy only when pushing to main branch.

<details>
<summary>Solution</summary>

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run build
      - name: Deploy
        if: github.ref == 'refs/heads/main'
        run: echo "Deploying..."
```
</details>

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [Actions Toolkit](https://github.com/actions/toolkit)

---

**Master GitHub Actions and automate everything! From testing to deployment, the possibilities are endless.** 🚀

*Created by GitSage - Automate, Learn, Deploy* 💾
