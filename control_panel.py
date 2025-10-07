# نظام إدارة التوصيات المالية
# ملف التحكم الرئيسي - control_panel.py

import os
import sys
import subprocess
import webbrowser
from datetime import datetime

class TradingSystemController:
    # ثوابت
    CONTINUE_MESSAGE = "اضغط Enter للمتابعة..."
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # تحديد مسار قاعدة البيانات حسب البيئة (نفس المنطق في app_enhanced.py)
        if os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'):
            self.db_file = '/tmp/trading_recommendations.db' if os.path.exists('/tmp') else 'trading_recommendations.db'
        else:
            self.db_file = os.path.join(self.base_dir, 'trading_recommendations.db')
        
        # ملف التطبيق
        self.app_file = os.path.join(self.base_dir, "app_enhanced.py")  # استخدام النسخة المحسنة
        
        print(f"📁 مسار قاعدة البيانات: {self.db_file}")
        print(f"📁 مسار التطبيق: {self.app_file}")
        print(f"📁 مسار التطبيق: {self.app_file}")
    
    def open_file_cross_platform(self, file_path):
        """فتح ملف بطريقة متوافقة مع جميع أنظمة التشغيل"""
        try:
            if sys.platform.startswith('win'):
                # في ويندوز، استخدم subprocess
                subprocess.run(['cmd', '/c', 'start', '', file_path], check=True, shell=True)
            elif sys.platform.startswith('darwin'):  # macOS
                subprocess.run(['open', file_path], check=True)
            else:  # Linux and other Unix systems
                subprocess.run(['xdg-open', file_path], check=True)
            return True
        except Exception as e:
            print(f"❌ خطأ في فتح الملف: {e}")
            return False
        
    def check_requirements(self):
        """فحص المتطلبات الأساسية"""
        print("🔍 فحص المتطلبات...")
        
        # فحص Python
        try:
            python_version = sys.version
            print(f"✅ Python: {python_version}")
        except Exception as e:
            print(f"❌ Python غير متوفر: {e}")
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
    
    def check_database_integrity(self):
        """فحص سلامة قاعدة البيانات والتقارير والمستخدمين"""
        print("� فحص سلامة قاعدة البيانات...")
        
        if not os.path.exists(self.db_file):
            print("❌ قاعدة البيانات غير موجودة!")
            return False
        
        try:
            import sqlite3
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # فحص الجداول الموجودة
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"📊 الجداول الموجودة: {[table[0] for table in tables]}")
            
            # فحص عدد المستخدمين
            try:
                cursor.execute("SELECT COUNT(*) FROM users")
                users_count = cursor.fetchone()[0]
                print(f"👥 عدد المستخدمين: {users_count}")
            except sqlite3.OperationalError:
                print("❌ جدول المستخدمين غير موجود أو تالف")
            
            # فحص عدد التقارير
            try:
                cursor.execute("SELECT COUNT(*) FROM reports")
                reports_count = cursor.fetchone()[0]
                print(f"📋 عدد التقارير: {reports_count}")
            except sqlite3.OperationalError:
                print("❌ جدول التقارير غير موجود أو تالف")
            
            # فحص عدد الصفقات
            try:
                cursor.execute("SELECT COUNT(*) FROM trades")
                trades_count = cursor.fetchone()[0]
                print(f"💹 عدد الصفقات: {trades_count}")
            except sqlite3.OperationalError:
                print("❌ جدول الصفقات غير موجود أو تالف")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ خطأ في فحص قاعدة البيانات: {e}")
            return False
    
    def fix_database_issues(self):
        """إصلاح مشاكل قاعدة البيانات"""
        print("🔧 إصلاح مشاكل قاعدة البيانات...")
        
        try:
            import sqlite3
            from datetime import datetime
            
            # إنشاء نسخة احتياطية أولاً
            if os.path.exists(self.db_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"db_backup_before_fix_{timestamp}.db"
                import shutil
                shutil.copy2(self.db_file, backup_file)
                print(f"✅ تم إنشاء نسخة احتياطية: {backup_file}")
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # إنشاء الجداول إذا لم تكن موجودة
            print("📋 إنشاء/تحديث جداول قاعدة البيانات...")
            
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
            
            # إنشاء مستخدم مدير افتراضي إذا لم يوجد
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
            admin_count = cursor.fetchone()[0]
            
            if admin_count == 0:
                import hashlib
                admin_password = hashlib.sha256("admin123".encode()).hexdigest()
                cursor.execute('''
                    INSERT OR IGNORE INTO users (username, email, password_hash, is_admin, admin_role, admin_permissions)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ("admin", "admin@example.com", admin_password, True, "super_admin", "all"))
                print("✅ تم إنشاء حساب المدير الافتراضي (admin/admin123)")
            
            conn.commit()
            conn.close()
            
            print("✅ تم إصلاح قاعدة البيانات بنجاح!")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إصلاح قاعدة البيانات: {e}")
            return False
    
    def reset_database(self):
        """إعادة تعيين قاعدة البيانات بالكامل"""
        print("⚠️  إعادة تعيين قاعدة البيانات...")
        
        confirm = input("هل أنت متأكد من إعادة تعيين قاعدة البيانات؟ (نعم/لا): ").strip().lower()
        if confirm not in ['نعم', 'yes', 'y']:
            print("❌ تم إلغاء العملية")
            return False
        
        try:
            # حذف قاعدة البيانات الحالية
            if os.path.exists(self.db_file):
                os.remove(self.db_file)
                print("🗑️ تم حذف قاعدة البيانات القديمة")
            
            # إنشاء قاعدة بيانات جديدة
            if self.fix_database_issues():
                print("✅ تم إنشاء قاعدة بيانات جديدة بنجاح!")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ خطأ في إعادة تعيين قاعدة البيانات: {e}")
            return False
            
    def test_report_saving(self):
        """اختبار حفظ التقارير"""
        print("🧪 اختبار حفظ التقارير...")
        
        try:
            import sqlite3
            from datetime import datetime
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # إنشاء تقرير اختبار
            test_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            test_content = """
تقرير اختبار
حالة السوق: إيجابية
مؤشر RSI: 60
قوة الاتجاه: صاعد

جدول الصفقات التفصيلي:
│ الرمز │ السعر │ التوصية │ الثقة │
│ AAPL │ 150.5 │ شراء │ 85% │
│ GOOGL │ 2500 │ بيع │ 75% │
"""
            
            # حفظ التقرير
            cursor.execute('''
                INSERT INTO reports (filename, content, market_analysis, total_symbols, 
                                   buy_recommendations, sell_recommendations, avg_confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (test_filename, test_content, "تقرير اختبار", 2, 1, 1, 80.0))
            
            report_id = cursor.lastrowid
            
            # حفظ الصفقات
            trades = [
                (report_id, "AAPL", 150.5, "شراء", 85.0, 145.0, 160.0, 2.0, 60.0, 0.5, "صاعد"),
                (report_id, "GOOGL", 2500.0, "بيع", 75.0, 2600.0, 2400.0, 2.0, 40.0, -0.3, "هابط")
            ]
            
            cursor.executemany('''
                INSERT INTO trades (report_id, symbol, price, recommendation, confidence,
                                  stop_loss, target_profit, risk_reward_ratio, rsi, macd, trend)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', trades)
            
            conn.commit()
            
            # التحقق من الحفظ
            cursor.execute("SELECT COUNT(*) FROM reports WHERE id = ?", (report_id,))
            report_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM trades WHERE report_id = ?", (report_id,))
            trades_count = cursor.fetchone()[0]
            
            conn.close()
            
            if report_count > 0 and trades_count > 0:
                print(f"✅ تم حفظ التقرير بنجاح! (ID: {report_id})")
                print(f"📊 الصفقات المحفوظة: {trades_count}")
                return True
            else:
                print("❌ فشل في حفظ التقرير")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في اختبار حفظ التقارير: {e}")
            return False
    
    def test_user_persistence(self):
        """اختبار ثبات بيانات المستخدمين"""
        print("👥 اختبار ثبات بيانات المستخدمين...")
        
        try:
            import sqlite3
            import hashlib
            from datetime import datetime
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # إنشاء مستخدم اختبار
            test_username = f"test_user_{datetime.now().strftime('%H%M%S')}"
            test_email = f"test_{datetime.now().strftime('%H%M%S')}@example.com"
            test_password = hashlib.sha256("test123".encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, subscription_type)
                VALUES (?, ?, ?, ?)
            ''', (test_username, test_email, test_password, "free"))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            # التحقق من الحفظ
            cursor.execute("SELECT COUNT(*) FROM users WHERE id = ?", (user_id,))
            user_count = cursor.fetchone()[0]
            
            conn.close()
            
            if user_count > 0:
                print(f"✅ تم حفظ المستخدم بنجاح! (ID: {user_id})")
                print(f"👤 اسم المستخدم: {test_username}")
                return True
            else:
                print("❌ فشل في حفظ المستخدم")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في اختبار حفظ المستخدمين: {e}")
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
        
        # فحص قاعدة البيانات
        print("\n" + "="*40)
        self.check_database_integrity()
    
    def handle_choice_1(self):
        """تشغيل التطبيق"""
        if self.check_requirements():
            self.start_app()
            print(f"\n{self.CONTINUE_MESSAGE}")
            input()
        else:
            print("❌ يرجى حل المشاكل أولاً")
            print(self.CONTINUE_MESSAGE)
            input()
    
    def handle_choice_2(self):
        """فحص النظام"""
        self.check_requirements()
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_3(self):
        """تثبيت المتطلبات"""
        self.install_requirements()
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_4(self):
        """نسخة احتياطية"""
        self.backup_database()
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_5(self):
        """عرض حالة النظام"""
        self.show_status()
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_6(self):
        """فتح دليل المستخدم"""
        guide_file = "USER_GUIDE.md"
        if os.path.exists(guide_file):
            if self.open_file_cross_platform(guide_file):
                print("✅ تم فتح دليل المستخدم")
            else:
                print("❌ فشل في فتح دليل المستخدم")
        else:
            print("❌ دليل المستخدم غير موجود")
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_7(self):
        """فحص سلامة قاعدة البيانات"""
        self.check_database_integrity()
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_8(self):
        """إصلاح مشاكل قاعدة البيانات"""
        self.fix_database_issues()
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_9(self):
        """إعادة تعيين قاعدة البيانات"""
        self.reset_database()
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_10(self):
        """اختبار حفظ التقارير"""
        self.test_report_saving()
        print(self.CONTINUE_MESSAGE)
        input()
    
    def handle_choice_11(self):
        """اختبار ثبات المستخدمين"""
        self.test_user_persistence()
        print(self.CONTINUE_MESSAGE)
        input()

    def main_menu(self):
        """القائمة الرئيسية"""
        menu_actions = {
            "1": self.handle_choice_1,
            "2": self.handle_choice_2,
            "3": self.handle_choice_3,
            "4": self.handle_choice_4,
            "5": self.handle_choice_5,
            "6": self.handle_choice_6,
            "7": self.handle_choice_7,
            "8": self.handle_choice_8,
            "9": self.handle_choice_9,
            "10": self.handle_choice_10,
            "11": self.handle_choice_11,
        }
        
        while True:
            print("\n" + "="*60)
            print("    🏦 نظام إدارة التوصيات المالية")
            print("="*60)
            print("1. 🚀 تشغيل التطبيق")
            print("2. 🔍 فحص النظام")
            print("3. 📦 تثبيت المتطلبات")
            print("4. 💾 نسخة احتياطية من قاعدة البيانات")
            print("5. 📊 عرض حالة النظام")
            print("6. 📖 فتح دليل المستخدم")
            print("-" * 40)
            print("🔧 أدوات إصلاح قاعدة البيانات:")
            print("7. � فحص سلامة قاعدة البيانات")
            print("8. 🛠️  إصلاح مشاكل قاعدة البيانات")
            print("9. ⚠️  إعادة تعيين قاعدة البيانات")
            print("-" * 40)
            print("10. �🚪 خروج")
            print("="*60)
            
            choice = input("اختر خياراً (1-12): ").strip()
            
            if choice in menu_actions:
                menu_actions[choice]()
            elif choice == "12":
                print("👋 شكراً لاستخدام النظام!")
                break
            else:
                print("❌ خيار غير صحيح، يرجى المحاولة مرة أخرى")
                print(self.CONTINUE_MESSAGE)
                input()

if __name__ == "__main__":
    controller = TradingSystemController()
    controller.main_menu()