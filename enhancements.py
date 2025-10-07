# ===== تحديثات وميزات إضافية =====

# المكتبات المطلوبة
import streamlit as st
import sqlite3
import re
import datetime

# إضافة هذا الكود في بداية ملف app.py بعد الاستيرادات الأساسية:
# from utils import create_charts, display_user_stats, export_report_to_csv
# from enhancements import enhanced_recommendations_tab, enhanced_admin_tab

# دالة مساعدة لجلب التقارير
def get_reports():
    """جلب التقارير من قاعدة البيانات"""
    conn = sqlite3.connect('trading_recommendations.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, filename, upload_time, total_symbols, buy_recommendations,
               sell_recommendations, avg_confidence
        FROM reports ORDER BY upload_time DESC
    ''')
    
    reports = []
    for row in cursor.fetchall():
        reports.append({
            'id': row[0],
            'filename': row[1],
            'upload_time': row[2],
            'total_symbols': row[3],
            'buy_recommendations': row[4],
            'sell_recommendations': row[5],
            'avg_confidence': row[6]
        })
    
    conn.close()
    return reports

# دالة حذف التقرير
def delete_report(report_id: int) -> bool:
    """
    حذف تقرير ومعلوماته من قاعدة البيانات
    
    Args:
        report_id (int): معرف التقرير المراد حذفه
    
    Returns:
        bool: True إذا تم الحذف بنجاح، False في حالة حدوث خطأ
    """
    try:
        conn = sqlite3.connect('trading_recommendations.db')
        cursor = conn.cursor()
        
        # حذف الصفقات المرتبطة بالتقرير أولاً (بسبب قيود الـ foreign key)
        cursor.execute('DELETE FROM trades WHERE report_id = ?', (report_id,))
        
        # حذف التقرير نفسه
        cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))
        
        # التحقق من عدد الصفوف المتأثرة
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    except Exception as e:
        print(f"خطأ في حذف التقرير: {str(e)}")
        if 'conn' in locals() and conn:
            conn.close()
        return False
        
# دالة حذف جميع التقارير
def delete_all_reports() -> bool:
    """
    حذف جميع التقارير وبياناتها من قاعدة البيانات
    
    Returns:
        bool: True إذا تم الحذف بنجاح، False في حالة حدوث خطأ
    """
    try:
        conn = sqlite3.connect('trading_recommendations.db')
        cursor = conn.cursor()
        
        # حذف جميع الصفقات أولاً
        cursor.execute('DELETE FROM trades')
        
        # ثم حذف جميع التقارير
        cursor.execute('DELETE FROM reports')
        
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"خطأ في حذف جميع التقارير: {str(e)}")
        if 'conn' in locals() and conn:
            conn.close()
        return False

# إضافة هذا الكود في دالة main_page() في تبويب التوصيات:

def enhanced_recommendations_tab():
    """تبويب التوصيات المحسن مع الرسوم البيانية"""
    st.header("📈 أحدث التوصيات")
    
    reports = get_reports()
    
    if not reports:
        st.info("لا توجد تقارير متاحة حالياً")
        return
    
    # عرض الرسوم البيانية
    try:
        from utils import create_charts
        fig_confidence, fig_recommendations = create_charts()
        
        if fig_confidence and fig_recommendations:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_confidence, use_container_width=True)
            with col2:
                st.plotly_chart(fig_recommendations, use_container_width=True)
    except ImportError:
        pass  # في حالة عدم توفر plotly
    
    # باقي كود التوصيات...

# إضافة هذا الكود في دالة main_page() في تبويب إدارة المستخدمين:

def enhanced_admin_tab():
    """تبويب إدارة محسن للمدير"""
    st.header("👥 إدارة المستخدمين")
    
    # عرض إحصائيات المستخدمين
    try:
        from utils import display_user_stats
        display_user_stats()
    except ImportError:
        pass
    
    # إضافة خيار تصدير التقارير
    st.subheader("📤 تصدير البيانات")
    
    reports = get_reports()
    if reports:
        selected_report = st.selectbox(
            "اختر تقريراً للتصدير:",
            options=reports,
            format_func=lambda x: f"{x['filename']} - {x['upload_time']}"
        )
        
        if st.button("تصدير إلى CSV"):
            try:
                from utils import export_report_to_csv
                csv_data = export_report_to_csv(selected_report['id'])
                st.download_button(
                    label="تحميل ملف CSV",
                    data=csv_data,
                    file_name=f"report_{selected_report['id']}.csv",
                    mime="text/csv"
                )
            except ImportError:
                st.error("خطأ في تصدير البيانات")

# ===== تحسينات الأمان =====

def track_login_attempts(username):
    """تتبع محاولات تسجيل الدخول"""
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = {}
    
    if 'login_cooldown' not in st.session_state:
        st.session_state.login_cooldown = {}
    
    if username not in st.session_state.login_attempts:
        st.session_state.login_attempts[username] = 0
    
    # التحقق مما إذا كان المستخدم في فترة الحظر المؤقت
    current_time = datetime.datetime.now()
    if username in st.session_state.login_cooldown and st.session_state.login_cooldown[username] > current_time:
        remaining_seconds = int((st.session_state.login_cooldown[username] - current_time).total_seconds())
        remaining_minutes = remaining_seconds // 60 + (1 if remaining_seconds % 60 > 0 else 0)
        st.error(f"تم حظرك مؤقتاً بسبب محاولات تسجيل دخول متعددة. يرجى المحاولة مرة أخرى بعد {remaining_minutes} دقيقة.")
        
        # إضافة خيار لإعادة تعيين الحظر عبر متغير الجلسة بدلاً من الزر
        if 'reset_login_cooldown' in st.session_state and st.session_state.reset_login_cooldown:
            st.session_state.login_attempts[username] = 0
            st.session_state.login_cooldown[username] = current_time
            st.session_state.reset_login_cooldown = False
            st.success("تم إعادة تعيين الحظر، يمكنك المحاولة الآن")
            st.rerun()
        return False
    
    st.session_state.login_attempts[username] += 1
    
    # حظر بعد 5 محاولات لمدة 5 دقائق
    if st.session_state.login_attempts[username] > 5:
        cooldown_time = current_time + datetime.timedelta(minutes=5)
        st.session_state.login_cooldown[username] = cooldown_time
        st.error("تم حظرك مؤقتاً بسبب محاولات تسجيل دخول متعددة. يرجى المحاولة مرة أخرى بعد 5 دقائق.")
        return False
    
    return True

def enhanced_password_validation(password):
    """التحقق من قوة كلمة المرور"""
    if len(password) < 8:
        return False, "كلمة المرور يجب أن تكون 8 أحرف على الأقل"
    
    if not re.search(r"[A-Z]", password):
        return False, "كلمة المرور يجب أن تحتوي على حرف كبير"
    
    if not re.search(r"[a-z]", password):
        return False, "كلمة المرور يجب أن تحتوي على حرف صغير"
    
    if not re.search(r"\d", password):
        return False, "كلمة المرور يجب أن تحتوي على رقم"
    
    return True, "كلمة مرور قوية"

# ===== إعدادات إضافية =====

# CSS مخصص لتحسين المظهر
CUSTOM_CSS = """
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}

.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
}

.recommendation-buy {
    color: #28a745;
    font-weight: bold;
}

.recommendation-sell {
    color: #dc3545;
    font-weight: bold;
}

.sidebar-content {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}

.footer {
    text-align: center;
    color: #6c757d;
    font-size: 0.9rem;
    margin-top: 3rem;
    padding: 1rem;
    border-top: 1px solid #dee2e6;
}
</style>
"""

# JavaScript لتحسين التفاعل
CUSTOM_JS = """
<script>
// إضافة تحديث تلقائي للصفحة كل 5 دقائق
setTimeout(function(){
    window.location.reload(1);
}, 300000);

// إضافة تأثيرات بصرية
document.addEventListener('DOMContentLoaded', function() {
    // تأثير hover للجداول
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        table.style.transition = 'all 0.3s ease';
    });
});
</script>
"""

# ===== إعدادات قاعدة البيانات المحسنة =====

def backup_database():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"trading_recommendations_backup_{timestamp}.db"
    
    try:
        shutil.copy2('trading_recommendations.db', backup_filename)
        return backup_filename
    except Exception:
        return None

def optimize_database():
    """تحسين أداء قاعدة البيانات"""
    conn = sqlite3.connect('trading_recommendations.db')
    cursor = conn.cursor()
    
    # إضافة فهارس لتحسين الأداء
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reports_upload_time ON reports(upload_time)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_trades_report_id ON trades(report_id)')
    
    # تنظيف قاعدة البيانات
    cursor.execute('VACUUM')
    
    conn.commit()
    conn.close()

# ===== إعدادات التطبيق المتقدمة =====

APP_CONFIG = {
    'max_file_size': 10 * 1024 * 1024,  # 10 MB
    'allowed_file_types': ['.txt', '.csv'],
    'session_timeout': 3600,  # ساعة واحدة
    'backup_interval': 24 * 3600,  # 24 ساعة
    'max_reports_per_user': 100,
    'pagination_size': 20
}

# دالة إعداد اللغة
def setup_arabic_support():
    """إعداد دعم اللغة العربية"""
    st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    .stTextInput > div > div > input {
        text-align: right;
    }
    
    .stSelectbox > div > div > select {
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)