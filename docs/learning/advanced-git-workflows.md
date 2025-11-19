# Advanced Git Workflows

> Master git rebase, cherry-pick, and bisect - the power tools of Git

## 📚 Table of Contents

1. [Git Rebase - Rewriting History](#git-rebase)
2. [Git Cherry-Pick - Selective Commits](#git-cherry-pick)
3. [Git Bisect - Bug Hunting](#git-bisect)
4. [Real-World Scenarios](#real-world-scenarios)
5. [Best Practices & Warnings](#best-practices)

---

## Git Rebase - Rewriting History

### What is Rebase?

**Simple explanation:** Rebase moves or combines a sequence of commits to a new base commit. Think of it like "replaying" your commits on top of another branch.

**Analogy:** If Git merge is like tying two ropes together, rebase is like unraveling one rope and re-weaving it into the other.

### When to Use Rebase

✅ **Good uses:**
- Clean up messy commit history before a pull request
- Keep feature branch up-to-date with main
- Create a linear project history

❌ **Never rebase:**
- Commits that have been pushed and shared with others
- On public/shared branches (main, develop)

### Basic Rebase

```bash
# Scenario: Your feature branch is behind main
# Current state:
#     A---B---C feature
#    /
# D---E---F---G main

# Update feature branch to latest main
git checkout feature
git rebase main

# Result:
#             A'--B'--C' feature
#            /
# D---E---F---G main
```

### Interactive Rebase

**The power tool** - edit, reorder, squash, or delete commits.

```bash
# Rebase the last 5 commits interactively
git rebase -i HEAD~5

# Or rebase from a specific commit
git rebase -i abc123
```

**Interactive rebase commands:**
```
pick   - use commit as-is
reword - change commit message
edit   - stop and amend commit
squash - combine with previous commit
fixup  - like squash but discard message
drop   - remove commit
```

### Practical Example: Clean Up Before PR

**Scenario:** You have messy commits you want to clean before creating a PR.

```bash
# Your current commits:
# a1b2c3d WIP
# e4f5g6h fix typo
# i7j8k9l add feature
# m1n2o3p fix bug
# p4q5r6s more WIP

# Start interactive rebase of last 5 commits
git rebase -i HEAD~5

# In the editor that opens:
pick i7j8k9l add feature
fixup a1b2c3d WIP           # Combine WIP into "add feature"
fixup p4q5r6s more WIP      # Combine more WIP
pick m1n2o3p fix bug
fixup e4f5g6h fix typo      # Combine into "fix bug"

# Save and close - now you have 2 clean commits!
```

### Handling Rebase Conflicts

```bash
# If conflicts occur during rebase:
# 1. Git stops and shows conflicts
git status  # See conflicted files

# 2. Edit files to resolve conflicts
# Remove conflict markers (<<<<<<<, =======, >>>>>>>)

# 3. Stage resolved files
git add <resolved-files>

# 4. Continue rebase
git rebase --continue

# Or skip this commit
git rebase --skip

# Or abort and return to original state
git rebase --abort
```

### Rebase vs Merge

| Aspect | Merge | Rebase |
|--------|-------|--------|
| History | Shows true project history | Creates linear history |
| Commits | Creates merge commit | No merge commit |
| Conflicts | Resolve once | May resolve multiple times |
| Safety | Safer (non-destructive) | Can lose work if misused |
| Use when | Shared branches | Local cleanup |

---

## Git Cherry-Pick - Selective Commits

### What is Cherry-Pick?

**Simple explanation:** Copy a specific commit from one branch to another. Like picking a cherry from one basket and putting it in another.

**Use case:** You need a specific bug fix from one branch, but don't want everything else from that branch.

### Basic Cherry-Pick

```bash
# Scenario: You want commit abc123 from feature-x onto your current branch

# 1. Find the commit hash
git log feature-x --oneline
# abc123 Fix critical bug
# def456 Add new feature
# ...

# 2. Cherry-pick it
git cherry-pick abc123

# Result: abc123 is now applied to your current branch
```

### Cherry-Pick Multiple Commits

```bash
# Pick several commits
git cherry-pick abc123 def456 ghi789

# Pick a range of commits
git cherry-pick abc123..ghi789

# Pick a range including the first commit
git cherry-pick abc123^..ghi789
```

### Cherry-Pick Options

```bash
# Don't commit immediately (stage changes only)
git cherry-pick -n abc123

# Edit the commit message
git cherry-pick -e abc123

# Sign off the commit
git cherry-pick -s abc123

# Continue after resolving conflicts
git cherry-pick --continue

# Abort cherry-pick
git cherry-pick --abort
```

### Practical Example: Backport a Bug Fix

```bash
# Scenario: You fixed a bug in main, need it in release-1.0

# 1. Find the fix commit
git log main --oneline | grep "bug"
# a1b2c3d Fix login bug

# 2. Switch to release branch
git checkout release-1.0

# 3. Cherry-pick the fix
git cherry-pick a1b2c3d

# 4. Push to release branch
git push origin release-1.0
```

### Handling Cherry-Pick Conflicts

```bash
# If conflicts occur:
# 1. See what's conflicted
git status

# 2. Resolve conflicts in files
# Edit files, remove markers

# 3. Stage resolved files
git add <files>

# 4. Continue
git cherry-pick --continue
```

### When to Use Cherry-Pick

✅ **Good uses:**
- Backport bug fixes to release branches
- Apply hotfix to multiple versions
- Copy specific features to experimental branch
- Rescue commits from abandoned branches

❌ **Avoid:**
- Regularly syncing branches (use merge/rebase instead)
- Large numbers of commits (use merge instead)

---

## Git Bisect - Bug Hunting

### What is Bisect?

**Simple explanation:** Binary search through your commit history to find which commit introduced a bug.

**Analogy:** Like playing "higher or lower" with commits - Git automatically finds the problem commit.

### How Bisect Works

Git uses **binary search**:
- 100 commits to check
- Bisect checks ~7 commits (log₂(100) ≈ 6.6)
- Much faster than checking each commit!

### Basic Bisect Workflow

```bash
# 1. Start bisect
git bisect start

# 2. Mark current commit as bad
git bisect bad

# 3. Mark a known good commit (e.g., last release)
git bisect good v1.0.0

# 4. Git checks out a middle commit
# Test if the bug exists

# 5a. If bug exists:
git bisect bad

# 5b. If bug doesn't exist:
git bisect good

# 6. Repeat steps 5a/5b until Git finds the culprit

# 7. Git shows you the first bad commit!

# 8. End bisect
git bisect reset
```

### Practical Example: Find When Tests Started Failing

```bash
# Your tests are failing now, but worked last month

# 1. Start bisect
git bisect start

# 2. Current state is bad
git bisect bad HEAD

# 3. Last month was good (find commit hash)
git log --since="1 month ago" --until="31 days ago" --oneline | tail -1
# abc123 ...

git bisect good abc123

# Git checks out a middle commit
# Bisecting: 15 revisions left to test after this

# 4. Run tests
npm test

# Tests fail:
git bisect bad

# Git checks out another commit
# Bisecting: 7 revisions left to test after this

# Run tests again
npm test

# Tests pass:
git bisect good

# Continue until Git finds the culprit:
# abc123def is the first bad commit
# Author: John Doe
# Date: 2 weeks ago
# Refactor authentication module

# 5. Exit bisect
git bisect reset

# Now you know commit abc123def broke the tests!
```

### Automated Bisect

**Skip manual testing** - let a script do it!

```bash
# Start bisect
git bisect start HEAD v1.0.0

# Run automated bisect with test script
git bisect run npm test

# Git automatically:
# 1. Checks out commit
# 2. Runs 'npm test'
# 3. Marks good (exit code 0) or bad (non-zero)
# 4. Repeats until finding the culprit

# Finishes with the first bad commit!
```

### Bisect with Custom Test Script

```bash
# Create test script: test-for-bug.sh
#!/bin/bash
# Exit 0 if good, 1 if bad

if [ -f "config.json" ]; then
    # Check if bug exists
    grep -q "buggy_config" config.json
    if [ $? -eq 0 ]; then
        exit 1  # Bug found (bad)
    else
        exit 0  # No bug (good)
    fi
else
    exit 125  # Skip this commit (can't test)
fi

# Make executable
chmod +x test-for-bug.sh

# Run bisect
git bisect start HEAD v1.0.0
git bisect run ./test-for-bug.sh
```

### Bisect Exit Codes

- **0** - Commit is good
- **1-127 (except 125)** - Commit is bad
- **125** - Skip this commit (can't be tested)

### Advanced Bisect

```bash
# Start with explicit good and bad
git bisect start <bad-commit> <good-commit>

# Skip a commit that can't be tested
git bisect skip

# Visualize bisect progress
git bisect visualize
# or
gitk bisect/bad --not bisect/good

# Check bisect log
git bisect log

# Replay bisect from log
git bisect replay <logfile>
```

---

## Real-World Scenarios

### Scenario 1: Update Feature Branch with Main

**Problem:** Your feature branch is 20 commits behind main, merge would create ugly history.

**Solution:** Rebase

```bash
# Save any uncommitted work
git stash

# Update main
git checkout main
git pull

# Rebase feature on main
git checkout feature/awesome-feature
git rebase main

# Resolve any conflicts
# git add <files>
# git rebase --continue

# Force push (branch wasn't shared yet)
git push --force-with-lease origin feature/awesome-feature

# Restore uncommitted work
git stash pop
```

### Scenario 2: Extract Fix for Multiple Releases

**Problem:** Fixed critical bug in main, need it in release-1.0 and release-2.0.

**Solution:** Cherry-pick

```bash
# Find the fix
git log main --oneline | grep "critical"
# a1b2c3d Fix critical security bug

# Apply to release-1.0
git checkout release-1.0
git cherry-pick a1b2c3d
git push origin release-1.0

# Apply to release-2.0
git checkout release-2.0
git cherry-pick a1b2c3d
git push origin release-2.0
```

### Scenario 3: Find When Performance Degraded

**Problem:** App is slow now, was fast 2 months ago. Which commit caused it?

**Solution:** Bisect

```bash
# Create performance test
cat > perf-test.sh << 'EOF'
#!/bin/bash
npm run build > /dev/null 2>&1
START=$(date +%s)
npm start &
PID=$!
sleep 5
RESPONSE=$(curl -w "%{time_total}" -s -o /dev/null http://localhost:3000)
kill $PID
if (( $(echo "$RESPONSE > 2.0" | bc -l) )); then
    exit 1  # Slow (bad)
else
    exit 0  # Fast (good)
fi
EOF

chmod +x perf-test.sh

# Run bisect
git bisect start HEAD HEAD~100
git bisect run ./perf-test.sh

# Git finds the commit that slowed down the app!
```

### Scenario 4: Clean Up Commits Before PR

**Problem:** 10 commits like "WIP", "fix", "oops", want 2-3 clean ones.

**Solution:** Interactive rebase

```bash
# Last 10 commits
git rebase -i HEAD~10

# In editor, squash related commits:
pick a1b2c3d Implement user authentication
fixup e4f5g6h fix typo
fixup i7j8k9l WIP
fixup m1n2o3p more changes
pick p4q5r6s Add password reset
fixup t7u8v9w fix bug
pick x1y2z3a Update documentation
fixup b4c5d6e typo

# Results in 3 clean commits!
```

---

## Best Practices & Warnings

### ⚠️ The Golden Rule of Rebase

**NEVER rebase commits that have been pushed to a shared/public branch.**

Why? Rebase rewrites history. If others have based work on your commits, rewriting breaks their work.

```bash
# ❌ DANGEROUS
git checkout main  # Public branch
git rebase feature # Don't do this!

# ✅ SAFE
git checkout feature  # Your branch
git rebase main       # This is fine
```

### Safe Force Push

```bash
# ❌ DANGEROUS - Can lose others' work
git push --force

# ✅ SAFER - Only force if no one else pushed
git push --force-with-lease

# This checks if remote branch is where you expect
# Fails if someone else pushed (protects their work)
```

### Rebase Workflow Best Practices

1. **Always on feature branches** - Never on main/shared branches
2. **Communicate** - Tell team if rebasing shared feature branch
3. **Backup** - Create a backup branch before risky rebase
   ```bash
   git branch backup-feature-branch
   git rebase -i main
   ```
4. **Small rebases** - Easier than rebasing 100 commits at once

### Cherry-Pick Best Practices

1. **Include commit message** - Makes tracking easier
2. **Use -x flag** - Records original commit
   ```bash
   git cherry-pick -x abc123
   # Adds "(cherry picked from commit abc123)"
   ```
3. **Document** - Note in PR why you cherry-picked

### Bisect Best Practices

1. **Good test** - Reliable, automated test is key
2. **Clean state** - No uncommitted changes when starting
3. **Reproducible** - Bug must be consistently reproducible
4. **Binary choice** - Test must clearly pass or fail

---

## Quick Reference

### Rebase Cheat Sheet

```bash
# Update feature with main
git rebase main

# Interactive rebase last N commits
git rebase -i HEAD~N

# Continue after conflict
git rebase --continue

# Skip current commit
git rebase --skip

# Abort rebase
git rebase --abort

# Rebase onto different base
git rebase --onto new-base old-base branch
```

### Cherry-Pick Cheat Sheet

```bash
# Pick single commit
git cherry-pick abc123

# Pick multiple commits
git cherry-pick abc123 def456

# Pick range
git cherry-pick abc123..xyz789

# Edit commit message
git cherry-pick -e abc123

# Don't commit yet
git cherry-pick -n abc123

# Continue after conflict
git cherry-pick --continue

# Abort
git cherry-pick --abort
```

### Bisect Cheat Sheet

```bash
# Start bisect
git bisect start

# Mark commits
git bisect bad <commit>
git bisect good <commit>

# Automated bisect
git bisect run <test-script>

# Skip untestable commit
git bisect skip

# End bisect
git bisect reset

# Show bisect log
git bisect log
```

---

## Practice Exercises

### Exercise 1: Interactive Rebase

Create a test repository and practice squashing commits:

```bash
mkdir git-rebase-practice && cd git-rebase-practice
git init

# Create multiple commits
echo "line 1" > file.txt && git add . && git commit -m "WIP"
echo "line 2" >> file.txt && git add . && git commit -m "more work"
echo "line 3" >> file.txt && git add . && git commit -m "fix typo"
echo "line 4" >> file.txt && git add . && git commit -m "final changes"

# Squash into one commit
git rebase -i HEAD~4
# In editor, keep first 'pick', change others to 'squash'
# Verify: git log --oneline
```

### Exercise 2: Cherry-Pick Practice

```bash
# Create two branches
git checkout -b branch-a
echo "Feature A" > feature-a.txt && git add . && git commit -m "Add feature A"

git checkout -b branch-b main
echo "Feature B" > feature-b.txt && git add . && git commit -m "Add feature B"

# Cherry-pick feature A into branch-b
COMMIT_HASH=$(git log branch-a --oneline | head -1 | cut -d' ' -f1)
git cherry-pick $COMMIT_HASH

# Verify both features exist
ls -la  # Should see feature-a.txt and feature-b.txt
```

### Exercise 3: Bisect Bug Hunt

```bash
# Create repo with a "bug" introduced partway through
mkdir bisect-practice && cd bisect-practice
git init

for i in {1..20}; do
    echo "Version $i" > version.txt

    # Introduce "bug" at commit 12
    if [ $i -ge 12 ]; then
        echo "BUG" >> version.txt
    fi

    git add version.txt
    git commit -m "Commit $i"
done

# Use bisect to find when BUG was introduced
git bisect start HEAD HEAD~19
git bisect run sh -c '! grep -q "BUG" version.txt'

# Should find commit 12!
```

---

## Additional Resources

- [Pro Git Book - Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)
- [Atlassian - Merging vs Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
- [Git Bisect Tutorial](https://git-scm.com/docs/git-bisect)
- [Interactive Rebase Guide](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History#_changing_multiple)

---

**Remember:** These are powerful tools. With great power comes great responsibility. Always know what you're doing before rewriting history!

*Created by GitSage - Learn GitHub, Master Git* 🚀
