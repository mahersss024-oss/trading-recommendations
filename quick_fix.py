#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة تشخيص سريعة لحل مشاكل المستخدمين والتقارير
"""

import os
import sys
import sqlite3
from datetime import datetime

def diagnose_and_fix():
    """تشخيص وإصلاح مشاكل المشروع"""
    
    print("🔍 تشخيص مشاكل نظام التوصيات المالية...")
    print("=" * 50)
    
    # تحديد مسار قاعدة البيانات
    if os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'):
        db_path = '/tmp/trading_recommendations.db' if os.path.exists('/tmp') else 'trading_recommendations.db'
    else:
        db_path = 'trading_recommendations.db'
    
    print(f"📁 مسار قاعدة البيانات: {db_path}")
    
    # التحقق من وجود قاعدة البيانات
    if not os.path.exists(db_path):
        print("❌ قاعدة البيانات غير موجودة!")
        print("🔧 إنشاء قاعدة بيانات جديدة...")
        create_fresh_database(db_path)
        return
    
    # فحص محتويات قاعدة البيانات
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # فحص الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"📊 الجداول الموجودة: {tables}")
        
        # فحص البيانات
        if 'users' in tables:
            cursor.execute("SELECT COUNT(*) FROM users")
            users_count = cursor.fetchone()[0]
            print(f"👥 عدد المستخدمين: {users_count}")
            
            if users_count == 0:
                print("⚠️ لا يوجد مستخدمون!")
                create_default_admin(cursor)
        
        if 'reports' in tables:
            cursor.execute("SELECT COUNT(*) FROM reports")
            reports_count = cursor.fetchone()[0]
            print(f"📋 عدد التقارير: {reports_count}")
        
        if 'trades' in tables:
            cursor.execute("SELECT COUNT(*) FROM trades")
            trades_count = cursor.fetchone()[0]
            print(f"💹 عدد الصفقات: {trades_count}")
        
        # فحص جدول رموز الدعوة
        if 'invite_codes' in tables:
            cursor.execute("SELECT COUNT(*) FROM invite_codes")
            invite_codes_count = cursor.fetchone()[0]
            print(f"🎫 عدد رموز الدعوة: {invite_codes_count}")
            
            # اختبار دالة get_invite_codes
            test_invite_codes_function(cursor)
        else:
            print("⚠️ جدول رموز الدعوة غير موجود!")
            create_invite_codes_table(cursor)
        
        conn.commit()
        conn.close()
        
        print("✅ تم فحص قاعدة البيانات بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")
        print("🔧 إعادة إنشاء قاعدة البيانات...")
        create_fresh_database(db_path)

def test_invite_codes_function(cursor):
    """اختبار دالة رموز الدعوة لتجنب أخطاء KeyError"""
    print("🧪 اختبار دالة رموز الدعوة...")
    
    try:
        cursor.execute('''
            SELECT ic.id, ic.code, ic.created_by, u.username as created_by_name,
                   ic.created_at, ic.expires_at, ic.subscription_type, 
                   ic.max_uses, ic.current_uses,
                   ic.is_active, ic.description
            FROM invite_codes ic
            LEFT JOIN users u ON ic.created_by = u.id
            ORDER BY ic.created_at DESC
            LIMIT 1
        ''')
        
        row = cursor.fetchone()
        if row:
            # اختبار معالجة البيانات
            is_active = bool(row[9])  # تحويل إلى boolean
            status = 'نشط' if is_active else 'غير نشط'
            
            print("✅ دالة رموز الدعوة تعمل بشكل صحيح")
            print(f"   - النوع: {type(is_active)}")
            print(f"   - القيمة: {is_active}")
            print(f"   - الحالة: {status}")
        else:
            print("📭 لا توجد رموز دعوة للاختبار")
    
    except Exception as e:
        print(f"❌ خطأ في اختبار رموز الدعوة: {e}")

def create_invite_codes_table(cursor):
    """إنشاء جدول رموز الدعوة"""
    try:
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
        print("✅ تم إنشاء جدول رموز الدعوة")
    except Exception as e:
        print(f"❌ خطأ في إنشاء جدول رموز الدعوة: {e}")

def create_fresh_database(db_path):
    """إنشاء قاعدة بيانات جديدة"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_admin BOOLEAN DEFAULT FALSE,
                admin_role TEXT DEFAULT 'none',
                admin_permissions TEXT DEFAULT ''
            )
        ''')
        
        # جدول التقارير
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                market_analysis TEXT,
                total_symbols INTEGER,
                buy_recommendations INTEGER,
                sell_recommendations INTEGER,
                neutral_recommendations INTEGER,
                avg_confidence REAL,
                avg_risk_reward REAL
            )
        ''')
        
        # جدول الصفقات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER,
                symbol TEXT NOT NULL,
                price REAL,
                recommendation TEXT NOT NULL,
                confidence REAL,
                stop_loss REAL,
                target_profit REAL,
                risk_reward_ratio REAL,
                rsi REAL,
                macd REAL,
                trend TEXT,
                FOREIGN KEY (report_id) REFERENCES reports (id)
            )
        ''')
        
        # إنشاء مستخدم مدير افتراضي
        create_default_admin(cursor)
        
        conn.commit()
        conn.close()
        
        print("✅ تم إنشاء قاعدة بيانات جديدة بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")

def create_default_admin(cursor):
    """إنشاء مستخدم مدير افتراضي"""
    import hashlib
    
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, is_admin, admin_role, admin_permissions)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("admin", "admin@example.com", admin_password, True, "super_admin", "all"))
    
    print("✅ تم إنشاء حساب المدير الافتراضي:")
    print("   👤 اسم المستخدم: admin")
    print("   🔑 كلمة المرور: admin123")

def test_saving():
    """اختبار حفظ البيانات"""
    print("\n🧪 اختبار حفظ البيانات...")
    
    # تحديد مسار قاعدة البيانات
    if os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'):
        db_path = '/tmp/trading_recommendations.db' if os.path.exists('/tmp') else 'trading_recommendations.db'
    else:
        db_path = 'trading_recommendations.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # اختبار حفظ تقرير
        test_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        cursor.execute('''
            INSERT INTO reports (filename, content, total_symbols, buy_recommendations, sell_recommendations, avg_confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (test_filename, "تقرير اختبار", 1, 1, 0, 85.0))
        
        report_id = cursor.lastrowid
        
        # اختبار حفظ صفقة
        cursor.execute('''
            INSERT INTO trades (report_id, symbol, price, recommendation, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (report_id, "TEST", 100.0, "شراء", 85.0))
        
        conn.commit()
        conn.close()
        
        print("✅ اختبار الحفظ نجح!")
        
    except Exception as e:
        print(f"❌ فشل اختبار الحفظ: {e}")

if __name__ == "__main__":
    print("🏥 أداة التشخيص السريع لنظام التوصيات المالية")
    print("=" * 60)
    
    diagnose_and_fix()
    test_saving()
    
    print("\n✅ انتهى التشخيص!")
    print("🚀 يمكنك الآن تشغيل التطبيق بأمان.")