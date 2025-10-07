#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لإضافة التقرير الجديد إلى قاعدة البيانات
"""

import sqlite3
import os
import sys
from datetime import datetime

# إضافة مجلد المشروع للمسار
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# استيراد دوال التطبيق
try:
    from app import parse_recommendations_file, save_report
except ImportError:
    print("❌ خطأ: لا يمكن استيراد دوال التطبيق")
    print("تأكد من وجود ملف app.py في نفس المجلد")
    sys.exit(1)

def add_latest_report():
    """إضافة أحدث تقرير إلى قاعدة البيانات"""
    
    report_file = "latest_report_20251006.txt"
    
    # التحقق من وجود الملف
    if not os.path.exists(report_file):
        print(f"❌ خطأ: ملف التقرير {report_file} غير موجود")
        return False
    
    # قراءة محتوى التقرير
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ تم قراءة ملف التقرير بنجاح")
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        return False
    
    # تحليل التقرير
    try:
        parsed_data = parse_recommendations_file(content)
        print("✅ تم تحليل التقرير بنجاح")
        
        # عرض ملخص البيانات
        stats = parsed_data['stats']
        print(f"📊 إجمالي الرموز: {stats['total_symbols']}")
        print(f"🟢 توصيات الشراء: {stats['buy_recommendations']}")
        print(f"🔴 توصيات البيع: {stats['sell_recommendations']}")
        print(f"⚪ توصيات محايدة: {stats['neutral_recommendations']}")
        print(f"📈 متوسط الثقة: {stats['avg_confidence']:.1f}%")
        
    except Exception as e:
        print(f"❌ خطأ في تحليل التقرير: {e}")
        return False
    
    # حفظ التقرير في قاعدة البيانات
    try:
        report_id = save_report(report_file, content, parsed_data)
        print(f"✅ تم حفظ التقرير بنجاح! رقم التقرير: {report_id}")
        return True
    except Exception as e:
        print(f"❌ خطأ في حفظ التقرير: {e}")
        return False

def check_database():
    """فحص حالة قاعدة البيانات"""
    db_file = "trading_recommendations.db"
    
    if not os.path.exists(db_file):
        print("⚠️ قاعدة البيانات غير موجودة. سيتم إنشاؤها عند تشغيل التطبيق أول مرة.")
        return False
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # عدد التقارير
        cursor.execute("SELECT COUNT(*) FROM reports")
        reports_count = cursor.fetchone()[0]
        
        # عدد المستخدمين
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        # عدد الصفقات
        cursor.execute("SELECT COUNT(*) FROM trades")
        trades_count = cursor.fetchone()[0]
        
        conn.close()
        
        print("📊 حالة قاعدة البيانات:")
        print(f"   • التقارير: {reports_count}")
        print(f"   • المستخدمين: {users_count}")
        print(f"   • الصفقات: {trades_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("       🏦 إضافة تقرير جديد إلى نظام التوصيات")
    print("=" * 60)
    print()
    
    # فحص قاعدة البيانات
    print("[1/3] فحص قاعدة البيانات...")
    check_database()
    print()
    
    # إضافة التقرير
    print("[2/3] إضافة التقرير الجديد...")
    success = add_latest_report()
    print()
    
    # فحص النتيجة
    print("[3/3] فحص النتيجة...")
    if success:
        check_database()
        print()
        print("🎉 تم إضافة التقرير بنجاح!")
        print("يمكنك الآن مشاهدة التقرير في التطبيق عبر:")
        print("http://localhost:8501")
    else:
        print("❌ فشل في إضافة التقرير")
        print("يرجى التحقق من الأخطاء أعلاه")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()