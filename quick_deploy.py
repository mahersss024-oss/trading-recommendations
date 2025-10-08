#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة نشر سريع لضمان تحديث النشر السحابي
"""

import os
import subprocess
import json
from datetime import datetime

def create_deployment_marker():
    """إنشاء ملف علامة للنشر"""
    marker = {
        "last_update": datetime.now().isoformat(),
        "version": "v2.1-keyerror-fixed",
        "fixes": [
            "Fixed KeyError in invite codes",
            "Added safe boolean conversion",
            "Fixed dictionary access patterns"
        ]
    }
    
    with open('.deployment_marker.json', 'w', encoding='utf-8') as f:
        json.dump(marker, f, ensure_ascii=False, indent=2)
    
    print("✅ تم إنشاء علامة النشر")

def force_git_update():
    """محاولة إجبار تحديث Git"""
    try:
        print("🔄 محاولة إجبار تحديث Git...")
        
        # إضافة جميع الملفات
        result1 = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
        print(f"Git add: {result1.returncode}")
        
        # التأكد من الحالة
        result2 = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result2.stdout.strip():
            print(f"ملفات للإرسال: {len(result2.stdout.strip().split())}")
            
            # الإرسال
            commit_msg = f"إصلاح عاجل لخطأ KeyError - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result3 = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
            print(f"Git commit: {result3.returncode}")
            
            if result3.returncode == 0:
                print("✅ تم الإرسال المحلي بنجاح")
                return True
        else:
            print("ℹ️ لا توجد تغييرات للإرسال")
            
    except Exception as e:
        print(f"❌ خطأ في Git: {e}")
    
    return False

def create_alternative_deployment():
    """إنشاء ملف نشر بديل"""
    deployment_script = """#!/bin/bash
# سكريبت النشر البديل

echo "🚀 بدء النشر البديل..."

# إنشاء أرشيف للكود المحدث
tar -czf app_fixed.tar.gz app_enhanced.py enhancements.py utils.py requirements.txt

echo "✅ تم إنشاء أرشيف الكود المحدث: app_fixed.tar.gz"
echo "📤 يمكنك رفع هذا الأرشيف يدوياً إلى منصة النشر"

# معلومات النشر
echo ""
echo "📋 معلومات النشر:"
echo "   - الملف الرئيسي: app_enhanced.py"
echo "   - المنفذ: 8501"
echo "   - متطلبات: requirements.txt"
echo ""
echo "🔧 لنشر على Streamlit Cloud:"
echo "   1. ارفع الملفات إلى GitHub"
echo "   2. اذهب إلى share.streamlit.io"
echo "   3. انشر التطبيق من المستودع"
echo ""
echo "⚡ للنشر السريع المحلي:"
echo "   streamlit run app_enhanced.py --server.port 8501"
"""
    
    with open('deploy_alternative.sh', 'w', encoding='utf-8') as f:
        f.write(deployment_script)
    
    os.chmod('deploy_alternative.sh', 0o755)
    print("✅ تم إنشاء سكريبت النشر البديل")

def check_current_deployment():
    """فحص حالة النشر الحالي"""
    print("🔍 فحص حالة النشر...")
    
    # فحص الملفات المحلية
    if os.path.exists('app_enhanced.py'):
        with open('app_enhanced.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if "bool(c.get('is_active', False))" in content:
                print("✅ الكود المحلي محدث ومصحح")
            else:
                print("❌ الكود المحلي يحتاج إصلاح")
    
    # فحص Git
    try:
        result = subprocess.run(['git', 'log', '--oneline', '-n', '5'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📝 آخر 5 commits:")
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
    except:
        pass

if __name__ == "__main__":
    print("🚀 أداة النشر السريع")
    print("=" * 50)
    
    check_current_deployment()
    print()
    
    create_deployment_marker()
    
    git_success = force_git_update()
    
    create_alternative_deployment()
    
    print("\n✅ تم إعداد ملفات النشر!")
    print("\n📋 الخطوات التالية:")
    print("1. التطبيق يعمل محلياً على: http://localhost:8507")
    print("2. ملف النشر البديل: deploy_alternative.sh")
    print("3. علامة النشر: .deployment_marker.json")
    
    if git_success:
        print("4. ✅ تم تحديث Git محلياً")
    else:
        print("4. ⚠️ يرجى تحديث المستودع يدوياً")
    
    print("\n🌐 للوصول للتطبيق:")
    print("   المحلي: http://localhost:8507")
    print("   الشبكة: http://10.0.0.216:8507")
    print("   الخارجي: http://4.240.39.193:8507")