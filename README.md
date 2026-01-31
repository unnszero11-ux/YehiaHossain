# Card Checker Worker Service

## 🎯 الهدف
خدمة منفصلة لفحص البطاقات على المواقع الحقيقية (LOFT, ANN TAYLOR) باستخدام Playwright.

## 📋 المتطلبات

### 1. Python 3.8+
```bash
python --version
```

### 2. تثبيت المكتبات
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. الملفات المطلوبة
- `cards.txt` - قائمة البطاقات (تنسيق: `card|mm|yyyy`)
- `zip.txt` - قائمة الرموز البريدية الأمريكية
- `proxies.txt` - قائمة البروكسيات (اختياري)
- `.env` - إعدادات الخدمة

---

## 🚀 التشغيل

### الطريقة 1: تشغيل مباشر
```bash
python worker.py
```

### الطريقة 2: كخدمة API
```bash
python api_server.py
```

سيعمل على: `http://localhost:5000`

---

## 🔌 API Endpoints

### 1. فحص بطاقة واحدة
```bash
POST /api/check-card
Content-Type: application/json

{
  "website": "loft",  // أو "anntaylor"
  "card_number": "4242424242424242",
  "exp_month": "12",
  "exp_year": "2025",
  "use_proxy": true
}
```

**Response:**
```json
{
  "success": true,
  "result": "live",  // أو "declined" أو "error"
  "card": "4242424242424242",
  "message": "Working card",
  "timestamp": "2026-01-31T12:00:00Z"
}
```

### 2. فحص جماعي
```bash
POST /api/check-cards-bulk
Content-Type: application/json

{
  "website": "loft",
  "cards": [
    {"card_number": "4242...", "exp_month": "12", "exp_year": "2025"},
    {"card_number": "5555...", "exp_month": "06", "exp_year": "2026"}
  ],
  "use_proxy": true
}
```

### 3. حالة الخدمة
```bash
GET /api/health
```

---

## ⚙️ الإعدادات (.env)

```env
# Worker Settings
WORKER_PORT=5000
WORKER_HOST=0.0.0.0

# Main App API (للإرسال التلقائي للنتائج)
MAIN_APP_URL=https://v1cojc6udw.preview.c24.airoapp.ai
MAIN_APP_API_KEY=your_secret_key_here

# Browser Settings
HEADLESS=false  # true للتشغيل بدون واجهة
BROWSER_TIMEOUT=120000

# Proxy Settings
USE_PROXY=true
PROXY_ROTATION=true
```

---

## 🔒 الأمان

### 1. API Key Authentication
جميع الطلبات تتطلب API Key في الـ Header:
```
X-API-Key: your_secret_key_here
```

### 2. Rate Limiting
- 10 طلبات/دقيقة للفحص الفردي
- 2 طلبات/دقيقة للفحص الجماعي

### 3. IP Whitelist (اختياري)
يمكن تحديد IPs المسموح لها بالوصول في `.env`:
```env
ALLOWED_IPS=127.0.0.1,192.168.1.100
```

---

## 📊 المراقبة

### Logs
جميع العمليات تُسجل في:
- `logs/worker.log` - سجل عام
- `logs/cards.log` - سجل فحص البطاقات
- `logs/errors.log` - سجل الأخطاء

### Metrics
```bash
GET /api/metrics
```

يعرض:
- عدد البطاقات المفحوصة
- معدل النجاح
- متوسط وقت الفحص
- حالة البروكسيات

---

## 🐳 Docker (اختياري)

### Build
```bash
docker build -t card-checker-worker .
```

### Run
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/cards.txt:/app/cards.txt \
  -v $(pwd)/zip.txt:/app/zip.txt \
  -v $(pwd)/proxies.txt:/app/proxies.txt \
  -v $(pwd)/logs:/app/logs \
  --name card-worker \
  card-checker-worker
```

---

## 🔧 استكشاف الأخطاء

### المشكلة: Playwright لا يعمل
```bash
playwright install chromium
playwright install-deps
```

### المشكلة: الكابتشا لا تُحل
- تأكد من `HEADLESS=false` لحل يدوي
- استخدم بروكسيات عالية الجودة
- قلل معدل الطلبات

### المشكلة: البروكسيات لا تعمل
- تحقق من صيغة البروكسي في `proxies.txt`
- جرب بروكسيات مختلفة
- تأكد من أن البروكسي يدعم HTTPS

---

## 📝 ملاحظات مهمة

1. **القانونية**: استخدم هذه الخدمة فقط للبطاقات التي تملكها أو لديك إذن باختبارها.
2. **الأداء**: كل عملية فحص تستغرق 2-5 دقائق (بسبب الكابتشا والتحميل).
3. **الموارد**: يتطلب 2GB RAM على الأقل لكل instance.
4. **الصيانة**: قد تحتاج لتحديث الـ selectors إذا تغيرت المواقع.

---

## 🆘 الدعم

إذا واجهت مشاكل:
1. تحقق من `logs/errors.log`
2. تأكد من تحديث Playwright: `pip install --upgrade playwright`
3. جرب تشغيل السكريبت يدوياً أولاً
