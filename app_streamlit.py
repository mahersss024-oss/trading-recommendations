"""
تطبيق التوصيات التجارية مع نظام الاشتراك
يتضمن فترة تجريبية مجانية لمدة 3 أيام
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib

# استيراد نظام الاشتراك
from subscription_system import subscription_middleware, check_subscription_status, WHATSAPP_URL

# إعداد الصفحة
st.set_page_config(
    page_title="التوصيات التجارية - Trading Recommendations",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f4e79, #2e8b57);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
    border-left: 4px solid #1f4e79;
}
.recommendation-card {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border-left: 4px solid #28a745;
}
.buy-signal { border-left-color: #28a745; }
.sell-signal { border-left-color: #dc3545; }
.hold-signal { border-left-color: #ffc107; }
</style>
""", unsafe_allow_html=True)

def get_user_id():
    """الحصول على معرف فريد للمستخدم"""
    # في التطبيق الحقيقي، يمكن استخدام نظام تسجيل دخول فعلي
    # هنا نستخدم معرف بناءً على session state
    if 'user_id' not in st.session_state:
        # إنشاء معرف فريد بناءً على الوقت والعشوائية
        import uuid
        st.session_state.user_id = str(uuid.uuid4())
    return st.session_state.user_id

def create_sample_data():
    """إنشاء بيانات تجريبية للتوصيات"""
    recommendations = [
        {
            "symbol": "AAPL",
            "name": "أبل",
            "action": "شراء",
            "current_price": 175.50,
            "target_price": 185.00,
            "stop_loss": 170.00,
            "confidence": 85,
            "timeframe": "1-2 أسابيع",
            "reason": "نتائج أرباح قوية ونمو في مبيعات iPhone"
        },
        {
            "symbol": "GOOGL",
            "name": "جوجل",
            "action": "احتفاظ",
            "current_price": 140.25,
            "target_price": 150.00,
            "stop_loss": 135.00,
            "confidence": 75,
            "timeframe": "2-3 أسابيع",
            "reason": "نمو مستقر في الإعلانات وخدمات السحابة"
        },
        {
            "symbol": "TSLA",
            "name": "تسلا",
            "action": "بيع",
            "current_price": 250.30,
            "target_price": 230.00,
            "stop_loss": 260.00,
            "confidence": 70,
            "timeframe": "1-3 أسابيع",
            "reason": "قلق حول تراجع مبيعات السيارات الكهربائية"
        }
    ]
    return recommendations

