# ✅ فحص جاهزية Worker Service

## 🔍 الفحوصات المطلوبة

### 1. فحص Python

```bash
# تحقق من إصدار Python
python --version
# أو
python3 --version

# يجب أن يكون 3.8 أو أحدث
```

**✅ النتيجة المتوقعة:**
```
Python 3.8.x أو أحدث
```

---

### 2. فحص الملفات الأساسية

```bash
cd worker

# تحقق من وجود الملفات
ls -lh api_server.py card_checker.py config.py utils.py requirements.txt
```

**✅ النتيجة المتوقعة:**
```
-rw-r--r-- 1 user user  10K api_server.py
-rw-r--r-- 1 user user  10K card_checker.py
-rw-r--r-- 1 user user 2.3K config.py
-rw-r--r-- 1 user user 6.4K utils.py
-rw-r--r-- 1 user user  363 requirements.txt
```

---

### 3. فحص ملف .env

```bash
# تحقق من وجود .env
if [ -f .env ]; then
    echo "✅ .env موجود"
    # تحقق من API_KEY
    if grep -q "change_this_to_secure_random_key" .env; then
        echo "⚠️  تحذير: API_KEY لم يتم تغييره"
    else
        echo "✅ API_KEY تم تكوينه"
    fi
else
    echo "❌ .env غير موجود - قم بإنشائه: cp .env.example .env"
fi
```

**✅ النتيجة المتوقعة:**
```
✅ .env موجود
✅ API_KEY تم تكوينه
```

---

### 4. فحص ملفات البيانات

```bash
# تحقق من cards.txt
if [ -f cards.txt ]; then
    count=$(grep -v '^#' cards.txt | grep -v '^$' | wc -l)
    echo "✅ cards.txt: $count بطاقة"
else
    echo "⚠️  cards.txt غير موجود - قم بإنشائه: cp cards.txt.example cards.txt"
fi

# تحقق من zip.txt
if [ -f zip.txt ]; then
    count=$(grep -v '^#' zip.txt | grep -v '^$' | wc -l)
    echo "✅ zip.txt: $count رمز بريدي"
else
    echo "⚠️  zip.txt غير موجود - قم بإنشائه: cp zip.txt.example zip.txt"
fi

# تحقق من proxies.txt (اختياري)
if [ -f proxies.txt ]; then
    count=$(grep -v '^#' proxies.txt | grep -v '^$' | wc -l)
    echo "✅ proxies.txt: $count بروكسي (اختياري)"
else
    echo "ℹ️  proxies.txt غير موجود (اختياري)"
fi
```

**✅ النتيجة المتوقعة:**
```
✅ cards.txt: 2 بطاقة
✅ zip.txt: 3 رمز بريدي
ℹ️  proxies.txt غير موجود (اختياري)
```

---

### 5. فحص المكتبات المثبتة

```bash
# تفعيل البيئة الافتراضية أولاً
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows

# تحقق من المكتبات
python -c "import flask; print('✅ Flask installed')"
python -c "import playwright; print('✅ Playwright installed')"
python -c "import dotenv; print('✅ python-dotenv installed')"
python -c "import faker; print('✅ Faker installed')"
```

**✅ النتيجة المتوقعة:**
```
✅ Flask installed
✅ Playwright installed
✅ python-dotenv installed
✅ Faker installed
```

**❌ إذا ظهرت أخطاء:**
```bash
# ثبّت المكتبات
pip install -r requirements.txt

# ثبّت Playwright browsers
playwright install chromium
playwright install-deps
```

---

### 6. فحص تحميل الوحدات

```bash
# تحقق من config.py
python -c "from config import config; print(f'✅ Config loaded - Port: {config.WORKER_PORT}')"

# تحقق من utils.py
python -c "from utils import setup_logging; print('✅ Utils loaded')"

# تحقق من api_server.py (لا تشغله، فقط استورده)
python -c "import api_server; print('✅ API Server module OK')"
```

**✅ النتيجة المتوقعة:**
```
✅ Config loaded - Port: 5000
✅ Utils loaded
✅ API Server module OK
```

---

### 7. اختبار سريع شامل

```bash
# شغّل سكريبت الاختبار الشامل
python test_worker.py
```

