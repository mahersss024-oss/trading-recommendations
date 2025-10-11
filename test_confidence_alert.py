#!/usr/bin/env python3
"""
اختبار عرض التنبيه الجديد في صفحة التوصيات
"""

import streamlit as st
import pandas as pd

def test_confidence_alert():
    """اختبار عرض تنبيه مستوى الثقة"""
    
    st.set_page_config(
        page_title="اختبار تنبيه الثقة",
        page_icon="⚠️",
        layout="wide"
    )
    
    st.title("🧪 اختبار تنبيه مستوى الثقة")
    
    # بيانات توضيحية للاختبار
    demo_data = [
        {"الرمز": "AAPL", "السعر": "$185.92", "التوصية": "🟢 شراء", "الثقة %": "78.5%", "وقف الخسارة": "$180.25", "هدف الربح": "$197.50", "نسبة ر/م": "3.20"},
        {"الرمز": "MSFT", "السعر": "$405.63", "التوصية": "🟢 شراء", "الثقة %": "82.1%", "وقف الخسارة": "$395.75", "هدف الربح": "$425.30", "نسبة ر/م": "2.95"},
        {"الرمز": "TSLA", "السعر": "$215.75", "التوصية": "🔴 بيع", "الثقة %": "67.8%", "وقف الخسارة": "$225.50", "هدف الربح": "$195.80", "نسبة ر/م": "2.50"},
        {"الرمز": "AMZN", "السعر": "$178.35", "التوصية": "🟢 شراء", "الثقة %": "75.2%", "وقف الخسارة": "$172.60", "هدف الربح": "$192.40", "نسبة ر/م": "3.10"}
    ]
    
    df = pd.DataFrame(demo_data)
    
    st.subheader("📊 جدول التوصيات التوضيحي")
    st.dataframe(df, use_container_width=True)
    
    # التنبيه الجديد
    st.markdown("""
    <div style="background: linear-gradient(120deg, #fef3c7, #fcd34d); border: 2px solid #f59e0b; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="font-size: 2rem; margin-right: 15px;">⚠️</div>
            <h4 style="margin: 0; color: #92400e; font-weight: 700; font-size: 1.3rem;">تنبيه مهم حول مستوى الثقة</h4>
        </div>
        <div style="color: #92400e; font-size: 1.1rem; line-height: 1.8; margin-bottom: 15px;">
            <strong>📊 التوصيات ذات الثقة فوق 70% مناسبة للتداول</strong>
        </div>
        <div style="background: rgba(146, 64, 14, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <div style="color: #92400e; font-size: 1rem; line-height: 1.7;">
                🎯 <strong>كلما ارتفعت نسبة الثقة، كلما زادت فرصة نجاح الصفقة</strong><br>
                📈 <strong>70% - 80%:</strong> فرصة جيدة للنجاح<br>
                🔥 <strong>80% - 90%:</strong> فرصة عالية للنجاح<br>
                ⭐ <strong>فوق 90%:</strong> فرصة ممتازة للنجاح
            </div>
        </div>
        <div style="color: #dc2626; font-size: 0.95rem; font-weight: 600; text-align: center; background: rgba(220, 38, 38, 0.1); padding: 10px; border-radius: 6px;">
            ⚠️ تذكر: التداول ينطوي على مخاطر. يرجى إدارة المخاطر بعناية واستخدام وقف الخسارة
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ تم إضافة التنبيه بنجاح! سيظهر هذا التنبيه تحت جدول التوصيات في التطبيق الرئيسي.")

if __name__ == "__main__":
    test_confidence_alert()