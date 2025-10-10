#!/bin/bash
# إعادة تشغيل آمنة للتطبيق بعد إصلاح KeyError

echo "🔄 إعادة تشغيل التطبيق بعد الإصلاح..."
echo "=========================================="

# 1. إيقاف جميع عمليات Streamlit
echo "⏹️ إيقاف العمليات الجارية..."
pkill -f streamlit 2>/dev/null || true
sleep 2

# 2. مسح الـ cache
echo "🧹 مسح الـ cache..."
rm -rf ~/.streamlit/ 2>/dev/null || true
rm -rf __pycache__/ 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# 3. اختبار سريع لقاعدة البيانات
echo "🔍 اختبار قاعدة البيانات..."
python -c "
import sqlite3
conn = sqlite3.connect('trading_recommendations.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM invite_codes')
count = cursor.fetchone()[0]
print(f'✅ توجد {count} رموز دعوة في قاعدة البيانات')
conn.close()
" 2>/dev/null || echo "⚠️ تحذير: مشكلة في قاعدة البيانات"

# 4. إضافة تأخير للتأكد من إغلاق العمليات
echo "⏳ انتظار 3 ثوانٍ..."
sleep 3

# 5. تشغيل التطبيق
echo "🚀 تشغيل التطبيق..."
echo "📱 سيتم فتح التطبيق على: http://localhost:8501"
echo "💡 إذا كان المنفذ مستخدم، سيتم استخدام منفذ آخر تلقائياً"
echo ""

# تشغيل مع معالجة الأخطاء
python -m streamlit run app_enhanced.py --server.port 8501 --server.address 0.0.0.0

echo ""
echo "🔚 تم إنهاء التطبيق"