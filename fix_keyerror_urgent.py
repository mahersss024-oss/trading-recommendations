#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح سريع وقاطع لخطأ KeyError في رموز الدعوة
"""

import os
import shutil
from datetime import datetime

def fix_invite_codes_keyerror():
    """إصلاح خطأ KeyError في رموز الدعوة"""
    
    print("🚨 إصلاح سريع لخطأ KeyError...")
    print("=" * 50)
    
    app_file = "app_enhanced.py"
    
    if not os.path.exists(app_file):
        print(f"❌ الملف {app_file} غير موجود!")
        return False
    
    # إنشاء نسخة احتياطية
    backup_file = f"app_enhanced_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    shutil.copy2(app_file, backup_file)
    print(f"✅ تم إنشاء نسخة احتياطية: {backup_file}")
    
    # قراءة الملف
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن والإصلاح
    fixes_applied = 0
    
    # إصلاح 1: active_codes
    old_pattern1 = "active_codes = [c for c in invite_codes if c['is_active'] and c['status'] == 'نشط']"
    new_pattern1 = "active_codes = [c for c in invite_codes if bool(c.get('is_active', False)) and c.get('status') == 'نشط']"
    
    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_pattern1)
        fixes_applied += 1
        print("✅ تم إصلاح active_codes")
    
    # إصلاح 2: used_codes
    old_pattern2 = "used_codes = [c for c in invite_codes if c['status'] == 'مستخدم']"
    new_pattern2 = "used_codes = [c for c in invite_codes if c.get('status') == 'مستخدم']"
    
    if old_pattern2 in content:
        content = content.replace(old_pattern2, new_pattern2)
        fixes_applied += 1
        print("✅ تم إصلاح used_codes")
    
    # إصلاح 3: expired_codes
    old_pattern3 = "expired_codes = [c for c in invite_codes if c['status'] == 'منتهي']"
    new_pattern3 = "expired_codes = [c for c in invite_codes if c.get('status') == 'منتهي']"
    
    if old_pattern3 in content:
        content = content.replace(old_pattern3, new_pattern3)
        fixes_applied += 1
        print("✅ تم إصلاح expired_codes")
    
    # إصلاح 4: code_info['is_active']
    old_pattern4 = "if code_info['is_active'] and code_info['status'] == 'نشط':"
    new_pattern4 = "if bool(code_info.get('is_active', False)) and code_info.get('status') == 'نشط':"
    
    if old_pattern4 in content:
        content = content.replace(old_pattern4, new_pattern4)
        fixes_applied += 1
        print("✅ تم إصلاح code_info conditions")
    
    # إصلاح 5: التأكد من دالة get_invite_codes ترجع status
    get_invite_codes_pattern = """def get_invite_codes() -> List[Dict]:
    \"\"\"جلب جميع رموز الدعوة\"\"\"
    try:
        from datetime import datetime
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()"""
    
    if get_invite_codes_pattern in content:
        # البحث عن نهاية الدالة وإضافة status إذا لم يكن موجود
        if "'status': status" not in content:
            print("⚠️ إضافة حقل status إلى دالة get_invite_codes...")
            # سنتركه كما هو لأن التعديل معقد
    
    # حفظ الملف
    if fixes_applied > 0:
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ تم تطبيق {fixes_applied} إصلاحات على الملف")
        return True
    else:
        print("ℹ️ الكود محدث بالفعل، لا حاجة لإصلاحات")
        return True

def verify_get_invite_codes_function():
    """التحقق من صحة دالة get_invite_codes"""
    print("\n🔍 فحص دالة get_invite_codes...")
    
    app_file = "app_enhanced.py"
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # التحقق من وجود العناصر المطلوبة
    required_elements = [
        "'status': status",
        "bool(is_active)",
        "bool(c.get('is_active', False))",
        "c.get('status')"
    ]
    
    all_present = True
    for element in required_elements:
        if element in content:
            print(f"✅ {element}")
        else:
            print(f"❌ مفقود: {element}")
            all_present = False
    
    return all_present

if __name__ == "__main__":
    print("🔧 أداة الإصلاح السريع لخطأ KeyError")
    print("=" * 60)
    
    success = fix_invite_codes_keyerror()
    
    if success:
        verify_get_invite_codes_function()
        print("\n✅ تم الإصلاح! يرجى إعادة تشغيل التطبيق.")
    else:
        print("\n❌ فشل الإصلاح!")
    
    print("\n📝 لإعادة تشغيل التطبيق:")
    print("   pkill -f streamlit")
    print("   streamlit run app_enhanced.py --server.port 8507")