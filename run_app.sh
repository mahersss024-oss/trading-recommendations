#!/bin/bash

# سكريبت تشغيل تطبيق التوصيات التجارية
echo "🚀 بدء تشغيل تطبيق التوصيات التجارية..."

# التأكد من تثبيت المتطلبات
echo "📦 فحص المتطلبات..."
pip install -r requirements.txt

# تشغيل تطبيق Streamlit
echo "🌐 تشغيل التطبيق على المنفذ 8501..."
streamlit run app_streamlit.py --server.port=8501 --server.address=0.0.0.0

echo "✅ التطبيق جاهز على: http://localhost:8501"