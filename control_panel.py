# نظام إدارة التوصيات المالية
# ملف التحكم الرئيسي - control_panel.py

import os
import sys
import subprocess
import webbrowser
from datetime import datetime

class TradingSystemController:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.app_file = os.path.join(self.base_dir, "app.py")
        self.db_file = os.path.join(self.base_dir, "trading_recommendations.db")
        
    def check_requirements(self):
        """فحص المتطلبات الأساسية"""
        print("🔍 فحص المتطلبات...")
        
        # فحص Python
        try:
            python_version = sys.version
            print(f"✅ Python: {python_version}")
        except:
            print("❌ Python غير متوفر")
            return False
        
        # فحص الملفات الأساسية
        if not os.path.exists(self.app_file):
            print("❌ ملف app.py غير موجود")
            return False
        print("✅ ملف التطبيق موجود")
        
        # فحص المكتبات
        try:
            import streamlit
            print(f"✅ Streamlit: {streamlit.__version__}")
        except ImportError:
            print("❌ Streamlit غير مثبت")
            return False
            
        try:
            import pandas
            print(f"✅ Pandas: {pandas.__version__}")
        except ImportError:
            print("❌ Pandas غير مثبت")
            return False
        
        return True
    
    def install_requirements(self):
        """تثبيت المتطلبات"""
        print("📦 تثبيت المكتبات...")
        
        packages = ["streamlit", "pandas"]
        for package in packages:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ])
                print(f"✅ تم تثبيت {package}")
            except subprocess.CalledProcessError:
                print(f"❌ فشل في تثبيت {package}")
                return False
        
        return True
    
    def start_app(self):
        """تشغيل التطبيق"""
        print("🚀 تشغيل التطبيق...")
        
        try:
            # تشغيل Streamlit
            subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", self.app_file
            ])
            
            print("✅ تم تشغيل التطبيق بنجاح!")
            print("🌐 العنوان: http://localhost:8501")
            
            # فتح المتصفح تلقائياً
            webbrowser.open("http://localhost:8501")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تشغيل التطبيق: {e}")
            return False
    
    def backup_database(self):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        if not os.path.exists(self.db_file):
            print("⚠️ قاعدة البيانات غير موجودة بعد")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_database_{timestamp}.db"
        
        try:
            import shutil
            shutil.copy2(self.db_file, backup_file)
            print(f"✅ تم إنشاء نسخة احتياطية: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
            return False
    
    def show_status(self):
        """عرض حالة النظام"""
        print("📊 حالة النظام:")
        print("-" * 40)
        
        # حالة الملفات
        files_status = {
            "app.py": os.path.exists(self.app_file),
            "قاعدة البيانات": os.path.exists(self.db_file),
            "دليل المستخدم": os.path.exists("USER_GUIDE.md"),
            "README": os.path.exists("README.md")
        }
        
        for file_name, exists in files_status.items():
            status = "✅" if exists else "❌"
            print(f"{status} {file_name}")
        
        # حالة المكتبات
        libraries_status = {}
        try:
            import streamlit
            libraries_status["Streamlit"] = streamlit.__version__
        except ImportError:
            libraries_status["Streamlit"] = "غير مثبت"
        
        try:
            import pandas
            libraries_status["Pandas"] = pandas.__version__
        except ImportError:
            libraries_status["Pandas"] = "غير مثبت"
        
        print("\n📚 المكتبات:")
        for lib, version in libraries_status.items():
            print(f"  • {lib}: {version}")
    
    def main_menu(self):
        """القائمة الرئيسية"""
        while True:
            print("\n" + "="*50)
            print("    🏦 نظام إدارة التوصيات المالية")
            print("="*50)
            print("1. 🚀 تشغيل التطبيق")
            print("2. 🔍 فحص النظام")
            print("3. 📦 تثبيت المتطلبات")
            print("4. 💾 نسخة احتياطية من قاعدة البيانات")
            print("5. 📊 عرض حالة النظام")
            print("6. 📖 فتح دليل المستخدم")
            print("7. 🚪 خروج")
            print("="*50)
            
            choice = input("اختر خياراً (1-7): ").strip()
            
            if choice == "1":
                if self.check_requirements():
                    self.start_app()
                    print("\nاضغط Enter للعودة للقائمة الرئيسية...")
                    input()
                else:
                    print("❌ يرجى حل المشاكل أولاً")
                    print("اضغط Enter للمتابعة...")
                    input()
            
            elif choice == "2":
                self.check_requirements()
                print("اضغط Enter للمتابعة...")
                input()
            
            elif choice == "3":
                self.install_requirements()
                print("اضغط Enter للمتابعة...")
                input()
            
            elif choice == "4":
                self.backup_database()
                print("اضغط Enter للمتابعة...")
                input()
            
            elif choice == "5":
                self.show_status()
                print("اضغط Enter للمتابعة...")
                input()
            
            elif choice == "6":
                guide_file = "USER_GUIDE.md"
                if os.path.exists(guide_file):
                    os.startfile(guide_file)
                    print("✅ تم فتح دليل المستخدم")
                else:
                    print("❌ دليل المستخدم غير موجود")
                print("اضغط Enter للمتابعة...")
                input()
            
            elif choice == "7":
                print("👋 شكراً لاستخدام النظام!")
                break
            
            else:
                print("❌ خيار غير صحيح، يرجى المحاولة مرة أخرى")
                print("اضغط Enter للمتابعة...")
                input()

if __name__ == "__main__":
    controller = TradingSystemController()
    controller.main_menu()