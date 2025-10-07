@echo off
REM 🚀 سكريبت النشر السريع لنظام التوصيات المالية (Windows)
REM يقوم بتحضير المشروع للنشر السحابي

echo 🔧 تحضير المشروع للنشر السحابي...
echo.

REM 1. تحديث المكتبات المطلوبة
echo 📦 تحديث requirements.txt...
pip freeze > requirements.txt

REM 2. إنشاء مجلد git إذا لم يكن موجوداً
if not exist ".git" (
    echo 🔄 تهيئة Git repository...
    git init
    git add .
    git commit -m "Initial commit for deployment"
)

REM 3. التحقق من الملفات المطلوبة
echo ✅ التحقق من ملفات النشر...

if exist "requirements.txt" (echo ✓ requirements.txt موجود) else (echo ❌ requirements.txt مفقود)
if exist "Procfile" (echo ✓ Procfile موجود) else (echo ❌ Procfile مفقود)
if exist "runtime.txt" (echo ✓ runtime.txt موجود) else (echo ❌ runtime.txt مفقود)
if exist ".gitignore" (echo ✓ .gitignore موجود) else (echo ❌ .gitignore مفقود)
if exist "app_enhanced.py" (echo ✓ app_enhanced.py موجود) else (echo ❌ app_enhanced.py مفقود)

echo.
echo 🎉 المشروع جاهز للنشر!
echo.
echo الخطوات التالية:
echo 1. أرفع المشروع على GitHub
echo 2. اذهب إلى https://share.streamlit.io/
echo 3. اربط حسابك وانشر التطبيق
echo.
echo أو استخدم أحد الأوامر التالية:
echo.
echo 🔵 Heroku:
echo heroku create your-app-name
echo git push heroku main
echo.
echo 🟣 Railway:
echo railway login
echo railway init
echo railway up
echo.

REM 4. فتح دليل النشر
if exist "C:\Program Files\Microsoft VS Code\Code.exe" (
    echo 📖 فتح دليل النشر...
    "C:\Program Files\Microsoft VS Code\Code.exe" DEPLOYMENT_GUIDE.md
)

echo ✨ تم الانتهاء من التحضير!
pause