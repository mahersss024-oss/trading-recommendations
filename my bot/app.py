import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import datetime
import json
import os
from typing import Dict, List, Optional
import re

# إعداد الصفحة
st.set_page_config(
    page_title="نظام التوصيات المالية",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إنشاء قاعدة البيانات
def init_database():
    conn = sqlite3.connect('trading_recommendations.db')
    cursor = conn.cursor()
    
    # جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            subscription_type TEXT DEFAULT 'free',
            subscription_end DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin BOOLEAN DEFAULT FALSE
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
            recommendation TEXT,
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
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, subscription_type, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', ("admin", "admin@trading.com", admin_password, "premium", True))
    except sqlite3.IntegrityError:
        pass  # المستخدم موجود بالفعل
    
    conn.commit()
    conn.close()

# دالة تشفير كلمة المرور
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# دالة التحقق من تسجيل الدخول
def authenticate_user(username: str, password: str) -> Optional[Dict]:
    conn = sqlite3.connect('trading_recommendations.db')
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute('''
        SELECT id, username, email, subscription_type, subscription_end, is_admin
        FROM users WHERE username = ? AND password_hash = ?
    ''', (username, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1], 
            'email': user[2],
            'subscription_type': user[3],
            'subscription_end': user[4],
            'is_admin': user[5]
        }
    return None

# دالة التسجيل
def register_user(username: str, email: str, password: str) -> bool:
    conn = sqlite3.connect('trading_recommendations.db')
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# دالة التحقق من صحة الاشتراك
def is_subscription_valid(user: Dict) -> bool:
    # المدير دائماً لديه صلاحية الوصول
    if user.get('is_admin'):
        return True
    if user['subscription_type'] == 'free':
        return True
    if user['subscription_end']:
        end_date = datetime.datetime.strptime(user['subscription_end'], '%Y-%m-%d').date()
        return datetime.date.today() <= end_date
    return False

# دالة تحليل ملف التوصيات
def parse_recommendations_file(content: str) -> Dict:
    lines = content.split('\n')
    
    # استخراج تحليل السوق
    market_analysis = ""
    for i, line in enumerate(lines):
        if "حالة السوق" in line or "مؤشر RSI" in line or "قوة الاتجاه" in line:
            market_analysis += line + "\n"
    
    # البحث عن جدول الصفقات
    trades_data = []
    in_table = False
    
    for line in lines:
        if "جدول الصفقات التفصيلي" in line:
            in_table = True
            continue
        
        if in_table and "│" in line and not line.strip().startswith("│  الرمز"):
            # تحليل بيانات الصفقة
            parts = [part.strip() for part in line.split('│') if part.strip()]
            if len(parts) >= 10:
                try:
                    symbol = parts[0]
                    price = float(parts[1].replace(',', ''))
                    recommendation = parts[2].replace('🟢', '').replace('🔴', '').strip()
                    confidence = float(parts[3])
                    stop_loss = float(parts[4].replace(',', ''))
                    target_profit = float(parts[5].replace(',', ''))
                    risk_reward = float(parts[6])
                    rsi = float(parts[7])
                    macd = float(parts[8])
                    trend = parts[9]
                    
                    trades_data.append({
                        'symbol': symbol,
                        'price': price,
                        'recommendation': recommendation,
                        'confidence': confidence,
                        'stop_loss': stop_loss,
                        'target_profit': target_profit,
                        'risk_reward_ratio': risk_reward,
                        'rsi': rsi,
                        'macd': macd,
                        'trend': trend
                    })
                except (ValueError, IndexError):
                    continue
        
        if "تحليل المخاطر والتوزيع" in line:
            in_table = False
    
    # استخراج الإحصائيات
    total_symbols = len(trades_data)
    buy_count = len([t for t in trades_data if 'شراء' in t['recommendation']])
    sell_count = len([t for t in trades_data if 'بيع' in t['recommendation']])
    neutral_count = total_symbols - buy_count - sell_count
    
    avg_confidence = sum(t['confidence'] for t in trades_data) / total_symbols if total_symbols > 0 else 0
    avg_risk_reward = sum(t['risk_reward_ratio'] for t in trades_data) / total_symbols if total_symbols > 0 else 0
    
    return {
        'market_analysis': market_analysis,
        'trades': trades_data,
        'stats': {
            'total_symbols': total_symbols,
            'buy_recommendations': buy_count,
            'sell_recommendations': sell_count,
            'neutral_recommendations': neutral_count,
            'avg_confidence': avg_confidence,
            'avg_risk_reward': avg_risk_reward
        }
    }

# دالة حفظ التقرير
def save_report(filename: str, content: str, parsed_data: Dict) -> int:
    conn = sqlite3.connect('trading_recommendations.db')
    cursor = conn.cursor()
    
    # حفظ التقرير
    cursor.execute('''
        INSERT INTO reports (filename, content, market_analysis, total_symbols, 
                           buy_recommendations, sell_recommendations, neutral_recommendations,
                           avg_confidence, avg_risk_reward)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        filename,
        content,
        parsed_data['market_analysis'],
        parsed_data['stats']['total_symbols'],
        parsed_data['stats']['buy_recommendations'],
        parsed_data['stats']['sell_recommendations'],
        parsed_data['stats']['neutral_recommendations'],
        parsed_data['stats']['avg_confidence'],
        parsed_data['stats']['avg_risk_reward']
    ))
    
    report_id = cursor.lastrowid
    
    # حفظ الصفقات
    for trade in parsed_data['trades']:
        cursor.execute('''
            INSERT INTO trades (report_id, symbol, price, recommendation, confidence,
                              stop_loss, target_profit, risk_reward_ratio, rsi, macd, trend)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            report_id,
            trade['symbol'],
            trade['price'],
            trade['recommendation'],
            trade['confidence'],
            trade['stop_loss'],
            trade['target_profit'],
            trade['risk_reward_ratio'],
            trade['rsi'],
            trade['macd'],
            trade['trend']
        ))
    
    conn.commit()
    conn.close()
    return report_id

