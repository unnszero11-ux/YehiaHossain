# 🚀 Quick Start Guide

## التشغيل السريع في 5 دقائق

### الخطوة 1: التثبيت

```bash
cd worker
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows

pip install -r requirements.txt
playwright install chromium
```

### الخطوة 2: الإعداد

```bash
# أنشئ ملف .env
cp .env.example .env

# عدّل .env وغيّر API_KEY
nano .env  # أو أي محرر نصوص
```

**في `.env`، غيّر:**
```env
API_KEY=your_secure_random_key_here_32_chars
```

### الخطوة 3: أنشئ ملفات البيانات

```bash
cp cards.txt.example cards.txt
cp zip.txt.example zip.txt
cp proxies.txt.example proxies.txt
```

**أضف بطاقاتك في `cards.txt`:**
```
4242424242424242|12|2025
5555555555554444|06|2026
```

### الخطوة 4: شغّل الخدمة

```bash
python api_server.py
```

**يجب أن ترى:**
```
============================================================
Card Checker Worker Service
============================================================
Host: 0.0.0.0
Port: 5000
Headless: False
Use Proxy: True
Rate Limit: True
Supported Websites: loft, anntaylor
============================================================
Starting server...
 * Running on http://0.0.0.0:5000
```

---

## ✅ اختبار الخدمة

### 1. Health Check

```bash
curl http://localhost:5000/api/health
```

**النتيجة:**
```json
{
  "status": "healthy",
  "service": "Card Checker Worker",
  "version": "1.0.0",
  "supported_websites": ["loft", "anntaylor"]
}
```

### 2. فحص بطاقة واحدة

```bash
curl -X POST http://localhost:5000/api/check-card \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "website": "loft",
    "card_number": "4242424242424242",
    "exp_month": "12",
    "exp_year": "2025",
    "use_proxy": false
  }'
```

### 3. عرض الإحصائيات

```bash
curl http://localhost:5000/api/metrics \
  -H "X-API-Key: your_api_key_here"
```

---

## 🔧 استكشاف الأخطاء

### المشكلة: "API key required"

**الحل:** أضف Header في الطلب:
```bash
-H "X-API-Key: your_api_key_from_env_file"
```

### المشكلة: "Playwright not found"

**الحل:**
```bash
playwright install chromium
playwright install-deps
```

### المشكلة: "No ZIP codes loaded"

**الحل:**
```bash
cp zip.txt.example zip.txt
# تأكد أن الملف يحتوي على رموز بريدية
```

### المشكلة: "Configuration validation failed"

**الحل:** غيّر API_KEY في `.env`:
```env
API_KEY=generate_secure_random_key_here
```

---

## 📝 الخطوات التالية

1. ✅ **اختبر الخدمة محلياً** - تأكد أنها تعمل
2. ✅ **أضف بطاقاتك الحقيقية** في `cards.txt`
3. ✅ **اضبط الإعدادات** في `.env` حسب احتياجك
4. ✅ **شغّل على VPS** للاستخدام الدائم (اختياري)
5. ✅ **اربط مع التطبيق الرئيسي** (الخطوة التالية)

---

## 🔗 الربط مع التطبيق الرئيسي

بعد تشغيل Worker Service، ارجع للتطبيق الرئيسي وأضف في `.env`:

```env
WORKER_SERVICE_URL=http://localhost:5000
WORKER_API_KEY=your_worker_api_key_here
ENABLE_REAL_CHECK=true
```

الآن يمكنك استخدام "فحص حقيقي" في الواجهة!

---

## 💡 نصائح

- **للاختبار:** اضبط `HEADLESS=false` لترى المتصفح
- **للإنتاج:** اضبط `HEADLESS=true` للأداء الأفضل
- **للأمان:** غيّر `API_KEY` لمفتاح عشوائي قوي
- **للسرعة:** استخدم `USE_PROXY=false` إذا لم تحتاج بروكسيات

---

## 📚 المزيد من التوثيق

- `README.md` - دليل كامل ومفصل
- `WORKER_INTEGRATION.md` - دليل التكامل مع التطبيق الرئيسي
- `.env.example` - جميع الإعدادات المتاحة
