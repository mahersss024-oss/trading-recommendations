#!/bin/bash
# نظافة تحذيرات Pylance وتحسين الأداء

echo "🧹 تنظيف تحذيرات Pylance وتحسين الأداء..."
echo "================================================"

# مسح cache Python
echo "🗑️ مسح Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# مسح cache VS Code
echo "🗑️ مسح VS Code cache..."
rm -rf ~/.vscode/extensions/ms-python*/pythonFiles/cache/ 2>/dev/null || true
rm -rf .vscode/.ropeproject 2>/dev/null || true

# مسح cache Pylance
echo "🗑️ مسح Pylance cache..."
rm -rf ~/.cache/pylance/ 2>/dev/null || true
rm -rf ~/.vscode/extensions/ms-python.vscode-pylance*/dist/bundled/stubs/ 2>/dev/null || true

# إعادة تحميل إعدادات VS Code
echo "🔄 إعادة تحميل إعدادات VS Code..."
if command -v code &> /dev/null; then
    code . --reload-window &
    echo "✅ تم إعادة تحميل VS Code"
else
    echo "⚠️ VS Code غير متاح في سطر الأوامر"
fi

# إعادة تشغيل خدمة Python
echo "🔄 إعادة تشغيل خدمة Python..."
pkill -f "python.*language.*server" 2>/dev/null || true
sleep 2

# فحص حالة التحسينات
echo ""
echo "📋 حالة التحسينات:"
echo "================================"

# فحص الملفات المهمة
important_files=(
    ".vscode/settings.json"
    "pyrightconfig.json" 
    "pyproject.toml"
    ".pylintrc"
)

for file in "${important_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file - موجود"
    else
        echo "❌ $file - مفقود"
    fi
done

# إحصائيات الملفات
echo ""
echo "📊 إحصائيات الملفات:"
echo "  🐍 ملفات Python النشطة: $(find . -name "*.py" -not -path "./*backup*" -not -path "./*fixed*" -not -path "./my bot/*" | wc -l)"
echo "  📄 ملفات Backup: $(find . -name "*backup*.py" | wc -l)"
echo "  🗄️ مجلدات __pycache__: $(find . -type d -name "__pycache__" | wc -l)"

echo ""
echo "💡 نصائح لتجنب التحذيرات:"
echo "  1. استخدم app_enhanced.py بدلاً من الملفات الاحتياطية"
echo "  2. تجاهل التحذيرات في الملفات الاحتياطية"
echo "  3. ركز على الملفات النشطة فقط"
echo "  4. استخدم نظام الثيم الجديد"

echo ""
echo "🎉 تم تنظيف التحذيرات بنجاح!"
echo "💡 أعد تشغيل VS Code إذا استمرت المشاكل"