# دالة جلب التقارير
def get_reports() -> List[Dict]:
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

# دالة جلب تفاصيل التقرير
def get_report_details(report_id: int) -> Dict:
    conn = sqlite3.connect('trading_recommendations.db')
    cursor = conn.cursor()
    
    # جلب بيانات التقرير
    cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
    report = cursor.fetchone()
    
    # جلب الصفقات
    cursor.execute('SELECT * FROM trades WHERE report_id = ?', (report_id,))
    trades = cursor.fetchall()
    
    conn.close()
    
    if report:
        return {
            'report': report,
            'trades': trades
        }
    return None

# صفحة تسجيل الدخول
def login_page():
    st.title("🔐 تسجيل الدخول")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            submitted = st.form_submit_button("تسجيل الدخول")
            
            if submitted:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("اسم المستخدم الجديد")
            new_email = st.text_input("البريد الإلكتروني")
            new_password = st.text_input("كلمة المرور", type="password")
            confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
            submitted = st.form_submit_button("إنشاء حساب")
            
            if submitted:
                if new_password != confirm_password:
                    st.error("كلمة المرور غير متطابقة")
                elif len(new_password) < 6:
                    st.error("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                else:
                    if register_user(new_username, new_email, new_password):
                        st.success("تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول")
                    else:
                        st.error("اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل")

# الصفحة الرئيسية
def main_page():
    user = st.session_state.user
    
    # شريط جانبي
    with st.sidebar:
        st.write(f"مرحباً، {user['username']}")
        st.write(f"نوع الاشتراك: {user['subscription_type']}")
        
        if user['subscription_end']:
            st.write(f"ينتهي الاشتراك: {user['subscription_end']}")
        
        if st.button("تسجيل الخروج"):
            del st.session_state.user
            st.rerun()
    
    st.title("📊 نظام التوصيات المالية")
    
    # التحقق من صحة الاشتراك
    if not is_subscription_valid(user):
        st.error("⚠️ انتهت صلاحية اشتراكك. يرجى تجديد الاشتراك للوصول إلى التوصيات.")
        return
    
    # تبويبات التطبيق
    if user['is_admin']:
        tabs = st.tabs(["📋 التوصيات", "📁 إدارة التقارير", "👥 إدارة المستخدمين"])
    else:
        tabs = st.tabs(["📋 التوصيات"])
    
    # تبويب التوصيات
    with tabs[0]:
        st.header("📈 أحدث التوصيات")
        
        reports = get_reports()
        
        if not reports:
            st.info("لا توجد تقارير متاحة حالياً")
        else:
            # عرض آخر تقرير
            latest_report = reports[0]
            st.subheader(f"📊 {latest_report['filename']}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("إجمالي الرموز", latest_report['total_symbols'])
            with col2:
                st.metric("توصيات الشراء", latest_report['buy_recommendations'])
            with col3:
                st.metric("توصيات البيع", latest_report['sell_recommendations'])
            with col4:
                st.metric("متوسط الثقة", f"{latest_report['avg_confidence']:.1f}%")
            
            # عرض تفاصيل التقرير
            report_details = get_report_details(latest_report['id'])
            if report_details:
                st.subheader("🔍 تحليل السوق")
                st.text(report_details['report'][4])  # market_analysis
                
                st.subheader("📋 جدول الصفقات")
                trades_df = pd.DataFrame([
                    {
                        'الرمز': trade[2],
                        'السعر': trade[3],
                        'التوصية': trade[4],
                        'الثقة %': trade[5],
                        'وقف الخسارة': trade[6],
                        'هدف الربح': trade[7],
                        'نسبة ر/م': trade[8],
                        'RSI': trade[9],
                        'MACD': trade[10],
                        'الاتجاه': trade[11]
                    }
                    for trade in report_details['trades']
                ])
                
                if not trades_df.empty:
                    st.dataframe(trades_df, use_container_width=True)
            
            # عرض التقارير السابقة
            if len(reports) > 1:
                st.subheader("📚 التقارير السابقة")
                for report in reports[1:]:
                    with st.expander(f"{report['filename']} - {report['upload_time']}"):
                        report_details = get_report_details(report['id'])
                        if report_details:
                            trades_df = pd.DataFrame([
                                {
                                    'الرمز': trade[2],
                                    'السعر': trade[3],
                                    'التوصية': trade[4],
                                    'الثقة %': trade[5]
                                }
                                for trade in report_details['trades']
                            ])
                            st.dataframe(trades_df, use_container_width=True)
    
    # تبويب إدارة التقارير (للمدير فقط)
    if user['is_admin'] and len(tabs) > 1:
        with tabs[1]:
            st.header("📁 إدارة التقارير")
            
            # رفع تقرير جديد
            st.subheader("📤 رفع تقرير جديد")
            uploaded_file = st.file_uploader("اختر ملف التقرير", type=['txt'])
            
            if uploaded_file is not None:
                content = uploaded_file.read().decode('utf-8')
                
                if st.button("معاينة التقرير"):
                    parsed_data = parse_recommendations_file(content)
                    
                    st.subheader("📊 إحصائيات التقرير")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("إجمالي الرموز", parsed_data['stats']['total_symbols'])
                    with col2:
                        st.metric("توصيات الشراء", parsed_data['stats']['buy_recommendations'])
                    with col3:
                        st.metric("متوسط الثقة", f"{parsed_data['stats']['avg_confidence']:.1f}%")
                    
                    st.subheader("📋 معاينة الصفقات")
                    if parsed_data['trades']:
                        trades_df = pd.DataFrame(parsed_data['trades'])
                        st.dataframe(trades_df)
                    
                    if st.button("حفظ التقرير"):
                        report_id = save_report(uploaded_file.name, content, parsed_data)
                        st.success(f"تم حفظ التقرير بنجاح! رقم التقرير: {report_id}")
        
        # تبويب إدارة المستخدمين (للمدير فقط)
        with tabs[2]:
            st.header("👥 إدارة المستخدمين")
            
            conn = sqlite3.connect('trading_recommendations.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, subscription_type, subscription_end, created_at
                FROM users WHERE is_admin = FALSE
            ''')
            
            users = cursor.fetchall()
            conn.close()
            
            if users:
                users_df = pd.DataFrame(users, columns=[
                    'المعرف', 'اسم المستخدم', 'البريد الإلكتروني', 
                    'نوع الاشتراك', 'تاريخ انتهاء الاشتراك', 'تاريخ التسجيل'
                ])
                st.dataframe(users_df, use_container_width=True)
            else:
                st.info("لا يوجد مستخدمون مسجلون")

def main():
    # إنشاء قاعدة البيانات
    init_database()
    
    # التحقق من تسجيل الدخول
    if 'user' not in st.session_state:
        login_page()
    else:
        main_page()

if __name__ == "__main__":
    main()