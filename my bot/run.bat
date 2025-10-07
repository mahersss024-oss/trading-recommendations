@echo off
echo تشغيل نظام التوصيات المالية...
echo.
echo تأكد من تثبيت Python و pip
echo.
echo تثبيت المكتبات المطلوبة...
pip install streamlit pandas
echo.
echo تشغيل التطبيق...
streamlit run app.py
pause