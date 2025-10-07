import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3

def create_charts():
    """إنشاء الرسوم البيانية للتحليلات"""
    
    # جلب البيانات من قاعدة البيانات
    conn = sqlite3.connect('trading_recommendations.db')
    
    # إحصائيات التوصيات
    query = """
    SELECT 
        DATE(upload_time) as date,
        COUNT(*) as total_reports,
        AVG(avg_confidence) as avg_confidence,
        SUM(buy_recommendations) as total_buy,
        SUM(sell_recommendations) as total_sell
    FROM reports 
    GROUP BY DATE(upload_time)
    ORDER BY DATE(upload_time) DESC
    LIMIT 30
    """
    
    import pandas as pd
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        # رسم بياني لتطور الثقة
        fig_confidence = px.line(
            df, 
            x='date', 
            y='avg_confidence',
            title='تطور متوسط مستوى الثقة',
            labels={'avg_confidence': 'متوسط الثقة (%)', 'date': 'التاريخ'}
        )
        fig_confidence.update_layout(
            title_font_size=16,
            xaxis_title='التاريخ',
            yaxis_title='متوسط الثقة (%)'
        )
        
        # رسم بياني للتوصيات
        fig_recommendations = go.Figure()
        fig_recommendations.add_trace(go.Bar(
            x=df['date'],
            y=df['total_buy'],
            name='توصيات الشراء',
            marker_color='green'
        ))
        fig_recommendations.add_trace(go.Bar(
            x=df['date'],
            y=df['total_sell'],
            name='توصيات البيع',
            marker_color='red'
        ))
        
        fig_recommendations.update_layout(
            title='توزيع التوصيات عبر الزمن',
            xaxis_title='التاريخ',
            yaxis_title='عدد التوصيات',
            barmode='stack',
            title_font_size=16
        )
        
        return fig_confidence, fig_recommendations
    
    return None, None

def display_user_stats():
    """عرض إحصائيات المستخدمين"""
    conn = sqlite3.connect('trading_recommendations.db')
    
    # إحصائيات عامة
    cursor = conn.cursor()
    
    # عدد المستخدمين
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 0")
    total_users = cursor.fetchone()[0]
    
    # المستخدمين المشتركين
    cursor.execute("""
        SELECT COUNT(*) FROM users 
        WHERE is_admin = 0 AND subscription_type != 'free'
    """)
    premium_users = cursor.fetchone()[0]
    
    # المستخدمين الجدد (آخر 7 أيام)
    cursor.execute("""
        SELECT COUNT(*) FROM users 
        WHERE is_admin = 0 AND DATE(created_at) >= DATE('now', '-7 days')
    """)
    new_users = cursor.fetchone()[0]
    
    conn.close()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("إجمالي المستخدمين", total_users)
    
    with col2:
        st.metric("المشتركين المميزين", premium_users)
    
    with col3:
        st.metric("مستخدمين جدد (7 أيام)", new_users)

def export_report_to_csv(report_id):
    """تصدير التقرير إلى ملف CSV"""
    conn = sqlite3.connect('trading_recommendations.db')
    
    query = """
    SELECT 
        symbol, price, recommendation, confidence,
        stop_loss, target_profit, risk_reward_ratio,
        rsi, macd, trend
    FROM trades 
    WHERE report_id = ?
    """
    
    import pandas as pd
    df = pd.read_sql_query(query, conn, params=(report_id,))
    conn.close()
    
    # تحويل أسماء الأعمدة للعربية
    df.columns = [
        'الرمز', 'السعر', 'التوصية', 'الثقة',
        'وقف الخسارة', 'هدف الربح', 'نسبة المخاطر/العائد',
        'RSI', 'MACD', 'الاتجاه'
    ]
    
    return df.to_csv(index=False, encoding='utf-8-sig')

def send_notification(user_id, message):
    """إرسال إشعار للمستخدم"""
    # يمكن تطوير هذه الوظيفة لاحقاً لإرسال إشعارات بالبريد الإلكتروني
    pass

def validate_subscription_renewal():
    """التحقق من انتهاء الاشتراكات وإرسال تنبيهات"""
    conn = sqlite3.connect('trading_recommendations.db')
    cursor = conn.cursor()
    
    # البحث عن الاشتراكات التي ستنتهي خلال 3 أيام
    cursor.execute("""
        SELECT id, username, email, subscription_end
        FROM users 
        WHERE subscription_end IS NOT NULL 
        AND DATE(subscription_end) <= DATE('now', '+3 days')
        AND subscription_type != 'free'
    """)
    
    expiring_users = cursor.fetchall()
    conn.close()
    
    return expiring_users