@echo off
echo 🚀 تشغيل نظام التوصيات المالية المتقدم...
echo.
echo ⏳ جاري التحقق من المكتبات...

REM التحقق من وجود streamlit
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 تثبيت Streamlit...
    pip install streamlit pandas plotly
)

echo ✅ جاري بدء التطبيق...
echo.
echo 🌐 سيتم فتح التطبيق في المتصفح تلقائياً...
echo 📍 الرابط المحلي: http://localhost:8501
echo.
echo 👤 بيانات المدير الافتراضية:
echo    اسم المستخدم: admin
echo    كلمة المرور: admin123
echo.
echo ⚠️  لإيقاف التطبيق: اضغط Ctrl+C في هذه النافذة
echo.

streamlit run app_enhanced.py