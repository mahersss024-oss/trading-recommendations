# Trading Recommendations System - AI Agent Guidelines

## Project Overview
Arabic financial trading recommendations system built with Streamlit. Analyzes trading reports, manages users with role-based access, and supports multi-platform cloud deployment.

## Architecture & Core Components

### Main Application Files
- **`app_enhanced.py`** - Primary application entry point (3200+ lines)
- **`app.py`** - Simplified version for basic functionality
- **`enhancements.py`** - Security features, login tracking, report management
- **`utils.py`** - Chart creation, data visualization utilities
- **`control_panel.py`** - System management and requirements checking

### Database Schema (SQLite)
Three main tables with specific patterns:
```sql
-- Users table with admin roles and permissions
users: id, username, email, password_hash, phone, subscription_type, subscription_end, is_admin, admin_role, admin_permissions

-- Reports storage with parsed statistics  
reports: id, filename, content, upload_time, market_analysis, total_symbols, buy_recommendations, sell_recommendations, avg_confidence

-- Individual trade details linked to reports
trades: id, report_id, symbol, price, recommendation, confidence, stop_loss, target_profit, risk_reward_ratio, rsi, macd, trend
```

## Critical Patterns & Conventions

### Database Path Resolution
**CRITICAL**: Database path varies by environment:
```python
# Always use this pattern for DB_NAME
if os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'):
    DB_NAME = '/tmp/trading_recommendations.db' if os.path.exists('/tmp') else 'trading_recommendations.db'
else:
    DB_NAME = 'trading_recommendations.db'
```

### Authentication & Session Management
- Session state key: `st.session_state.user` (Dict with user info)
- Login attempts tracking in `st.session_state.login_attempts[username]`
- 5-minute cooldown after 5 failed attempts
- Password hashing: `hashlib.sha256(password.encode()).hexdigest()`
- Admin detection: `user.get('is_admin')` boolean check

### Report File Parsing
The `parse_recommendations_file()` function expects specific Arabic text patterns:
- Market analysis sections: "حالة السوق", "مؤشر RSI", "قوة الاتجاه"
- Table detection: "جدول الصفقات التفصيلي" or lines containing "│"
- Recommendation keywords: "شراء" (buy), "بيع" (sell), "🟢" (buy emoji), "🔴" (sell emoji)
- Returns structured dict with `market_analysis`, `trades`, and `stats` keys

### Import Strategy
Modular imports with fallback handling:
```python
try:
    from enhancements import track_login_attempts, enhanced_password_validation
except ImportError:
    pass  # Continue without enhanced features
```

## Development Workflows

### Local Development
```bash
# Quick start (Windows)
run_enhanced.bat

# Manual start
pip install -r requirements.txt
streamlit run app_enhanced.py

# Add new report via script
python add_report.py
```

### Cloud Deployment Setup
Run deployment preparation:
```bash
# Linux/Mac
chmod +x deploy_setup.sh && ./deploy_setup.sh

# Windows  
deploy_setup.bat
```

### Multi-Platform Deployment
- **Streamlit Cloud**: Uses `app_enhanced.py` directly, automatic GitHub integration
- **Heroku**: Requires `Procfile` with port binding
- **Railway**: Uses `railway.toml` configuration
- **All platforms**: Support both `requirements.txt` and `requirements_cloud.txt`

## UI & Styling Patterns

### Arabic RTL Support
Extensive CSS customization for right-to-left text direction:
- Custom sidebar styling with RTL support
- Arabic font loading: "Noto Sans Arabic", "Cairo"
- Tab styling with Arabic text alignment
- Form elements with proper RTL layout

### Streamlit Component Patterns
- Tab-based navigation: `st.tabs()` with Arabic labels
- Form submission: Always use `st.form()` for user inputs
- Metrics display: `st.metric()` for key statistics
- File uploads: `st.file_uploader()` with `.txt` type restriction

## Security Considerations

### Login Security
- Failed login tracking per username
- Temporary lockout after 5 attempts (5 minutes)
- Session state reset on successful login
- Admin permissions stored as comma-separated strings

### Data Protection
- Password hashing (SHA-256)
- No plaintext password storage
- Session-based authentication
- Admin role separation

## Testing & Validation

### File Upload Testing
Test with Arabic trading reports containing:
- Market analysis sections in Arabic
- Pipe-separated table data (`│`)
- Arabic financial terms
- Numeric confidence values and ratios

### Multi-User Testing
- Test admin vs regular user permissions
- Verify subscription validation logic
- Test login attempt tracking and cooldowns

## Common Debugging Points

1. **Database Connection**: Always check `DB_NAME` path resolution
2. **File Parsing**: Print debug info in `parse_recommendations_file()`
3. **Session State**: Clear `st.session_state` during development
4. **Import Errors**: Handle missing `enhancements.py` gracefully
5. **RTL Issues**: Check CSS selectors for Arabic text alignment

## File Structure Notes
- `my bot/` directory contains duplicate files (legacy)
- Multiple app versions: `app.py`, `app_enhanced.py`, `app_enhanced_fixed.py`
- Deployment configs for each platform in root directory
- Batch files for Windows, shell scripts for Unix systems