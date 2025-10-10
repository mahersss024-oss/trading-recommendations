#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة نظام تبديل الثيم للتطبيق
"""

def add_theme_switcher():
    """إضافة أداة تبديل الثيم إلى الشريط الجانبي"""
    
    with st.sidebar:
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
            st.info("🌞 الوضع الحالي: لايت ثيم")
        else:
            st.info("🌙 الوضع الحالي: دارك ثيم")

def apply_enhanced_css():
    """تطبيق CSS محسن مع دعم تبديل الثيم"""
    
    theme = st.session_state.get('theme_mode', 'light')
    
    if theme == 'light':
        # Light Theme
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700;800;900&display=swap');

        .stApp {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
        }

        /* تحسين النصوص - لايت ثيم */
        .stMarkdown, .stText {
            color: #1e293b !important;
            font-size: 1.1rem !important;
            direction: rtl !important;
            text-align: right !important;
            line-height: 1.7 !important;
            font-weight: 500 !important;
        }

        /* العنوان الرئيسي */
        .main-header {
            font-size: 3.5rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 2rem;
            padding: 1.5rem 0;
            color: #1e40af;
            text-shadow: 0 2px 8px rgba(30, 64, 175, 0.1);
            direction: rtl;
            line-height: 1.4;
        }

        /* البطاقات */
        .metric-card {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
            border-color: #3b82f6;
        }

        /* الشريط الجانبي */
        div[data-testid="stSidebarContent"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
        }

        /* الأزرار */
        button[kind="primary"] {
            background: linear-gradient(120deg, #3b82f6, #1d4ed8) !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            transition: all 0.2s ease !important;
        }

        button[kind="primary"]:hover {
            background: linear-gradient(120deg, #2563eb, #1e40af) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        }

        /* التبويبات */
        div[data-testid="stTabsCtrlWrapper"] button[role="tab"] {
            font-weight: 700;
            font-size: 1.1rem;
            border-radius: 8px 8px 0 0;
            padding: 12px 20px !important;
            color: #475569 !important;
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            transition: all 0.3s ease;
        }

        div[data-testid="stTabsCtrlWrapper"] button[role="tab"][aria-selected="true"] {
            background-color: #ffffff !important;
            color: #1e40af !important;
            border-color: #3b82f6 !important;
            font-weight: 800;
        }

        /* النماذج والإدخالات */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #ffffff !important;
            border: 1px solid #d1d5db !important;
            border-radius: 6px !important;
            color: #374151 !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }

        /* الجداول */
        .stDataFrame {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }

        /* الرسائل */
        .success-message {
            background-color: #f0fdf4;
            border: 1px solid #bbf7d0;
            color: #166534;
        }

        .error-message {
            background-color: #fef2f2;
            border: 1px solid #fecaca;
            color: #dc2626;
        }
        </style>
        """, unsafe_allow_html=True)
    
    else:
        # Dark Theme
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700;800;900&display=swap');

        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif !important;
        }

        /* تحسين النصوص - دارك ثيم */
        .stMarkdown, .stText {
            color: #f1f5f9 !important;
            font-size: 1.1rem !important;
            direction: rtl !important;
            text-align: right !important;
            line-height: 1.7 !important;
            font-weight: 500 !important;
        }

        /* العنوان الرئيسي */
        .main-header {
            font-size: 3.5rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 2rem;
            padding: 1.5rem 0;
            color: #60a5fa;
            text-shadow: 0 2px 8px rgba(96, 165, 250, 0.3);
            direction: rtl;
            line-height: 1.4;
        }

        /* البطاقات */
        .metric-card {
            background: #1f2937;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #374151;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            border-color: #60a5fa;
        }

        /* الشريط الجانبي */
        div[data-testid="stSidebarContent"] {
            background-color: #1f2937;
            border-right: 1px solid #374151;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
        }

        /* الأزرار */
        button[kind="primary"] {
            background: linear-gradient(120deg, #3b82f6, #1d4ed8) !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            transition: all 0.2s ease !important;
        }

        button[kind="primary"]:hover {
            background: linear-gradient(120deg, #2563eb, #1e40af) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
        }

        /* التبويبات */
        div[data-testid="stTabsCtrlWrapper"] button[role="tab"] {
            font-weight: 700;
            font-size: 1.1rem;
            border-radius: 8px 8px 0 0;
            padding: 12px 20px !important;
            color: #9ca3af !important;
            background-color: #374151 !important;
            border: 1px solid #4b5563 !important;
            transition: all 0.3s ease;
        }

        div[data-testid="stTabsCtrlWrapper"] button[role="tab"][aria-selected="true"] {
            background-color: #1f2937 !important;
            color: #60a5fa !important;
            border-color: #3b82f6 !important;
            font-weight: 800;
        }

        /* النماذج والإدخالات */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #374151 !important;
            border: 1px solid #4b5563 !important;
            border-radius: 6px !important;
            color: #f9fafb !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        }

        /* الجداول */
        .stDataFrame {
            background-color: #1f2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 8px !important;
        }

        .stDataFrame th {
            background-color: #374151 !important;
            color: #f9fafb !important;
        }

        .stDataFrame td {
            color: #e5e7eb !important;
            border-bottom: 1px solid #374151 !important;
        }

        /* الرسائل */
        .success-message {
            background-color: #064e3b;
            border: 1px solid #047857;
            color: #10b981;
        }

        .error-message {
            background-color: #7f1d1d;
            border: 1px solid #dc2626;
            color: #ef4444;
        }

        /* تحسين العناصر الأخرى */
        .stSelectbox label, .stTextInput label, .stTextArea label {
            color: #f9fafb !important;
        }

        .stRadio label {
            color: #f9fafb !important;
        }

        .stCheckbox label {
            color: #f9fafb !important;
        }
        </style>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    import streamlit as st
    
    # تهيئة الثيم
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'light'
    
    # تطبيق CSS
    apply_enhanced_css()
    
    # إضافة تبديل الثيم
    add_theme_switcher()
    
    print("✅ تم إضافة نظام تبديل الثيم بنجاح!")