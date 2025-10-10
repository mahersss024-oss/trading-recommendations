import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import datetime
import os
import random
import string
import json
from typing import Dict, List, Optional, Tuple

# Constants
TYPE_LABEL = 'النوع'

# UI Text Constants
ADMIN_USERS_TAB = "إدارة المستخدمين"
ADMIN_REPORTS_TAB = "إدارة التقارير"
ADMIN_MANAGERS_TAB = "إدارة المشرفين"
ADMIN_BACKUP_TAB = "النسخ الاحتياطي"
USERNAME_LABEL = "اسم المستخدم"
PASSWORD_LABEL = "كلمة المرور"
EMAIL_LABEL = "البريد الإلكتروني"
PHONE_LABEL = "رقم الجوال"
NEW_USERNAME_LABEL = "اسم المستخدم الجديد"

# Table Column Constants
SYMBOL_COL = "الرمز"
PRICE_COL = "السعر"
RECOMMENDATION_COL = "التوصية"
CONFIDENCE_COL = "الثقة %"
STOP_LOSS_COL = "وقف الخسارة"
TARGET_PROFIT_COL = "هدف الربح"
RISK_REWARD_COL = "نسبة ر/م"
TREND_COL = "الاتجاه"

# Recommendation Constants
BUY_RECOMMENDATION = "🟢 شراء"
SELL_RECOMMENDATION = "🔴 بيع"

# Database Constants
COUNT_COL = 'العدد'
SUBSCRIPTION_TYPE_COL = 'نوع الاشتراك'
SUBSCRIPTION_END_COL = 'تاريخ انتهاء الاشتراك'

# Message Constants
FILL_ALL_FIELDS_MSG = "⚠️ يرجى ملء جميع الحقول المطلوبة"
CHOOSE_USER_MSG = "اختر مستخدم..."
NO_USERS_MSG = "📭 لا يوجد مستخدمون مسجلون بعد"
CONFIRM_DELETE_MSG = "اكتب 'تأكيد' للمتابعة:"
CONFIRM_TEXT = "تأكيد"

# SQL Queries Constants
DELETE_USER_SQL = "DELETE FROM users WHERE id = ?"
UPDATE_PASSWORD_SQL = "UPDATE users SET password_hash = ? WHERE id = ?"
CHECK_USERNAME_SQL = "SELECT id FROM users WHERE username = ? AND id != ?"
UPDATE_USERNAME_SQL = "UPDATE users SET username = ? WHERE id = ?"

# Styling Constants
BORDER_STYLE = '1px solid #e5e7eb'

# Contact Information Constants
WHATSAPP_NUMBER = "0549764152"
WHATSAPP_LINK = "https://wa.me/966549764152"
SUPPORT_EMAIL = "maherss024@hotmail.com"

# Invite Code Constants
INVITE_CODE_LENGTH = 8
INVITE_CODE_EXPIRY_DAYS = 7
DEFAULT_SUBSCRIPTION_DURATION_DAYS = 30

# استيراد التحسينات
try:
    from enhancements import track_login_attempts, enhanced_password_validation
    # Import other modules if needed in the future
except ImportError:
    # في حالة عدم توفر الملفات الإضافية
    pass

# إعداد الصفحة
st.set_page_config(
    page_title="نظام التوصيات المالية",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة متغيرات الجلسة
if 'show_admin_form' not in st.session_state:
    st.session_state.show_admin_form = False

# تهيئة متغير الثيم
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'  # افتراضي لايت ثيم

# ثوابت التطبيق
# تحديد مسار قاعدة البيانات حسب البيئة
if os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'):
    # في بيئة الإنتاج، استخدم مسار مؤقت
    DB_NAME = '/tmp/trading_recommendations.db' if os.path.exists('/tmp') else 'trading_recommendations.db'
else:
    # في بيئة التطوير المحلية
    DB_NAME = 'trading_recommendations.db'

def apply_custom_css():
    """تطبيق CSS مخصص حسب الثيم المختار"""
    
    if st.session_state.theme_mode == 'light':
        # Light Theme CSS
        css_content = """
        <style>
        /* تنسيق عام للتطبيق وتحميل خطوط عربية - لايت ثيم */
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700;800;900&display=swap');

        .stApp {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
        }

        /* تحسين تباين النصوص ودعم اللغة العربية - لايت ثيم */
        .stMarkdown, .stText {
            color: #1e293b !important;
            font-size: 1.25rem !important;
            direction: rtl !important;
            text-align: right !important;
            line-height: 1.9 !important;
            font-weight: 600 !important;
            text-rendering: optimizeLegibility !important;
            -webkit-font-smoothing: antialiased !important;
        }

        /* تحسين كافة النصوص في التطبيق */
        body, button, input, textarea, select, label, div {
            font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
            letter-spacing: 0 !important;
        }

        /* تحسين وضوح كل العناصر */
        .stButton button, .stSelectbox, .stTextInput input, .stTextArea textarea {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            direction: rtl !important;
            background-color: #ffffff !important;
            color: #1e293b !important;
            border: 1px solid #e2e8f0 !important;
        }

        /* تنسيق العنوان الرئيسي - لايت ثيم */
        .main-header {
            font-size: 4rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 2.5rem;
            padding: 2rem 0;
            color: #1e40af;
            text-shadow: 0 2px 8px rgba(30, 64, 175, 0.1);
            letter-spacing: 0px;
            direction: rtl;
            line-height: 1.6;
            font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
        }

        /* تنسيق البطاقات - لايت ثيم */
        .metric-card {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            border-color: #3b82f6;
        }

        /* تنسيق الشريط الجانبي - لايت ثيم */
        div[data-testid="stSidebarContent"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.05);
            padding: 1.8rem 1.5rem;
        }

        /* تنسيق الأزرار - لايت ثيم */
        button[kind="primary"] {
            background: linear-gradient(120deg, #3b82f6, #1d4ed8) !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            transition: all 0.2s ease !important;
        }

        button[kind="primary"]:hover {
            background: linear-gradient(120deg, #2563eb, #1e40af) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(59, 130, 246, 0.3) !important;
        }

        /* تنسيق التبويبات - لايت ثيم */
        div[data-testid="stTabsCtrlWrapper"] button[role="tab"] {
            font-weight: 700;
            font-size: 1.25rem;
            border-radius: 8px 8px 0 0;
            padding: 16px 24px !important;
            color: #475569 !important;
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-bottom: none !important;
            transition: all 0.3s ease;
        }

        div[data-testid="stTabsCtrlWrapper"] button[role="tab"]:hover {
            background-color: #f1f5f9 !important;
            color: #3b82f6 !important;
        }

        div[data-testid="stTabsCtrlWrapper"] button[role="tab"][aria-selected="true"] {
            background-color: #ffffff !important;
            color: #1e40af !important;
            border-color: #3b82f6 !important;
            font-weight: 800;
            box-shadow: 0 -2px 8px rgba(59, 130, 246, 0.1);
        }

        /* تنسيق الرسائل - لايت ثيم */
        .success-message {
            background-color: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 8px;
            padding: 1rem;
            color: #166534;
        }

        .error-message {
            background-color: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 8px;
            padding: 1rem;
            color: #dc2626;
        }

        /* تنسيق الجداول - لايت ثيم */
        .stDataFrame {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }

        .stDataFrame table {
            background-color: #ffffff !important;
        }

        .stDataFrame th {
            background-color: #f8fafc !important;
            color: #374151 !important;
            border-bottom: 1px solid #e2e8f0 !important;
        }

        .stDataFrame td {
            color: #1f2937 !important;
            border-bottom: 1px solid #f3f4f6 !important;
        }

        /* تنسيق النماذج - لايت ثيم */
        .stForm {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        }

        /* تحسين الإدخالات - لايت ثيم */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #ffffff !important;
            border: 1px solid #d1d5db !important;
            border-radius: 6px !important;
            color: #374151 !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
        </style>
        """
    else:
        # Dark Theme CSS
        css_content = """
        <style>
        /* تنسيق عام للتطبيق وتحميل خطوط عربية - دارك ثيم */
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700;800;900&display=swap');

        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
        }

        /* تحسين تباين النصوص ودعم اللغة العربية - دارك ثيم */
        .stMarkdown, .stText {
            color: #f1f5f9 !important;
            font-size: 1.25rem !important;
            direction: rtl !important;
            text-align: right !important;
            line-height: 1.9 !important;
            font-weight: 600 !important;
            text-rendering: optimizeLegibility !important;
            -webkit-font-smoothing: antialiased !important;
        }

        /* تحسين كافة النصوص في التطبيق */
        body, button, input, textarea, select, label, div {
            font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
            letter-spacing: 0 !important;
        }

        /* تحسين وضوح كل العناصر */
        .stButton button, .stSelectbox, .stTextInput input, .stTextArea textarea {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            direction: rtl !important;
            background-color: #374151 !important;
            color: #f9fafb !important;
            border: 1px solid #4b5563 !important;
        }

        /* تنسيق العنوان الرئيسي - دارك ثيم */
        .main-header {
            font-size: 4rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 2.5rem;
            padding: 2rem 0;
            color: #60a5fa;
            text-shadow: 0 2px 8px rgba(96, 165, 250, 0.3);
            letter-spacing: 0px;
            direction: rtl;
            line-height: 1.6;
            font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
        }

        /* تنسيق البطاقات - دارك ثيم */
        .metric-card {
            background: #1f2937;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #374151;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            border-color: #60a5fa;
        }

        /* تنسيق الشريط الجانبي - دارك ثيم */
        div[data-testid="stSidebarContent"] {
            background-color: #1f2937;
            border-right: 1px solid #374151;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.2);
            padding: 1.8rem 1.5rem;
        }

        /* تنسيق الأزرار - دارك ثيم */
        button[kind="primary"] {
            background: linear-gradient(120deg, #3b82f6, #1d4ed8) !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            transition: all 0.2s ease !important;
        }

        button[kind="primary"]:hover {
            background: linear-gradient(120deg, #2563eb, #1e40af) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4) !important;
        }

        /* تنسيق التبويبات - دارك ثيم */
        div[data-testid="stTabsCtrlWrapper"] button[role="tab"] {
            font-weight: 700;
            font-size: 1.25rem;
            border-radius: 8px 8px 0 0;
            padding: 16px 24px !important;
            color: #9ca3af !important;
            background-color: #374151 !important;
            border: 1px solid #4b5563 !important;
            border-bottom: none !important;
            transition: all 0.3s ease;
        }

        div[data-testid="stTabsCtrlWrapper"] button[role="tab"]:hover {
            background-color: #4b5563 !important;
            color: #60a5fa !important;
        }

        div[data-testid="stTabsCtrlWrapper"] button[role="tab"][aria-selected="true"] {
            background-color: #1f2937 !important;
            color: #60a5fa !important;
            border-color: #3b82f6 !important;
            font-weight: 800;
            box-shadow: 0 -2px 8px rgba(59, 130, 246, 0.2);
        }

        /* تنسيق الرسائل - دارك ثيم */
        .success-message {
            background-color: #064e3b;
            border: 1px solid #047857;
            border-radius: 8px;
            padding: 1rem;
            color: #10b981;
        }

        .error-message {
            background-color: #7f1d1d;
            border: 1px solid #dc2626;
            border-radius: 8px;
            padding: 1rem;
            color: #ef4444;
        }

        /* تنسيق الجداول - دارك ثيم */
        .stDataFrame {
            background-color: #1f2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 8px !important;
        }

        .stDataFrame table {
            background-color: #1f2937 !important;
        }

        .stDataFrame th {
            background-color: #374151 !important;
            color: #f9fafb !important;
            border-bottom: 1px solid #4b5563 !important;
        }

        .stDataFrame td {
            color: #e5e7eb !important;
            border-bottom: 1px solid #374151 !important;
        }

        /* تنسيق النماذج - دارك ثيم */
        .stForm {
            background-color: #1f2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        }

        /* تحسين الإدخالات - دارك ثيم */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #374151 !important;
            border: 1px solid #4b5563 !important;
            border-radius: 6px !important;
            color: #f9fafb !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        }
        </style>
        """
    
    st.markdown(css_content, unsafe_allow_html=True)

# تطبيق CSS المخصص
apply_custom_css()

def add_theme_switcher():
    """إضافة أداة تبديل الثيم إلى الشريط الجانبي"""
    
    st.markdown("---")
    st.subheader("🎨 إعدادات المظهر")
    
    # زر تبديل الثيم
    current_theme = st.session_state.get('theme_mode', 'light')
    
    theme_options = {
        'light': '☀️ لايت ثيم',
        'dark': '🌙 دارك ثيم'
    }
    
    selected_theme = st.radio(
        "اختر المظهر:",
        options=['light', 'dark'],
        format_func=lambda x: theme_options[x],
        index=0 if current_theme == 'light' else 1,
        key="theme_selector"
    )
    
    # تحديث الثيم إذا تغير
    if selected_theme != current_theme:
        st.session_state.theme_mode = selected_theme
        st.rerun()
    
    # معلومات إضافية
    if current_theme == 'light':
        st.success("🌞 الوضع الحالي: لايت ثيم")
    else:
        st.info("🌙 الوضع الحالي: دارك ثيم")
st.markdown("""
<style>
/* تنسيق عام للتطبيق وتحميل خطوط عربية */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700;800;900&display=swap');

.stApp {
    background: linear-gradient(135deg, #f0f5fa 0%, #e2eaf2 100%);
    font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
}

/* تحسين تباين النصوص ودعم اللغة العربية */
.stMarkdown, .stText {
    color: #0f172a !important;
    font-size: 1.25rem !important;
    direction: rtl !important;
    text-align: right !important;
    line-height: 1.9 !important;
    font-weight: 600 !important;
    text-rendering: optimizeLegibility !important;
    -webkit-font-smoothing: antialiased !important;
}

/* تحسين كافة النصوص في التطبيق */
body, button, input, textarea, select, label, div {
    font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
    letter-spacing: 0 !important;
}

/* تحسين وضوح كل العناصر */
.stButton button, .stSelectbox, .stTextInput input, .stTextArea textarea {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    direction: rtl !important;
}

/* تحسين نصوص القوائم */
ul, ol {
    padding-right: 2rem !important;
    padding-left: 0 !important;
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
}

ul li, ol li {
    margin-bottom: 1rem !important;
    font-size: 1.2rem !important;
    font-weight: 500 !important;
    color: #1e293b !important;
    line-height: 1.7 !important;
}

/* تنسيق العنوان الرئيسي - تحسين كبير للوضوح والتباين */
.main-header {
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 2.5rem;
    padding: 2rem 0;
    color: #0f2350;
    text-shadow: 0 4px 12px rgba(30, 60, 114, 0.15), 0 0 1px rgba(30, 60, 114, 0.2);
    letter-spacing: 2px;
    display: inline-block;
    position: relative;
    z-index: 1;
    letter-spacing: 0px;
    direction: rtl;
    line-height: 1.6;
    font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
}

/* تنسيق البطاقات */
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 0.8rem;
    border: none;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.09);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #2a5298, #1e3c72);
}

/* تنسيق توصيات الشراء والبيع */
.recommendation-buy {
    color: #10b981;
    font-weight: bold;
    background-color: rgba(16, 185, 129, 0.1);
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
}

.recommendation-sell {
    color: #ef4444;
    font-weight: bold;
    background-color: rgba(239, 68, 68, 0.1);
    padding: 0.3rem 0.8rem;
    border-radius: 4px;
}

/* تنسيق الشريط الجانبي */
div[data-testid="stSidebarContent"] {
    background-color: #ffffff;
    border-right: 1px solid #cbd5e1;
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.05);
    padding: 1.8rem 1.5rem;
}

/* تحسين نصوص الشريط الجانبي */
div[data-testid="stSidebarContent"] .stMarkdown {
    font-size: 1.1rem !important;
    color: #0f2336 !important;
    font-weight: 500;
}

div[data-testid="stSidebarContent"] button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
}

div[data-testid="stSidebarContent"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* تنسيق الأزرار */
button[kind="primary"] {
    background: linear-gradient(120deg, #1e3c72, #2a5298) !important;
    border: none !important;
    padding: 0.6rem 1.5rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(30, 60, 114, 0.2) !important;
}

/* تنسيق التبويبات لزيادة الوضوح */
div[data-testid="stTabsCtrlWrapper"] button[role="tab"] {
    font-weight: 800;
    font-size: 1.35rem;
    border-radius: 12px 12px 0 0;
    letter-spacing: 0px;
    padding: 18px 25px !important;
    color: #0f2350 !important;
    margin-right: 5px;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
    border: 2px solid transparent;
    transition: all 0.3s ease;
}

div[data-testid="stTabsCtrlWrapper"] button[role="tab"]:hover {
    background-color: rgba(15, 35, 80, 0.05);
    border-bottom: 2px solid #1e4db7;
}

div[data-testid="stTabsCtrlWrapper"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(180deg, rgba(42, 82, 152, 0.2) 0%, rgba(42, 82, 152, 0) 100%);
    border: 2px solid #1e4db7;
    border-bottom: none;
    font-weight: 900;
    box-shadow: 0 -5px 15px rgba(30, 77, 183, 0.1);
}

div[data-testid="stTabsCtrlWrapper"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(180deg, rgba(42, 82, 152, 0.2) 0%, rgba(42, 82, 152, 0) 100%);
    border-bottom: 2px solid #2a5298;
}

/* تنسيق الرسائل */
.success-message {
    background-color: #ecfdf5;
    border: 1px solid #d1fae5;
    border-radius: 8px;
    padding: 1rem;
    color: #065f46;
    box-shadow: 0 2px 10px rgba(6, 95, 70, 0.1);
}

.error-message {
    background-color: #fef2f2;
    border: 1px solid #fee2e2;
    border-radius: 8px;
    padding: 1rem;
    color: #991b1b;
    box-shadow: 0 2px 10px rgba(153, 27, 27, 0.1);
}

/* تنسيق الجداول */
div[data-testid="stTable"] {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

div[data-testid="stTable"] table {
    border: none;
}

div[data-testid="stTable"] th {
    background: #e2e8f0;
    font-weight: 700;
    font-size: 1.05rem;
    text-align: center;
    padding: 12px 8px;
    color: #1e293b;
}

div[data-testid="stTable"] td {
    text-align: center;
    font-size: 1.02rem;
    padding: 10px 8px;
}

/* تنسيق النماذج */
div[data-testid="stForm"] {
    background-color: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

div[data-testid="stForm"] label {
    font-weight: 500;
    color: #374151;
}

/* تنسيق الفواصل */
hr {
    margin: 1.5rem 0;
    border: none;
    height: 1px;
    background: linear-gradient(90deg, rgba(42, 82, 152, 0) 0%, rgba(42, 82, 152, 0.2) 50%, rgba(42, 82, 152, 0) 100%);
}

/* تنسيق الرسوم البيانية */
div[data-testid="stArrow"] {
    display: none;
}

div[data-testid="element-container"] div[data-testid="stVega"] {
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    background-color: white;
}

/* تأثيرات حركية */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.stApp > div > div {
    animation: fadeIn 0.6s ease-out;
}
</style>
""", unsafe_allow_html=True)

# إنشاء قاعدة البيانات
def init_database():
    conn = sqlite3.connect(DB_NAME)
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
    
    # التحقق من وجود عمود phone وإضافته إذا لم يكن موجوداً
    try:
        cursor.execute("SELECT phone FROM users LIMIT 1")
    except sqlite3.OperationalError:
        # إضافة عمود phone إلى الجدول
        cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
        
    # التحقق من وجود عمود admin_role وإضافته إذا لم يكن موجوداً
    try:
        cursor.execute("SELECT admin_role FROM users LIMIT 1")
    except sqlite3.OperationalError:
        # إضافة عمود admin_role إلى الجدول
        cursor.execute("ALTER TABLE users ADD COLUMN admin_role TEXT DEFAULT 'none'")
        
    # التحقق من وجود عمود admin_permissions وإضافته إذا لم يكن موجوداً
    try:
        cursor.execute("SELECT admin_permissions FROM users LIMIT 1")
    except sqlite3.OperationalError:
        # إضافة عمود admin_permissions إلى الجدول
        cursor.execute("ALTER TABLE users ADD COLUMN admin_permissions TEXT DEFAULT ''")
        conn.commit()
        print("تم إضافة عمود 'phone' إلى جدول المستخدمين")
    
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
    
    # جدول رموز الدعوة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invite_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            used_by INTEGER DEFAULT NULL,
            used_at TIMESTAMP DEFAULT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            subscription_type TEXT DEFAULT 'free',
            subscription_duration_days INTEGER DEFAULT 30,
            max_uses INTEGER DEFAULT 1,
            current_uses INTEGER DEFAULT 0,
            description TEXT DEFAULT '',
            FOREIGN KEY (created_by) REFERENCES users (id),
            FOREIGN KEY (used_by) REFERENCES users (id)
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

# دالة للحصول على أسماء الصلاحيات العربية
def get_permission_name(permission_code):
    """الحصول على الاسم العربي للصلاحية"""
    permissions_map = {
        'users': "إدارة المستخدمين",
        'reports': "إدارة التقارير",
        'admins': "إدارة المشرفين",
        'backup': "النسخ الاحتياطي"
    }
    return permissions_map.get(permission_code, permission_code)

# دالة تشفير كلمة المرور
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# دالة التحقق من تسجيل الدخول المحسنة
def authenticate_user(username: str, password: str) -> Optional[Dict]:
    # فحص محاولات تسجيل الدخول
    try:
        if not track_login_attempts(username):
            return None
    except NameError:
        pass  # الدالة غير متوفرة
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute('''
        SELECT id, username, email, subscription_type, subscription_end, is_admin
        FROM users WHERE username = ? AND password_hash = ?
    ''', (username, password_hash))
    
    user = cursor.fetchone()
    
    result = None
    if user:
        # إعادة تعيين محاولات تسجيل الدخول عند النجاح
        if 'login_attempts' in st.session_state and username in st.session_state.login_attempts:
            st.session_state.login_attempts[username] = 0
        
        # الحصول على معلومات الصلاحيات للمشرفين
        admin_role = 'none'
        admin_permissions = ''
        
        if user[5]:  # إذا كان مديرًا
            admin_cursor = conn.cursor()
            admin_cursor.execute(
                "SELECT admin_role, admin_permissions FROM users WHERE id = ?",
                (user[0],)
            )
            admin_info = admin_cursor.fetchone()
            if admin_info:
                admin_role = admin_info[0] or 'none'
                admin_permissions = admin_info[1] or ''
        
        result = {
            'id': user[0],
            'username': user[1], 
            'email': user[2],
            'subscription_type': user[3],
            'subscription_end': user[4],
            'is_admin': user[5],
            'admin_role': admin_role,
            'admin_permissions': admin_permissions.split(',') if admin_permissions else []
        }
    
    conn.close()  # Cerramos la conexión después de todas las operaciones
    return result
    
# دالة إعادة تعيين كلمة المرور
def reset_password(username: str, email: str) -> Tuple[bool, str]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # التحقق من وجود المستخدم بالاسم والبريد الإلكتروني
    cursor.execute('SELECT id FROM users WHERE username = ? AND email = ?', (username, email))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False, "لا يوجد حساب مسجل بهذه البيانات"
    
    # إنشاء كلمة مرور مؤقتة عشوائية
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    temp_password_hash = hash_password(temp_password)
    
    # تحديث كلمة المرور في قاعدة البيانات
    cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (temp_password_hash, user[0]))
    conn.commit()
    conn.close()
    
    # في بيئة حقيقية، هنا سيتم إرسال بريد إلكتروني بكلمة المرور المؤقتة
    # لكن في هذا المثال سنكتفي بعرض رسالة بكلمة المرور المؤقتة
    
    return True, f"تم إعادة تعيين كلمة المرور بنجاح. كلمة المرور المؤقتة هي: {temp_password}"

