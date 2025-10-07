@echo off
chcp 65001 >nul
echo ===================================================
echo        نظام التوصيات المالية - الإعداد السريع        
echo ===================================================
echo.

echo [1/4] فحص Python...
python --version 2>nul
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت
    echo يرجى تحميل Python من: https://python.org
    pause
    exit /b 1
)
echo ✅ Python مثبت بنجاح

echo.
echo [2/4] فحص pip...
pip --version 2>nul
if errorlevel 1 (
    echo ❌ خطأ: pip غير متوفر
    pause
    exit /b 1
)
echo ✅ pip متوفر

echo.
echo [3/4] تثبيت المكتبات المطلوبة...
echo تثبيت Streamlit...
pip install streamlit -q
if errorlevel 1 (
    echo ❌ خطأ في تثبيت Streamlit
    pause
    exit /b 1
)

echo تثبيت Pandas...
pip install pandas -q
if errorlevel 1 (
    echo ❌ خطأ في تثبيت Pandas
    pause
    exit /b 1
)

echo ✅ تم تثبيت جميع المكتبات بنجاح

echo.
echo [4/4] فحص ملفات التطبيق...
if not exist "app.py" (
    echo ❌ خطأ: ملف app.py غير موجود
    pause
    exit /b 1
)
echo ✅ جميع الملفات موجودة

echo.
echo ===================================================
echo               الإعداد مكتمل بنجاح! ✅               
echo ===================================================
echo.
echo سيتم تشغيل التطبيق الآن...
echo التطبيق سيفتح في المتصفح على العنوان:
echo http://localhost:8501
echo.
echo لإيقاف التطبيق اضغط Ctrl+C
echo.

streamlit run app.py

echo.
echo شكراً لاستخدام نظام التوصيات المالية!
pause