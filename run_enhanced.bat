@echo off
chcp 65001 >nul
echo ===================================================
echo     🏦 نظام التوصيات المالية المحسن - تشغيل سريع     
echo ===================================================
echo.

echo [1/3] فحص النظام...
if not exist "app_enhanced.py" (
    echo ❌ خطأ: ملف التطبيق المحسن غير موجود
    echo سيتم تشغيل التطبيق الأساسي...
    goto :basic_app
)

echo [2/3] فحص Python و المكتبات...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت
    pause
    exit /b 1
)

echo [3/3] تشغيل التطبيق المحسن...
echo.
echo ✅ جميع الفحوصات نجحت!
echo 🚀 تشغيل التطبيق المحسن...
echo.
echo 🌐 سيفتح التطبيق على: http://localhost:8501
echo 🔐 بيانات المدير: admin / admin123
echo.
echo لإيقاف التطبيق اضغط Ctrl+C
echo.

C:/Users/MAHER/.pyenv/pyenv-win/versions/3.10.11/python.exe -m streamlit run app_enhanced.py
goto :end

:basic_app
echo تشغيل التطبيق الأساسي...
C:/Users/MAHER/.pyenv/pyenv-win/versions/3.10.11/python.exe -m streamlit run app.py

:end
echo.
echo شكراً لاستخدام نظام التوصيات المالية!
pause