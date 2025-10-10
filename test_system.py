#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع للتأكد من عمل النظام
"""

import sqlite3
import os

def test_invite_codes_system():
    """اختبار نظام رموز الدعوة"""
    print("🧪 اختبار نظام رموز الدعوة...")
    
    DB_NAME = 'trading_recommendations.db'
    
    if not os.path.exists(DB_NAME):
        print("❌ قاعدة البيانات غير موجودة!")
        return False
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # التحقق من جدول رموز الدعوة
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invite_codes'")
        if not cursor.fetchone():
            print("❌ جدول invite_codes غير موجود!")
            return False
        
        # التحقق من الأعمدة
        cursor.execute("PRAGMA table_info(invite_codes)")
        columns = [col[1] for col in cursor.fetchall()]
        required_cols = ['id', 'code', 'created_by', 'created_at', 'expires_at', 'is_active', 'used_by', 'used_at']
        
        missing_cols = [col for col in required_cols if col not in columns]
        if missing_cols:
            print(f"❌ أعمدة مفقودة: {missing_cols}")
            return False
        
        print("✅ جدول invite_codes موجود مع جميع الأعمدة")
        
        # اختبار جلب البيانات
        cursor.execute("SELECT COUNT(*) FROM invite_codes")
        count = cursor.fetchone()[0]
        print(f"📊 عدد رموز الدعوة: {count}")
        
        # اختبار البيانات مع القيم المنطقية
        cursor.execute("SELECT code, is_active FROM invite_codes LIMIT 3")
        rows = cursor.fetchall()
        
        for code, is_active in rows:
            print(f"   كود: {code}, نشط: {bool(is_active)}")
        
        conn.close()
        print("✅ نجح اختبار قاعدة البيانات")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")
        return False

def test_app_import():
    """اختبار استيراد التطبيق"""
    print("\n🧪 اختبار استيراد التطبيق...")
    
    try:
        # محاولة استيراد الوحدات الأساسية
        import streamlit as st
        print("✅ Streamlit")
        
        import pandas as pd
        print("✅ Pandas")
        
        try:
            import plotly.express as px
            print("✅ Plotly")
        except ImportError:
            print("⚠️ Plotly غير متوفر (اختياري)")
        
        # محاولة استيراد الوحدات المحلية
        try:
            from enhancements import track_login_attempts
            print("✅ Enhancements")
        except ImportError:
            print("⚠️ Enhancements غير متوفر (اختياري)")
        
        try:
            from utils import create_chart
            print("✅ Utils")
        except ImportError:
            print("⚠️ Utils غير متوفر (اختياري)")
        
        print("✅ نجح اختبار الاستيراد")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الاستيراد: {e}")
        return False

def test_main_functions():
    """اختبار الوظائف الرئيسية"""
    print("\n🧪 اختبار الوظائف الرئيسية...")
    
    try:
        # قراءة الملف الرئيسي
        with open('app_enhanced.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود الإصلاحات
        checks = [
            ("bool(c.get('is_active', False))", "تحويل القيم المنطقية الآمن"),
            ("c.get('status')", "الوصول الآمن للقاموس"),
            ("def get_invite_codes()", "دالة جلب رموز الدعوة"),
            ("def display_invite_codes_tab()", "تبويب رموز الدعوة"),
            ("'status': status", "حقل الحالة في البيانات")
        ]
        
        all_passed = True
        for check, desc in checks:
            if check in content:
                print(f"✅ {desc}")
            else:
                print(f"❌ {desc}")
                all_passed = False
        
        if all_passed:
            print("✅ جميع الإصلاحات موجودة")
        else:
            print("⚠️ بعض الإصلاحات مفقودة")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الوظائف: {e}")
        return False

if __name__ == "__main__":
    print("🔬 اختبار شامل للنظام")
    print("=" * 40)
    
    db_test = test_invite_codes_system()
    import_test = test_app_import()
    functions_test = test_main_functions()
    
    print("\n📊 ملخص النتائج:")
    print(f"   قاعدة البيانات: {'✅' if db_test else '❌'}")
    print(f"   الاستيراد: {'✅' if import_test else '❌'}")
    print(f"   الوظائف: {'✅' if functions_test else '❌'}")
    
    if all([db_test, import_test, functions_test]):
        print("\n🎉 النظام جاهز وعامل بشكل صحيح!")
        print("🌐 يمكنك الوصول للتطبيق على:")
        print("   http://localhost:8507")
        print("   http://10.0.0.216:8507")
        print("   http://4.240.39.193:8507")
    else:
        print("\n⚠️ يحتاج النظام لمزيد من الإصلاحات")
    
    print("\n🔑 للدخول كمدير:")
    print("   المستخدم: admin")
    print("   كلمة المرور: admin123")