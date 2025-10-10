#!/usr/bin/env python3
"""
سكريبت لاختبار وظيفة رموز الدعوة بعد الإصلاح
"""

import sqlite3
import os
import sys
import hashlib
from datetime import datetime, timedelta

# تحديد مسار قاعدة البيانات
if os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'):
    DB_NAME = '/tmp/trading_recommendations.db' if os.path.exists('/tmp') else 'trading_recommendations.db'
else:
    DB_NAME = 'trading_recommendations.db'

def test_invite_code_functionality():
    """اختبار وظيفة رموز الدعوة"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        print("🧪 اختبار وظيفة رموز الدعوة...")
        
        # 1. إنشاء رمز دعوة تجريبي
        test_code = "TEST1234"
        expires_at = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        
        # حذف رمز الاختبار إذا كان موجوداً
        cursor.execute("DELETE FROM invite_codes WHERE code = ?", (test_code,))
        
        # إدراج رمز الاختبار
        cursor.execute('''
            INSERT INTO invite_codes (
                code, created_by, expires_at, subscription_type, 
                subscription_duration_days, max_uses, current_uses, 
                is_active, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_code, 1, expires_at, 'premium', 
            30, 1, 0, True, 'رمز اختبار'
        ))
        
        print(f"✅ تم إنشاء رمز اختبار: {test_code}")
        
        # 2. اختبار الاستعلام الذي كان يفشل
        cursor.execute('''
            SELECT id, created_by, expires_at, subscription_type, subscription_duration_days,
                   max_uses, current_uses, is_active, description
            FROM invite_codes 
            WHERE code = ?
        ''', (test_code,))
        
        result = cursor.fetchone()
        
        if result:
            print("✅ تم استرجاع بيانات رمز الدعوة بنجاح:")
            print(f"  - معرف: {result[0]}")
            print(f"  - منشئ بواسطة: {result[1]}")
            print(f"  - تاريخ انتهاء الصلاحية: {result[2]}")
            print(f"  - نوع الاشتراك: {result[3]}")
            print(f"  - مدة الاشتراك (أيام): {result[4]}")
            print(f"  - الحد الأقصى للاستخدام: {result[5]}")
            print(f"  - مرات الاستخدام الحالية: {result[6]}")
            print(f"  - نشط: {result[7]}")
            print(f"  - الوصف: {result[8]}")
        else:
            print("❌ فشل في استرجاع بيانات رمز الدعوة")
            return False
        
        # 3. اختبار التحديث
        cursor.execute('''
            UPDATE invite_codes 
            SET current_uses = current_uses + 1 
            WHERE code = ?
        ''', (test_code,))
        
        print("✅ تم تحديث عداد الاستخدام بنجاح")
        
        # 4. حذف رمز الاختبار
        cursor.execute("DELETE FROM invite_codes WHERE code = ?", (test_code,))
        print("🗑️ تم حذف رمز الاختبار")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 جميع الاختبارات نجحت! وظيفة رموز الدعوة تعمل بشكل صحيح.")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {str(e)}")
        return False

def validate_invite_code_test(code: str):
    """اختبار دالة التحقق من رمز الدعوة"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, created_by, expires_at, subscription_type, subscription_duration_days,
                   max_uses, current_uses, is_active, description
            FROM invite_codes 
            WHERE code = ?
        ''', (code,))
        
        invite_data = cursor.fetchone()
        conn.close()
        
        if not invite_data:
            return False, "رمز الدعوة غير صحيح", {}
        
        # التحقق من الحالة النشطة
        if not invite_data[7]:  # is_active
            return False, "رمز الدعوة غير نشط", {}
        
        # التحقق من تاريخ انتهاء الصلاحية
        expires_at = datetime.strptime(invite_data[2], '%Y-%m-%d %H:%M:%S')
        if datetime.now() > expires_at:
            return False, "انتهت صلاحية رمز الدعوة", {}
        
        # التحقق من عدد مرات الاستخدام
        if invite_data[6] >= invite_data[5]:  # current_uses >= max_uses
            return False, "تم استنفاد عدد مرات استخدام رمز الدعوة", {}
        
        # إرجاع بيانات الرمز
        invite_info = {
            'id': invite_data[0],
            'created_by': invite_data[1],
            'expires_at': invite_data[2],
            'subscription_type': invite_data[3],
            'subscription_duration_days': invite_data[4],
            'max_uses': invite_data[5],
            'current_uses': invite_data[6],
            'description': invite_data[8]
        }
        
        return True, "رمز الدعوة صحيح", invite_info
        
    except Exception as e:
        return False, f"خطأ في التحقق من رمز الدعوة: {str(e)}", {}

if __name__ == "__main__":
    print("🚀 بدء اختبار وظيفة رموز الدعوة...")
    print(f"📍 مسار قاعدة البيانات: {DB_NAME}")
    
    if test_invite_code_functionality():
        print("\n🎯 اختبار دالة التحقق من رمز الدعوة...")
        
        # إنشاء رمز تجريبي للاختبار
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        test_code = "VALID123"
        expires_at = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("DELETE FROM invite_codes WHERE code = ?", (test_code,))
        cursor.execute('''
            INSERT INTO invite_codes (
                code, created_by, expires_at, subscription_type, 
                subscription_duration_days, max_uses, current_uses, 
                is_active, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (test_code, 1, expires_at, 'premium', 30, 1, 0, True, 'اختبار'))
        
        conn.commit()
        conn.close()
        
        # اختبار دالة التحقق
        is_valid, message, info = validate_invite_code_test(test_code)
        
        if is_valid:
            print(f"✅ دالة التحقق تعمل: {message}")
            print(f"  - مدة الاشتراك: {info['subscription_duration_days']} يوماً")
        else:
            print(f"❌ دالة التحقق فشلت: {message}")
        
        # تنظيف
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM invite_codes WHERE code = ?", (test_code,))
        conn.commit()
        conn.close()
        
        print("\n✨ تم الانتهاء من جميع الاختبارات!")
    else:
        print("\n❌ فشل في الاختبارات الأساسية.")
        sys.exit(1)