# دالة التسجيل المحسنة
def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    # التحقق من قوة كلمة المرور
    try:
        is_valid, message = enhanced_password_validation(password)
        if not is_valid:
            return False, message
    except NameError:
        # التحقق الأساسي إذا لم تكن الدالة المحسنة متوفرة
        if len(password) < 6:
            return False, "كلمة المرور يجب أن تكون 6 أحرف على الأقل"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    # تحقق من وجود عمود phone
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    try:
        if 'phone' in columns:
            # إضافة رقم الجوال إذا كان العمود موجودًا
            phone = None
            if 'register_phone' in st.session_state:
                phone = st.session_state.register_phone
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, phone)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, phone))
        else:
            # إضافة المستخدم بدون رقم الجوال
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
        conn.commit()
        conn.close()
        return True, "تم إنشاء الحساب بنجاح!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل"

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

# ================= دوال إدارة رموز الدعوة =================

# دالة توليد رمز دعوة جديد
def generate_invite_code(created_by: int, subscription_type: str = 'free', 
                         duration_days: int = DEFAULT_SUBSCRIPTION_DURATION_DAYS, 
                         max_uses: int = 1, description: str = '') -> Tuple[bool, str]:
    """إنشاء رمز دعوة جديد"""
    try:
        import random
        import string
        from datetime import datetime, timedelta
        
        # توليد رمز عشوائي
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=INVITE_CODE_LENGTH))
        
        # تاريخ انتهاء الصلاحية
        expires_at = (datetime.now() + timedelta(days=INVITE_CODE_EXPIRY_DAYS)).strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # التأكد من أن الرمز فريد
        while True:
            cursor.execute("SELECT id FROM invite_codes WHERE code = ?", (code,))
            if not cursor.fetchone():
                break
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=INVITE_CODE_LENGTH))
        
        # حفظ الرمز في قاعدة البيانات
        cursor.execute('''
            INSERT INTO invite_codes (code, created_by, expires_at, subscription_type, 
                                     max_uses, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (code, created_by, expires_at, subscription_type, max_uses, description))
        
        conn.commit()
        conn.close()
        
        return True, code
        
    except Exception as e:
        return False, f"خطأ في إنشاء رمز الدعوة: {str(e)}"

# دالة التحقق من صحة رمز الدعوة
def validate_invite_code(code: str) -> Tuple[bool, str, Dict]:
    """التحقق من صحة رمز الدعوة"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, created_by, expires_at, subscription_type, subscription_duration_days,
                   max_uses, current_uses, is_active, description
            FROM invite_codes 
            WHERE code = ?
        ''', (code,))
        
        invite_data = cursor.fetchone()
        conn.close()
        
        if not invite_data:
            return False, "رمز الدعوة غير صحيح", {}
        
        # التحقق من الحالة النشطة
        if not invite_data[7]:  # is_active
            return False, "رمز الدعوة غير نشط", {}
        
        # التحقق من تاريخ انتهاء الصلاحية
        expires_at = datetime.datetime.strptime(invite_data[2], '%Y-%m-%d %H:%M:%S')
        if datetime.datetime.now() > expires_at:
            return False, "انتهت صلاحية رمز الدعوة", {}
        
        # التحقق من عدد مرات الاستخدام
        if invite_data[6] >= invite_data[5]:  # current_uses >= max_uses
            return False, "تم استنفاد عدد مرات استخدام رمز الدعوة", {}
        
        # إرجاع بيانات الرمز
        invite_info = {
            'id': invite_data[0],
            'created_by': invite_data[1],
            'expires_at': invite_data[2],
            'subscription_type': invite_data[3],
            'subscription_duration_days': invite_data[4],
            'max_uses': invite_data[5],
            'current_uses': invite_data[6],
            'description': invite_data[8]
        }
        
        return True, "رمز الدعوة صحيح", invite_info
        
    except Exception as e:
        return False, f"خطأ في التحقق من رمز الدعوة: {str(e)}", {}

# دالة استخدام رمز الدعوة
def use_invite_code(code: str, user_id: int) -> Tuple[bool, str]:
    """استخدام رمز الدعوة عند التسجيل"""
    try:
        # التحقق من صحة الرمز أولاً
        is_valid, message, invite_info = validate_invite_code(code)
        if not is_valid:
            return False, message
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # تحديث معلومات الاستخدام
        cursor.execute('''
            UPDATE invite_codes 
            SET current_uses = current_uses + 1, used_by = ?, used_at = CURRENT_TIMESTAMP
            WHERE code = ?
        ''', (user_id, code))
        
        # تحديث اشتراك المستخدم إذا كان الرمز يتضمن اشتراك مميز
        if invite_info['subscription_type'] != 'free':
            from datetime import datetime, timedelta
            end_date = (datetime.now() + timedelta(days=invite_info['subscription_duration_days'])).strftime('%Y-%m-%d')
            
            cursor.execute('''
                UPDATE users 
                SET subscription_type = ?, subscription_end = ?
                WHERE id = ?
            ''', (invite_info['subscription_type'], end_date, user_id))
        
        conn.commit()
        conn.close()
        
        return True, "تم استخدام رمز الدعوة بنجاح"
        
    except Exception as e:
        return False, f"خطأ في استخدام رمز الدعوة: {str(e)}"

# دالة جلب جميع رموز الدعوة للمدير
def get_invite_codes() -> List[Dict]:
    """جلب جميع رموز الدعوة"""
    try:
        from datetime import datetime
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
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
                'is_active': bool(is_active),
                'description': row[10] or '',
                'status': status
            })
        
        conn.close()
        return codes
        
    except Exception as e:
        st.error(f"خطأ في جلب رموز الدعوة: {str(e)}")
        return []

# دالة إلغاء تفعيل رمز الدعوة
def deactivate_invite_code(code_id: int) -> Tuple[bool, str]:
    """إلغاء تفعيل رمز دعوة"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE invite_codes 
            SET is_active = FALSE 
            WHERE id = ?
        ''', (code_id,))
        
        conn.commit()
        conn.close()
        
        return True, "تم إلغاء تفعيل رمز الدعوة بنجاح"
        
    except Exception as e:
        return False, f"خطأ في إلغاء تفعيل رمز الدعوة: {str(e)}"

# دالة حذف رمز الدعوة
def delete_invite_code(code_id: int) -> bool:
    """حذف رمز دعوة نهائياً"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM invite_codes WHERE id = ?", (code_id,))
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"خطأ في حذف رمز الدعوة: {str(e)}")
        return False

