# Quick Start Guide - دليل البدء السريع

## English Version

### 1. Choose Your Deployment Platform

Pick one of the following options based on your preference:

#### Option A: Heroku (Recommended - Easiest)
1. Sign up for a free account at [heroku.com](https://heroku.com)
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
3. Run these commands:
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

#### Option B: Google Cloud Platform (Free Trial Available)
1. Sign up for GCP with $300 free credit: [cloud.google.com](https://cloud.google.com)
2. Install gcloud CLI: https://cloud.google.com/sdk/docs/install
3. Run these commands:
```bash
gcloud init
gcloud app deploy app.yaml
gcloud app browse
```

#### Option C: DigitalOcean (Simple Dashboard)
1. Sign up at [digitalocean.com](https://digitalocean.com)
2. Go to App Platform in the dashboard
3. Connect your GitHub repository
4. Select this repository and branch `main`
5. Click "Deploy"

#### Option D: AWS (Industry Standard)
See detailed guide in `deploy/AWS_DEPLOYMENT.md`

#### Option E: Azure (Microsoft Cloud)
See detailed guide in `deploy/AZURE_DEPLOYMENT.md`

### 2. Verify Deployment

Once deployed, test your API:
```bash
# Replace YOUR_URL with your actual deployment URL
curl https://YOUR_URL/health

# Expected response:
# {"status": "healthy", "timestamp": "..."}
```

### 3. Use Your API

Access these endpoints:
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/recommendations` - Get all recommendations
- `GET /api/recommendations/1` - Get specific recommendation

---

## النسخة العربية

### 1. اختر منصة النشر الخاصة بك

اختر واحدة من الخيارات التالية حسب تفضيلاتك:

#### الخيار أ: Heroku (موصى به - الأسهل)
1. سجل حساب مجاني في [heroku.com](https://heroku.com)
2. ثبت Heroku CLI من: https://devcenter.heroku.com/articles/heroku-cli
3. شغل هذه الأوامر:
```bash
heroku login
heroku create اسم-تطبيقك
git push heroku main
heroku open
```

#### الخيار ب: Google Cloud Platform (يوجد نسخة تجريبية مجانية)
1. سجل في GCP مع رصيد مجاني $300: [cloud.google.com](https://cloud.google.com)
2. ثبت gcloud CLI من: https://cloud.google.com/sdk/docs/install
3. شغل هذه الأوامر:
```bash
gcloud init
gcloud app deploy app.yaml
gcloud app browse
```

#### الخيار ج: DigitalOcean (لوحة تحكم بسيطة)
1. سجل في [digitalocean.com](https://digitalocean.com)
2. اذهب إلى App Platform في لوحة التحكم
3. اربط مستودع GitHub الخاص بك
4. اختر هذا المستودع والفرع `main`
5. اضغط "Deploy"

#### الخيار د: AWS (المعيار الصناعي)
راجع الدليل التفصيلي في `deploy/AWS_DEPLOYMENT.md`

#### الخيار هـ: Azure (سحابة مايكروسوفت)
راجع الدليل التفصيلي في `deploy/AZURE_DEPLOYMENT.md`

### 2. تحقق من النشر

بعد النشر، اختبر API الخاص بك:
```bash
# استبدل YOUR_URL بعنوان النشر الفعلي الخاص بك
curl https://YOUR_URL/health

# الاستجابة المتوقعة:
# {"status": "healthy", "timestamp": "..."}
```

### 3. استخدم API الخاص بك

الوصول إلى هذه النقاط:
- `GET /` - معلومات API
- `GET /health` - فحص الصحة
- `GET /api/recommendations` - احصل على جميع التوصيات
- `GET /api/recommendations/1` - احصل على توصية محددة

---

## Support / الدعم

For issues, please open a GitHub issue in this repository.
للمشاكل، يرجى فتح مشكلة GitHub في هذا المستودع.
