#!/bin/bash
# تشغيل التطبيق مع نظام الثيم الجديد

echo "🎨 تشغيل التطبيق مع نظام الثيم الجديد..."
echo "=============================================="

# إيقاف العمليات الجارية
echo "⏹️ إيقاف العمليات السابقة..."
pkill -f streamlit 2>/dev/null || true
sleep 2

# مسح الـ cache
echo "🧹 مسح الـ cache..."
rm -rf ~/.streamlit/ 2>/dev/null || true
rm -rf __pycache__/ 2>/dev/null || true

echo ""
echo "🎯 المميزات الجديدة:"
echo "  ☀️ لايت ثيم (الافتراضي)"
echo "  🌙 دارك ثيم"
echo "  🎛️ تبديل سهل من الشريط الجانبي"
echo "  🎨 ألوان محسنة ومتناسقة"
echo "  📱 دعم كامل للعربية"
echo ""

echo "💡 كيفية الاستخدام:"
echo "  1. شغل التطبيق"
echo "  2. اذهب للشريط الجانبي"
echo "  3. ابحث عن 'إعدادات المظهر'"
echo "  4. اختر الثيم المفضل"
echo ""

echo "🚀 تشغيل التطبيق..."
echo "📱 سيتم فتح التطبيق على: http://localhost:8501"
echo ""

# تشغيل التطبيق
python -m streamlit run app_enhanced.py --server.port 8501 --server.address 0.0.0.0

echo ""
echo "🔚 تم إنهاء التطبيق"