**✅ النتيجة المتوقعة:**
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          WORKER SERVICE - COMPREHENSIVE TEST              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

============================================================
TEST 1: Python Version
============================================================

✅ Python version: 3.x.x (OK)

============================================================
TEST 2: Core Files
============================================================

✅ API Server: api_server.py (9988 bytes)
✅ Card Checker: card_checker.py (10006 bytes)
✅ Config: config.py (2274 bytes)
✅ Utils: utils.py (6510 bytes)
✅ Requirements: requirements.txt (363 bytes)
✅ Env Example: .env.example (595 bytes)

============================================================
TEST 3: Python Packages
============================================================

✅ Flask installed
✅ Flask-CORS installed
✅ Flask-Limiter installed
✅ Playwright installed
✅ python-dotenv installed
✅ Requests installed
✅ Faker installed

============================================================
TEST 4: Configuration
============================================================

✅ .env file exists
✅ API_KEY is configured

============================================================
TEST 5: Data Files
============================================================

✅ Cards file: 2 entries
✅ ZIP codes file: 3 entries
ℹ️  Proxies file: NOT found (optional)

============================================================
TEST 6: Config Module
============================================================

✅ Config module loaded
ℹ️  - Worker Port: 5000
ℹ️  - Worker Host: 0.0.0.0
ℹ️  - Headless: False
ℹ️  - Use Proxy: True
ℹ️  - Rate Limit: True
ℹ️  - Supported Sites: loft, anntaylor

============================================================
TEST 7: Utils Module
============================================================

✅ Utils module loaded
✅ Logging setup OK
✅ Cards loaded: 2 cards
✅ ZIP codes loaded: 3 codes

============================================================
TEST 8: API Server Module
============================================================

✅ API server module loaded
ℹ️  - Flask app initialized
ℹ️  - CORS enabled
ℹ️  - Rate limiter configured

============================================================
TEST REPORT
============================================================

Total Tests: 8
✅ Passed: 8
✅ Failed: 0

============================================================

✅ 🎉 ALL TESTS PASSED! Worker Service is ready!

ℹ️  
Next steps:
ℹ️    1. Run: python api_server.py
ℹ️    2. Test: curl http://localhost:5000/api/health
```

---

## 🚀 إذا نجحت جميع الاختبارات

```bash
# شغّل Worker Service
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
 * Serving Flask app 'api_server'
 * Running on http://0.0.0.0:5000
```

**ثم اختبر:**
```bash
# في نافذة أخرى
curl http://localhost:5000/api/health
```

**النتيجة المتوقعة:**
```json
{
  "status": "healthy",
  "service": "Card Checker Worker",
  "version": "1.0.0",
  "supported_websites": ["loft", "anntaylor"]
}
```

---

## ❌ إذا فشلت الاختبارات

### المشكلة: Python version < 3.8
**الحل:** ثبّت Python 3.8 أو أحدث

### المشكلة: Packages not installed
**الحل:**
```bash
pip install -r requirements.txt
playwright install chromium
```

### المشكلة: .env not found
**الحل:**
```bash
cp .env.example .env
nano .env  # غيّر API_KEY
```

### المشكلة: Data files not found
**الحل:**
```bash
cp cards.txt.example cards.txt
cp zip.txt.example zip.txt
```

### المشكلة: API_KEY not changed
**الحل:**
```bash
# ولّد مفتاح آمن
python -c "import secrets; print(secrets.token_urlsafe(32))"

# انسخه وضعه في .env
nano .env
```

---

## 📋 قائمة فحص سريعة

- [ ] Python 3.8+ مثبت
- [ ] جميع الملفات الأساسية موجودة
- [ ] المكتبات مثبتة (`pip install -r requirements.txt`)
- [ ] Playwright مثبت (`playwright install chromium`)
- [ ] ملف `.env` موجود ومُعد
- [ ] `API_KEY` تم تغييره
- [ ] ملفات البيانات موجودة (`cards.txt`, `zip.txt`)
- [ ] جميع الوحدات تُحمّل بدون أخطاء
- [ ] `python test_worker.py` ينجح
- [ ] `python api_server.py` يعمل
- [ ] `curl http://localhost:5000/api/health` يرد بنجاح

---

**تاريخ الإنشاء:** 2026-01-31  
**الحالة:** ✅ جاهز للاستخدام
