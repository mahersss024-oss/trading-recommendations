#!/bin/bash
# سكريبت النشر البديل

echo "🚀 بدء النشر البديل..."

# إنشاء أرشيف للكود المحدث
tar -czf app_fixed.tar.gz app_enhanced.py enhancements.py utils.py requirements.txt

echo "✅ تم إنشاء أرشيف الكود المحدث: app_fixed.tar.gz"
echo "📤 يمكنك رفع هذا الأرشيف يدوياً إلى منصة النشر"

# معلومات النشر
echo ""
echo "📋 معلومات النشر:"
echo "   - الملف الرئيسي: app_enhanced.py"
echo "   - المنفذ: 8501"
echo "   - متطلبات: requirements.txt"
echo ""
echo "🔧 لنشر على Streamlit Cloud:"
echo "   1. ارفع الملفات إلى GitHub"
echo "   2. اذهب إلى share.streamlit.io"
echo "   3. انشر التطبيق من المستودع"
echo ""
echo "⚡ للنشر السريع المحلي:"
echo "   streamlit run app_enhanced.py --server.port 8501"
