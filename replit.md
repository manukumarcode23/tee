# Terabox Multi-Account Login Automation Tool

## Overview
A Python-based automation tool that uses Selenium WebDriver to automatically log into multiple Terabox accounts (1024terabox.com) simultaneously. Each account runs in its own fully private browser session with no cookie sharing between accounts.

## Purpose
Automate the Terabox login process for multiple accounts, maintain 24/7 sessions, and enable automated workflows with complete privacy isolation.

## Current State
- **Status**: Fully functional with multi-account support
- **Website**: https://www.1024terabox.com/
- **Last Updated**: October 28, 2025
- **Verified**: Successfully logs in multiple accounts and redirects to https://dm.1024terabox.com/ai/index

## Key Features ✨
- ✅ **Multiple Account Support** - Login to unlimited Terabox accounts simultaneously
- ✅ **Full Private Browsing** - Each account runs in incognito mode (no cookie sharing)
- ✅ **24/7 Session Keeping** - Maintain sessions alive indefinitely
- ✅ **Isolated Sessions** - Each account has its own private browser instance
- ✅ **Parallel Login** - All accounts login simultaneously for speed
- ✅ **Headless & Visible Modes** - Choose between background or visible browser
- ✅ **Screenshot Capture** - Automatic screenshots for verification
- ✅ **Anti-Bot Detection** - Bypasses automation detection
- ✅ **JSON Configuration** - Easy account management via config file
- ✅ **Telegram Notifications** - Automatically sends captured cookies to your Telegram bot
- ✅ **Filtered Cookie Format** - Extracts specific cookies in custom order (browserid first)

## Project Architecture

### Directory Structure
```
.
├── src/
│   ├── __init__.py
│   ├── terabox_automation.py      # Single account automation with incognito mode
│   └── multi_account_manager.py   # Multi-account orchestration
├── test_terabox.py                # Main entry point
├── accounts.json                  # Your account credentials (gitignored)
├── accounts.json.example          # Example configuration file
├── pyproject.toml                 # Python dependencies
└── replit.md                      # This file
```

### Key Components

**TeraboxAutomation Class** (`src/terabox_automation.py`)
- Manages individual account automation
- **Full incognito mode** - Each instance runs in private browsing
- Executes 6-step login process:
  1. Navigate to Terabox homepage
  2. Click the Login button
  3. Wait for login dialog to appear
  4. Click the email icon
  5. Fill in email and password
  6. Submit and verify login
- Session keep-alive functionality
- Headless and visible browser modes
- Screenshot capture functionality
- Anti-bot detection bypass
- **Cookie capture & Telegram notification**:
  - Captures cookies from https://dm.1024terabox.com/ai/index?clearCache=1
  - Filters and orders cookies: browserid, lang, __bid_n, ab_sr, ri, ndus
  - HTML-escapes all content for safe Telegram delivery
  - Sends formatted message to Telegram bot after login

**MultiAccountManager Class** (`src/multi_account_manager.py`)
- Orchestrates multiple accounts
- **No cookie sharing** - Each account isolated in private tab
- Parallel login execution using threading
- 24/7 session management
- Status monitoring and reporting
- Automatic error handling per account

**Main Script** (`test_terabox.py`)
- Loads accounts from JSON configuration
- Interactive mode selection
- Manages all accounts through lifecycle
- Session keeping with graceful shutdown

## Dependencies
- Python 3.11
- Selenium 4.38.0+
- requests (for Telegram API)
- html (built-in for HTML escaping)
- webdriver-manager 4.0.2+
- Chromium (auto-installed)
- ChromeDriver (auto-managed)

## Setup & Usage

### 1. Configure Your Accounts

Create `accounts.json` based on the example:

```bash
cp accounts.json.example accounts.json
```

Edit `accounts.json` with your credentials:

```json
{
  "accounts": [
    {
      "name": "Work Account",
      "email": "work@example.com",
      "password": "your-password-1"
    },
    {
      "name": "Personal Account",
      "email": "personal@example.com",
      "password": "your-password-2"
    },
    {
      "name": "Backup Account",
      "email": "backup@example.com",
      "password": "your-password-3"
    }
  ]
}
```

**Security Note**: `accounts.json` is gitignored to protect your credentials.

### 2. Run the Multi-Account Automation

```bash
python test_terabox.py
```

The script will:
1. Load all accounts from `accounts.json`
2. Ask if you want headless mode (y/n)
3. Login to all accounts **simultaneously**
4. Each account gets its own **private browser** (incognito mode)
5. Ask if you want to keep sessions alive 24/7 (y/n)
6. Monitor all sessions and report status

### 3. Example Output

```
============================================================
Terabox Multi-Account Login Automation
============================================================
Features:
  • Multiple account support
  • Full private browsing (incognito mode)
  • No cookie sharing between accounts
  • 24/7 session keeping
============================================================

Loaded 3 account(s) from accounts.json

Run in headless mode? (y/n, default=n): y

============================================================
[Manager] Logging in 3 accounts...
[Manager] Each in FULL PRIVATE mode (no cookie sharing)
============================================================

[Work Account] Browser initialized in PRIVATE mode
[Personal Account] Browser initialized in PRIVATE mode
[Backup Account] Browser initialized in PRIVATE mode
[Work Account] Navigating to Terabox...
[Personal Account] Navigating to Terabox...
[Backup Account] Navigating to Terabox...
...
[Manager] ✓ Work Account logged in successfully
[Manager] ✓ Personal Account logged in successfully
[Manager] ✓ Backup Account logged in successfully

============================================================
[Manager] All login attempts completed

Status Summary:
  Total Accounts: 3
  ✓ Logged In: 3
  ✗ Failed: 0
  • Pending: 0

Account Details:
  ✓ Work Account: logged_in
  ✓ Personal Account: logged_in
  ✓ Backup Account: logged_in
============================================================

✓ 3 account(s) logged in successfully

Keep sessions alive 24/7? (y/n, default=y): y

Starting 24/7 session keeper...
Each account maintains its own private session
Press Ctrl+C to stop

[Manager] Starting 24/7 session keeper (interval: 300s)
[Manager] Press Ctrl+C to stop

[Work Account] Session active - 2025-10-28 14:23:45
[Personal Account] Session active - 2025-10-28 14:23:45
[Backup Account] Session active - 2025-10-28 14:23:45
...
```

