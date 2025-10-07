@echo off
chcp 65001 >nul
echo ===================================================
echo        إضافة تقرير جديد إلى نظام التوصيات         
echo ===================================================
echo.

echo جاري إضافة التقرير الجديد...
C:/Users/MAHER/.pyenv/pyenv-win/versions/3.10.11/python.exe add_report.py

echo.
echo اضغط أي مفتاح للمتابعة...
pause >nul