# ================= نهاية دوال رموز الدعوة =================

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
    table_header_found = False
    
    # طباعة للتصحيح - عرض محتويات الملف
    print(f"محتوى الملف الذي تم تحليله: {len(lines)} سطر")
    
    # مسح أولي لتحديد جدول الصفقات
    for line_index, line in enumerate(lines):
        # طباعة كل سطر للتشخيص
        print(f"[فحص] سطر {line_index + 1}: {line}")
        
        # التحقق من بداية جدول الصفقات
        if "جدول الصفقات التفصيلي" in line or "جدول الصفقات المفصل" in line:
            in_table = True
            print(f"تم العثور على بداية جدول الصفقات في السطر {line_index + 1}")
            continue
        
        # البحث عن عناوين الأعمدة
        if in_table and not table_header_found and ("الرمز" in line and "السعر" in line and "التوصية" in line):
            table_header_found = True
            print(f"تم العثور على رؤوس الجدول في السطر {line_index + 1}: {line}")
            continue
        
        # التحقق مما إذا كنا في جدول الصفقات والسطر يحتوي على بيانات
        if in_table and table_header_found:
            # التحقق من نهاية الجدول
            if "تحليل المخاطر" in line or "====" in line or ("مخاطر" in line and "•" in line):
                print(f"تم العثور على نهاية الجدول في السطر {line_index + 1}")
                break
                
            # نتحقق ما إذا كان السطر يحتوي على بيانات صفقة
            if ('│' in line or '|' in line) and len(line.strip()) > 10:
                # تحقق إضافي: يجب أن تكون هناك أرقام في السطر (للسعر أو الثقة)
                has_numbers = any(c.isdigit() for c in line)
                if has_numbers:
                    print(f"سطر صفقة محتمل ({line_index + 1}): {line}")
                    
                    # تحليل سطر الصفقة
                    try:
                        # تحديد الفاصل المستخدم
                        separator = '│' if '│' in line else '|'
                        
                        # تقسيم السطر إلى أجزاء
                        parts = [part.strip() for part in line.split(separator) if part.strip()]
                        print(f"الأجزاء المستخرجة: {parts}")
                        
                        # تحقق من أن هناك أجزاء كافية للتحليل
                        if len(parts) >= 3:
                            symbol = parts[0]
                            
                            # تنظيف وتحويل السعر
                            price_str = parts[1].replace(',', '').replace('$', '')
                            try:
                                price = float(price_str)
                            except ValueError:
                                price = 0
                            
                            # تنظيف واستخراج التوصية
                            recommendation = parts[2]
                            if "🟢" in recommendation:
                                recommendation = "شراء"
                            elif "🔴" in recommendation:
                                recommendation = "بيع"
                            elif "شراء" in recommendation.lower():
                                recommendation = "شراء"
                            elif "بيع" in recommendation.lower():
                                recommendation = "بيع"
                            else:
                                recommendation = recommendation.strip()
                            
                            # استخراج البيانات الأخرى بأمان
                            def safe_extract(parts, index, default=0):
                                if index < len(parts):
                                    try:
                                        value = parts[index].replace(',', '').replace('$', '').replace('%', '')
                                        return float(value)
                                    except ValueError:
                                        return default
                                return default
                            
                            # استخراج باقي البيانات
                            confidence = safe_extract(parts, 3)
                            stop_loss = safe_extract(parts, 4)
                            target_profit = safe_extract(parts, 5)
                            risk_reward = safe_extract(parts, 6)
                            rsi = safe_extract(parts, 7)
                            macd = safe_extract(parts, 8)
                            
                            # استخراج الاتجاه (قد يكون نصًا)
                            trend = parts[9].strip() if len(parts) > 9 else ""
                            
                            # إنشاء كائن الصفقة
                            trade = {
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
                            }
                            
                            # إضافة الصفقة للقائمة
                            trades_data.append(trade)
                            print(f"✅ تمت إضافة صفقة: {symbol} - {recommendation}")
                    
                    except Exception as e:
                        print(f"❌ خطأ في تحليل سطر الصفقة: {e}")
    
    # حساب الإحصائيات بعد المسح الكامل للملف
    total_symbols = len(trades_data)
    
    # استخدام الاسم العربي أو المسار .recommendation حسب الهيكل
    buy_count = 0
    sell_count = 0
    
    for trade in trades_data:
        if 'شراء' in str(trade.get('recommendation', '')).lower():
            buy_count += 1
        elif 'بيع' in str(trade.get('recommendation', '')).lower():
            sell_count += 1
    
    neutral_count = total_symbols - buy_count - sell_count
    
    # حساب المتوسطات
    confidence_sum = 0
    risk_reward_sum = 0
    
    for trade in trades_data:
        confidence_sum += float(trade.get('confidence', 0))
        risk_reward_sum += float(trade.get('risk_reward_ratio', 0))
    
    avg_confidence = confidence_sum / total_symbols if total_symbols > 0 else 0
    avg_risk_reward = risk_reward_sum / total_symbols if total_symbols > 0 else 0
    
    # طباعة ملخص النتائج للتشخيص
    print("===== ملخص التحليل =====")
    print(f"تم تحليل {total_symbols} رمز من الملف")
    print(f"توصيات الشراء: {buy_count}")
    print(f"توصيات البيع: {sell_count}")
    print(f"توصيات محايدة: {neutral_count}")
    print(f"متوسط الثقة: {avg_confidence:.1f}%")
    print(f"متوسط نسبة المخاطرة/المكافأة: {avg_risk_reward:.2f}")
    
    # بناء وإعادة قاموس النتائج
    result = {
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
    
    # طباعة للتشخيص
    print(f"تحليل كامل للتقرير: {total_symbols} رمز, {len(trades_data)} صفقة")
    
    return result

# دالة حفظ التقرير
def save_report(filename: str, content: str, parsed_data: Dict) -> int:
    try:
        # طباعة بنية البيانات المحللة للتشخيص
        print("بيانات التقرير المحللة:", json.dumps(parsed_data, ensure_ascii=False, default=str))
        
        # حساب الإحصائيات من البيانات المحللة
        total_symbols = len(parsed_data['trades'])
        
        # حساب توصيات الشراء والبيع
        buy_count = sum(1 for t in parsed_data['trades'] if 'شراء' in str(t.get('recommendation', '')).lower())
        sell_count = sum(1 for t in parsed_data['trades'] if 'بيع' in str(t.get('recommendation', '')).lower())
        neutral_count = total_symbols - buy_count - sell_count
        
        # حساب متوسط الثقة ونسبة المخاطرة/المكافأة
        confidence_values = [float(t.get('confidence', 0)) for t in parsed_data['trades'] if t.get('confidence') is not None]
        risk_reward_values = [float(t.get('risk_reward_ratio', 0)) for t in parsed_data['trades'] if t.get('risk_reward_ratio') is not None]
        
        avg_confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0
        avg_risk_reward = sum(risk_reward_values) / len(risk_reward_values) if risk_reward_values else 0
        
        # تحديث الإحصائيات المحسوبة
        if 'stats' not in parsed_data:
            parsed_data['stats'] = {}
            
        parsed_data['stats']['total_symbols'] = total_symbols
        parsed_data['stats']['buy_recommendations'] = buy_count
        parsed_data['stats']['sell_recommendations'] = sell_count
        parsed_data['stats']['neutral_recommendations'] = neutral_count
        parsed_data['stats']['avg_confidence'] = avg_confidence
        parsed_data['stats']['avg_risk_reward'] = avg_risk_reward
        
        print(f"إحصائيات محدثة: إجمالي الرموز={total_symbols}, شراء={buy_count}, بيع={sell_count}, متوسط الثقة={avg_confidence:.1f}%")
        
        conn = sqlite3.connect(DB_NAME)
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
            parsed_data.get('market_analysis', ''),
            total_symbols,
            buy_count,
            sell_count,
            neutral_count,
            avg_confidence,
            avg_risk_reward
        ))

        report_id = cursor.lastrowid
        if report_id is None:
            raise Exception("فشل في الحصول على معرف التقرير")
        
        print(f"تم إنشاء التقرير برقم: {report_id}")
        
        # حفظ الصفقات
        success_count = 0
        for trade in parsed_data['trades']:
            try:
                symbol = trade.get('symbol', '')
                price = float(trade.get('price', 0))
                recommendation = trade.get('recommendation', '')
                confidence = float(trade.get('confidence', 0))
                stop_loss = float(trade.get('stop_loss', 0))
                target_profit = float(trade.get('target_profit', 0))
                risk_reward_ratio = float(trade.get('risk_reward_ratio', 0))
                rsi = float(trade.get('rsi', 0))
                macd = float(trade.get('macd', 0))
                trend = trade.get('trend', '')
                
                cursor.execute('''
                    INSERT INTO trades (report_id, symbol, price, recommendation, confidence,
                                      stop_loss, target_profit, risk_reward_ratio, rsi, macd, trend)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    report_id,
                    symbol,
                    price,
                    recommendation,
                    confidence,
                    stop_loss,
                    target_profit,
                    risk_reward_ratio,
                    rsi,
                    macd,
                    trend
                ))
                success_count += 1
            except Exception as trade_error:
                print(f"خطأ في حفظ صفقة {trade.get('symbol', 'غير معروف')}: {str(trade_error)}")
                continue
        
        conn.commit()
        conn.close()
        print(f"تم حفظ {success_count} صفقة من أصل {len(parsed_data['trades'])} صفقة")
        return report_id
    except Exception as e:
        print(f"❌ خطأ في حفظ التقرير: {str(e)}")
        if 'conn' in locals() and conn:
            conn.close()
        raise

# دالة جلب التقارير
def get_reports() -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
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
    try:
        conn = sqlite3.connect(DB_NAME)
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
                'trades': trades if trades else []
            }
        return {}
    except Exception as e:
        print(f"خطأ في get_report_details: {str(e)}")
        # إذا حدث خطأ، نعيد قاموس فارغ ولكن مع بنية صحيحة
        return {'report': None, 'trades': []}

# صفحة تسجيل الدخول المحسنة
def login_page():
        # تحسين العنوان الرئيسي بتنسيق أكثر وضوحاً
        st.markdown("""
        <div style="text-align:center; margin-bottom:40px; padding:20px; position:relative;">
            <div style="position:absolute; top:0; left:0; width:100%; height:100%; background:linear-gradient(120deg, #0f2350 0%, #1e4db7 100%); opacity:0.06; border-radius:15px; z-index:-1;"></div>
            <div style="display:inline-block; background:#0f2350; color:white; padding:10px 20px; border-radius:50px; font-weight:800; font-size:1.6rem; margin-bottom:15px; box-shadow:0 5px 15px rgba(15, 35, 80, 0.2);">🔐 نظام التوصيات المالية</div>
            <!-- إزالة العنوان الثانوي "مرحباً بك في النظام" بناءً على طلب المستخدم -->
            <div style="width:100px; height:5px; background:linear-gradient(90deg, #0f2350, #1e4db7); margin:0 auto; border-radius:50px;"></div>
        </div>
        """, unsafe_allow_html=True)

        # شرح احترافي للمميزات
        st.markdown("""
        <div style='background: linear-gradient(90deg, #f8fafc 60%, #e3eafc 100%); border-radius:16px; padding:30px 28px 25px 28px; margin-bottom:30px; border:2px solid #c7d5f4; box-shadow:0 10px 25px rgba(31,119,180,0.12);'>
            <h3 style='color:#0f2350; margin-bottom:18px; font-size:1.8rem; font-weight:800; text-align:right; direction:rtl;'>نظام التوصيات المالية</h3>
            <ul style='font-size:1.35rem; color:#1e293b; line-height:2.5; padding-right:25px; text-align:right; direction:rtl; font-weight:500;'>
                <li>يعتمد النظام على تحليل أكثر من <strong style='color:#0f2350; background-color:rgba(37, 99, 235, 0.15); padding:5px 15px; border-radius:8px; font-size:1.4rem; font-weight:700; display:inline-block; margin:5px 0;'>25 مؤشر فني</strong> للأسهم والأسواق المالية.</li>
                <li>يقوم بتحليلات متقدمة وجلب أكثر من <strong style='color:#166534; background-color:rgba(16, 185, 129, 0.15); padding:5px 15px; border-radius:8px; font-size:1.4rem; font-weight:700; display:inline-block; margin:5px 0;'>500 خبر يومياً</strong> وتحليلها تلقائياً.</li>
                <li>تحليل مشاعر السوق باستخدام <strong style='color:#581c87; background-color:rgba(139, 92, 246, 0.15); padding:5px 15px; border-radius:8px; font-size:1.4rem; font-weight:700; display:inline-block; margin:5px 0;'>نماذج ذكاء اصطناعي</strong> تعتمد على خوارزميات معقدة لتحليل بيانات الأسهم التاريخية ومؤشراتها الفنية.</li>
                <li>يتم تقديم توصيات دقيقة عبر دمج <strong style='color:#92400e; background-color:rgba(245, 158, 11, 0.15); padding:5px 15px; border-radius:8px; font-size:1.4rem; font-weight:700; display:inline-block; margin:5px 0;'>التحليل الشامل</strong> للسوق والمؤشرات والأخبار.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <style>
            /* تحسين نموذج تسجيل الدخول */
            div[data-testid="stTabs"] > div[data-testid="stTabsHeader"] {
                background-color: white;
                border-radius: 15px 15px 0 0;
                border-top: 2px solid #c7d5f4;
                border-left: 2px solid #c7d5f4;
                border-right: 2px solid #c7d5f4;
                padding: 10px 10px 0 10px;
                box-shadow: 0 -5px 15px rgba(30, 60, 114, 0.05);
            }
            div[data-testid="stTabs"] > div[data-testid="stTabContent"] {
                background-color: white;
                border-radius: 0 0 15px 15px;
                border-bottom: 2px solid #c7d5f4;
                border-left: 2px solid #c7d5f4;
                border-right: 2px solid #c7d5f4;
                padding: 35px 30px;
                box-shadow: 0 10px 25px rgba(30, 60, 114, 0.08);
            }
            
            /* تحسين حقول الإدخال */
            div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
                font-size: 1.2rem !important;
                font-weight: 600 !important;
                direction: rtl !important;
                padding: 15px !important;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05) !important;
            }
            
            /* تحسين وضوح التسميات */
            div[data-baseweb="form-control-label"] {  
                font-size: 1.25rem !important;
                font-weight: 700 !important;
                color: #0f2350 !important;
                margin-bottom: 8px !important;
            }
            
            /* تحسين أزرار تسجيل الدخول */
            div.stButton button {
                font-size: 1.25rem !important;
                font-weight: 700 !important;
                padding: 12px 24px !important;
                background: linear-gradient(120deg, #0f2350, #1e4db7) !important;
                color: white !important;
                border-radius: 8px !important;
                box-shadow: 0 5px 15px rgba(15, 35, 80, 0.2) !important;
                transition: all 0.3s ease !important;
                border: none !important;
            }
            
            div.stButton button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px rgba(15, 35, 80, 0.3) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            tab1, tab2, tab3, tab4 = st.tabs(["🔑 تسجيل الدخول", "📝 إنشاء حساب جديد", "🔄 استعادة كلمة المرور", "📜 السياسة والأحكام"])
        with tab1:
            with st.form("login_form"):
                st.markdown("<h3 style='font-size:1.6rem; text-align:center; color:#0f2350; font-weight:800; margin-bottom:20px; text-shadow: 0 1px 1px rgba(0,0,0,0.1);'>تسجيل الدخول</h3>", unsafe_allow_html=True)
                
                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                
                username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم")
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                
                password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
                
                st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
                
                col_btn1, _ = st.columns([3, 1])
                with col_btn1:
                    submitted = st.form_submit_button("تسجيل الدخول", use_container_width=True)
                if submitted:
                    if username and password:
                        user = authenticate_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.success("✅ تم تسجيل الدخول بنجاح!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                            # تحقق من عدد محاولات تسجيل الدخول
                            if 'login_attempts' in st.session_state and username in st.session_state.login_attempts:
                                attempts_count = st.session_state.login_attempts[username]
                                if attempts_count >= 3:
                                    st.warning("⚠️ لقد تجاوزت الحد المسموح من المحاولات. يرجى المحاولة لاحقًا.")
                            
                            # عرض رابط نسيت كلمة المرور
                            st.markdown("هل نسيت كلمة المرور؟ [اضغط هنا](#)")
                            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ يرجى ملء جميع الحقول")
        with tab2:
            with st.form("register_form"):
                st.subheader("إنشاء حساب جديد")
                # رسالة قانونية بشأن التوصيات
                st.markdown("""
                <div style='background-color:#fff3cd; border:1px solid #ffeeba; border-radius:6px; padding:10px; margin-bottom:10px; color:#856404;'>
                <strong>تنويه قانوني:</strong><br>
                تسجيلك بالموقع يعتبر موافقة على السياسة والأحكام.<br>
                جميع التوصيات المقدمة عبر هذا النظام هي لأغراض تعليمية وتثقيفية فقط، ولا تعتبر نصيحة مالية أو استثمارية مباشرة. يجب على المستخدمين اتخاذ قراراتهم الاستثمارية بناءً على مسؤوليتهم الشخصية وبعد استشارة الجهات المختصة. إدارة النظام غير مسؤولة عن أي خسائر أو أضرار قد تنتج عن استخدام التوصيات.
                </div>
                """, unsafe_allow_html=True)
                new_username = st.text_input("اسم المستخدم الجديد", placeholder="اختر اسم مستخدم")
                new_email = st.text_input("البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
                new_phone = st.text_input("رقم الجوال", placeholder="مثال: 05XXXXXXXX")
                invite_code = st.text_input("رمز الدعوة (من الإدارة)", placeholder="أدخل الرمز المؤقت المرسل لك")
                new_password = st.text_input("كلمة المرور", type="password", placeholder="اختر كلمة مرور قوية")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password", placeholder="أعد إدخال كلمة المرور")
                submitted = st.form_submit_button("إنشاء حساب", use_container_width=True)
                if submitted:
                    if new_username and new_email and new_phone and invite_code and new_password and confirm_password:
                        st.session_state.register_phone = new_phone
                        if new_password != confirm_password:
                            st.error("❌ كلمة المرور غير متطابقة")
                        else:
                            # تحقق من صحة رمز الدعوة
                            is_valid, code_msg, _ = validate_invite_code(invite_code)
                            if not is_valid:
                                st.error(f"❌ رمز الدعوة غير صالح أو منتهي الصلاحية: {code_msg}")
                            else:
                                success, message = register_user(new_username, new_email, new_password)
                                if success:
                                    # الحصول على معرف المستخدم الجديد لاستهلاك الرمز
                                    conn = sqlite3.connect(DB_NAME)
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT id FROM users WHERE username = ?", (new_username,))
                                    user_result = cursor.fetchone()
                                    conn.close()
                                    
                                    if user_result:
                                        user_id = user_result[0]
                                        # عند نجاح التسجيل، يتم استهلاك الرمز
                                        use_invite_code(invite_code, user_id)
                                    
                                    st.success(f"✅ {message}")
                                    st.info("يمكنك الآن تسجيل الدخول باستخدام بياناتك الجديدة")
                                else:
                                    st.error(f"❌ {message}")
                    else:
                        st.warning("⚠️ يرجى ملء جميع الحقول (بما في ذلك رمز الدعوة)")
        with tab3:
            with st.form("reset_password_form"):
                st.markdown("<h3 style='font-size:1.6rem; text-align:center; color:#0f2350; font-weight:800; margin-bottom:20px; text-shadow: 0 1px 1px rgba(0,0,0,0.1);'>استعادة كلمة المرور</h3>", unsafe_allow_html=True)
                
                # شرح عملية استعادة كلمة المرور
                st.markdown("""
                <div style='background-color:#e3f2fd; border:1px solid #90caf9; border-radius:6px; padding:15px; margin-bottom:20px; color:#0d47a1;'>
                <strong>كيفية استعادة كلمة المرور:</strong><br>
                1. أدخل اسم المستخدم والبريد الإلكتروني المسجل في الحساب<br>
                2. سيتم إرسال رابط لإعادة تعيين كلمة المرور إلى بريدك الإلكتروني<br>
                3. في الوقت الحالي، سيتم تعيين كلمة مرور مؤقتة يمكنك استخدامها للدخول ثم تغييرها لاحقاً
                </div>
                """, unsafe_allow_html=True)
                
                reset_username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم", key="reset_username")
                reset_email = st.text_input("البريد الإلكتروني", placeholder="أدخل البريد الإلكتروني المسجل", key="reset_email")
                
                submitted_reset = st.form_submit_button("استعادة كلمة المرور", use_container_width=True)
                if submitted_reset:
                    if reset_username and reset_email:
                        # التحقق من وجود المستخدم والبريد الإلكتروني
                        success, message = reset_password(reset_username, reset_email)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.warning("⚠️ يرجى إدخال اسم المستخدم والبريد الإلكتروني")
                        
        with tab4:
            st.markdown("""
            <div style='background-color:#fdeaea; border-radius:10px; padding:18px 24px; border:1px solid #f5c6cb; margin-bottom:18px; color:#721c24; font-size:1.13rem;'>
                <strong style='font-size:1.15rem;'>📢 تنبيه قانوني:</strong><br>
                تسجيلك في النظام يعتبر موافقة كاملة على جميع الشروط والأحكام.<br>
                جميع التوصيات المقدمة لأغراض تعليمية وتثقيفية فقط وليست نصيحة مالية مباشرة.
            </div>
            """, unsafe_allow_html=True)
            st.subheader("📜 السياسة والأحكام")
            st.markdown("""
            <div style='background-color:#f8f9fa; border-radius:10px; padding:28px; border:1px solid #d1e3ff; margin-top:10px; font-size:1.08rem; color:#222;'>
            <h4 style='color:#1f77b4;'>أولاً: الشروط والأحكام</h4>
            <ol>
                <li><strong>طبيعة الخدمة</strong><br>
                - يقدم الموقع تحليلات وتوصيات تداول للأسواق المالية (مثل الأسهم، المؤشرات وغيرها) بغرض التثقيف والمساعدة في اتخاذ القرار.<br>
                - جميع المعلومات والتوصيات المعروضة لا تُعتبر استشارة استثمارية شخصية أو توصية مباشرة بالشراء أو البيع.<br>
                - المستخدم يتحمل المسؤولية الكاملة عن قراراته الاستثمارية.
                </li>
                <li><strong>عدم ضمان الأرباح</strong><br>
                - التداول في الأسواق المالية ينطوي على مخاطر عالية قد تؤدي إلى خسارة رأس المال كليًا أو جزئيًا.<br>
                - لا يضمن الموقع بأي حال من الأحوال تحقيق أرباح أو تجنب خسائر نتيجة استخدام التوصيات.<br>
                - الأداء السابق لا يُعتبر مؤشرًا أو ضمانًا للنتائج المستقبلية.
                </li>
                <li><strong>حدود المسؤولية</strong><br>
                - لا يتحمل الموقع أو القائمون عليه أي مسؤولية عن أي خسائر أو أضرار مالية قد تنتج عن اعتماد المستخدم على التوصيات أو التحليلات المقدمة.<br>
                - تقع المسؤولية الكاملة على المستخدم في تقييم المخاطر قبل الدخول في أي صفقة.
                </li>
                <li><strong>استخدام المحتوى</strong><br>
                - جميع التوصيات والتحليلات متاحة فقط للاستخدام الشخصي للمستخدمين المسجلين.<br>
                - يُمنع نسخ أو إعادة نشر أو توزيع محتوى الموقع دون إذن مسبق.
                </li>
                <li><strong>الاشتراك والدفع (إن وجد)</strong><br>
                - في حال وجود اشتراكات مدفوعة، يلتزم الموقع بتوفير الخدمة المتفق عليها، مع العلم أن قيمة الاشتراك لا تُمثل بأي شكل ضمانًا للعائد المالي.<br>
                - لن يتم استرجاع المبالغ المدفوعة إلا وفق الشروط المحددة في سياسة الاسترجاع الخاصة بالموقع.
                </li>
                <li><strong>القوانين المعمول بها</strong><br>
                - يخضع استخدام هذا الموقع للقوانين والأنظمة المعمول بها في المملكة العربية السعودية.<br>
                - في حال وجود نزاع قانوني، تكون الجهة القضائية المختصة هي محاكم المملكة العربية السعودية.
                </li>
                <li><strong>موافقة المستخدم</strong><br>
                - بدخولك إلى الموقع أو استخدامك للتوصيات، فإنك تقر بأنك قرأت هذه السياسة وفهمتها وتوافق على الالتزام بها.
                </li>
            </ol>
            <hr>
            <h4 style='color:#1f77b4;'>ثانياً: سياسة الخصوصية</h4>
            <ol>
                <li><strong>جمع المعلومات</strong><br>
                - قد يقوم الموقع بجمع بعض المعلومات مثل: الاسم، البريد الإلكتروني، رقم الهاتف (إن وُجد)، وبيانات الدفع عند الاشتراك.<br>
                - يتم أيضًا جمع بيانات تقنية مثل: عنوان IP، نوع المتصفح، وملفات تعريف الارتباط (Cookies) لتحسين تجربة الاستخدام.
                </li>
                <li><strong>استخدام المعلومات</strong><br>
                - تُستخدم البيانات فقط للأغراض التالية:<br>
                    • توفير خدمات التوصيات والتحليلات.<br>
                    • إدارة حسابات المستخدمين.<br>
                    • تحسين محتوى وتجربة الموقع.<br>
                    • إرسال إشعارات أو تحديثات متعلقة بالخدمة (مع إمكانية إلغاء الاشتراك).
                </li>
                <li><strong>حماية المعلومات</strong><br>
                - يتخذ الموقع إجراءات أمنية مناسبة لحماية بيانات المستخدمين.<br>
                - رغم ذلك، لا يمكن ضمان الحماية المطلقة للبيانات عبر الإنترنت، والمستخدم يقر بالمخاطر المحتملة.
                </li>
                <li><strong>مشاركة المعلومات</strong><br>
                - لا يشارك الموقع بيانات المستخدمين مع أي طرف ثالث لأغراض تسويقية دون إذن مسبق.<br>
                - قد يتم مشاركة بعض المعلومات مع مزودي الخدمات (مثل شركات الدفع) لأداء الخدمة فقط.<br>
                - يمكن الكشف عن البيانات إذا طُلب ذلك بموجب القوانين أو بأمر من الجهات المختصة.
                </li>
                <li><strong>ملفات تعريف الارتباط (Cookies)</strong><br>
                - يستخدم الموقع الكوكيز لتحسين تجربة المستخدم وتحليل الاستخدام.<br>
                - يمكن للمستخدم إيقاف الكوكيز من إعدادات المتصفح، وقد يؤثر ذلك على بعض الخصائص.
                </li>
                <li><strong>حقوق المستخدم</strong><br>
                - يحق للمستخدم الوصول إلى بياناته الشخصية أو تعديلها أو طلب حذفها.<br>
                - يمكن للمستخدم طلب إيقاف تلقي الرسائل الإخبارية أو التسويقية في أي وقت.
                </li>
                <li><strong>التغييرات على السياسة</strong><br>
                - يحتفظ الموقع بحق تحديث أو تعديل سياسة الخصوصية في أي وقت، مع إخطار المستخدمين بالتغييرات الجوهرية.<br>
                - استمرار استخدام الموقع بعد التعديل يُعتبر موافقة على السياسة الجديدة.
                </li>
                <li><strong>التواصل معنا</strong><br>
                - لأي استفسارات بخصوص سياسة الخصوصية، يمكن التواصل معنا:<br>
                &nbsp;&nbsp;📧 <strong>البريد الإلكتروني:</strong> <a href='mailto:{SUPPORT_EMAIL}'>{SUPPORT_EMAIL}</a><br>
                &nbsp;&nbsp;📱 <strong>واتساب (الدعم السريع):</strong> <a href='{WHATSAPP_LINK}'>{WHATSAPP_NUMBER}</a>
                </li>
            </ol>
            </div>
            """, unsafe_allow_html=True)

# الصفحة الرئيسية المحسنة
def main_page():
    user = st.session_state.user
    
    # شريط جانبي محسن
    with st.sidebar:
        # بطاقة المستخدم
        badge_color = "#10b981" if user['subscription_type'] == 'premium' else "#f59e0b"
        badge_text = "مميز" if user['subscription_type'] == 'premium' else "مجاني"
        
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 50px; background: linear-gradient(90deg, #1e3c72, #2a5298); opacity: 0.8;"></div>
            <div style="position: relative; display: flex; flex-direction: column; align-items: center; margin-top: 25px;">
                <div style="background: white; width: 70px; height: 70px; border-radius: 50%; display: flex; justify-content: center; align-items: center; border: 3px solid #2a5298; box-shadow: 0 4px 10px rgba(42, 82, 152, 0.3); margin-bottom: 12px; font-size: 30px;">👤</div>
                <h3 style="margin: 0; font-size: 1.3rem; font-weight: 600; color: #334155;">{user['username']}</h3>
                <span style="display: inline-block; background: {badge_color}; color: white; font-size: 0.7rem; padding: 3px 10px; border-radius: 50px; margin-top: 8px; font-weight: 600;">{badge_text}</span>
                {f'<p style="margin-top: 8px; font-size: 0.85rem; color: #64748b;"><span style="font-weight: 500;">انتهاء الاشتراك:</span> {user["subscription_end"]}</p>' if user['subscription_end'] else '<div style="height: 8px;"></div>'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # إحصائيات سريعة
        st.markdown("### 📊 لوحة التحكم")
        
        reports = get_reports()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
                <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 5px;">إجمالي التقارير</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #334155;">{len(reports)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if reports:
                latest_report = reports[0]
                st.markdown(f"""
                <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
                    <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 5px;">آخر توصيات</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #334155;">{latest_report['total_symbols']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
                    <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 5px;">آخر توصيات</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #334155;">0</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # قسم الدعم والتواصل
        st.markdown("### 📞 الدعم والمساعدة")
        st.markdown(f"""
        <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.05); margin-bottom: 15px;">
            <div style="color: #334155; font-size: 0.9rem; line-height: 1.5;">
                <strong>🆘 تحتاج مساعدة؟</strong><br>
                تواصل معنا للحصول على الدعم الفني
            </div>
            <div style="margin-top: 10px;">
                <a href="{WHATSAPP_LINK}" target="_blank" style="display: inline-block; background: #25d366; color: white; padding: 8px 15px; border-radius: 20px; text-decoration: none; font-size: 0.85rem; font-weight: 600; margin-right: 5px;">
                    📱 واتساب
                </a>
                <a href="mailto:{SUPPORT_EMAIL}" style="display: inline-block; background: #0ea5e9; color: white; padding: 8px 15px; border-radius: 20px; text-decoration: none; font-size: 0.85rem; font-weight: 600;">
                    📧 إيميل
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # إضافة نظام تبديل الثيم
        add_theme_switcher()
        
        # زر تسجيل الخروج محسن
        with st.container():
            _, col2, _ = st.columns([1, 10, 1])
            with col2:
                if st.button("🚪 تسجيل الخروج", use_container_width=True, 
                          key="styled_logout", 
                          type="primary", 
                          help="انقر لتسجيل الخروج من النظام"):
                    del st.session_state.user
                    st.rerun()
    
    # العنوان الرئيسي - تم تكبير الإطار وزيادة البروز
    # التحقق من بيئة النشر
    is_cloud_deployment = bool(os.getenv('STREAMLIT_SHARING') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT'))
    deployment_badge = "☁️ نسخة سحابية" if is_cloud_deployment else "💻 نسخة محلية"
    
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; margin:40px auto 70px; background:linear-gradient(120deg, #f0f9ff, #e0f2fe); padding:50px 40px; border-radius:25px; box-shadow:0 20px 50px rgba(14, 44, 109, 0.25); border:4px solid #93c5fd; max-width:95%;">
        <div style="background:linear-gradient(120deg, #0f2350, #1e40af); color:white; font-size:1.4rem; font-weight:bold; padding:12px 30px; border-radius:50px; margin-bottom:25px; box-shadow:0 8px 20px rgba(14, 44, 109, 0.4); letter-spacing:1px;">إصدار 2025 - {deployment_badge}</div>
        <h1 style="font-size:4.5rem; line-height:1.3; font-weight:900; margin:20px 0; text-align:center; color:#0f2350; text-shadow:3px 3px 6px rgba(14, 44, 109, 0.2);">📊 نظام التوصيات المالية المتقدم</h1>
        <div style="width:300px; height:10px; background:linear-gradient(90deg, #0f2350, #1e40af); border-radius:50px; margin:25px 0; box-shadow:0 5px 15px rgba(14, 44, 109, 0.25);"></div>
        <div style="font-size:1.6rem; color:#0f2350; margin-top:25px; font-weight:600; text-align:center; line-height:1.6; text-shadow:1px 1px 3px rgba(255, 255, 255, 0.8); padding:0 20px;">أحدث التوصيات والتحليلات المالية لاتخاذ قرارات استثمارية مدروسة</div>
    </div>
    """, unsafe_allow_html=True)
    
    # التحقق من صحة الاشتراك
    if not is_subscription_valid(user):
        st.error("⚠️ انتهت صلاحية اشتراكك. يرجى تجديد الاشتراك للوصول إلى التوصيات.")
        with st.expander("📞 تواصل معنا لتجديد الاشتراك"):
            st.info("يرجى التواصل مع الإدارة لتجديد اشتراكك والاستمرار في الحصول على التوصيات.")
            
            # معلومات التواصل
            st.markdown(f"""
            **طرق التواصل:**
            
            📱 **واتساب (الدعم السريع):** 
            [{WHATSAPP_NUMBER}]({WHATSAPP_LINK})
            
            📧 **البريد الإلكتروني:** 
            [{SUPPORT_EMAIL}](mailto:{SUPPORT_EMAIL})
            """)
        return
    
    # تبويبات التطبيق
    if user['is_admin']:
        # تحديد التبويبات المتاحة بناءً على الصلاحيات
        tab_titles = ["📋 التوصيات"]
        
        # المدير الرئيسي له كل الصلاحيات أو المشرف لديه الصلاحيات المحددة
        is_super_admin = not user.get('admin_role') or user['admin_role'] == 'none' or user['admin_role'] is None
        
        # معالجة admin_permissions بشكل آمن
        permissions = user.get('admin_permissions', '')
        if isinstance(permissions, list):
            admin_permissions = permissions
        elif isinstance(permissions, str):
            admin_permissions = permissions.split(',') if permissions else []
        else:
            admin_permissions = []
        
        if is_super_admin or "manage_reports" in admin_permissions:
            tab_titles.append("📁 إدارة التقارير")
            
        if is_super_admin or "manage_users" in admin_permissions:
            tab_titles.append("👥 إدارة المستخدمين")
        
        if is_super_admin or "manage_invites" in admin_permissions:
            tab_titles.append("🎫 رموز الدعوة")
            
        tab_titles.append("⚙️ الإعدادات")
        
        tabs = st.tabs(tab_titles)
    else:
        tabs = st.tabs(["📋 التوصيات", "📊 الإحصائيات", "⚙️ إعدادات الحساب"])
    
    # تبويب التوصيات
    with tabs[0]:
        display_recommendations_tab()
    
    # عرض التبويبات للمدير بناءً على الصلاحيات
    if user['is_admin']:
        # إنشاء خريطة للتبويبات
        tab_map = {title: idx for idx, title in enumerate(tab_titles)}
        
        # عرض تبويب إدارة التقارير
        if "📁 إدارة التقارير" in tab_map:
            with tabs[tab_map["📁 إدارة التقارير"]]:
                display_admin_reports_tab()
        
        # عرض تبويب إدارة المستخدمين
        if "👥 إدارة المستخدمين" in tab_map:
            with tabs[tab_map["👥 إدارة المستخدمين"]]:
                display_admin_users_tab()
        
        # عرض تبويب رموز الدعوة
        if "🎫 رموز الدعوة" in tab_map:
            with tabs[tab_map["🎫 رموز الدعوة"]]:
                display_invite_codes_tab()
        
        # عرض تبويب الإعدادات (متاح للجميع)
        settings_index = tab_map["⚙️ الإعدادات"]
        with tabs[settings_index]:
            display_settings_tab()
    
    elif not user['is_admin'] and len(tabs) > 1:
        with tabs[1]:
            display_statistics_tab()
        
        # تبويب إعدادات الحساب للمستخدمين العاديين
        with tabs[2]:
            display_regular_user_settings_tab()

def display_recommendations_tab():
    """عرض تبويب التوصيات"""
    st.header("📈 أحدث التوصيات المالية")
    
    reports = get_reports()
    
    if not reports:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; padding:40px 0; background:white; border-radius:12px; box-shadow:0 5px 15px rgba(0,0,0,0.05); margin:20px 0;">
            <div style="font-size:4rem; margin-bottom:20px; opacity:0.6;">📭</div>
            <h3 style="margin-bottom:10px; color:#334155; font-weight:600;">لا توجد تقارير متاحة حالياً</h3>
            <p style="color:#64748b; max-width:400px; text-align:center;">سيتم عرض التوصيات هنا فور توفرها من فريق التحليل.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # عرض آخر تقرير
    latest_report = reports[0]
    
    # معلومات التقرير مع تصميم محسن
    st.markdown("""
    <div style="background:linear-gradient(120deg, #0f2350, #1e4db7); border-radius:12px; padding:20px 24px; margin-bottom:25px; box-shadow:0 10px 25px rgba(15, 35, 80, 0.25); color:white;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h3 style="margin:0; font-size:1.4rem; font-weight:600;">📊 تقرير اليوم</h3>
            </div>
            <div style="background:rgba(255,255,255,0.2); padding:4px 12px; border-radius:50px; font-size:0.85rem;">
                ⏰ آخر تحديث: {}</div>
        </div>
    </div>
    """.format(latest_report['upload_time']), unsafe_allow_html=True)
    
    # معلومات التقرير
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"📊 {latest_report['filename']}")
        st.caption(f"⏰ آخر تحديث: {latest_report['upload_time']}")
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="position:absolute; top:-12px; right:-12px; background:linear-gradient(120deg, #1e3c72, #2a5298); color:white; font-size:0.8rem; padding:5px 12px; border-radius:50px; box-shadow:0 4px 10px rgba(30, 60, 114, 0.3);">ملخص سريع</div>
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; margin-top:10px;">
                <div style="flex:0 0 48%; margin-bottom:15px;">
                    <div style="color:#64748b; font-size:0.8rem; margin-bottom:3px;">الرموز</div>
                    <div style="font-size:1.5rem; font-weight:700; color:#334155;">{latest_report['total_symbols']}</div>
                </div>
                <div style="flex:0 0 48%; margin-bottom:15px;">
                    <div style="color:#64748b; font-size:0.8rem; margin-bottom:3px;">الشراء</div>
                    <div style="font-size:1.5rem; font-weight:700; color:#10b981;">{latest_report['buy_recommendations']}</div>
                </div>
                <div style="flex:0 0 48%;">
                    <div style="color:#64748b; font-size:0.8rem; margin-bottom:3px;">البيع</div>
                    <div style="font-size:1.5rem; font-weight:700; color:#ef4444;">{latest_report['sell_recommendations']}</div>
                </div>
                <div style="flex:0 0 48%;">
                    <div style="color:#64748b; font-size:0.8rem; margin-bottom:3px;">الثقة</div>
                    <div style="font-size:1.5rem; font-weight:700; color:#2563eb;">{latest_report['avg_confidence']:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # عرض تفاصيل التقرير
    report_details = get_report_details(latest_report['id'])
    if report_details:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.subheader("🔍 تحليل السوق")
            st.text_area(
                "حالة السوق الحالية:",
                report_details['report'][4],  # market_analysis
                height=200,
                disabled=True
            )
        
        with col2:
            st.subheader("📊 توزيع التوصيات")
            # رسم بياني للتوصيات
            recommendation_data = {
                TYPE_LABEL: ['شراء', 'بيع', 'محايد'],
                'العدد': [
                    latest_report['buy_recommendations'],
                    latest_report['sell_recommendations'],
                    latest_report['total_symbols'] - latest_report['buy_recommendations'] - latest_report['sell_recommendations']
                ]
            }
            
            df_chart = pd.DataFrame(recommendation_data)
            st.bar_chart(df_chart.set_index(TYPE_LABEL))
        
        # جدول الصفقات مع تصميم محسن
        st.subheader("📋 جدول الصفقات التفصيلي")
        
        # التحقق من وجود الصفقات في تفاصيل التقرير
        trades_exist = report_details and 'trades' in report_details and report_details['trades']
        
        # إضافة زر لتوليد بيانات عرض توضيحي إذا لم تكن هناك صفقات
        if not trades_exist:
            demo_btn = st.button("✨ توليد بيانات توضيحية", key="generate_demo_data")
            if demo_btn:
                # إنشاء بيانات توضيحية
                trades_data = [
                    {"الرمز": "AAPL", "السعر": "$185.92", "التوصية": "🟢 شراء", "الثقة %": "78.5%", "وقف الخسارة": "$180.25", "هدف الربح": "$197.50", "نسبة ر/م": "3.20", "RSI": "58.4", "MACD": "2.15", "الاتجاه": "صاعد"},
                    {"الرمز": "MSFT", "السعر": "$405.63", "التوصية": "🟢 شراء", "الثقة %": "82.1%", "وقف الخسارة": "$395.75", "هدف الربح": "$425.30", "نسبة ر/م": "2.95", "RSI": "62.7", "MACD": "3.42", "الاتجاه": "صاعد"},
                    {"الرمز": "TSLA", "السعر": "$215.75", "التوصية": "🔴 بيع", "الثقة %": "67.8%", "وقف الخسارة": "$225.50", "هدف الربح": "$195.80", "نسبة ر/م": "2.50", "RSI": "42.3", "MACD": "-1.85", "الاتجاه": "هابط"},
                    {"الرمز": "AMZN", "السعر": "$178.35", "التوصية": "🟢 شراء", "الثقة %": "75.2%", "وقف الخسارة": "$172.60", "هدف الربح": "$192.40", "نسبة ر/م": "3.10", "RSI": "56.8", "MACD": "2.05", "الاتجاه": "صاعد"}
                ]
                trades_df = pd.DataFrame(trades_data)
                
                # تنسيق الجدول مباشرة
                styled_df = trades_df.style.map(
                    lambda val: 'background-color: rgba(16, 185, 129, 0.2); color: #047857; font-weight: bold; font-size: 1.05rem; padding: 6px 8px; border-radius: 4px;' if 'شراء' in str(val) else 'background-color: rgba(239, 68, 68, 0.2); color: #b91c1c; font-weight: bold; font-size: 1.05rem; padding: 6px 8px; border-radius: 4px;' if 'بيع' in str(val) else '',
                    subset=['التوصية']
                )
                
                # إضافة خصائص التنسيق العامة
                styled_df = styled_df.set_properties(
                    **{
                        'border': BORDER_STYLE,
                        'text-align': 'center',
                        'font-size': '14px',
                        'padding': '10px'
                    },
                    subset=None
                )
                
                st.success("✅ تم توليد بيانات توضيحية بنجاح!")
                st.dataframe(styled_df, use_container_width=True)
                return
            
        if trades_exist:
            try:
                # محاولة استخراج البيانات بناءً على بنية البيانات المتوقعة
                trades_data = []
                
                for trade in report_details['trades']:
                    # قد تكون البيانات مخزنة بتنسيقات مختلفة حسب الإصدار
                    # نحاول معالجة كل الاحتمالات
                    trade_dict = {}
                    
                    # الحالة الأولى: البيانات مخزنة كسلسلة JSON
                    if isinstance(trade[1], str) and trade[1].startswith('{'):
                        try:
                            trade_data = json.loads(trade[1])
                            # استخراج البيانات من كائن JSON مع حماية من القيم الفارغة
                            trade_dict['الرمز'] = trade_data.get('symbol', '')
                            
                            # تحويل القيم مع الحماية من None
                            price_value = trade_data.get('price', 0)
                            price = float(price_value) if price_value is not None else 0
                            
                            recommendation = trade_data.get('recommendation', '')
                            
                            confidence_value = trade_data.get('confidence', 0)
                            confidence = float(confidence_value) if confidence_value is not None else 0
                            
                            position_size_value = trade_data.get('position_size', 0)
                            position_size = int(position_size_value) if position_size_value is not None else 0
                            
                            position_value_val = trade_data.get('position_value', 0)
                            position_value = float(position_value_val) if position_value_val is not None else 0
                            
                            stop_loss_value = trade_data.get('stop_loss', 0)
                            stop_loss = float(stop_loss_value) if stop_loss_value is not None else 0
                            
                            target_value = trade_data.get('target_profit', 0)
                            target = float(target_value) if target_value is not None else 0
                            
                            risk_reward_value = trade_data.get('risk_reward_ratio', 0)
                            risk_reward = float(risk_reward_value) if risk_reward_value is not None else 0
                            
                            rsi_value = trade_data.get('rsi', 0)
                            rsi = float(rsi_value) if rsi_value is not None else 0
                            
                            macd_value = trade_data.get('macd', 0)
                            macd = float(macd_value) if macd_value is not None else 0
                            
                            trend = trade_data.get('trend', '')
                        except (json.JSONDecodeError, IndexError, TypeError):
                            # إذا فشل تحليل JSON أو تحويل البيانات، تخطي هذا السجل
                            continue
                    
                    # الحالة الثانية: البيانات مخزنة مباشرة في العمود
                    else:
                        try:
                            # قراءة البيانات مباشرة من السجل
                            trade_dict['الرمز'] = trade[2] if len(trade) > 2 else ''
                            price = float(trade[3]) if len(trade) > 3 and trade[3] is not None else 0
                            recommendation = trade[4] if len(trade) > 4 else ''
                            confidence = float(trade[5]) if len(trade) > 5 and trade[5] is not None else 0
                            position_size = int(trade[6]) if len(trade) > 6 and trade[6] is not None else 0
                            position_value = float(trade[7]) if len(trade) > 7 and trade[7] is not None else 0
                            stop_loss = float(trade[8]) if len(trade) > 8 and trade[8] is not None else 0
                            target = float(trade[9]) if len(trade) > 9 and trade[9] is not None else 0
                            risk_reward = float(trade[10]) if len(trade) > 10 and trade[10] is not None else 0
                            rsi = float(trade[11]) if len(trade) > 11 and trade[11] is not None else 0
                            macd = float(trade[12]) if len(trade) > 12 and trade[12] is not None else 0
                            trend = trade[13] if len(trade) > 13 else ''
                        except (ValueError, IndexError, TypeError):
                            # إذا فشل تحليل البيانات، تخطى هذا السجل
                            continue
                    
                    # تنسيق بيانات الجدول بشكل موحد مع حماية من القيم الفارغة
                    try:
                        trade_dict['السعر'] = f"${price:.2f}" if price and price > 0 else "-"
                        
                        # تنسيق التوصية مع إضافة ألوان وأيقونات
                        if "شراء" in str(recommendation):
                            trade_dict['التوصية'] = "🟢 شراء"
                        elif "بيع" in str(recommendation):
                            trade_dict['التوصية'] = "🔴 بيع"
                        else:
                            trade_dict['التوصية'] = str(recommendation) if recommendation else "-"
                        
                        trade_dict['الثقة %'] = f"{confidence:.1f}%" if confidence and confidence > 0 else "-"
                        trade_dict['حجم المركز'] = f"{position_size}" if position_size and position_size > 0 else "-"
                        trade_dict['قيمة المركز'] = f"${position_value:.2f}" if position_value and position_value > 0 else "-"
                        trade_dict['وقف الخسارة'] = f"${stop_loss:.2f}" if stop_loss and stop_loss > 0 else "-"
                        trade_dict['هدف الربح'] = f"${target:.2f}" if target and target > 0 else "-"
                        trade_dict['نسبة ر/م'] = f"{risk_reward:.2f}" if risk_reward and risk_reward > 0 else "-"
                        trade_dict['RSI'] = f"{rsi:.1f}" if rsi and rsi > 0 else "-"
                        trade_dict['MACD'] = f"{macd:.2f}" if macd else "-"
                        trade_dict['الاتجاه'] = str(trend) if trend else "-"
                    except (ValueError, TypeError, AttributeError):
                        # في حالة خطأ في التنسيق، استخدم قيم افتراضية
                        trade_dict['السعر'] = "-"
                        trade_dict['التوصية'] = "-"
                        trade_dict['الثقة %'] = "-"
                        trade_dict['حجم المركز'] = "-"
                        trade_dict['قيمة المركز'] = "-"
                        trade_dict['وقف الخسارة'] = "-"
                        trade_dict['هدف الربح'] = "-"
                        trade_dict['نسبة ر/م'] = "-"
                        trade_dict['RSI'] = "-"
                        trade_dict['MACD'] = "-"
                        trade_dict['الاتجاه'] = "-"
                    
                    trades_data.append(trade_dict)
                
                # إنشاء DataFrame من البيانات المعدة
                if trades_data:
                    trades_df = pd.DataFrame(trades_data)
                else:
                    # إذا لم تكن هناك بيانات، إنشاء DataFrame فارغ مع الأعمدة المتوقعة
                    trades_df = pd.DataFrame({
                        'الرمز': ["-"], 
                        'السعر': ["-"], 
                        'التوصية': ["لا توجد توصيات متاحة"],
                        'الثقة %': ["-"],
                        'وقف الخسارة': ["-"],
                        'هدف الربح': ["-"],
                        'نسبة ر/م': ["-"],
                        'RSI': ["-"],
                        'MACD': ["-"],
                        'الاتجاه': ["-"]
                    })
                
            except Exception as e:
                # في حالة وجود خطأ في معالجة البيانات، ننشئ جدولًا بسيطًا
                st.error(f"حدثت مشكلة في معالجة بيانات الصفقات: {str(e)}")
                # نعرض البيانات الخام بدلاً من ذلك
                raw_trades = []
                
                if 'trades' in report_details and report_details['trades']:
                    for trade in report_details['trades']:
                        raw_trade = {}
                        # تحقق من نوع البيانات
                        if isinstance(trade, dict):
                            # إذا كانت بيانات معجم، نستخدمها مباشرة
                            raw_trade = {str(k): str(v) for k, v in trade.items()}
                        elif isinstance(trade, (list, tuple)):
                            # إذا كانت بيانات قائمة، نحولها إلى معجم مع تسمية العناوين
                            for i, value in enumerate(trade):
                                column_name = f"العمود {i+1}"
                                # محاولة استخدام أسماء عامودية افتراضية
                                if i == 0:
                                    column_name = "معرف"
                                elif i == 1:
                                    column_name = "تقرير"
                                elif i == 2:
                                    column_name = "الرمز"
                                elif i == 3:
                                    column_name = "السعر"
                                elif i == 4:
                                    column_name = "التوصية"
                                try:
                                    raw_trade[column_name] = str(value)
                                except Exception:
                                    raw_trade[column_name] = "-"
                        else:
                            # نوع آخر من البيانات
                            raw_trade["البيانات"] = str(trade)
                        
                        raw_trades.append(raw_trade)
                
                # إذا كانت القائمة فارغة، إنشاء معجم فارغ مع أعمدة افتراضية
                if not raw_trades:
                    raw_trades = [{"الرمز": "-", "السعر": "-", "التوصية": "لا توجد بيانات متاحة", "ملاحظة": "يرجى إضافة تقرير جديد"}]
                
                trades_df = pd.DataFrame(raw_trades)
            
            # تلوين الصفوف حسب التوصية بشكل احترافي
            def highlight_recommendations(val):
                if 'شراء' in str(val):
                    return 'background-color: rgba(16, 185, 129, 0.2); color: #047857; font-weight: bold; font-size: 1.05rem; padding: 6px 8px; border-radius: 4px;'
                elif 'بيع' in str(val):
                    return 'background-color: rgba(239, 68, 68, 0.2); color: #b91c1c; font-weight: bold; font-size: 1.05rem; padding: 6px 8px; border-radius: 4px;'
                return ''
            
            # تنسيق إضافي للجدول
            def add_table_styles(styler):
                return styler.set_properties(**{
                    'border': '1px solid #e5e7eb',
                    'text-align': 'center',
                    'font-size': '14px',
                    'padding': '10px'
                }).set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#f8fafc'), 
                                               ('color', '#334155'),
                                               ('font-weight', '600'),
                                               ('text-align', 'center'),
                                               ('padding', '12px'),
                                               ('border', '1px solid #e5e7eb')]},
                    {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#fafafa')]},
                ])
            
            # تحقق من وجود العمود قبل تطبيق التنسيق
            if 'التوصية' in trades_df.columns:
                styled_df = trades_df.style.map(highlight_recommendations, subset=['التوصية']).pipe(add_table_styles)
            else:
                styled_df = trades_df.style.pipe(add_table_styles)
            
            # إضافة عنوان للجدول
            st.markdown("""
            <div style="background: linear-gradient(90deg, #1e3c72, #2a5298); color: white; padding: 8px 15px; border-radius: 8px 8px 0 0; font-weight: 600; display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
                <div>جدول التوصيات التفصيلي</div>
                <div style="font-size: 0.8rem; background: rgba(255,255,255,0.2); padding: 3px 10px; border-radius: 50px;">تم التحديث: اليوم</div>
            </div>
            """, unsafe_allow_html=True)
            
            # التحقق من وجود بيانات حقيقية في الجدول
            if trades_df.shape[0] == 1 and trades_df['الرمز'].iloc[0] == "-":
                st.info("⚠️ لا توجد توصيات متاحة حالياً. يرجى إضافة تقرير جديد أو التحقق من التقارير المتوفرة.")
            
            # عرض الجدول بغض النظر
            st.dataframe(styled_df, use_container_width=True)
            
            # خيار التصدير
            csv = trades_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 تحميل التقرير (CSV)",
                data=csv,
                file_name=f"recommendations_{latest_report['filename']}.csv",
                mime="text/csv"
            )
    
    # التقارير السابقة
    if len(reports) > 1:
        st.subheader("📚 التقارير السابقة")
        
        for i, report in enumerate(reports[1:6]):  # عرض آخر 5 تقارير
            with st.expander(f"📄 {report['filename']} - {report['upload_time']}"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("الرموز", report['total_symbols'])
                with col2:
                    st.metric("الشراء", report['buy_recommendations'])
                with col3:
                    st.metric("البيع", report['sell_recommendations'])
                with col4:
                    st.metric("الثقة", f"{report['avg_confidence']:.1f}%")

def display_admin_reports_tab():
    """عرض تبويب إدارة التقارير للمدير"""
    # استيراد دالة حذف التقرير
    from enhancements import delete_report
    
    st.header("📁 إدارة التقارير")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 رفع تقرير جديد")
        uploaded_file = st.file_uploader(
            "اختر ملف التقرير", 
            type=['txt'],
            help="يجب أن يكون الملف بتنسيق نصي (.txt) ويتبع النموذج المحدد"
        )
        
        if uploaded_file is not None:
            content = uploaded_file.read().decode('utf-8')
            
            st.success(f"✅ تم تحميل الملف: {uploaded_file.name}")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("👁️ معاينة التقرير", use_container_width=True):
                    st.session_state.preview_data = parse_recommendations_file(content)
                    st.session_state.preview_content = content
                    st.session_state.preview_filename = uploaded_file.name
            
            with col_btn2:
                if st.button("💾 حفظ التقرير", use_container_width=True):
                    try:
                        parsed_data = parse_recommendations_file(content)
                        report_id = save_report(uploaded_file.name, content, parsed_data)
                        st.success(f"🎉 تم حفظ التقرير بنجاح! رقم التقرير: {report_id}")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ في حفظ التقرير: {str(e)}")
    
    with col2:
        st.subheader("📊 إحصائيات سريعة")
        reports = get_reports()
        
        total_reports = len(reports)
        total_symbols = sum(r['total_symbols'] for r in reports) if reports else 0
        avg_confidence = sum(r['avg_confidence'] for r in reports) / total_reports if total_reports > 0 else 0
        
        st.metric("📈 إجمالي التقارير", total_reports)
        st.metric("🎯 إجمالي الرموز", total_symbols)
        st.metric("📊 متوسط الثقة", f"{avg_confidence:.1f}%")
    
    # إضافة قسم إدارة التقارير الموجودة
    st.markdown("---")
    st.subheader("📋 إدارة التقارير الموجودة")
    
    reports = get_reports()
    if not reports:
        st.info("لا توجد تقارير مخزنة حالياً")
    else:
        # تنظيم البيانات
        formatted_reports = []
        for r in reports:
            # تحويل timestamp إلى تنسيق أكثر قابلية للقراءة
            try:
                upload_date = r['upload_time'].split()[0] if ' ' in r['upload_time'] else r['upload_time']
            except Exception:
                upload_date = r['upload_time']
            
            formatted_reports.append({
                'معرف التقرير': r['id'],
                'اسم الملف': r['filename'],
                'تاريخ الرفع': upload_date,
                'عدد الرموز': r['total_symbols'],
                'توصيات الشراء': r['buy_recommendations'],
                'توصيات البيع': r['sell_recommendations']
            })
        
        # إنشاء DataFrame للعرض
        reports_df = pd.DataFrame(formatted_reports)
        
        # عرض قائمة التقارير
        st.dataframe(reports_df, use_container_width=True)
        
        # عرض إجمالي عدد التقارير
        st.info(f"🗃️ العدد الإجمالي للتقارير: {len(reports)} تقرير")
        
        # قسم إدارة التقارير
        col_single, col_all = st.columns(2)
        
        # قسم حذف تقرير واحد
        with col_single:
            with st.expander("🗑️ حذف تقرير محدد", expanded=True):
                if reports:
                    selected_report_id = st.selectbox(
                        "اختر التقرير المراد حذفه",
                        options=[r['id'] for r in reports],
                        format_func=lambda x: next((f"#{x} - {r['filename']} ({r['upload_time']})" for r in reports if r['id'] == x), str(x))
                    )
                    
                    if selected_report_id is not None:
                        # كود التأكيد لمنع الحذف العرضي
                        confirmation_key = f"delete_confirmation_{selected_report_id}"
                        if confirmation_key not in st.session_state:
                            st.session_state[confirmation_key] = False
                            
                        if st.button("حذف التقرير المحدد", use_container_width=True, type="primary", key=f"delete_btn_{selected_report_id}"):
                            st.session_state[confirmation_key] = True
                        
                        # عرض رسالة التأكيد
                        if st.session_state[confirmation_key]:
                            st.warning(f"هل أنت متأكد من حذف التقرير #{selected_report_id}؟ لا يمكن التراجع عن هذه العملية!")
                            
                            col_confirm, col_cancel = st.columns(2)
                            
                            with col_confirm:
                                if st.button("✅ نعم، احذف التقرير", use_container_width=True, key=f"confirm_delete_{selected_report_id}"):
                                    success = delete_report(selected_report_id)
                                    if success:
                                        st.success(f"✓ تم حذف التقرير #{selected_report_id} بنجاح")
                                        # إعادة تعيين حالة التأكيد ومسح الجلسة
                                        st.session_state[confirmation_key] = False
                                        # إعادة تشغيل الصفحة لتحديث القائمة
                                        st.rerun()
                                    else:
                                        st.error(f"❌ فشل في حذف التقرير #{selected_report_id}")
                            
                            with col_cancel:
                                if st.button("❌ إلغاء", use_container_width=True, key=f"cancel_delete_{selected_report_id}"):
                                    st.session_state[confirmation_key] = False
                                    st.rerun()
                else:
                    st.info("📭 لا توجد تقارير للحذف")
        
        # قسم حذف جميع التقارير
        with col_all:
            # استيراد دالة حذف جميع التقارير
            from enhancements import delete_all_reports
            
            with st.expander("⚠️ حذف جميع التقارير", expanded=True):
                st.warning("⚠️ هذا الإجراء سيؤدي إلى حذف جميع التقارير والصفقات المرتبطة بها بشكل نهائي!")
                
                # كود التأكيد لمنع الحذف العرضي
                if "delete_all_confirmation" not in st.session_state:
                    st.session_state.delete_all_confirmation = False
                
                if st.button("حذف جميع التقارير", use_container_width=True, type="primary", key="delete_all_btn"):
                    st.session_state.delete_all_confirmation = True
                
                # عرض رسالة التأكيد
                if st.session_state.delete_all_confirmation:
                    st.error(f"⚠️ هل أنت متأكد من حذف جميع التقارير وعددها {len(reports)} تقرير؟")
                    st.error("⛔ لا يمكن التراجع عن هذه العملية نهائياً!")
                    
                    col_confirm_all, col_cancel_all = st.columns(2)
                    
                    with col_confirm_all:
                        if st.button("✅ نعم، احذف جميع التقارير", use_container_width=True, key="confirm_delete_all"):
                            success = delete_all_reports()
                            if success:
                                st.success("✓ تم حذف جميع التقارير بنجاح")
                                # إعادة تعيين حالة التأكيد
                                st.session_state.delete_all_confirmation = False
                                # إعادة تشغيل الصفحة لتحديث القائمة
                                st.rerun()
                            else:
                                st.error("❌ حدث خطأ أثناء حذف التقارير")
                    
                    with col_cancel_all:
                        if st.button("❌ إلغاء", use_container_width=True, key="cancel_delete_all"):
                            # إعادة تعيين حالة التأكيد
                            st.session_state.delete_all_confirmation = False
                            st.rerun()
    
    # عرض معاينة التقرير
    if 'preview_data' in st.session_state:
        st.markdown("---")
        st.subheader("👁️ معاينة التقرير")
        
        parsed_data = st.session_state.preview_data
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("إجمالي الرموز", parsed_data['stats']['total_symbols'])
        with col2:
            st.metric("توصيات الشراء", parsed_data['stats']['buy_recommendations'])
        with col3:
            st.metric("توصيات البيع", parsed_data['stats']['sell_recommendations'])
        with col4:
            st.metric("متوسط الثقة", f"{parsed_data['stats']['avg_confidence']:.1f}%")
        
        if parsed_data['trades']:
            st.subheader("📋 معاينة الصفقات")
            preview_df = pd.DataFrame(parsed_data['trades'][:10])  # عرض أول 10 صفقات
            st.dataframe(preview_df, use_container_width=True)
            
            if len(parsed_data['trades']) > 10:
                st.info(f"عرض أول 10 صفقات من أصل {len(parsed_data['trades'])} صفقة")

def display_admin_users_tab():
    """عرض تبويب إدارة المستخدمين للمدير"""
    st.header("👥 إدارة المستخدمين")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # إحصائيات المستخدمين محسنة
    # صف أول من الإحصائيات
    metrics_container = st.container()
    
    with metrics_container:
        col1, col2, col3, col4 = st.columns(4)
        
        # إحصائيات المستخدمين
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0 AND subscription_type = "premium"')
        premium_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0 AND DATE(created_at) >= DATE("now", "-7 days")')
        new_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0 AND subscription_end < DATE("now") AND subscription_type = "premium"')
        expired_users = cursor.fetchone()[0]
        
        free_users = total_users - premium_users
        premium_percentage = (premium_users / total_users * 100) if total_users > 0 else 0
        
        with col1:
            st.metric("👤 إجمالي المستخدمين", total_users)
        with col2:
            st.metric("💎 المشتركين المميزين", premium_users, f"{premium_percentage:.1f}%")
        with col3:
            st.metric("⭐ مشتركين مجاني", free_users)
        with col4:
            st.metric("🆕 مستخدمين جدد (7 أيام)", new_users)
    
    # رسم بياني للمستخدمين
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📊 توزيع الاشتراكات")
        
        # التحقق من وجود بيانات قبل إنشاء الرسم البياني
        if total_users > 0:
            # حساب القيم بشكل آمن
            active_premium = max(0, premium_users - expired_users)  # لا تسمح بالقيم السالبة
            
            pie_data = {
                'نوع الاشتراك': ['مميز', 'مجاني', 'منتهي'],
                'العدد': [active_premium, free_users, expired_users]
            }
            
            # التأكد من أن المجموع لا يساوي صفر
            if sum(pie_data['العدد']) > 0:
                # استخدام plotly بدلاً من matplotlib لتجنب مشاكل النوع
                try:
                    import plotly.express as px
                    df_pie = pd.DataFrame(pie_data)
                    fig = px.pie(df_pie, values='العدد', names='نوع الاشتراك', 
                                title='توزيع أنواع الاشتراكات')
                    st.plotly_chart(fig, use_container_width=True)
                except ImportError:
                    # في حالة عدم توفر plotly، عرض البيانات كجدول
                    df_pie = pd.DataFrame(pie_data)
                    st.bar_chart(df_pie.set_index('نوع الاشتراك'))
            else:
                st.info("لا توجد بيانات كافية لعرض الرسم البياني")
        else:
            st.info("لا يوجد مستخدمون مسجلون بعد لعرض الرسم البياني")
    
    with col_chart2:
        st.subheader("📈 نشاط المستخدمين")
        # احصائيات للنشاط اليومي (محاكاة)
        cursor.execute('''
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM users 
            WHERE DATE(created_at) > DATE('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        ''')
        activity_data = cursor.fetchall()
        
        if activity_data:
            df_activity = pd.DataFrame(activity_data, columns=['التاريخ', 'عدد المستخدمين الجدد'])
            st.bar_chart(df_activity.set_index('التاريخ'))
        else:
            st.info("لا توجد بيانات نشاط كافية للعرض")
    
    # أدوات إدارة المستخدمين
    st.markdown("---")
    
    user_management_tabs = st.tabs([
        "📋 قائمة المستخدمين", 
        "➕ إضافة مستخدم", 
        "🔄 تعديل مستخدم", 
        "🗑️ حذف مستخدم",
        "📅 تمديد اشتراك"
    ])
    
    # 1. قائمة المستخدمين
    with user_management_tabs[0]:
        st.subheader("📋 قائمة المستخدمين")
        
        # خيارات البحث والتصفية المتقدمة
        search_col1, search_col2, search_col3 = st.columns(3)
        
        with search_col1:
            search_username = st.text_input("🔍 بحث باسم المستخدم", key="search_username")
        
        with search_col2:
            filter_subscription = st.selectbox(
                "🏷️ تصفية حسب نوع الاشتراك:",
                ["الكل", "premium", "free"]
            )
        
        with search_col3:
            sort_option = st.selectbox(
                "🔢 ترتيب حسب:",
                ["تاريخ التسجيل (الأحدث)", "تاريخ التسجيل (الأقدم)", "اسم المستخدم"]
            )
        
        # بناء الاستعلام مع التصفية
        query = '''
            SELECT id, username, email, IFNULL(phone, '') as phone, subscription_type, subscription_end, created_at,
                  (CASE WHEN subscription_end < DATE('now') AND subscription_type = 'premium' THEN 'منتهي' 
                        WHEN subscription_type = 'premium' THEN 'مميز'
                        ELSE 'مجاني' END) as status
            FROM users WHERE is_admin = FALSE
        '''
        
        params = []
        
        if search_username:
            query += " AND username LIKE ?"
            params.append(f"%{search_username}%")
        
        if filter_subscription != "الكل":
            query += " AND subscription_type = ?"
            params.append(filter_subscription)
        
        # إضافة الترتيب
        if sort_option == "تاريخ التسجيل (الأحدث)":
            query += " ORDER BY created_at DESC"
        elif sort_option == "تاريخ التسجيل (الأقدم)":
            query += " ORDER BY created_at ASC"
        else:
            query += " ORDER BY username"
        
        # تنفيذ الاستعلام
        cursor.execute(query, params)
        users = cursor.fetchall()
        
        if users:
            users_df = pd.DataFrame(users, columns=[
                'المعرف', 'اسم المستخدم', 'البريد الإلكتروني', 'رقم الجوال',
                'نوع الاشتراك', 'تاريخ انتهاء الاشتراك', 'تاريخ التسجيل', 'الحالة'
            ])
            
            # تنسيق العرض
            users_df['تاريخ انتهاء الاشتراك'] = users_df['تاريخ انتهاء الاشتراك'].fillna('غير محدد')
            
            # عرض جدول المستخدمين
            st.dataframe(users_df, use_container_width=True)
            
            # تصدير قائمة المستخدمين
            csv = users_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 تصدير قائمة المستخدمين (CSV)",
                data=csv,
                file_name=f"users_list_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # إحصائيات سريعة
            st.info(f"👥 إجمالي النتائج: {len(users_df)} مستخدم")
        else:
            st.info("📭 لا يوجد مستخدمون مطابقون لمعايير البحث")
    
    # 2. إضافة مستخدم جديد
    with user_management_tabs[1]:
        st.subheader("➕ إضافة مستخدم جديد")
        
        with st.form("add_user_form"):
            new_username = st.text_input("اسم المستخدم", key="add_username")
            new_email = st.text_input("البريد الإلكتروني", key="add_email")
            new_phone = st.text_input("رقم الجوال", key="add_phone")
            new_password = st.text_input("كلمة المرور", type="password", key="add_password")
            
            # خيارات إضافية
            col1, col2 = st.columns(2)
            with col1:
                new_subscription = st.selectbox(
                    "نوع الاشتراك",
                    ["free", "premium"],
                    key="add_subscription"
                )
            
            with col2:
                if new_subscription == "premium":
                    sub_duration = st.number_input("مدة الاشتراك (بالأشهر)", min_value=1, value=3, key="add_sub_duration")
                    sub_end_date = (datetime.datetime.now() + datetime.timedelta(days=30 * sub_duration)).date()
                else:
                    sub_end_date = None
            
            # زر الإضافة
            submitted = st.form_submit_button("✅ إضافة المستخدم")
            
            if submitted:
                if not new_username or not new_email or not new_password:
                    st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")
                else:
                    # التحقق من عدم تكرار المستخدم
                    cursor.execute("SELECT username FROM users WHERE username = ? OR email = ?", 
                                (new_username, new_email))
                    existing = cursor.fetchone()
                    
                    if existing:
                        st.error("❌ اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل")
                    else:
                        # إضافة المستخدم الجديد
                        password_hash = hash_password(new_password)
                        try:
                            # التأكد من أن قيمة new_phone ليست فارغة
                            phone_value = new_phone if new_phone.strip() else None
                            
                            cursor.execute('''
                                INSERT INTO users (username, email, phone, password_hash, subscription_type, subscription_end)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (new_username, new_email, phone_value, password_hash, new_subscription, sub_end_date))
                            conn.commit()
                            st.success(f"✅ تمت إضافة المستخدم {new_username} بنجاح!")
                        except Exception as e:
                            st.error(f"❌ خطأ في إضافة المستخدم: {str(e)}")
    
    # 3. تعديل بيانات مستخدم
    with user_management_tabs[2]:
        st.subheader("🔄 تعديل بيانات مستخدم")
        
        # قائمة المستخدمين للاختيار منها
        cursor.execute("SELECT id, username FROM users WHERE is_admin = FALSE ORDER BY username")
        all_users = cursor.fetchall()
        
        if all_users:
            user_options = ["اختر مستخدم..."] + [f"{u[1]} (ID: {u[0]})" for u in all_users]
            selected_user_option = st.selectbox("اختر المستخدم المراد تعديله:", user_options)
            
            if selected_user_option != "اختر مستخدم...":
                user_id = int(selected_user_option.split("ID: ")[1].rstrip(")"))
                
                # الحصول على بيانات المستخدم الحالية
                cursor.execute('''
                    SELECT username, email, phone, subscription_type, subscription_end
                    FROM users WHERE id = ?
                ''', (user_id,))
                user_data = cursor.fetchone()
                
                if user_data:
                    username, email, phone, sub_type, sub_end = user_data
                    
                    with st.form("edit_user_form"):
                        st.subheader(f"تعديل بيانات المستخدم: {username}")
                        
                        new_email = st.text_input("البريد الإلكتروني", value=email)
                        new_phone = st.text_input("رقم الجوال", value=phone if phone else "")
                        new_password = st.text_input("كلمة المرور الجديدة (اترك فارغًا للاحتفاظ بالحالية)", type="password")
                        
                        # خيارات الاشتراك
                        new_sub_type = st.selectbox("نوع الاشتراك", 
                                                 ["free", "premium"], 
                                                 index=0 if sub_type == "free" else 1)
                        
                        # إذا كان الاشتراك مميزًا، عرض خيار تاريخ الانتهاء
                        if new_sub_type == "premium":
                            if sub_end:
                                default_date = datetime.datetime.strptime(sub_end, '%Y-%m-%d').date()
                            else:
                                default_date = (datetime.datetime.now() + datetime.timedelta(days=30)).date()
                            
                            new_sub_end = st.date_input("تاريخ انتهاء الاشتراك", value=default_date)
                        else:
                            new_sub_end = None
                        
                        submitted = st.form_submit_button("💾 حفظ التغييرات")
                        
                        if submitted:
                            # بناء استعلام التحديث
                            update_fields = []
                            update_values = []
                            
                            # تحديث البريد الإلكتروني إذا تغير
                            if new_email != email:
                                update_fields.append("email = ?")
                                update_values.append(new_email)
                            
                            # تحديث رقم الجوال إذا تغير
                            if new_phone != phone:
                                update_fields.append("phone = ?")
                                update_values.append(new_phone)
                            
                            # تحديث كلمة المرور إذا تم إدخالها
                            if new_password:
                                update_fields.append("password_hash = ?")
                                update_values.append(hash_password(new_password))
                            
                            # تحديث نوع الاشتراك
                            update_fields.append("subscription_type = ?")
                            update_values.append(new_sub_type)
                            
                            # تحديث تاريخ انتهاء الاشتراك
                            update_fields.append("subscription_end = ?")
                            update_values.append(new_sub_end)
                            
                            # إضافة معرف المستخدم للقيم
                            update_values.append(user_id)
                            
                            if update_fields:
                                try:
                                    # تنفيذ التحديث
                                    cursor.execute(f'''
                                        UPDATE users SET {", ".join(update_fields)}
                                        WHERE id = ?
                                    ''', tuple(update_values))
                                    conn.commit()
                                    st.success("✅ تم تحديث بيانات المستخدم بنجاح!")
                                except Exception as e:
                                    st.error(f"❌ خطأ في تحديث البيانات: {str(e)}")
                else:
                    st.error("❌ لم يتم العثور على بيانات المستخدم")
        else:
            st.info("📭 لا يوجد مستخدمون مسجلون بعد")
    
    # 4. حذف مستخدم
    with user_management_tabs[3]:
        st.subheader("🗑️ حذف مستخدم")
        
        cursor.execute("SELECT id, username, email FROM users WHERE is_admin = FALSE ORDER BY username")
        all_users = cursor.fetchall()
        
        if all_users:
            user_options = ["اختر مستخدم..."] + [f"{u[1]} ({u[2]}) (ID: {u[0]})" for u in all_users]
            selected_user_option = st.selectbox("اختر المستخدم المراد حذفه:", user_options, key="del_user_select")
            
            if selected_user_option != "اختر مستخدم...":
                user_id = int(selected_user_option.split("ID: ")[1].rstrip(")"))
                username = selected_user_option.split(" (")[0]
                
                st.warning(f"⚠️ أنت على وشك حذف المستخدم: {username}")
                st.warning("⚠️ هذا الإجراء لا يمكن التراجع عنه!")
                
                # التأكيد على الحذف
                confirm = st.text_input("اكتب 'تأكيد' للمتابعة:", key="confirm_delete")
                
                if st.button("❌ حذف المستخدم نهائيًا", key="delete_user_btn"):
                    if confirm.strip() == "تأكيد":
                        try:
                            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                            conn.commit()
                            st.success(f"✅ تم حذف المستخدم {username} بنجاح")
                            # إعادة تحميل الصفحة
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ في حذف المستخدم: {str(e)}")
                    else:
                        st.error("❌ يرجى كتابة 'تأكيد' للمتابعة")
        else:
            st.info("📭 لا يوجد مستخدمون مسجلون بعد")
    
    # 5. تمديد اشتراك
    with user_management_tabs[4]:
        st.subheader("📅 تمديد اشتراك")
        
        # استعلام للحصول على المستخدمين المميزين أو المنتهية اشتراكاتهم
        cursor.execute('''
            SELECT id, username, email, subscription_end, 
                (CASE WHEN subscription_end < DATE('now') THEN 'منتهي' ELSE 'نشط' END) as status
            FROM users 
            WHERE is_admin = FALSE AND (subscription_type = 'premium' OR subscription_type = 'free')
            ORDER BY username
        ''')
        sub_users = cursor.fetchall()
        
        if sub_users:
            user_options = ["اختر مستخدم..."] + [
                f"{u[1]} ({u[2]}) - الاشتراك: {u[3] or 'غير محدد'} ({u[4]}) (ID: {u[0]})" 
                for u in sub_users
            ]
            
            selected_user_option = st.selectbox("اختر المستخدم لتمديد الاشتراك:", user_options, key="extend_sub_select")
            
            if selected_user_option != "اختر مستخدم...":
                user_id = int(selected_user_option.split("ID: ")[1].rstrip(")"))
                username = selected_user_option.split(" (")[0]
                
                # الحصول على تفاصيل الاشتراك الحالية
                cursor.execute('''
                    SELECT subscription_type, subscription_end
                    FROM users WHERE id = ?
                ''', (user_id,))
                sub_data = cursor.fetchone()
                
                if sub_data:
                    current_type, current_end = sub_data
                    
                    with st.form("extend_subscription_form"):
                        st.subheader(f"تمديد اشتراك: {username}")
                        
                        # خيارات تمديد الاشتراك
                        new_sub_type = st.selectbox("نوع الاشتراك", 
                                                 ["free", "premium"], 
                                                 index=0 if current_type == "free" else 1,
                                                 key="extend_sub_type")
                        
                        # خيارات التمديد
                        if new_sub_type == "premium":
                            extension_options = st.radio(
                                "طريقة التمديد:",
                                ["إضافة فترة للتاريخ الحالي", "تحديد تاريخ جديد"],
                                key="extension_method"
                            )
                            
                            if extension_options == "إضافة فترة للتاريخ الحالي":
                                months = st.number_input("عدد الشهور للإضافة", min_value=1, value=3, key="months_to_add")
                                
                                # حساب التاريخ الجديد
                                if current_end and current_end != "None" and current_type == "premium":
                                    try:
                                        current_date = datetime.datetime.strptime(current_end, '%Y-%m-%d').date()
                                        if current_date < datetime.datetime.now().date():
                                            # إذا كان الاشتراك منتهيًا، ابدأ من اليوم
                                            new_end_date = datetime.datetime.now().date() + datetime.timedelta(days=30 * months)
                                        else:
                                            # إضافة إلى التاريخ الحالي
                                            new_end_date = current_date + datetime.timedelta(days=30 * months)
                                    except Exception:
                                        new_end_date = datetime.datetime.now().date() + datetime.timedelta(days=30 * months)
                                else:
                                    new_end_date = datetime.datetime.now().date() + datetime.timedelta(days=30 * months)
                                
                                st.info(f"سيتم تمديد الاشتراك حتى: {new_end_date.strftime('%Y-%m-%d')}")
                            else:
                                # تحديد تاريخ محدد
                                min_date = datetime.datetime.now().date()
                                new_end_date = st.date_input(
                                    "تاريخ انتهاء الاشتراك الجديد",
                                    value=min_date + datetime.timedelta(days=90),
                                    min_value=min_date,
                                    key="specific_end_date"
                                )
                        else:
                            new_end_date = None
                        
                        # زر التأكيد
                        submitted = st.form_submit_button("💾 تمديد الاشتراك")
                        
                        if submitted:
                            try:
                                # تحديث بيانات الاشتراك
                                cursor.execute('''
                                    UPDATE users 
                                    SET subscription_type = ?, subscription_end = ?
                                    WHERE id = ?
                                ''', (new_sub_type, new_end_date, user_id))
                                conn.commit()
                                
                                # عرض رسالة نجاح
                                if new_sub_type == "premium":
                                    st.success(f"✅ تم تمديد اشتراك المستخدم {username} حتى {new_end_date}")
                                else:
                                    st.success(f"✅ تم تغيير اشتراك المستخدم {username} إلى مجاني")
                                
                            except Exception as e:
                                st.error(f"❌ خطأ في تمديد الاشتراك: {str(e)}")
                else:
                    st.error("❌ لم يتم العثور على بيانات الاشتراك")
        else:
            st.info("📭 لا يوجد مستخدمون مسجلون بعد")
    
    conn.close()

def display_invite_codes_tab():
    """عرض تبويب إدارة رموز الدعوة للمدير"""
    st.header("🎫 إدارة رموز الدعوة")
    
    user = st.session_state.user
    
    # تقسيم الصفحة إلى عمودين
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 إنشاء رمز دعوة جديد")
        
        with st.form("create_invite_code_form"):
            # نوع الاشتراك
            subscription_type = st.selectbox(
                "نوع الاشتراك",
                ["free", "premium"],
                format_func=lambda x: "مجاني" if x == "free" else "مميز"
            )
            
            # مدة الصلاحية
            expiry_days = st.slider(
                "مدة الصلاحية (بالأيام)",
                min_value=1,
                max_value=30,
                value=7
            )
            
            # عدد مرات الاستخدام
            max_uses = st.number_input(
                "عدد مرات الاستخدام المسموح",
                min_value=1,
                max_value=100,
                value=1
            )
            
            # مدة الاشتراك (للمميز فقط) - سيتم إضافتها لاحقاً
            # subscription_duration = 30
            # if subscription_type == "premium":
            #     subscription_duration = st.slider(
            #         "مدة الاشتراك المميز (بالأيام)",
            #         min_value=30,
            #         max_value=365,
            #         value=30
            #     )
            
            # وصف اختياري
            description = st.text_area(
                "وصف الرمز (اختياري)",
                placeholder="مثال: رمز دعوة لعميل جديد"
            )
            
            submitted = st.form_submit_button("🎫 إنشاء رمز الدعوة", use_container_width=True)
            
            if submitted:
                success, message = generate_invite_code(
                    created_by=user['id'],
                    subscription_type=subscription_type,
                    duration_days=expiry_days,
                    max_uses=max_uses,
                    description=description
                )
                
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    with col2:
        st.subheader("📋 الرموز الحالية")
        
        # جلب رموز الدعوة
        try:
            invite_codes = get_invite_codes()
        except Exception as e:
            st.error(f"خطأ في جلب رموز الدعوة: {str(e)}")
            invite_codes = []
        
        if invite_codes:
            # إحصائيات سريعة
            active_codes = [c for c in invite_codes if bool(c.get('is_active', False)) and c.get('status') == 'نشط']
            used_codes = [c for c in invite_codes if c.get('status') == 'مستخدم']
            expired_codes = [c for c in invite_codes if c.get('status') == 'منتهي']
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("نشط", len(active_codes))
            with col_stats2:
                st.metric("مستخدم", len(used_codes))
            with col_stats3:
                st.metric("منتهي", len(expired_codes))
            
            st.markdown("---")
            
            # عرض الرموز في جدول
            for idx, code_info in enumerate(invite_codes):
                with st.expander(f"🎫 {code_info['code']} - {code_info['status']}", expanded=False):
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.write(f"**الرمز:** `{code_info['code']}`")
                        st.write(f"**النوع:** {code_info['subscription_type']}")
                        st.write(f"**المنشئ:** {code_info['created_by_username']}")
                        st.write(f"**تاريخ الإنشاء:** {code_info['created_at']}")
                    
                    with col_info2:
                        st.write(f"**الصلاحية:** {code_info['expires_at']}")
                        st.write(f"**الاستخدام:** {code_info['current_uses']}/{code_info['max_uses']}")
                        st.write(f"**الحالة:** {code_info['status']}")
                        if code_info['description']:
                            st.write(f"**الوصف:** {code_info['description']}")
                    
                    # خيارات إدارة الرمز
                    if bool(code_info.get('is_active', False)) and code_info.get('status') == 'نشط':
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("🗑️ حذف الرمز", key=f"delete_code_{idx}"):
                                success = delete_invite_code(code_info['id'])
                                if success:
                                    st.success("✅ تم حذف الرمز بنجاح")
                                    st.rerun()
                                else:
                                    st.error("❌ فشل في حذف الرمز")
                        
                        with col_action2:
                            if st.button("📋 نسخ الرمز", key=f"copy_code_{idx}"):
                                st.info(f"الرمز: {code_info['code']}")
                                st.balloons()
        else:
            st.info("📭 لا توجد رموز دعوة حالياً")

def display_settings_tab():
    """عرض تبويب الإعدادات للمدير"""
    st.header("⚙️ إعدادات النظام")
    
    user = st.session_state.user
    
    # إدارة المشرفين
    if user['is_admin']:
        st.markdown("""
        <div style="background: linear-gradient(120deg, #1e3c72, #2a5298); border-radius: 12px; padding: 16px 20px; margin: 20px 0; box-shadow: 0 5px 15px rgba(30, 60, 114, 0.2); color: white; text-align: center;">
            <h2 style="margin: 0; font-weight: 700; font-size: 1.5rem; text-shadow: 0 2px 3px rgba(0,0,0,0.1);">👥 إدارة المشرفين</h2>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["➕ إضافة مشرف جديد", "🔄 إدارة المشرفين الحاليين"])
        
        # تبويب إضافة مشرف جديد
        with tab1:
            if st.button("➕ إضافة مشرف جديد", type="primary", use_container_width=True):
                st.session_state.show_admin_form = True
                
            # عرض نموذج إضافة مشرف إذا تم النقر على الزر
            if st.session_state.get('show_admin_form', False):
                with st.form("إضافة_مشرف_مباشر"):
                    st.subheader("👤 إضافة مشرف جديد")
                    new_admin_name = st.text_input("اسم المستخدم", key="direct_admin_name")
                    new_admin_email = st.text_input("البريد الإلكتروني", key="direct_admin_email")
                    new_admin_password = st.text_input("كلمة المرور", type="password", key="direct_admin_password")
                
                    # تحديد الصلاحيات
                    st.write("تحديد الصلاحيات:")
                    col1, col2 = st.columns(2)
                    with col1:
                        can_manage_users = st.checkbox("إدارة المستخدمين", value=True, key="direct_perm_users")
                        can_manage_reports = st.checkbox("إدارة التقارير", value=True, key="direct_perm_reports")
                    with col2:
                        can_manage_admins = st.checkbox("إدارة المشرفين", key="direct_perm_admins")
                        can_backup = st.checkbox("النسخ الاحتياطي", key="direct_perm_backup")
                
                    submit_new_admin = st.form_submit_button("إضافة مشرف", type="primary")
                    cancel_button = st.form_submit_button("إلغاء")
                    
                    if cancel_button:
                        st.session_state.show_admin_form = False
                        st.rerun()
                    
                    if submit_new_admin:
                        if not new_admin_name or not new_admin_email or not new_admin_password:
                            st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")
                        elif len(new_admin_password) < 6:
                            st.error("⚠️ كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                        else:
                            conn = sqlite3.connect(DB_NAME)
                            cursor = conn.cursor()
                            
                            # التحقق من وجود اسم المستخدم أو البريد الإلكتروني
                            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (new_admin_name, new_admin_email))
                            if cursor.fetchone():
                                st.error("⚠️ اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل")
                            else:
                                # إنشاء مصفوفة الصلاحيات
                                permissions = []
                                if can_manage_users:
                                    permissions.append("users")
                                if can_manage_reports:
                                    permissions.append("reports")
                                if can_manage_admins:
                                    permissions.append("admins")
                                if can_backup:
                                    permissions.append("backup")
                            
                            # إضافة المشرف الجديد
                            try:
                                password_hash = hash_password(new_admin_password)
                                cursor.execute('''
                                INSERT INTO users (username, email, password_hash, is_admin, admin_role, admin_permissions)
                                VALUES (?, ?, ?, 1, ?, ?)
                                ''', (new_admin_name, new_admin_email, password_hash, "supervisor", ",".join(permissions)))
                                
                                conn.commit()
                                st.success(f"✅ تم إضافة المشرف {new_admin_name} بنجاح")
                                # إعادة تعيين حالة النموذج
                                st.session_state.show_admin_form = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ حدث خطأ أثناء إضافة المشرف: {str(e)}")
                            finally:
                                conn.close()

        # تبويب إدارة المشرفين الحاليين
        with tab2:
            st.subheader("🔄 إدارة المشرفين الحاليين")
            
            # جلب قائمة المشرفين الحاليين
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # استثناء المستخدم الحالي من القائمة
            cursor.execute('''
            SELECT id, username, email, admin_role, admin_permissions 
            FROM users WHERE is_admin = 1 AND id != ? ORDER BY username
            ''', (user['id'],))
            
            admins = cursor.fetchall()
            
            if not admins:
                st.info("📭 لا يوجد مشرفون إضافيون حالياً")
            else:
                # إنشاء قائمة منسدلة لاختيار المشرف
                admin_options = [(admin[0], f"{admin[1]} ({admin[2]})" if admin[2] else admin[1]) for admin in admins]
                selected_admin_id = st.selectbox(
                    "اختر المشرف للإدارة",
                    options=[admin[0] for admin in admin_options],
                    format_func=lambda x: next((admin[1] for admin in admin_options if admin[0] == x), "غير معروف")
                )
                
                # الحصول على بيانات المشرف المحدد
                selected_admin = next((admin for admin in admins if admin[0] == selected_admin_id), None)
                
                if selected_admin:
                    admin_id, username, email, role, permissions_str = selected_admin
                    permissions_list = permissions_str.split(',') if permissions_str else []
                    
                    st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px;">
                        <h3 style="margin-top: 0; color: #334155; font-size: 1.2rem;">{username}</h3>
                        <div style="color: #64748b; margin-bottom: 10px;">{email if email else '(لا يوجد بريد إلكتروني)'}</div>
                        <div style="background: rgba(30, 60, 114, 0.1); display: inline-block; padding: 4px 10px; border-radius: 30px; font-size: 0.85rem; color: #1e3c72;">{role if role else 'بدون دور محدد'}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # تعديل الصلاحيات
                    st.subheader("تعديل الصلاحيات")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        manage_users = st.checkbox("إدارة المستخدمين", value="users" in permissions_list, key="edit_perm_users_"+str(admin_id))
                        manage_reports = st.checkbox("إدارة التقارير", value="reports" in permissions_list, key="edit_perm_reports_"+str(admin_id))
                    
                    with col2:
                        manage_admins = st.checkbox("إدارة المشرفين", value="admins" in permissions_list, key="edit_perm_admins_"+str(admin_id))
                        can_backup = st.checkbox("النسخ الاحتياطي", value="backup" in permissions_list, key="edit_perm_backup_"+str(admin_id))
                    
                    if st.button("💾 تحديث الصلاحيات", key="update_perms_"+str(admin_id)):
                        # تجميع الصلاحيات الجديدة
                        new_permissions = []
                        if manage_users:
                            new_permissions.append("users")
                        if manage_reports:
                            new_permissions.append("reports")
                        if manage_admins:
                            new_permissions.append("admins")
                        if can_backup:
                            new_permissions.append("backup")
                        
                        # تحديث الصلاحيات في قاعدة البيانات
                        cursor.execute(
                            "UPDATE users SET admin_permissions = ? WHERE id = ?",
                            (",".join(new_permissions), admin_id)
                        )
                        conn.commit()
                        st.success("✅ تم تحديث الصلاحيات بنجاح")
                        st.rerun()
                    
                    # خيارات إضافية
                    st.subheader("خيارات إضافية")
                    col_actions1, col_actions2 = st.columns(2)
                    
                    with col_actions1:
                        if st.button("🔄 إعادة تعيين كلمة المرور", key="reset_pass_"+str(admin_id), use_container_width=True):
                            # إنشاء كلمة مرور عشوائية
                            import random
                            import string
                            
                            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                            password_hash = hash_password(temp_password)
                            
                            cursor.execute(
                                "UPDATE users SET password_hash = ? WHERE id = ?",
                                (password_hash, admin_id)
                            )
                            conn.commit()
                            st.success(f"✅ تم إعادة تعيين كلمة المرور بنجاح. كلمة المرور المؤقتة هي: **{temp_password}**")
                    
                    with col_actions2:
                        if st.button("❌ حذف المشرف", key="delete_admin_"+str(admin_id), use_container_width=True):
                            if st.text_input("اكتب 'تأكيد' للمتابعة:", key="confirm_delete_"+str(admin_id)) == "تأكيد":
                                cursor.execute("DELETE FROM users WHERE id = ?", (admin_id,))
                                conn.commit()
                                st.success(f"✅ تم حذف المشرف {username} بنجاح")
                                st.rerun()
            
            # إغلاق الاتصال بقاعدة البيانات
            conn.close()
    
    # إعدادات المدير
    st.markdown("""
    <div style="background: linear-gradient(120deg, #f8fafc, #e5e7eb); border-radius: 12px; padding: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 30px;">
        <h3 style="margin-top: 0; color: #334155; font-weight: 600; font-size: 1.3rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 15px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
            <span style="background: #1e3c72; color: white; width: 32px; height: 32px; display: flex; justify-content: center; align-items: center; border-radius: 50%; font-size: 1rem;">👑</span>
            حساب المدير
        </h3>
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="min-width: 120px; color: #64748b; font-weight: 600;">اسم المستخدم:</div>
                <div style="font-weight: 600; color: #334155; background: #f8fafc; padding: 8px 15px; border-radius: 6px; flex-grow: 1;">{}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="min-width: 120px; color: #64748b; font-weight: 600;">البريد الإلكتروني:</div>
                <div style="font-weight: 600; color: #334155; background: #f8fafc; padding: 8px 15px; border-radius: 6px; flex-grow: 1;">{}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="min-width: 120px; color: #64748b; font-weight: 600;">الصلاحية:</div>
                <div style="font-weight: 600; color: #0f2350; background: rgba(30, 60, 114, 0.1); padding: 8px 15px; border-radius: 6px; display: inline-block;">{}</div>
            </div>
        </div>
    </div>
    """.format(user['username'], user['email'], "مدير النظام" if not user.get('admin_role') or user['admin_role'] == 'none' else (user['admin_role'])), unsafe_allow_html=True)
    
    # عرض الصلاحيات للمشرفين
    if user.get('admin_permissions') and user['admin_role'] != 'none' and user['is_admin']:
        st.markdown("""<div style="margin-top: 15px; margin-bottom: 25px;">
            <h4 style="margin-top: 0; font-size: 1.1rem; color: #475569;">الصلاحيات الممنوحة:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px;">
                {}
            </div>
        </div>""".format(
            ''.join([f'<span style="background: #f1f5f9; padding: 5px 10px; border-radius: 20px; font-size: 0.85rem; color: #334155;">{get_permission_name(perm)}</span>' for perm in user.get('admin_permissions', [])])
        ), unsafe_allow_html=True)
    
    # تعديل بيانات المدير
    col_admin1, col_admin2 = st.columns(2)
    
    # تعديل اسم المستخدم
    with col_admin1:
        st.subheader("✏️ تعديل اسم المستخدم")
        
        with st.form("تعديل_اسم_المدير"):
            new_admin_username = st.text_input("اسم المستخدم الجديد", value=user['username'], key="admin_username")
            admin_username_submit = st.form_submit_button("تحديث اسم المستخدم", type="primary")
            
            if admin_username_submit and new_admin_username != user['username']:
                if not new_admin_username or len(new_admin_username) < 3:
                    st.error("⚠️ يجب أن يحتوي اسم المستخدم على 3 أحرف على الأقل")
                else:
                    # التحقق من أن اسم المستخدم غير مستخدم
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (new_admin_username, user['id']))
                    if cursor.fetchone():
                        st.error("⚠️ اسم المستخدم مستخدم بالفعل، يرجى اختيار اسم آخر.")
                    else:
                        # تحديث اسم المستخدم
                        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_admin_username, user['id']))
                        conn.commit()
                        conn.close()
                        
                        # تحديث معلومات المستخدم في الجلسة
                        st.session_state.user['username'] = new_admin_username
                        st.success("✅ تم تحديث اسم المستخدم بنجاح.")
                        st.rerun()
    
    # تغيير كلمة المرور
    with col_admin2:
        st.subheader("🔐 تغيير كلمة المرور")
        
        with st.form("تغيير_كلمة_المرور_المدير"):
            new_admin_password = st.text_input("كلمة المرور الجديدة", type="password", key="admin_password")
            confirm_admin_password = st.text_input("تأكيد كلمة المرور الجديدة", type="password", key="admin_confirm")
            admin_password_submit = st.form_submit_button("تغيير كلمة المرور", type="primary")
            
            if admin_password_submit:
                if not new_admin_password or not confirm_admin_password:
                    st.error("⚠️ يرجى ملء جميع الحقول.")
                elif new_admin_password != confirm_admin_password:
                    st.error("⚠️ كلمات المرور الجديدة غير متطابقة.")
                elif len(new_admin_password) < 6:
                    st.error("⚠️ كلمة المرور الجديدة يجب أن تحتوي على 6 أحرف على الأقل.")
                else:
                    # تحديث كلمة المرور
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    new_password_hash = hash_password(new_admin_password)
                    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", 
                                  (new_password_hash, user['id']))
                    conn.commit()
                    conn.close()
                    st.success("✅ تم تغيير كلمة المرور بنجاح.")
    
    st.markdown("---")
    
    # إدارة قاعدة البيانات
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗄️ إدارة قاعدة البيانات")
        
        if st.button("💾 إنشاء نسخة احتياطية", use_container_width=True):
            try:
                from enhancements import backup_database
                backup_file = backup_database()
                if backup_file:
                    st.success(f"✅ تم إنشاء نسخة احتياطية: {backup_file}")
                else:
                    st.error("❌ فشل في إنشاء النسخة الاحتياطية")
            except ImportError:
                st.error("❌ دالة النسخ الاحتياطي غير متوفرة")
        
        if st.button("🔧 تحسين قاعدة البيانات", use_container_width=True):
            try:
                from enhancements import optimize_database
                optimize_database()
                st.success("✅ تم تحسين قاعدة البيانات بنجاح")
            except ImportError:
                st.error("❌ دالة التحسين غير متوفرة")
    
    with col2:
        st.subheader("📊 معلومات النظام")
        
        # معلومات قاعدة البيانات
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM reports")
        reports_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM trades")
        trades_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        conn.close()
        
        st.info(f"""
        **📊 إحصائيات قاعدة البيانات:**
        - التقارير: {reports_count}
        - الصفقات: {trades_count}
        - المستخدمين: {users_count}
        
        **💾 معلومات الملف:**
        - حجم قاعدة البيانات: {os.path.getsize(DB_NAME) / 1024:.2f} KB
        """)

def display_statistics_tab():
    """عرض تبويب الإحصائيات للمستخدمين العاديين"""
    # عنوان محسن
    st.markdown("""
    <div style="background: linear-gradient(120deg, #1e3c72, #2a5298); border-radius: 12px; padding: 16px 20px; margin-bottom: 25px; box-shadow: 0 5px 15px rgba(30, 60, 114, 0.2); color: white; text-align: center;">
        <h2 style="margin: 0; font-weight: 700; font-size: 1.8rem; text-shadow: 0 2px 3px rgba(0,0,0,0.1);">📊 الإحصائيات والتحليلات</h2>
        <div style="width: 50px; height: 3px; background: white; margin: 10px auto 0; border-radius: 50px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    reports = get_reports()
    
    if not reports:
        st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; padding: 40px 0; background: white; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin: 20px 0;">
            <div style="font-size: 4rem; margin-bottom: 20px; opacity: 0.6;">📭</div>
            <h3 style="margin-bottom: 10px; color: #334155; font-weight: 600;">لا توجد بيانات إحصائية متاحة</h3>
            <p style="color: #64748b; max-width: 400px; text-align: center;">سيتم عرض الإحصائيات فور توفر التقارير.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # إحصائيات عامة محسنة
    total_symbols = sum(r['total_symbols'] for r in reports)
    total_buy = sum(r['buy_recommendations'] for r in reports)
    total_sell = sum(r['sell_recommendations'] for r in reports)
    avg_confidence = sum(r['avg_confidence'] for r in reports) / len(reports)
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px;">
        <div class="metric-card">
            <div style="position: absolute; top: -15px; right: -10px; background: #f3f4f6; border-radius: 50%; width: 36px; height: 36px; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-size: 18px;">📈</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 8px;">إجمالي الرموز</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: #0f2350;">{}</div>
        </div>
        <div class="metric-card">
            <div style="position: absolute; top: -15px; right: -10px; background: rgba(16, 185, 129, 0.15); border-radius: 50%; width: 36px; height: 36px; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 5px rgba(16, 185, 129, 0.2); font-size: 18px;">🟢</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 8px;">توصيات الشراء</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: #047857;">{}</div>
        </div>
        <div class="metric-card">
            <div style="position: absolute; top: -15px; right: -10px; background: rgba(239, 68, 68, 0.15); border-radius: 50%; width: 36px; height: 36px; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 5px rgba(239, 68, 68, 0.2); font-size: 18px;">🔴</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 8px;">توصيات البيع</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: #b91c1c;">{}</div>
        </div>
        <div class="metric-card">
            <div style="position: absolute; top: -15px; right: -10px; background: rgba(37, 99, 235, 0.15); border-radius: 50%; width: 36px; height: 36px; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 5px rgba(37, 99, 235, 0.2); font-size: 18px;">🎯</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 8px;">متوسط الثقة</div>
            <div style="font-size: 2.1rem; font-weight: 800; color: #1e40af;">{:.1f}%</div>
        </div>
    </div>
    """.format(total_symbols, total_buy, total_sell, avg_confidence), unsafe_allow_html=True)
    
    # رسوم بيانية محسنة
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 15px rgba(0,0,0,0.05); margin-bottom: 15px;">
            <h3 style="margin-top: 0; color: #334155; font-weight: 600; font-size: 1.2rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 10px;">
                <span style="margin-right: 8px;">📊</span>
                توزيع التوصيات
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        pie_data = {
            TYPE_LABEL: ['شراء', 'بيع', 'محايد'],
            'العدد': [total_buy, total_sell, total_symbols - total_buy - total_sell]
        }
        df_pie = pd.DataFrame(pie_data)
        st.bar_chart(df_pie.set_index(TYPE_LABEL))
    
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 15px rgba(0,0,0,0.05); margin-bottom: 15px;">
            <h3 style="margin-top: 0; color: #334155; font-weight: 600; font-size: 1.2rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 10px;">
                <span style="margin-right: 8px;">📈</span>
                تطور الثقة عبر الزمن
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        if len(reports) >= 5:
            confidence_data = {
                'التقرير': [f"تقرير {i+1}" for i in range(min(10, len(reports)))],
                'الثقة': [r['avg_confidence'] for r in reports[:10]]
            }
            df_confidence = pd.DataFrame(confidence_data)
            st.line_chart(df_confidence.set_index('التقرير'))
        else:
            st.markdown("""
            <div style="padding: 20px; text-align: center; background: #f8fafc; border-radius: 8px; border: 1px dashed #cbd5e1; margin-top: 10px;">
                <div style="font-size: 2rem; margin-bottom: 10px; opacity: 0.6;">⚠️</div>
                <p style="color: #64748b; margin: 0;">يحتاج إلى 5 تقارير على الأقل لعرض الرسم البياني</p>
            </div>
            """, unsafe_allow_html=True)
            
    # إضافة قسم جديد للمؤشرات المالية
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(120deg, #f8fafc, #e5e7eb); border-radius: 12px; padding: 20px; box-shadow: 0 3px 10px rgba(0,0,0,0.03); margin: 10px 0 25px; border: 1px solid #e2e8f0;">
        <h3 style="margin-top: 0; color: #334155; font-weight: 600; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;">
            <span style="background: #1e3c72; color: white; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center; border-radius: 50%; font-size: 1rem;">💹</span>
            المؤشرات والتنبؤات المالية
        </h3>
        <div style="display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px;">
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.05); min-width: 180px; text-align: center; border: 1px solid #e5e7eb;">
                <div style="font-size: 2rem; margin-bottom: 10px; background: linear-gradient(120deg, #0891b2, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📈</div>
                <div style="color: #334155; font-weight: 600; font-size: 1.1rem; margin-bottom: 5px;">مؤشر السوق</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #0891b2;">+1.2%</div>
            </div>
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.05); min-width: 180px; text-align: center; border: 1px solid #e5e7eb;">
                <div style="font-size: 2rem; margin-bottom: 10px; background: linear-gradient(120deg, #10b981, #059669); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">💰</div>
                <div style="color: #334155; font-weight: 600; font-size: 1.1rem; margin-bottom: 5px;">عائد الاستثمار</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #10b981;">14.8%</div>
            </div>
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.05); min-width: 180px; text-align: center; border: 1px solid #e5e7eb;">
                <div style="font-size: 2rem; margin-bottom: 10px; background: linear-gradient(120deg, #8b5cf6, #6d28d9); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📏</div>
                <div style="color: #334155; font-weight: 600; font-size: 1.1rem; margin-bottom: 5px;">دقة التوقعات</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #8b5cf6;">82%</div>
            </div>
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.05); min-width: 180px; text-align: center; border: 1px solid #e5e7eb;">
                <div style="font-size: 2rem; margin-bottom: 10px; background: linear-gradient(120deg, #f59e0b, #d97706); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">⚡</div>
                <div style="color: #334155; font-weight: 600; font-size: 1.1rem; margin-bottom: 5px;">مؤشر النشاط</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #f59e0b;">9.5</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_user_settings_tab():
    # Obtener el usuario actual desde la sesión
    user = st.session_state.user
    
    # Crear columnas para el diseño
    col1, col2 = st.columns(2)
    
    # تعديل اسم المستخدم
    with col1:
        st.subheader("✏️ تعديل اسم المستخدم")
        
        with st.form("تعديل_اسم_المدير"):
            new_admin_username = st.text_input("اسم المستخدم الجديد", value=user['username'], key="admin_username")
            admin_username_submit = st.form_submit_button("تحديث اسم المستخدم", type="primary")
            
            if admin_username_submit and new_admin_username != user['username']:
                if not new_admin_username or len(new_admin_username) < 3:
                    st.error("⚠️ يجب أن يحتوي اسم المستخدم على 3 أحرف على الأقل")
                else:
                    # التحقق من أن اسم المستخدم غير مستخدم
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (new_admin_username, user['id']))
                    if cursor.fetchone():
                        st.error("⚠️ اسم المستخدم مستخدم بالفعل، يرجى اختيار اسم آخر.")
                    else:
                        # تحديث اسم المستخدم
                        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_admin_username, user['id']))
                        conn.commit()
                        conn.close()
                        
                        # تحديث معلومات المستخدم في الجلسة
                        st.session_state.user['username'] = new_admin_username
                        st.success("✅ تم تحديث اسم المستخدم بنجاح.")
                        st.rerun()
    
    # تغيير كلمة المرور
    with col2:
        st.subheader("🔐 تغيير كلمة المرور")
        
        with st.form("تغيير_كلمة_المرور_المدير"):
            new_admin_password = st.text_input("كلمة المرور الجديدة", type="password", key="admin_password")
            confirm_admin_password = st.text_input("تأكيد كلمة المرور الجديدة", type="password", key="admin_confirm")
            admin_password_submit = st.form_submit_button("تغيير كلمة المرور", type="primary")
            
            if admin_password_submit:
                if not new_admin_password or not confirm_admin_password:
                    st.error("⚠️ يرجى ملء جميع الحقول.")
                elif new_admin_password != confirm_admin_password:
                    st.error("⚠️ كلمات المرور الجديدة غير متطابقة.")
                elif len(new_admin_password) < 6:
                    st.error("⚠️ كلمة المرور الجديدة يجب أن تحتوي على 6 أحرف على الأقل.")
                else:
                    # تحديث كلمة المرور
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    new_password_hash = hash_password(new_admin_password)
                    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", 
                                  (new_password_hash, user['id']))
                    conn.commit()
                    conn.close()
                    st.success("✅ تم تغيير كلمة المرور بنجاح.")
    
    # إدارة المشرفين والصلاحيات
    st.header("👥 إدارة المشرفين والصلاحيات")
    
    # عرض معلومات تشخيصية
    st.write("معلومات المستخدم الحالي:")
    st.write(f"نوع المستخدم: {'مدير' if user['is_admin'] else 'مستخدم عادي'}")
    st.write(f"دور المدير: {user.get('admin_role', 'none')}")
    st.write(f"الصلاحيات: {', '.join(user.get('admin_permissions', []))}")
    
    # نسمح لجميع المديرين بإضافة مشرفين
    if user['is_admin']:  # أي مدير
        st.success("👑 يمكنك إضافة مشرفين جدد")
        with st.expander("➕ إضافة مشرف جديد"):
            col_new1, col_new2 = st.columns(2)
            
            with col_new1:
                with st.form("إضافة_مشرف_جديد"):
                    new_admin_name = st.text_input("اسم المستخدم", key="new_admin_name")
                    new_admin_email = st.text_input("البريد الإلكتروني", key="new_admin_email")
                    new_admin_password = st.text_input("كلمة المرور", type="password", key="new_admin_password")
                    
                    # تحديد الصلاحيات
                    st.write("تحديد الصلاحيات:")
                    can_manage_users = st.checkbox("إدارة المستخدمين", value=True, key="perm_users")
                    can_manage_reports = st.checkbox("إدارة التقارير", value=True, key="perm_reports")
                    can_manage_admins = st.checkbox("إدارة المشرفين", key="perm_admins")
                    can_backup = st.checkbox("النسخ الاحتياطي", key="perm_backup")
                    
                    submit_new_admin = st.form_submit_button("إضافة مشرف", type="primary")
                    
                    if submit_new_admin:
                        if not new_admin_name or not new_admin_email or not new_admin_password:
                            st.error("⚠️ يرجى ملء جميع الحقول المطلوبة")
                        elif len(new_admin_password) < 6:
                            st.error("⚠️ كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                        else:
                            conn = sqlite3.connect(DB_NAME)
                            cursor = conn.cursor()
                            
                            # التحقق من وجود اسم المستخدم أو البريد الإلكتروني
                            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (new_admin_name, new_admin_email))
                            if cursor.fetchone():
                                st.error("⚠️ اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل")
                            else:
                                # إنشاء مصفوفة الصلاحيات
                                permissions = []
                                if can_manage_users:
                                    permissions.append("users")
                                if can_manage_reports:
                                    permissions.append("reports")
                                if can_manage_admins:
                                    permissions.append("admins")
                                if can_backup:
                                    permissions.append("backup")
                                
                                # إضافة المشرف الجديد
                                try:
                                    password_hash = hash_password(new_admin_password)
                                    cursor.execute('''
                                    INSERT INTO users (username, email, password_hash, is_admin, admin_role, admin_permissions)
                                    VALUES (?, ?, ?, 1, ?, ?)
                                    ''', (new_admin_name, new_admin_email, password_hash, "supervisor", ",".join(permissions)))
                                    
                                    conn.commit()
                                    st.success(f"✅ تم إضافة المشرف {new_admin_name} بنجاح")
                                except Exception as e:
                                    st.error(f"❌ حدث خطأ أثناء إضافة المشرف: {str(e)}")
                                finally:
                                    conn.close()
            
            with col_new2:
                # عرض المشرفين الحاليين
                st.subheader("المشرفون الحاليون")
                
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                
                cursor.execute('''
                SELECT id, username, email, admin_role, admin_permissions 
                FROM users WHERE is_admin = 1 AND id != ? ORDER BY username
                ''', (user['id'],))
                
                admins = cursor.fetchall()
                conn.close()
                
                if admins:
                    for admin in admins:
                        with st.container():
                            st.markdown(f'''
                            <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <div style="font-weight: 600; font-size: 1.1rem;">{admin[1]}</div>
                                        <div style="color: #64748b; font-size: 0.9rem;">{admin[2]}</div>
                                    </div>
                                    <div style="background: rgba(30, 60, 114, 0.1); padding: 4px 10px; border-radius: 30px; font-size: 0.8rem; color: #1e3c72;">{admin[3]}</div>
                                </div>
                                <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 5px;">
                                    {' '.join([f'<span style="background: #f1f5f9; padding: 3px 8px; border-radius: 20px; font-size: 0.8rem; color: #334155;">{perm}</span>' for perm in (admin[4].split(',') if admin[4] else [])])}
                                </div>
                            </div>
                            ''', unsafe_allow_html=True)
                else:
                    st.info("لا يوجد مشرفون إضافيون حالياً")
        
        with st.expander("🔄 إدارة المشرفين الحاليين"):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, username FROM users WHERE is_admin = 1 AND id != ? ORDER BY username
            ''', (user['id'],))
            
            admin_options = cursor.fetchall()
            
            if admin_options:
                selected_admin_id = st.selectbox(
                    "اختر المشرف", 
                    options=[admin[0] for admin in admin_options],
                    format_func=lambda x: next((admin[1] for admin in admin_options if admin[0] == x), "غير معروف")
                )
                
                # الحصول على تفاصيل المشرف المحدد
                cursor.execute('''
                SELECT username, email, admin_role, admin_permissions 
                FROM users WHERE id = ?
                ''', (selected_admin_id,))
                
                selected_admin = cursor.fetchone()
                
                if selected_admin:
                    username, email, role, permissions = selected_admin
                    permissions_list = permissions.split(',') if permissions else []
                    
                    col_edit1, col_edit2 = st.columns(2)
                    
                    with col_edit1:
                        st.write("تعديل الصلاحيات:")
                        
                        new_can_manage_users = st.checkbox("إدارة المستخدمين", value="users" in permissions_list, key="edit_perm_users")
                        new_can_manage_reports = st.checkbox("إدارة التقارير", value="reports" in permissions_list, key="edit_perm_reports")
                        new_can_manage_admins = st.checkbox("إدارة المشرفين", value="admins" in permissions_list, key="edit_perm_admins")
                        new_can_backup = st.checkbox("النسخ الاحتياطي", value="backup" in permissions_list, key="edit_perm_backup")
                        
                        if st.button("تحديث الصلاحيات", type="primary"):
                            new_permissions = []
                            if new_can_manage_users:
                                new_permissions.append("users")
                            if new_can_manage_reports:
                                new_permissions.append("reports")
                            if new_can_manage_admins:
                                new_permissions.append("admins")
                            if new_can_backup:
                                new_permissions.append("backup")
                            
                            cursor.execute(
                                "UPDATE users SET admin_permissions = ? WHERE id = ?",
                                (",".join(new_permissions), selected_admin_id)
                            )
                            conn.commit()
                            st.success("✅ تم تحديث الصلاحيات بنجاح")
                            st.rerun()
                    
                    with col_edit2:
                        if st.button("🔄 إعادة تعيين كلمة المرور", use_container_width=True):
                            # إنشاء كلمة مرور عشوائية
                            import random
                            import string
                            
                            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                            password_hash = hash_password(temp_password)
                            
                            cursor.execute(
                                "UPDATE users SET password_hash = ? WHERE id = ?",
                                (password_hash, selected_admin_id)
                            )
                            conn.commit()
                            st.success(f"✅ تم إعادة تعيين كلمة المرور بنجاح. كلمة المرور المؤقتة هي: **{temp_password}**")
                        
                        if st.button("❌ إزالة المشرف", use_container_width=True):
                            confirm = st.text_input("اكتب 'تأكيد' للمتابعة:", key="confirm_admin_delete")
                            if confirm == "تأكيد":
                                cursor.execute("DELETE FROM users WHERE id = ?", (selected_admin_id,))
                                conn.commit()
                                st.success(f"✅ تم حذف المشرف {username} بنجاح")
                                st.rerun()
            else:
                st.info("لا يوجد مشرفون إضافيون لإدارتهم")
            
            conn.close()
    
    # إعدادات النظام العامة
    st.header("🛠️ إعدادات النظام العامة")
    
    with st.expander("💾 النسخ الاحتياطي واستعادة البيانات"):
        col_backup1, col_backup2 = st.columns(2)
        
        with col_backup1:
            if st.button("📤 إنشاء نسخة احتياطية", use_container_width=True):
                # إنشاء نسخة احتياطية من قاعدة البيانات
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"trading_recommendations_backup_{now}.db"
                
                try:
                    import shutil
                    shutil.copy(DB_NAME, backup_file)
                    st.success(f"✅ تم إنشاء نسخة احتياطية بنجاح: {backup_file}")
                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء إنشاء النسخة الاحتياطية: {str(e)}")
        
        with col_backup2:
            st.download_button(
                label="📥 تحميل قاعدة البيانات الحالية",
                data=open(DB_NAME, "rb").read(),
                file_name=f"trading_recommendations_{datetime.datetime.now().strftime('%Y%m%d')}.db",
                mime="application/octet-stream",
                use_container_width=True
            )
    
    with st.expander("🧹 تنظيف قاعدة البيانات"):
        st.warning("⚠️ هذه العمليات تؤثر على البيانات، يرجى التأكد من إنشاء نسخة احتياطية قبل المتابعة.")
        
        col_clean1, col_clean2 = st.columns(2)
        
        with col_clean1:
            if st.button("🗑️ حذف التقارير القديمة", use_container_width=True):
                # حذف التقارير الأقدم من 6 أشهر
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM reports WHERE upload_time < date('now', '-6 months')")
                deleted = cursor.rowcount
                conn.commit()
                conn.close()
                st.info(f"تم حذف {deleted} تقارير قديمة")
        
        with col_clean2:
            if st.button("🔄 إعادة تعيين محاولات تسجيل الدخول", use_container_width=True):
                # إعادة تعيين محاولات تسجيل الدخول
                if 'login_attempts' in st.session_state:
                    st.session_state.login_attempts = {}
                    st.info("✅ تم إعادة تعيين محاولات تسجيل الدخول بنجاح")
                else:
                    st.info("لا توجد محاولات تسجيل دخول مسجلة")

def display_regular_user_settings_tab():
    """عرض تبويب إعدادات الحساب للمستخدمين العاديين"""
    st.header("👤 إعدادات الحساب")
    
    user = st.session_state.user
    
    # عرض معلومات المستخدم الحالية
    st.markdown("""
    <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 30px;">
        <h3 style="margin-top: 0; color: #334155; font-weight: 600; font-size: 1.3rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 15px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
            <span style="background: #1e3c72; color: white; width: 32px; height: 32px; display: flex; justify-content: center; align-items: center; border-radius: 50%; font-size: 1rem;">👤</span>
            معلومات الحساب
        </h3>
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="min-width: 120px; color: #64748b; font-weight: 600;">اسم المستخدم:</div>
                <div style="font-weight: 600; color: #334155; background: #f8fafc; padding: 8px 15px; border-radius: 6px; flex-grow: 1;">{}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="min-width: 120px; color: #64748b; font-weight: 600;">البريد الإلكتروني:</div>
                <div style="font-weight: 600; color: #334155; background: #f8fafc; padding: 8px 15px; border-radius: 6px; flex-grow: 1;">{}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="min-width: 120px; color: #64748b; font-weight: 600;">نوع الاشتراك:</div>
                <div style="font-weight: 600; color: #{}; background: rgba({}, 0.1); padding: 8px 15px; border-radius: 6px; display: inline-block;">{}</div>
            </div>
        </div>
    </div>
    """.format(
        user['username'],
        user['email'],
        "10b981" if user['subscription_type'] == 'premium' else "f59e0b",
        "16, 185, 129" if user['subscription_type'] == 'premium' else "245, 158, 11",
        "مميز" if user['subscription_type'] == 'premium' else "مجاني"
    ), unsafe_allow_html=True)
    
    # تعديل اسم المستخدم
    st.subheader("✏️ تعديل اسم المستخدم")
    
    with st.form("تعديل_اسم_المستخدم"):
        new_username = st.text_input("اسم المستخدم الجديد", value=user['username'])
        username_submit = st.form_submit_button("تحديث اسم المستخدم", type="primary")
        
        if username_submit and new_username != user['username']:
            # التحقق من أن اسم المستخدم غير مستخدم
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (new_username, user['id']))
            if cursor.fetchone():
                st.error("⚠️ اسم المستخدم مستخدم بالفعل، يرجى اختيار اسم آخر.")
            else:
                # تحديث اسم المستخدم
                cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user['id']))
                conn.commit()
                conn.close()
                
                # تحديث معلومات المستخدم في الجلسة
                st.session_state.user['username'] = new_username
                st.success("✅ تم تحديث اسم المستخدم بنجاح.")
                st.rerun()
    
    # تغيير كلمة المرور
    st.subheader("🔐 تغيير كلمة المرور")
    
    with st.form("تغيير_كلمة_المرور"):
        new_password = st.text_input("كلمة المرور الجديدة", type="password")
        confirm_password = st.text_input("تأكيد كلمة المرور الجديدة", type="password")
        password_submit = st.form_submit_button("تغيير كلمة المرور", type="primary")
        
        if password_submit:
            if not new_password or not confirm_password:
                st.error("⚠️ يرجى ملء جميع الحقول.")
            elif new_password != confirm_password:
                st.error("⚠️ كلمات المرور الجديدة غير متطابقة.")
            elif len(new_password) < 6:
                st.error("⚠️ كلمة المرور الجديدة يجب أن تحتوي على 6 أحرف على الأقل.")
            else:
                # تحديث كلمة المرور مباشرة
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                new_password_hash = hash_password(new_password)
                cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", 
                              (new_password_hash, user['id']))
                conn.commit()
                conn.close()
                st.success("✅ تم تغيير كلمة المرور بنجاح.")

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