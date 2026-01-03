# Terabox Multi-Account Login Automation

Automate login to multiple Terabox accounts simultaneously with full privacy isolation.

## Quick Start

### 1. Setup Accounts

```bash
cp accounts.json.example accounts.json
```

Edit `accounts.json` with your credentials:
```json
{
  "accounts": [
    {
      "name": "Account 1",
      "email": "your-email@example.com",
      "password": "your-password"
    }
  ]
}
```

### 2. Run

```bash
python test_terabox.py
```

## Features

✅ **Multiple Accounts** - Login unlimited accounts simultaneously  
✅ **Full Privacy** - Each account in separate incognito browser  
✅ **No Cookie Sharing** - Complete isolation between accounts  
✅ **24/7 Sessions** - Keep all sessions alive indefinitely  
✅ **Parallel Login** - All accounts login at once  

## Documentation

See [replit.md](replit.md) for complete documentation.

## Security

- `accounts.json` is gitignored (never committed)
- Each account runs in incognito mode
- No data sharing between accounts
