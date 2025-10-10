#!/bin/bash
# ملف تشغيل مبسط للتطبيق المُحدث

echo "🚀 تشغيل نظام التوصيات المالية (النسخة المُحدثة)"
echo "=================================="

# إيقاف أي عمليات Streamlit سابقة
echo "⏹️ إيقاف العمليات السابقة..."
pkill -f streamlit 2>/dev/null || true

# انتظار ثانية للتأكد
sleep 1

# تشغيل التطبيق
echo "🔄 تشغيل التطبيق..."
echo "📍 سيعمل على: http://localhost:8506"
echo ""

# تشغيل مع Python من البيئة الافتراضية
/workspaces/trading-recommendations/.venv/bin/python -m streamlit run app_enhanced.py --server.port 8506 --server.address 0.0.0.0