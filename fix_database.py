#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح قاعدة البيانات - إضافة الأعمدة المفقودة
"""

import sqlite3
import os

def fix_database_schema():
    """إصلاح مخطط قاعدة البيانات"""
    
    DB_NAME = 'trading_recommendations.db'
    
    if not os.path.exists(DB_NAME):
        print("❌ قاعدة البيانات غير موجودة!")
        return False
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        print("🔧 إصلاح مخطط قاعدة البيانات...")
        
        # التحقق من الأعمدة الحالية
        cursor.execute("PRAGMA table_info(invite_codes)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        print(f"الأعمدة الحالية: {existing_columns}")
        
        # إضافة الأعمدة المفقودة
        columns_to_add = [
            ("used_by", "TEXT DEFAULT NULL"),
            ("used_at", "DATETIME DEFAULT NULL")
        ]
        
        for col_name, col_def in columns_to_add:
            if col_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE invite_codes ADD COLUMN {col_name} {col_def}")
                    print(f"✅ تمت إضافة العمود: {col_name}")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        print(f"ℹ️ العمود {col_name} موجود بالفعل")
                    else:
                        print(f"❌ خطأ في إضافة العمود {col_name}: {e}")
            else:
                print(f"ℹ️ العمود {col_name} موجود بالفعل")
        
        # التحقق النهائي
        cursor.execute("PRAGMA table_info(invite_codes)")
        final_columns = [col[1] for col in cursor.fetchall()]
        print(f"الأعمدة النهائية: {final_columns}")
        
        # إنشاء رمز دعوة تجريبي إذا لم توجد رموز
        cursor.execute("SELECT COUNT(*) FROM invite_codes")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📝 إنشاء رمز دعوة تجريبي...")
            from datetime import datetime, timedelta
            
            test_code = "TEST123"
            expires_at = (datetime.now() + timedelta(days=30)).isoformat()
            
            cursor.execute("""
                INSERT INTO invite_codes 
                (code, created_by, created_at, expires_at, is_active, used_by, used_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (test_code, "admin", datetime.now().isoformat(), expires_at, True, None, None))
            
            print(f"✅ تم إنشاء رمز دعوة تجريبي: {test_code}")
        
        conn.commit()
        conn.close()
        
        print("✅ تم إصلاح قاعدة البيانات بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح قاعدة البيانات: {e}")
        return False

if __name__ == "__main__":
    print("🛠️ أداة إصلاح قاعدة البيانات")
    print("=" * 40)
    
    success = fix_database_schema()
    
    if success:
        print("\n✅ تم الإصلاح بنجاح!")
        print("🔄 يرجى إعادة تشغيل اختبار النظام")
    else:
        print("\n❌ فشل الإصلاح!")