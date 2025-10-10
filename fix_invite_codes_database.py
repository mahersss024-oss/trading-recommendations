#!/usr/bin/env python3
"""
سكريبت لإصلاح قاعدة البيانات وإضافة العمود المفقود subscription_duration_days
"""

import sqlite3
import os
import sys

# تحديد مسار قاعدة البيانات
if os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'):
    DB_NAME = '/tmp/trading_recommendations.db' if os.path.exists('/tmp') else 'trading_recommendations.db'
else:
    DB_NAME = 'trading_recommendations.db'

def fix_invite_codes_table():
    """إصلاح جدول رموز الدعوة بإضافة العمود المفقود"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        print("🔍 فحص جدول invite_codes...")
        
        # التحقق من وجود الجدول
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='invite_codes'
        """)
        
        if not cursor.fetchone():
            print("⚠️ جدول invite_codes غير موجود، سيتم إنشاؤه...")
            # إنشاء الجدول بالكامل
            cursor.execute('''
                CREATE TABLE invite_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    created_by INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    used_by INTEGER DEFAULT NULL,
                    used_at TIMESTAMP DEFAULT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    subscription_type TEXT DEFAULT 'free',
                    subscription_duration_days INTEGER DEFAULT 30,
                    max_uses INTEGER DEFAULT 1,
                    current_uses INTEGER DEFAULT 0,
                    description TEXT DEFAULT '',
                    FOREIGN KEY (created_by) REFERENCES users (id),
                    FOREIGN KEY (used_by) REFERENCES users (id)
                )
            ''')
            print("✅ تم إنشاء جدول invite_codes بنجاح")
        else:
            # التحقق من وجود العمود subscription_duration_days
            cursor.execute("PRAGMA table_info(invite_codes)")
            columns = [column[1] for column in cursor.fetchall()]
            print(f"الأعمدة الموجودة: {columns}")
            
            if 'subscription_duration_days' not in columns:
                print("⚠️ العمود subscription_duration_days غير موجود، سيتم إضافته...")
                cursor.execute("""
                    ALTER TABLE invite_codes 
                    ADD COLUMN subscription_duration_days INTEGER DEFAULT 30
                """)
                print("✅ تم إضافة العمود subscription_duration_days بنجاح")
            else:
                print("✅ العمود subscription_duration_days موجود بالفعل")
            
            # التحقق من الأعمدة الأخرى وإضافتها إذا لزم الأمر
            missing_columns = {
                'max_uses': 'INTEGER DEFAULT 1',
                'current_uses': 'INTEGER DEFAULT 0',
                'description': 'TEXT DEFAULT ""',
                'is_active': 'BOOLEAN DEFAULT TRUE'
            }
            
            for col_name, col_def in missing_columns.items():
                if col_name not in columns:
                    print(f"⚠️ العمود {col_name} غير موجود، سيتم إضافته...")
                    cursor.execute(f"ALTER TABLE invite_codes ADD COLUMN {col_name} {col_def}")
                    print(f"✅ تم إضافة العمود {col_name} بنجاح")
        
        # حفظ التغييرات
        conn.commit()
        print("\n✅ تم إصلاح قاعدة البيانات بنجاح!")
        
        # عرض بنية الجدول النهائية
        cursor.execute("PRAGMA table_info(invite_codes)")
        columns_info = cursor.fetchall()
        print("\n📋 بنية جدول invite_codes النهائية:")
        for col in columns_info:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح قاعدة البيانات: {str(e)}")
        return False

def verify_database():
    """التحقق من سلامة قاعدة البيانات"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # اختبار الاستعلام الذي كان يفشل
        cursor.execute("""
            SELECT id, created_by, expires_at, subscription_type, subscription_duration_days,
                   max_uses, current_uses, is_active, description
            FROM invite_codes 
            LIMIT 1
        """)
        
        print("✅ اختبار الاستعلام نجح!")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ فشل اختبار الاستعلام: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 بدء إصلاح قاعدة البيانات...")
    print(f"📍 مسار قاعدة البيانات: {DB_NAME}")
    
    if fix_invite_codes_table():
        print("\n🧪 اختبار قاعدة البيانات...")
        if verify_database():
            print("\n🎉 تم إصلاح المشكلة بنجاح!")
            print("يمكنك الآن تشغيل التطبيق مرة أخرى.")
        else:
            print("\n⚠️ لا تزال هناك مشاكل في قاعدة البيانات.")
            sys.exit(1)
    else:
        print("\n❌ فشل في إصلاح قاعدة البيانات.")
        sys.exit(1)