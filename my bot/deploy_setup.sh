#!/bin/bash

# 🚀 سكريبت النشر السريع لنظام التوصيات المالية
# يقوم بتحضير المشروع للنشر السحابي

echo "🔧 تحضير المشروع للنشر السحابي..."

# 1. تحديث المكتبات المطلوبة
echo "📦 تحديث requirements.txt..."
pip freeze > requirements.txt

# 2. إنشاء مجلد git إذا لم يكن موجوداً
if [ ! -d ".git" ]; then
    echo "🔄 تهيئة Git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
fi

# 3. التحقق من الملفات المطلوبة
echo "✅ التحقق من ملفات النشر..."

files=("requirements.txt" "Procfile" "runtime.txt" ".gitignore" "app_enhanced.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file موجود"
    else
        echo "❌ $file مفقود"
    fi
done

echo ""
echo "🎉 المشروع جاهز للنشر!"
echo ""
echo "الخطوات التالية:"
echo "1. أرفع المشروع على GitHub"
echo "2. اذهب إلى https://share.streamlit.io/"
echo "3. اربط حسابك وانشر التطبيق"
echo ""
echo "أو استخدم أحد الأوامر التالية:"
echo ""
echo "🔵 Heroku:"
echo "heroku create your-app-name"
echo "git push heroku main"
echo ""
echo "🟣 Railway:"
echo "railway login"
echo "railway init"
echo "railway up"
echo ""

# 4. فتح دليل النشر
if command -v code &> /dev/null; then
    echo "📖 فتح دليل النشر..."
    code DEPLOYMENT_GUIDE.md
fi

echo "✨ تم الانتهاء من التحضير!"