## How It Works

### Privacy Architecture
1. **Separate Browser Instances** - Each account gets a unique Chrome instance
2. **Incognito Mode** - All instances run with `--incognito` flag
3. **No Cookie Sharing** - Cookies isolated per instance
4. **Independent Sessions** - Accounts cannot interfere with each other

### Login Process Per Account
Each account follows this automated flow:
1. **Navigate** → Opens https://www.1024terabox.com/ in private mode
2. **Click Login** → Finds and clicks the "Login" button
3. **Open Dialog** → Waits for the login dialog to appear
4. **Select Email** → Clicks the email icon
5. **Fill Form** → Enters email and password
6. **Submit** → Clicks submit button
7. **Verify** → Checks URL changed to dashboard
8. **Keep Alive** → Periodically checks session (every 5 minutes)

### 24/7 Session Management
- Each logged-in account runs a background thread
- Pings the browser every 5 minutes (configurable)
- Prevents session timeout
- Runs until Ctrl+C or error

## Advanced Usage

### Programmatic API

```python
from src.multi_account_manager import MultiAccountManager

# Create manager
manager = MultiAccountManager(headless=True)

# Add accounts
manager.add_account("Account1", "email1@example.com", "password1")
manager.add_account("Account2", "email2@example.com", "password2")

# Login all at once
manager.login_all_accounts()

# Keep sessions alive forever
manager.keep_all_sessions_alive(interval=300)

# Or login individually
manager.login_account("Account1")

# Check status
status = manager.get_status()
print(f"Logged in: {status['logged_in']}")

# Cleanup
manager.close_all()
```

### Single Account Usage

```python
from src.terabox_automation import TeraboxAutomation

# Create instance (always in private mode)
automation = TeraboxAutomation(headless=True, account_name="MyAccount")

# Login
success = automation.login("email@example.com", "password")

if success:
    automation.take_screenshot("success.png")
    automation.keep_session_alive(interval=300)

automation.close()
```

## Configuration Options

### Headless Mode
- **True**: Runs in background (no visible browser)
- **False**: Shows browser window (useful for debugging)

### Session Keep-Alive Interval
- Default: 300 seconds (5 minutes)
- Adjustable via `keep_all_sessions_alive(interval=X)`

### Screenshot Naming
- Automatic: `{account_name}_success.png` or `{account_name}_failed.png`
- Custom: Call `automation.take_screenshot("custom_name.png")`

## Security Best Practices

1. **Never commit accounts.json** - Already gitignored
2. **Use strong passwords** - Your credentials are stored in plaintext locally
3. **Limit access** - Only run on trusted machines
4. **Review code** - Understand what automation does before running

## Troubleshooting

### Issue: "Account file not found"
**Solution**: Create `accounts.json` from the example template

### Issue: Login fails for specific account
**Solution**: 
- Check credentials in `accounts.json`
- View screenshot: `{account_name}_failed.png`
- Run in visible mode to see what's happening

### Issue: "ChromeDriver version mismatch"
**Solution**: webdriver-manager auto-updates. If issues persist, clear cache:
```bash
rm -rf ~/.wdm
```

### Issue: Sessions timeout despite keep-alive
**Solution**: Reduce interval to check more frequently:
```python
manager.keep_all_sessions_alive(interval=60)  # Check every minute
```

### Issue: Can see cookies from other accounts
**Solution**: This shouldn't happen! Each account runs in incognito mode. If you see this, it's a bug.

## Recent Changes
- **October 28, 2025**: 
  - ✨ Added multi-account support
  - ✨ Implemented full private browsing (incognito mode)
  - ✨ Added 24/7 session keeping
  - ✨ Created JSON-based account configuration
  - ✨ Added parallel login execution
  - ✨ Isolated each account in separate browser instance
  - ✨ No cookie sharing between accounts
  - ✨ **Added Telegram bot integration** - Cookies automatically sent after login
  - ✨ **Custom cookie filtering** - Extracts specific cookies in user-defined order
  - ✨ **HTML-safe formatting** - Proper escaping for reliable Telegram delivery
  - ✅ Verified working with multiple accounts
  - 📝 Complete documentation rewrite

## User Preferences
- Headless mode by default for efficiency
- Console-based output for automation tasks
- Screenshot evidence for debugging
- JSON configuration for easy account management
- Interactive prompts for mode selection

## Technical Notes
- Uses Chrome incognito mode (`--incognito` flag)
- Each account = separate Chrome process
- Threading for parallel execution
- Daemon threads for session keeping
- Auto-managed ChromeDriver via webdriver-manager
- Anti-automation detection bypass
- 10-second timeout for element detection
- 5-second wait after submission for page load
- Logs all steps per account for debugging
