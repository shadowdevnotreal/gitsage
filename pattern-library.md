# GitSage Pattern Library

> Multi-Agent Code Perfection System - Documented Patterns
>
> Created: 2025-11-27
> Repository: shadowdevnotreal/gitsage

## Table of Contents

1. [Exception Handling Patterns](#exception-handling-patterns)
2. [Logging Patterns](#logging-patterns)
3. [Security Patterns](#security-patterns)
4. [Terminal Output Patterns](#terminal-output-patterns)
5. [Code Organization Patterns](#code-organization-patterns)

---

## Exception Handling Patterns

### Anti-Pattern: Bare Except Clauses

**Problem:**
```python
try:
    risky_operation()
except:  # BAD: Catches everything, including SystemExit and KeyboardInterrupt
    handle_error()
```

**Issues:**
- Hides bugs by catching all exceptions indiscriminately
- Catches system exceptions (SystemExit, KeyboardInterrupt) that should propagate
- Makes debugging extremely difficult
- No error context for logging or user feedback

**Solution:**
```python
try:
    risky_operation()
except (ValueError, IndexError) as e:  # GOOD: Specific exceptions
    logger.error(f"Operation failed: {e}")
    handle_error()
```

**Best Practices:**
1. **Always specify exception types** - Only catch what you can handle
2. **Capture exception object** - Use `as e` for logging and debugging
3. **Log the error** - Include context about what failed
4. **Consider exception hierarchy** - Use base classes when appropriate:
   - `OSError` for file/network operations
   - `subprocess.CalledProcessError` for subprocess failures
   - `ValueError` for invalid values
   - `TypeError` for type mismatches

**Examples from GitSage:**

```python
# Before (CQ001): readme-generator.py:562
except:
    config['badges']['shields'] = ['license', 'version', 'stars', 'maintained']

# After:
except (ValueError, IndexError) as e:
    console.print(f"[yellow][WARN] Invalid badge selection: {e}. Using defaults.[/yellow]")
    config['badges']['shields'] = ['license', 'version', 'stars', 'maintained']
```

```python
# Before (CQ002): check_installation.py:57
except:
    return False, "Not installed"

# After:
except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
    return False, f"Not installed ({type(e).__name__})"
```

**When to use broader exceptions:**
- `Exception` - When you truly need to catch all non-system exceptions
- Only in top-level error handlers (main loops, API endpoints)
- Always log the full traceback

---

## Logging Patterns

### Anti-Pattern: Using print() in Applications

**Problem:**
```python
print(f"Starting server on port {port}")  # BAD: No log level, can't filter
print("Error occurred!")  # BAD: Goes to stdout, not stderr
```

**Issues:**
- No log levels (DEBUG, INFO, WARNING, ERROR)
- Can't filter or route different severity levels
- Difficult to disable in production
- No timestamps or context
- Can't easily redirect to files
- Mixes application output with logging

**Solution:**
```python
logger.info(f"Starting server on port {port}")  # GOOD: Proper log level
logger.error("Error occurred!", exc_info=True)  # GOOD: Includes traceback
```

**Best Practices:**
1. **Use logger for application messages** - Reserve print() only for:
   - Direct user output (CLI tools showing results)
   - Interactive prompts (input/output)
   - Formatted reports meant for users
2. **Choose appropriate log levels:**
   - `DEBUG` - Detailed information for diagnosing problems
   - `INFO` - Confirmation that things are working as expected
   - `WARNING` - Indication something unexpected happened (but continue)
   - `ERROR` - Serious problem, function couldn't complete
   - `CRITICAL` - Very serious error, program may not be able to continue
3. **Include context** - Add relevant variables and state
4. **Use structured logging** - Consider JSON logging for production

**Examples from GitSage:**

```python
# Before (CQ010): src/gitsage/web/app.py:504-506
print(f"Starting {PROJECT_NAME} Web Interface v{__version__}")
print("Access at: http://localhost:5000")
print("Press Ctrl+C to stop")

# After:
logger.info(f"Starting {PROJECT_NAME} Web Interface v{__version__}")
logger.info("Access at: http://localhost:5000")
logger.info("Press Ctrl+C to stop")
```

**When print() is appropriate:**
- CLI commands showing formatted output to users
- Interactive wizards with prompts
- Help text and usage information
- Progress bars and status updates for users
- Test output (though pytest captures this)

---

## Security Patterns

### Pattern: Web Application Security Headers

**Problem:**
Modern web applications without security headers are vulnerable to:
- Cross-Site Scripting (XSS)
- Clickjacking
- MIME-type sniffing attacks
- Man-in-the-middle attacks

**Solution:**
```python
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: https:;"
    return response
```

**Header Explanations:**

1. **X-Content-Type-Options: nosniff**
   - Prevents browser from MIME-sniffing
   - Forces browser to respect declared Content-Type
   - Prevents executing scripts disguised as images

2. **X-Frame-Options: SAMEORIGIN**
   - Prevents clickjacking attacks
   - Only allows framing from same origin
   - Alternative: DENY (no framing at all)

3. **X-XSS-Protection: 1; mode=block**
   - Enables XSS filter in older browsers
   - Blocks page if XSS attack detected
   - Modern browsers use CSP instead

4. **Strict-Transport-Security (HSTS)**
   - Forces HTTPS connections
   - Prevents protocol downgrade attacks
   - `max-age=31536000` - 1 year validity
   - `includeSubDomains` - Applies to all subdomains

5. **Content-Security-Policy (CSP)**
   - Controls resource loading
   - Prevents XSS by restricting script sources
   - `default-src 'self'` - Only load from same origin
   - `'unsafe-inline'/'unsafe-eval'` - Allow inline scripts (relax for development)
   - `img-src 'self' data: https:` - Images from self, data URIs, or HTTPS

**Production Hardening:**
```python
# Tighten CSP for production
response.headers['Content-Security-Policy'] = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "  # CSS often needs unsafe-inline
    "img-src 'self' data: https:; "
    "font-src 'self'; "
    "connect-src 'self'; "
    "frame-ancestors 'none';"
)
```

### Pattern: CSRF Protection

**Problem:**
Without CSRF protection, attackers can trick authenticated users into performing unwanted actions.

**Solution:**
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
csrf.init_app(app)
```

**Best Practices:**
1. **Enable CSRF globally** - Protect all POST/PUT/DELETE endpoints
2. **Exempt API endpoints** - Use `@csrf.exempt` for stateless APIs
3. **Include tokens in forms** - `{{ csrf_token() }}` in templates
4. **AJAX requests** - Include `X-CSRFToken` header

**Example from GitSage (SEC001):**
```python
# Enable CSRF protection with graceful fallback
if CSRF_AVAILABLE:
    csrf = CSRFProtect()
    csrf.init_app(app)
    logger.info("CSRF protection enabled")
else:
    logger.warning("Flask-WTF not installed, CSRF protection disabled")
```

---

## Terminal Output Patterns

### Pattern: ASCII-Only Terminal Characters

**Problem:**
Emoji and Unicode characters in terminal output cause alignment issues:
- Single-width character space with double-width display
- Breaks table formatting and borders
- Inconsistent rendering across terminals
- May not display on all systems (Windows PowerShell)

**Anti-Pattern:**
```powershell
Write-Host "[✓] Success" -ForegroundColor Green  # BAD: Emoji breaks alignment
Write-Host "[✗] Failed" -ForegroundColor Red     # BAD: May not render
```

**Issues:**
- ✓ (U+2713) and ✗ (U+2717) are double-width in many terminals
- String padding treats them as 1 character, causing misalignment
- Not universally supported
- Accessibility issues with screen readers

**Solution:**
```powershell
Write-Host "[OK] Success" -ForegroundColor Green    # GOOD: ASCII-only
Write-Host "[FAIL] Failed" -ForegroundColor Red     # GOOD: Consistent width
```

**Standard ASCII Replacements:**
```
✓ → [OK] or [*]
✗ → [FAIL] or [X]
→ → -> or >>
⚠ → [WARN] or [!]
💡 → [!] or [INFO]
🎯 → [>>]
📦 → [PKG]
🚀 → [ROCKET]
📊 → [STATS]
🔧 → [TOOL]
```

**Benefits:**
- Perfect alignment in all terminals
- Works on all operating systems
- Better accessibility
- Easier to grep/search
- Professional appearance

**Examples from GitSage (CQ011, CQ012):**
```powershell
# Before:
function Write-Success {
    Write-Host "[✓] $Message" -ForegroundColor Green
}
function Write-Error {
    Write-Host "[✗] $Message" -ForegroundColor Red
}

# After:
function Write-Success {
    Write-Host "[OK] $Message" -ForegroundColor Green
}
function Write-Error {
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}
```

**Box Drawing:**
Instead of Unicode box characters (│─┌┐└┘), use ASCII:
```
║ → |
═ → =
╔╗╚╝ → +--+
```

---

## Code Organization Patterns

### Pattern: Python File Naming Conventions

**Problem:**
Python files with hyphens instead of underscores create import issues:

**Anti-Pattern:**
```bash
readme-generator.py  # BAD: Can't import directly
backup-manager.py    # BAD: Hyphen not valid in Python identifiers
```

**Issues:**
```python
import readme-generator  # SyntaxError: invalid syntax
from readme-generator import ReadmeGenerator  # SyntaxError
```

**Workarounds (hacky):**
```python
readme_gen = __import__('readme-generator')  # Works but ugly
```

**Solution:**
```bash
readme_generator.py  # GOOD: PEP 8 compliant
backup_manager.py    # GOOD: Can import normally
```

```python
import readme_generator  # Clean import
from backup_manager import BackupManager  # Pythonic
```

**PEP 8 Guidelines:**
- Module names: lowercase with underscores
- Package names: lowercase, preferably without underscores
- Class names: CapWords (PascalCase)
- Function/variable names: lowercase with underscores

**Migration Strategy:**
1. Create new file with underscored name
2. Update all imports in codebase
3. Update tests
4. Update documentation
5. Use `git mv` to preserve history
6. Delete old hyphenated file

**Example Renames Needed (CQ004):**
```
backup-manager.py → backup_manager.py
readme-generator.py → readme_generator.py
script-generator.py → script_generator.py
wiki-generator.py → wiki_generator.py
```

---

## Pattern Summary Table

| Pattern | Anti-Pattern | Solution | Priority | Effort |
|---------|--------------|----------|----------|--------|
| Exception Handling | `except:` | `except (ValueError, IndexError) as e:` | High | Low |
| Logging | `print("msg")` | `logger.info("msg")` | Medium | Low |
| Security Headers | No headers | `@app.after_request` decorator | High | Low |
| CSRF Protection | No CSRF | `CSRFProtect().init_app(app)` | High | Low |
| Terminal Output | Emoji chars | ASCII equivalents `[OK]` | Medium | Low |
| File Naming | `file-name.py` | `file_name.py` | Low | High* |

*High effort due to import updates across codebase

---

## Pattern Detection Checklist

Use this checklist to scan new code:

### Code Quality
- [ ] No bare `except:` clauses
- [ ] Specific exception types caught
- [ ] Exceptions logged with context
- [ ] Using logger instead of print()
- [ ] Appropriate log levels (DEBUG/INFO/WARNING/ERROR)
- [ ] Python files use underscores, not hyphens

### Security
- [ ] CSRF protection enabled for web apps
- [ ] Security headers on all HTTP responses
- [ ] Input validation on all user inputs
- [ ] No SQL injection vulnerabilities
- [ ] No command injection (subprocess with user input)
- [ ] Secrets not hardcoded

### Terminal/CLI
- [ ] ASCII-only characters in output
- [ ] Consistent padding/alignment
- [ ] Color used purposefully
- [ ] Progress indicators for long operations
- [ ] Graceful degradation without color support

### Testing
- [ ] Unit tests for all public functions
- [ ] Integration tests for workflows
- [ ] Edge cases covered
- [ ] Error paths tested
- [ ] Mocks used for external dependencies

---

## References

- PEP 8: Style Guide for Python Code
- OWASP Top 10 Web Application Security Risks
- Flask Security Best Practices
- Python Logging Cookbook
- Terminal Color & Formatting Guide

---

## Changelog

- **2025-11-27**: Initial pattern library created from Phase 1 implementations
  - Added exception handling patterns (CQ001, CQ002)
  - Added logging patterns (CQ010)
  - Added security patterns (SEC001, SEC004)
  - Added terminal output patterns (CQ011, CQ012)
  - Added file naming patterns (CQ004 reference)
