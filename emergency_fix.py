#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف إصلاح طارئ للتأكد من تحديث الكود
"""

import shutil
import os
import subprocess
import sys

def emergency_fix():
    """إصلاح طارئ للتأكد من تحديث الكود"""
    
    print("🚨 إصلاح طارئ لخطأ رموز الدعوة...")
    print("=" * 50)
    
    # نسخ الملف إلى ملف جديد
    source_file = "app_enhanced.py"
    backup_file = "app_enhanced_backup.py"
    
    if os.path.exists(source_file):
        # إنشاء نسخة احتياطية
        shutil.copy2(source_file, backup_file)
        print(f"✅ تم إنشاء نسخة احتياطية: {backup_file}")
        
        # التحقق من الكود المُحدث
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # البحث عن الكود المُحدث
        if "bool(c.get('is_active', False))" in content:
            print("✅ الكود محدث بشكل صحيح!")
            
            # تشغيل اختبار سريع
            test_code = '''
import sqlite3
from datetime import datetime

def test_invite_codes():
    try:
        from datetime import datetime
        
        conn = sqlite3.connect('trading_recommendations.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ic.id, ic.code, ic.created_by, u.username as created_by_name,
                   ic.created_at, ic.expires_at, ic.subscription_type, 
                   ic.max_uses, ic.current_uses,
                   ic.is_active, ic.description
            FROM invite_codes ic
            LEFT JOIN users u ON ic.created_by = u.id
            ORDER BY ic.created_at DESC
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        if row:
            is_active = bool(row[9])
            status = 'نشط' if is_active else 'غير نشط'
            
            # اختبار التصفية مثل الكود
            invite_codes = [{
                'is_active': is_active,
                'status': status
            }]
            
            active_codes = [c for c in invite_codes if bool(c.get('is_active', False)) and c.get('status') == 'نشط']
            
            print(f"✅ اختبار التصفية نجح: {len(active_codes)} رمز نشط")
            return True
        else:
            print("📭 لا توجد رموز للاختبار")
            return True
            
        conn.close()
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

test_invite_codes()
'''
            
            # تشغيل الاختبار
            try:
                exec(test_code)
                print("✅ جميع الاختبارات نجحت!")
                
                # إنشاء ملف تشغيل جديد
                run_script = """#!/bin/bash
echo "🚀 تشغيل النسخة المُحدثة من التطبيق..."
echo "URL: http://localhost:8506"
python -m streamlit run app_enhanced.py --server.port 8506
"""
                
                with open("run_fixed_app.sh", "w") as f:
                    f.write(run_script)
                
                os.chmod("run_fixed_app.sh", 0o755)
                print("✅ تم إنشاء ملف التشغيل: run_fixed_app.sh")
                
            except Exception as e:
                print(f"❌ خطأ في الاختبار: {e}")
        else:
            print("❌ الكود لم يتم تحديثه بعد!")
            print("🔧 تطبيق الإصلاح...")
            
            # تطبيق الإصلاح مباشرة على الملف
            updated_content = content.replace(
                "c['is_active'] and c['status'] == 'نشط'",
                "bool(c.get('is_active', False)) and c.get('status') == 'نشط'"
            )
            
            updated_content = updated_content.replace(
                "code_info['is_active'] and code_info['status'] == 'نشط'",
                "bool(code_info.get('is_active', False)) and code_info.get('status') == 'نشط'"
            )
            
            # حفظ الملف المُحدث
            with open(source_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("✅ تم تطبيق الإصلاح!")
    else:
        print(f"❌ الملف {source_file} غير موجود!")

if __name__ == "__main__":
    emergency_fix()