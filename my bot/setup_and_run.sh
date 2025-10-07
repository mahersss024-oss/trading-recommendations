#!/bin/bash

echo "====================================================="
echo "     نظام التوصيات المالية - الإعداد السريع"
echo "====================================================="
echo

echo "[1/4] فحص Python..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 مثبت بنجاح"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    echo "✅ Python مثبت بنجاح"
    PYTHON_CMD="python"
else
    echo "❌ خطأ: Python غير مثبت"
    echo "يرجى تثبيت Python من: https://python.org"
    exit 1
fi

echo
echo "[2/4] فحص pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 متوفر"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo "✅ pip متوفر"
    PIP_CMD="pip"
else
    echo "❌ خطأ: pip غير متوفر"
    exit 1
fi

echo
echo "[3/4] تثبيت المكتبات المطلوبة..."
echo "تثبيت Streamlit..."
$PIP_CMD install streamlit
if [ $? -ne 0 ]; then
    echo "❌ خطأ في تثبيت Streamlit"
    exit 1
fi

echo "تثبيت Pandas..."
$PIP_CMD install pandas
if [ $? -ne 0 ]; then
    echo "❌ خطأ في تثبيت Pandas"
    exit 1
fi

echo "✅ تم تثبيت جميع المكتبات بنجاح"

echo
echo "[4/4] فحص ملفات التطبيق..."
if [ ! -f "app.py" ]; then
    echo "❌ خطأ: ملف app.py غير موجود"
    exit 1
fi
echo "✅ جميع الملفات موجودة"

echo
echo "====================================================="
echo "              الإعداد مكتمل بنجاح! ✅"
echo "====================================================="
echo
echo "سيتم تشغيل التطبيق الآن..."
echo "التطبيق سيفتح في المتصفح على العنوان:"
echo "http://localhost:8501"
echo
echo "لإيقاف التطبيق اضغط Ctrl+C"
echo

streamlit run app.py

echo
echo "شكراً لاستخدام نظام التوصيات المالية!"