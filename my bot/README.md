# 📊 نظام التوصيات المالية المتقدم

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

نظام شامل ومتطور لإدارة التوصيات المالية وتحليل البيانات المالية باللغة العربية مع دعم كامل للنشر السحابي.

## 🌟 الميزات الرئيسية

- ✅ **تحليل ذكي للتقارير المالية** - تحليل تلقائي للملفات النصية واستخراج البيانات
- ✅ **إدارة شاملة للمستخدمين** - نظام صلاحيات متعدد المستويات  
- ✅ **واجهة عربية متجاوبة** - دعم كامل لـ RTL والخطوط العربية
- ✅ **رسوم بيانية تفاعلية** - تصورات بصرية للبيانات المالية
- ✅ **تصدير متعدد الصيغ** - CSV, Excel, PDF
- ✅ **نظام أمان متقدم** - تشفير وحماية البيانات
- ✅ **نشر سحابي مجاني** - دعم عدة منصات سحابية

## 🚀 النشر السحابي السريع

### خيار 1: Streamlit Community Cloud (الأسهل)
```bash
# 1. ارفع على GitHub
git add .
git commit -m "Deploy to cloud"
git push origin main

# 2. زر https://share.streamlit.io/
# 3. اربط GitHub وانشر!
```

### خيار 2: Heroku
```bash
heroku create your-trading-app
git push heroku main
```

### خيار 3: Railway
```bash
railway login && railway init && railway up
```

## 💻 التشغيل المحلي

### الطريقة السريعة:
```bash
# Windows
run_enhanced.bat

# أو يدوياً
pip install -r requirements.txt
streamlit run app_enhanced.py
```

## 🔧 إعداد النشر التلقائي

```bash
# Windows
deploy_setup.bat

# Linux/Mac  
chmod +x deploy_setup.sh && ./deploy_setup.sh
```

## 👥 المستخدمون الافتراضيون

| المستخدم | كلمة المرور | الصلاحية |
|-----------|-------------|----------|
| admin     | admin123    | مدير     |

⚠️ **مهم:** غيّر كلمة مرور المدير فور أول تسجيل دخول!

## 📁 هيكل المشروع

```
📦 نظام التوصيات المالية/
├── 📄 app_enhanced.py          # التطبيق الرئيسي
├── 📄 enhancements.py          # الميزات الإضافية  
├── 📄 requirements.txt         # المكتبات المطلوبة
├── 📄 Procfile                # إعدادات النشر
├── 📁 .streamlit/             # إعدادات Streamlit
├── 📄 DEPLOYMENT_GUIDE.md     # دليل النشر الشامل
└── 📄 QUICK_DEPLOY.md         # دليل النشر السريع
```

## 🔐 الأمان والخصوصية

- 🔒 **تشفير كلمات المرور** - SHA-256 hashing
- 🛡️ **حماية من الهجمات** - تتبع محاولات تسجيل الدخول  
- 📊 **بيانات آمنة** - قاعدة بيانات SQLite محلية
- 🔑 **صلاحيات متدرجة** - تحكم كامل في الوصول

## 📈 أحدث التحديثات

### الإصدار 2.0 (أكتوبر 2025)
- ✨ دعم النشر السحابي الكامل
- 🛠️ إصلاح مشكلة تكرار البيانات
- 🎨 تحسين الواجهة والأداء
- 🔐 تعزيز الأمان

## 📞 الدعم والتواصل

للاستفسارات والدعم الفني، راجع ملفات الدليل المرفقة أو اتصل بفريق التطوير.

---

<p align="center">
  <strong>نظام التوصيات المالية المتقدم - إصدار 2025</strong><br>
  صُنع بـ ❤️ للمجتمع العربي
</p>