def display_recommendation_card(rec):
    """عرض بطاقة توصية واحدة"""
    action_colors = {
        "شراء": "#28a745",
        "بيع": "#dc3545", 
        "احتفاظ": "#ffc107"
    }
    
    action_icons = {
        "شراء": "📈",
        "بيع": "📉",
        "احتفاظ": "📊"
    }
    
    color = action_colors.get(rec["action"], "#6c757d")
    icon = action_icons.get(rec["action"], "📊")
    
    profit_loss = ((rec["target_price"] - rec["current_price"]) / rec["current_price"]) * 100
    
    st.markdown(f"""
    <div class="recommendation-card" style="border-left-color: {color};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: {color};">{icon} {rec['symbol']} - {rec['name']}</h4>
                <p style="margin: 5px 0; font-size: 14px; color: #666;">
                    <strong>التوصية:</strong> {rec['action']} | 
                    <strong>الثقة:</strong> {rec['confidence']}% |
                    <strong>الإطار الزمني:</strong> {rec['timeframe']}
                </p>
            </div>
            <div style="text-align: left;">
                <div style="font-size: 18px; font-weight: bold;">${rec['current_price']:.2f}</div>
                <div style="font-size: 12px; color: {'green' if profit_loss > 0 else 'red'};">
                    هدف: ${rec['target_price']:.2f} ({profit_loss:+.1f}%)
                </div>
            </div>
        </div>
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">
            <p style="margin: 0; font-size: 13px;"><strong>وقف الخسارة:</strong> ${rec['stop_loss']:.2f}</p>
            <p style="margin: 5px 0 0 0; font-size: 13px;"><strong>السبب:</strong> {rec['reason']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_portfolio_overview():
    """عرض نظرة عامة على المحفظة"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #1f4e79;">📊 إجمالي التوصيات</h3>
            <h2 style="margin: 10px 0; color: #2e8b57;">15</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #1f4e79;">📈 توصيات شراء</h3>
            <h2 style="margin: 10px 0; color: #28a745;">8</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #1f4e79;">📉 توصيات بيع</h3>
            <h2 style="margin: 10px 0; color: #dc3545;">4</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #1f4e79;">💰 معدل النجاح</h3>
            <h2 style="margin: 10px 0; color: #2e8b57;">87%</h2>
        </div>
        """, unsafe_allow_html=True)

def display_performance_chart():
    """عرض مخطط الأداء"""
    # بيانات تجريبية لأداء المحفظة
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    portfolio_value = [10000]
    
    for i in range(1, 30):
        # نمو عشوائي للمحاكاة
        change = portfolio_value[-1] * (0.98 + 0.04 * (i % 7 / 7))
        portfolio_value.append(change)
    
    df = pd.DataFrame({
        'التاريخ': dates,
        'قيمة المحفظة': portfolio_value
    })
    
    fig = px.line(df, x='التاريخ', y='قيمة المحفظة', 
                  title='أداء المحفظة خلال آخر 30 يوم',
                  line_shape='spline')
    
    fig.update_layout(
        xaxis_title="التاريخ",
        yaxis_title="قيمة المحفظة ($)",
        font=dict(family="Arial", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_traces(line=dict(color='#2e8b57', width=3))
    
    st.plotly_chart(fig, use_container_width=True)

def display_sector_analysis():
    """عرض تحليل القطاعات"""
    sectors_data = {
        'القطاع': ['التكنولوجيا', 'الصحة', 'المالي', 'الطاقة', 'الاستهلاكي'],
        'النسبة': [35, 20, 18, 15, 12],
        'التوصية': ['شراء قوي', 'شراء', 'احتفاظ', 'بيع', 'احتفاظ']
    }
    
    df = pd.DataFrame(sectors_data)
    
    fig = px.pie(df, values='النسبة', names='القطاع', 
                 title='توزيع التوصيات حسب القطاع',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(font=dict(family="Arial", size=12))
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    """الدالة الرئيسية للتطبيق"""
    
    # الحصول على معرف المستخدم
    user_id = get_user_id()
    
    # فحص صلاحية الوصول والاشتراك
    status_info = subscription_middleware(user_id)
    
    # العنوان الرئيسي
    st.markdown("""
    <div class="main-header">
        <h1>📈 التوصيات التجارية</h1>
        <p>توصيات استثمارية دقيقة ومحدثة لتحقيق أفضل عوائد</p>
    </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي
    with st.sidebar:
        st.header("📋 القائمة الرئيسية")
        
        # عرض معلومات الاشتراك
        st.success(f"✅ {status_info['message']}")
        
        if status_info['status'] == 'trial_active':
            st.markdown(f"""
            <div style="background: #fff3cd; padding: 10px; border-radius: 5px; border-left: 4px solid #ffc107;">
                <strong>🎯 للاشتراك الكامل:</strong><br>
                <a href="{WHATSAPP_URL}" target="_blank">📱 تواصل معنا</a>
            </div>
            """, unsafe_allow_html=True)
        
        # خيارات القائمة
        page = st.selectbox(
            "اختر الصفحة:",
            ["🏠 الرئيسية", "📈 التوصيات", "📊 تحليل القطاعات", "💼 أداء المحفظة", "📞 التواصل"]
        )
    
    # عرض المحتوى حسب الصفحة المختارة
    if page == "🏠 الرئيسية":
        display_portfolio_overview()
        
        st.header("📈 آخر التوصيات")
        recommendations = create_sample_data()[:3]  # عرض أول 3 توصيات
        
        for rec in recommendations:
            display_recommendation_card(rec)
        
        st.info("💡 **نصيحة اليوم:** تنويع المحفظة هو مفتاح تقليل المخاطر وزيادة العوائد على المدى الطويل.")
    
    elif page == "📈 التوصيات":
        st.header("📈 جميع التوصيات")
        
        # فلاتر التوصيات
        col1, col2 = st.columns(2)
        with col1:
            action_filter = st.selectbox("فلترة حسب التوصية:", ["الكل", "شراء", "بيع", "احتفاظ"])
        with col2:
            confidence_filter = st.slider("الحد الأدنى للثقة:", 0, 100, 70, 5)
        
        recommendations = create_sample_data()
        
        # تطبيق الفلاتر
        if action_filter != "الكل":
            recommendations = [r for r in recommendations if r["action"] == action_filter]
        
        recommendations = [r for r in recommendations if r["confidence"] >= confidence_filter]
        
        if recommendations:
            for rec in recommendations:
                display_recommendation_card(rec)
        else:
            st.info("لا توجد توصيات تطابق المعايير المحددة.")
    
    elif page == "📊 تحليل القطاعات":
        st.header("📊 تحليل القطاعات")
        display_sector_analysis()
        
        st.subheader("تفاصيل القطاعات")
        
        sectors_details = pd.DataFrame({
            'القطاع': ['التكنولوجيا', 'الصحة', 'المالي', 'الطاقة', 'الاستهلاكي'],
            'عدد الأسهم': [8, 4, 3, 2, 3],
            'متوسط العائد المتوقع': ['12%', '8%', '6%', '4%', '7%'],
            'مستوى المخاطر': ['متوسط', 'منخفض', 'متوسط', 'عالي', 'منخفض']
        })
        
        st.dataframe(sectors_details, use_container_width=True)
    
    elif page == "💼 أداء المحفظة":
        st.header("💼 أداء المحفظة")
        display_performance_chart()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 إحصائيات الأداء")
            metrics_df = pd.DataFrame({
                'المؤشر': ['العائد الإجمالي', 'العائد الشهري', 'أفضل يوم', 'أسوأ يوم', 'معدل شارب'],
                'القيمة': ['+15.6%', '+2.3%', '+4.1%', '-2.8%', '1.42']
            })
            st.dataframe(metrics_df, use_container_width=True)
        
        with col2:
            st.subheader("🎯 أهداف الاستثمار")
            st.info("🎯 **الهدف السنوي:** +20% عائد")
            st.success("✅ **التقدم:** 78% من الهدف")
            st.warning("⚠️ **تنبيه:** اقترب موسم إعلان الأرباح")
    
    elif page == "📞 التواصل":
        st.header("📞 التواصل والدعم")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📱 تواصل معنا")
            st.markdown(f"""
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>💬 الواتس اب</h3>
                <p>للاستفسارات والاشتراك</p>
                <a href="{WHATSAPP_URL}" target="_blank" 
                   style="background: #25D366; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 25px; display: inline-block;">
                    📱 تواصل الآن - 0549764152
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("❓ الأسئلة الشائعة")
            
            with st.expander("ما هي دقة التوصيات؟"):
                st.write("معدل نجاح توصياتنا يبلغ 87% خلال آخر 6 أشهر.")
            
            with st.expander("كم مرة يتم تحديث التوصيات؟"):
                st.write("يتم تحديث التوصيات يومياً، مع تنبيهات فورية للفرص العاجلة.")
            
            with st.expander("ما هي أسعار الاشتراك؟"):
                st.write("تواصل معنا عبر الواتس اب للاطلاع على خطط الاشتراك المختلفة.")
    
    # تذييل الصفحة
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🔒 جميع البيانات محمية ومشفرة | ⚠️ الاستثمار ينطوي على مخاطر</p>
        <p>📞 للدعم الفني: تواصل معنا عبر الواتس اب</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()