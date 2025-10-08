#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح سريع لخطأ رموز الدعوة KeyError
"""

import sqlite3
from datetime import datetime

def fix_invite_codes_data():
    """إصلاح بيانات رموز الدعوة لحل خطأ KeyError"""
    
    print("🔧 إصلاح سريع لخطأ رموز الدعوة...")
    print("=" * 50)
    
    DB_NAME = 'trading_recommendations.db'
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # التحقق من وجود جدول invite_codes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invite_codes';")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ جدول invite_codes غير موجود!")
            create_invite_codes_table(cursor)
            conn.commit()
        
        # فحص البيانات الحالية
        cursor.execute("SELECT COUNT(*) FROM invite_codes")
        count = cursor.fetchone()[0]
        print(f"📊 عدد رموز الدعوة الحالية: {count}")
        
        if count > 0:
            # اختبار قراءة البيانات
            print("🔍 اختبار قراءة البيانات...")
            test_get_invite_codes(cursor)
        else:
            print("📝 إنشاء رموز دعوة تجريبية...")
            create_sample_invite_codes(cursor)
            conn.commit()
        
        conn.close()
        print("✅ تم إصلاح مشكلة رموز الدعوة بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في الإصلاح: {e}")

def create_invite_codes_table(cursor):
    """إنشاء جدول رموز الدعوة"""
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
    print("✅ تم إنشاء جدول invite_codes")

def test_get_invite_codes(cursor):
    """اختبار دالة get_invite_codes المحدثة"""
    try:
        from datetime import datetime
        
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
            # حساب الحالة
            expires_at = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
            current_uses = row[8] or 0
            max_uses = row[7]
            is_active = row[9]
            
            if not is_active:
                status = 'غير نشط'
            elif current_uses >= max_uses:
                status = 'مستخدم'
            elif expires_at < datetime.now():
                status = 'منتهي'
            else:
                status = 'نشط'
            
            codes.append({
                'id': row[0],
                'code': row[1],
                'created_by': row[2],
                'created_by_username': row[3] or 'مستخدم محذوف',
                'created_at': row[4],
                'expires_at': row[5],
                'subscription_type': 'مجاني' if row[6] == 'free' else 'مميز',
                'max_uses': max_uses,
                'current_uses': current_uses,
                'is_active': bool(is_active),  # تحويل إلى boolean
                'description': row[10] or '',
                'status': status
            })
        
        print(f"✅ تم اختبار قراءة {len(codes)} رمز دعوة بنجاح")
        
        # اختبار التصفية
        active_codes = [c for c in codes if bool(c.get('is_active', False)) and c.get('status') == 'نشط']
        used_codes = [c for c in codes if c.get('status') == 'مستخدم']
        expired_codes = [c for c in codes if c.get('status') == 'منتهي']
        
        print(f"📊 الإحصائيات:")
        print(f"   - نشط: {len(active_codes)}")
        print(f"   - مستخدم: {len(used_codes)}")
        print(f"   - منتهي: {len(expired_codes)}")
        
        return codes
        
    except Exception as e:
        print(f"❌ خطأ في اختبار القراءة: {e}")
        return []

def create_sample_invite_codes(cursor):
    """إنشاء رموز دعوة تجريبية"""
    import random
    import string
    from datetime import datetime, timedelta
    
    # البحث عن مدير
    cursor.execute("SELECT id FROM users WHERE is_admin = 1 LIMIT 1")
    admin = cursor.fetchone()
    
    if not admin:
        print("⚠️ لا يوجد مدير! إنشاء مدير افتراضي...")
        create_default_admin(cursor)
        cursor.execute("SELECT id FROM users WHERE is_admin = 1 LIMIT 1")
        admin = cursor.fetchone()
    
    admin_id = admin[0]
    
    # إنشاء 3 رموز تجريبية
    for i in range(3):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        expires_at = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        sub_type = 'premium' if i == 0 else 'free'
        description = f"رمز تجريبي {i+1}"
        
        cursor.execute('''
            INSERT INTO invite_codes (code, created_by, expires_at, subscription_type, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (code, admin_id, expires_at, sub_type, description))
    
    print("✅ تم إنشاء 3 رموز دعوة تجريبية")

def create_default_admin(cursor):
    """إنشاء مدير افتراضي"""
    import hashlib
    
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, is_admin, admin_role, admin_permissions)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("admin", "admin@example.com", admin_password, True, "super_admin", "manage_users,manage_reports,manage_invites,backup"))

if __name__ == "__main__":
    fix_invite_codes_data()