"""
نظام إدارة الاشتراكات للتطبيق
يتضمن فترة تجريبية مجانية لمدة 3 أيام
"""
import streamlit as st
from datetime import datetime, timedelta
import json
import os

# معلومات الاشتراك
WHATSAPP_NUMBER = "0549764152"
WHATSAPP_MESSAGE = "مرحباً، أرغب في الاشتراك في تطبيق التوصيات التجارية"
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}?text={WHATSAPP_MESSAGE}"

# مدة الفترة التجريبية (3 أيام)
TRIAL_PERIOD_DAYS = 3

def get_subscription_file_path():
    """الحصول على مسار ملف بيانات الاشتراكات"""
    return "subscriptions.json"

def load_subscriptions():
    """تحميل بيانات الاشتراكات من الملف"""
    file_path = get_subscription_file_path()
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_subscriptions(subscriptions):
    """حفظ بيانات الاشتراكات في الملف"""
    file_path = get_subscription_file_path()
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(subscriptions, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def get_user_subscription_info(user_id):
    """الحصول على معلومات اشتراك المستخدم"""
    subscriptions = load_subscriptions()
    
    if user_id not in subscriptions:
        # مستخدم جديد - إنشاء فترة تجريبية
        trial_start = datetime.now()
        trial_end = trial_start + timedelta(days=TRIAL_PERIOD_DAYS)
        
        subscription_info = {
            "user_id": user_id,
            "subscription_type": "trial",
            "trial_start": trial_start.isoformat(),
            "trial_end": trial_end.isoformat(),
            "is_active": True,
            "subscription_start": None,
            "subscription_end": None,
            "created_at": trial_start.isoformat()
        }
        
        subscriptions[user_id] = subscription_info
        save_subscriptions(subscriptions)
        return subscription_info
    
    return subscriptions[user_id]

def check_subscription_status(user_id):
    """فحص حالة اشتراك المستخدم"""
    subscription_info = get_user_subscription_info(user_id)
    current_time = datetime.now()
    
    # فحص الفترة التجريبية
    if subscription_info["subscription_type"] == "trial":
        trial_end = datetime.fromisoformat(subscription_info["trial_end"])
        if current_time <= trial_end:
            days_remaining = (trial_end - current_time).days + 1
            return {
                "status": "trial_active",
                "days_remaining": days_remaining,
                "message": f"الفترة التجريبية المجانية - متبقي {days_remaining} أيام"
            }
        else:
            return {
                "status": "trial_expired",
                "days_remaining": 0,
                "message": "انتهت الفترة التجريبية المجانية"
            }
    
    # فحص الاشتراك المدفوع
    elif subscription_info["subscription_type"] == "paid":
        if subscription_info["subscription_end"]:
            subscription_end = datetime.fromisoformat(subscription_info["subscription_end"])
            if current_time <= subscription_end:
                days_remaining = (subscription_end - current_time).days + 1
                return {
                    "status": "subscription_active",
                    "days_remaining": days_remaining,
                    "message": f"اشتراك مدفوع نشط - متبقي {days_remaining} أيام"
                }
            else:
                return {
                    "status": "subscription_expired",
                    "days_remaining": 0,
                    "message": "انتهى الاشتراك المدفوع"
                }
    
    return {
        "status": "no_subscription",
        "days_remaining": 0,
        "message": "لا يوجد اشتراك نشط"
    }

def upgrade_to_paid_subscription(user_id, duration_days=30):
    """ترقية المستخدم إلى اشتراك مدفوع"""
    subscriptions = load_subscriptions()
    current_time = datetime.now()
    subscription_end = current_time + timedelta(days=duration_days)
    
    if user_id in subscriptions:
        subscriptions[user_id].update({
            "subscription_type": "paid",
            "subscription_start": current_time.isoformat(),
            "subscription_end": subscription_end.isoformat(),
            "is_active": True,
            "upgraded_at": current_time.isoformat()
        })
    else:
        subscriptions[user_id] = {
            "user_id": user_id,
            "subscription_type": "paid",
            "trial_start": None,
            "trial_end": None,
            "is_active": True,
            "subscription_start": current_time.isoformat(),
            "subscription_end": subscription_end.isoformat(),
            "created_at": current_time.isoformat()
        }
    
    return save_subscriptions(subscriptions)

def display_subscription_block_page():
    """عرض صفحة حجب الوصول مع رابط الواتس اب"""
    st.markdown("""
    <style>
    .subscription-block {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin: 2rem 0;
        color: white;
    }
    .subscription-block h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subscription-block p {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    .whatsapp-button {
        background: #25D366;
        color: white;
        padding: 15px 30px;
        border-radius: 50px;
        text-decoration: none;
        font-size: 1.1rem;
        font-weight: bold;
        display: inline-block;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
        transition: all 0.3s ease;
    }
    .whatsapp-button:hover {
        background: #128C7E;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
    }
    .features-list {
        text-align: right;
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
    }
    .features-list ul {
        list-style-type: none;
        padding: 0;
    }
    .features-list li {
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    .features-list li:before {
        content: "✅ ";
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="subscription-block">
        <h1>🔒 انتهت الفترة التجريبية المجانية</h1>
        <p>
            شكراً لك على تجربة تطبيق التوصيات التجارية!<br>
            لقد انتهت فترتك التجريبية المجانية البالغة 3 أيام.
        </p>
        
        <div class="features-list">
            <h3>🌟 مميزات الاشتراك المدفوع:</h3>
            <ul>
                <li>توصيات تجارية دقيقة ومحدثة باستمرار</li>
                <li>تحليلات فنية شاملة للأسهم والعملات</li>
                <li>إشارات دخول وخروج محددة بوقت</li>
                <li>دعم فني متواصل على مدار الساعة</li>
                <li>تنبيهات فورية للفرص الاستثمارية</li>
                <li>تقارير أداء مفصلة لاستثماراتك</li>
            </ul>
        </div>
        
        <p>للاشتراك والاستمتاع بجميع المميزات، تواصل معنا الآن:</p>
        
        <a href="{WHATSAPP_URL}" target="_blank" class="whatsapp-button">
            📱 تواصل عبر الواتس اب - {WHATSAPP_NUMBER}
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # إضافة معلومات إضافية
    st.info("💡 **نصيحة:** احفظ رقم الواتس اب في جهازك للتواصل السريع!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 تحديث الصفحة", use_container_width=True):
            st.rerun()

def display_trial_status(status_info):
    """عرض حالة الفترة التجريبية"""
    if status_info["status"] == "trial_active":
        days_remaining = status_info["days_remaining"]
        if days_remaining <= 1:
            st.warning(f"⚠️ **تنبيه:** {status_info['message']} - الفترة التجريبية تنتهي اليوم!")
        elif days_remaining <= 2:
            st.info(f"ℹ️ **تذكير:** {status_info['message']}")
        
        # إضافة رابط الاشتراك المبكر
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #4CAF50, #45a049); padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0;">
            <p style="color: white; margin: 0;">
                🎯 <strong>اشترك الآن ولا تنتظر انتهاء الفترة التجريبية!</strong>
            </p>
            <a href="{WHATSAPP_URL}" target="_blank" style="color: white; text-decoration: underline;">
                📱 تواصل معنا عبر الواتس اب
            </a>
        </div>
        """, unsafe_allow_html=True)

def check_access_permission(user_id):
    """فحص صلاحية الوصول للتطبيق"""
    status_info = check_subscription_status(user_id)
    
    if status_info["status"] in ["trial_active", "subscription_active"]:
        return True, status_info
    else:
        return False, status_info

def subscription_middleware(user_id):
    """وسيط فحص الاشتراك - يجب استدعاؤه في بداية كل صفحة"""
    has_access, status_info = check_access_permission(user_id)
    
    if not has_access:
        display_subscription_block_page()
        st.stop()
    
    # عرض حالة الفترة التجريبية إذا كانت نشطة
    if status_info["status"] == "trial_active":
        display_trial_status(status_info)
    
    return status_info