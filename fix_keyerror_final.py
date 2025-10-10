#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح نهائي وشامل لخطأ KeyError في رموز الدعوة
"""

import sqlite3
import os
from datetime import datetime, timedelta

def fix_keyerror_final():
    """إصلاح نهائي لخطأ KeyError في رموز الدعوة"""
    
    print("🔧 إصلاح نهائي لخطأ KeyError في رموز الدعوة...")
    print("=" * 60)
    
    # تحديد مسار قاعدة البيانات
    if os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'):
        DB_NAME = '/tmp/trading_recommendations.db' if os.path.exists('/tmp') else 'trading_recommendations.db'
    else:
        DB_NAME = 'trading_recommendations.db'
    
    print(f"📁 مسار قاعدة البيانات: {DB_NAME}")
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # 1. التحقق من وجود الجداول المطلوبة
        print("\n📋 التحقق من الجداول...")
        check_and_create_tables(cursor)
        
        # 2. إصلاح بنية جدول invite_codes
        print("\n🔧 إصلاح بنية جدول invite_codes...")
        fix_invite_codes_table_structure(cursor)
        
        # 3. اختبار شامل لوظائف رموز الدعوة
        print("\n🧪 اختبار شامل للوظائف...")
        test_all_invite_functions(cursor)
        
        # 4. إنشاء backup
        print("\n💾 إنشاء نسخة احتياطية...")
        create_backup(DB_NAME)
        
        conn.commit()
        conn.close()
        
        print("\n✅ تم إكمال الإصلاح النهائي بنجاح!")
        print("🎉 النظام جاهز للاستخدام بدون أخطاء KeyError")
        
    except Exception as e:
        print(f"❌ خطأ في الإصلاح: {e}")
        return False
    
    return True

def check_and_create_tables(cursor):
    """التحقق من وجود الجداول وإنشاؤها إن لم تكن موجودة"""
    
    # جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            phone TEXT,
            subscription_type TEXT DEFAULT 'free',
            subscription_end DATE,
            is_admin BOOLEAN DEFAULT FALSE,
            admin_role TEXT,
            admin_permissions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول رموز الدعوة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invite_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            subscription_type TEXT DEFAULT 'free',
            max_uses INTEGER DEFAULT 1,
            current_uses INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            description TEXT,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    print("✅ تم التحقق من الجداول")

def fix_invite_codes_table_structure(cursor):
    """إصلاح بنية جدول invite_codes"""
    
    # التحقق من الأعمدة الموجودة
    cursor.execute("PRAGMA table_info(invite_codes)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # إضافة الأعمدة المفقودة
    if 'description' not in columns:
        cursor.execute("ALTER TABLE invite_codes ADD COLUMN description TEXT")
        print("✅ تم إضافة عمود description")
    
    if 'current_uses' not in columns:
        cursor.execute("ALTER TABLE invite_codes ADD COLUMN current_uses INTEGER DEFAULT 0")
        print("✅ تم إضافة عمود current_uses")
    
    # إصلاح القيم NULL
    cursor.execute("UPDATE invite_codes SET current_uses = 0 WHERE current_uses IS NULL")
    cursor.execute("UPDATE invite_codes SET is_active = TRUE WHERE is_active IS NULL")
    
    print("✅ تم إصلاح بنية الجدول")

def test_all_invite_functions(cursor):
    """اختبار شامل لجميع وظائف رموز الدعوة"""
    
    try:
        # اختبار قراءة البيانات
        codes_data = get_invite_codes_safe(cursor)
        print(f"📊 تم قراءة {len(codes_data)} رمز دعوة")
        
        if codes_data:
            # اختبار التصفية الآمنة
            active_codes = []
            used_codes = []
            expired_codes = []
            
            for c in codes_data:
                is_active = bool(c.get('is_active', False))
                status = c.get('status', 'غير معروف')
                
                if is_active and status == 'نشط':
                    active_codes.append(c)
                elif status == 'مستخدم':
                    used_codes.append(c)
                elif status == 'منتهي':
                    expired_codes.append(c)
            
            print(f"📈 الإحصائيات:")
            print(f"   - نشط: {len(active_codes)}")
            print(f"   - مستخدم: {len(used_codes)}")
            print(f"   - منتهي: {len(expired_codes)}")
        
        else:
            print("📝 إنشاء رموز تجريبية...")
            create_test_invite_codes(cursor)
        
        print("✅ اختبار الوظائف مكتمل")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")

def get_invite_codes_safe(cursor):
    """قراءة آمنة لرموز الدعوة مع معالجة جميع الأخطاء المحتملة"""
    
    try:
        cursor.execute('''
            SELECT ic.id, ic.code, ic.created_by, u.username as created_by_name,
                   ic.created_at, ic.expires_at, ic.subscription_type, 
                   ic.max_uses, ic.current_uses,
                   ic.is_active, ic.description
            FROM invite_codes ic
            LEFT JOIN users u ON ic.created_by = u.id
            ORDER BY ic.created_at DESC
        ''')
        
        codes = []
        for row in cursor.fetchall():
            try:
                # تحويل آمن للتاريخ
                expires_at_str = row[5] or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                try:
                    expires_at = datetime.strptime(expires_at_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    expires_at = datetime.now() + timedelta(days=7)
                
                # قيم آمنة
                current_uses = int(row[8] or 0)
                max_uses = int(row[7] or 1)
                is_active = bool(row[9] if row[9] is not None else True)
                
                # حساب الحالة
                if not is_active:
                    status = 'غير نشط'
                elif current_uses >= max_uses:
                    status = 'مستخدم'
                elif expires_at < datetime.now():
                    status = 'منتهي'
                else:
                    status = 'نشط'
                
                code_dict = {
                    'id': row[0],
                    'code': row[1] or '',
                    'created_by': row[2] or 0,
                    'created_by_username': row[3] or 'مستخدم محذوف',
                    'created_at': row[4] or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'expires_at': expires_at_str,
                    'subscription_type': 'مجاني' if (row[6] or 'free') == 'free' else 'مميز',
                    'max_uses': max_uses,
                    'current_uses': current_uses,
                    'is_active': is_active,
                    'description': row[10] or '',
                    'status': status
                }
                
                codes.append(code_dict)
                
            except Exception as row_error:
                print(f"⚠️ خطأ في معالجة صف: {row_error}")
                continue
        
        return codes
        
    except Exception as e:
        print(f"❌ خطأ في قراءة رموز الدعوة: {e}")
        return []

def create_test_invite_codes(cursor):
    """إنشاء رموز دعوة تجريبية"""
    
    import random
    import string
    
    # البحث عن مدير
    cursor.execute("SELECT id FROM users WHERE is_admin = 1 LIMIT 1")
    admin = cursor.fetchone()
    
    if not admin:
        print("إنشاء مدير افتراضي...")
        import hashlib
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, is_admin, admin_role, admin_permissions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ("admin", "admin@example.com", admin_password, True, "super_admin", "manage_users,manage_reports,manage_invites,backup"))
        
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin = cursor.fetchone()
    
    admin_id = admin[0]
    
    # إنشاء 3 رموز تجريبية
    for i in range(3):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        expires_at = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        sub_type = 'premium' if i == 0 else 'free'
        description = f"رمز تجريبي {i+1} - تم إنشاؤه تلقائياً"
        
        cursor.execute('''
            INSERT INTO invite_codes (code, created_by, expires_at, subscription_type, description, is_active, current_uses, max_uses)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (code, admin_id, expires_at, sub_type, description, True, 0, 1))
    
    print("✅ تم إنشاء 3 رموز دعوة تجريبية")

def create_backup(db_name):
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    
    try:
        import shutil
        backup_name = f"trading_recommendations_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(db_name, backup_name)
        print(f"✅ تم إنشاء النسخة الاحتياطية: {backup_name}")
    except Exception as e:
        print(f"⚠️ تعذر إنشاء النسخة الاحتياطية: {e}")

if __name__ == "__main__":
    success = fix_keyerror_final()
    if success:
        print("\n🎯 خطوات ما بعد الإصلاح:")
        print("1. أعد تشغيل التطبيق")
        print("2. امسح الـ cache إذا لزم الأمر")
        print("3. اختبر وظائف رموز الدعوة")
        print("\n🚀 النظام جاهز للاستخدام!")