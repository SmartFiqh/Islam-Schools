import streamlit as st
import requests

# إعدادات الخادم الخلفي
BACKEND_URL = "http://localhost:5000"  # غيّر هذا في الإنتاج

# تهيئة حالة الجلسة
if 'pi_user' not in st.session_state:
    st.session_state.pi_user = None

st.set_page_config(
    page_title="تطبيق Pi Network",
    page_icon="π",
    layout="wide"
)

st.title("🔐 تطبيق Pi Network - مصادقة متكاملة")

# ==========================================================
# ✅ فحص اتصال يظهر في الصفحة الرئيسية مباشرة (وليس داخل الإطار
# المضمّن)، ليكون واضحاً فوراً هل الخادم الخلفي يعمل أصلاً أم لا،
# بدل الاعتماد على أخطاء مخفية داخل الـ iframe لا تظهر عند نسخ نص
# الصفحة.
# ==========================================================
with st.expander("🔧 فحص الاتصال بالخادم الخلفي", expanded=(st.session_state.pi_user is None)):
    if st.button("فحص الآن"):
        try:
            health_resp = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if health_resp.status_code == 200:
                st.success(f"✅ الخادم الخلفي يعمل ويستجيب على {BACKEND_URL}")
            else:
                st.error(f"⚠️ الخادم الخلفي استجاب برمز غير متوقع: {health_resp.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(
                f"❌ تعذّر الاتصال بـ {BACKEND_URL} — الخادم الخلفي غير مُشغَّل. "
                "افتح طرفية (terminal) منفصلة وشغّل: `python backend.py`، ثم اضغط فحص الآن مجدداً."
            )
        except requests.exceptions.Timeout:
            st.error(f"❌ انتهت مهلة الاتصال بـ {BACKEND_URL} (لم يستجب خلال 5 ثوانٍ).")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ خطأ في الاتصال: {e}")
    else:
        st.caption("اضغط الزر أعلاه للتأكد من أن `backend.py` يعمل قبل محاولة تسجيل الدخول.")

# ==========================================================
# ✅ إصلاح: استقبال uid من الرابط بعد المصادقة، والتحقق منه
# من الخادم الخلفي مباشرة (بدلاً من الوثوق ببيانات JSON قادمة
# من المتصفح مباشرة، والتي كان يمكن لأي شخص تلفيقها يدوياً في
# الرابط والدخول بهوية مزوّرة).
# ==========================================================
params = st.query_params
if 'pi_uid' in params and not st.session_state.pi_user:
    uid = params['pi_uid']
    try:
        resp = requests.get(f"{BACKEND_URL}/pi-user/{uid}", timeout=10)
        if resp.status_code == 200:
            st.session_state.pi_user = resp.json()
        else:
            st.error("تعذّر التحقق من هوية المستخدم من الخادم الخلفي. حاول تسجيل الدخول مرة أخرى.")
    except requests.exceptions.RequestException as e:
        st.error(f"تعذّر الاتصال بالخادم الخلفي: {e}")
    finally:
        st.query_params.clear()
        st.rerun()

# عرض حالة المستخدم
if st.session_state.pi_user:
    st.success(f"✅ مرحباً {st.session_state.pi_user.get('username', 'مستخدم')} (UID: {st.session_state.pi_user.get('uid', 'N/A')})")
    if st.button("تسجيل الخروج"):
        st.session_state.pi_user = None
        st.rerun()
else:
    st.info("👋 لم تقم بتسجيل الدخول بعد. استخدم زر تسجيل الدخول أدناه.")
    st.caption(
        "⚠️ تسجيل الدخول عبر Pi Network يعمل فقط داخل تطبيق **Pi Browser** الرسمي، "
        "وليس داخل متصفح عادي مثل Chrome أو Firefox — إن كنت تختبر خارج Pi Browser "
        "فستظهر رسالة خطأ من Pi SDK داخل مربع تسجيل الدخول أدناه، وهذا متوقع."
    )

# ==========================================================
# تضمين واجهة HTML/JS لمصادقة Pi — تُعرض فقط إن لم يكن المستخدم
# مسجلاً دخوله بعد (✅ إصلاح: كانت تُعرض دائماً حتى بعد تسجيل
# الدخول، فتُعيد تشغيل نافذة Pi في كل مرة يُعاد فيها رسم الصفحة).
# ==========================================================
if not st.session_state.pi_user:
    html_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://sdk.minepi.com/pi-sdk.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; text-align: center; padding: 20px; }
        #status { margin-top: 20px; font-size: 18px; color: #333; }
        button { padding: 12px 28px; font-size: 18px; background-color: #1e3a2f; color: white; border: none; border-radius: 8px; cursor: pointer; }
        button:hover { background-color: #2a5c4a; }
        .loader { border: 4px solid #f3f3f3; border-top: 4px solid #1e3a2f; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div id="status">⏳ جاري التحقق من جلسة Pi...</div>
    <div id="loader" class="loader" style="display:none;"></div>
    <button id="signInBtn" style="display:none;">🔑 تسجيل الدخول عبر Pi Network</button>

    <script>
        const BACKEND_URL = "__BACKEND_URL__";  // يُحقن من Python أدناه لضمان تطابقه دائماً

        function onIncompletePaymentFound(payment) {
            console.log('دفعة غير مكتملة:', payment);
        }

        window.addEventListener('load', async function() {
            try {
                await Pi.init({ version: '2.0', sandbox: true });

                const auth = await Pi.authenticate(['username'], onIncompletePaymentFound);

                const response = await fetch(BACKEND_URL + '/pi-auth', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ accessToken: auth.accessToken })
                });

                if (response.ok) {
                    const data = await response.json();
                    const uid = data.user && data.user.uid;

                    if (!uid) {
                        document.getElementById('status').innerHTML = '❌ لم يُعِد الخادم الخلفي معرّف مستخدم صالح.';
                        document.getElementById('signInBtn').style.display = 'inline-block';
                        return;
                    }

                    document.getElementById('status').innerHTML = '✅ تم تسجيل الدخول بنجاح! جاري تحديث الصفحة...';
                    document.getElementById('signInBtn').style.display = 'none';

                    // ✅ إصلاح: نُعيد توجيه الصفحة الأصلية (وليس الإطار المضمّن
                    // فقط) بمعرّف uid حصراً، ليقوم Streamlit بالتحقق منه من
                    // الخادم الخلفي بنفسه بدل الوثوق بأي بيانات من المتصفح.
                    setTimeout(function () {
                        window.parent.location.href =
                            window.parent.location.pathname + '?pi_uid=' + encodeURIComponent(uid);
                    }, 800);
                } else {
                    const err = await response.json();
                    document.getElementById('status').innerHTML = '❌ فشل التحقق من التوكن: ' + (err.error || 'خطأ غير معروف');
                    document.getElementById('signInBtn').style.display = 'inline-block';
                }
            } catch (error) {
                console.error('خطأ في Pi Auth:', error);
                document.getElementById('status').innerHTML = '❌ حدث خطأ: ' + error.message;
                document.getElementById('signInBtn').style.display = 'inline-block';
            }
        });

        document.getElementById('signInBtn')?.addEventListener('click', function() {
            window.location.reload();
        });
    </script>
</body>
</html>
"""
    html_code = html_code.replace("__BACKEND_URL__", BACKEND_URL)
    st.components.v1.html(html_code, height=300)

# عرض معلومات إضافية بعد تسجيل الدخول
if st.session_state.pi_user:
    st.subheader("📋 معلومات حسابك")
    st.json(st.session_state.pi_user)

    st.markdown("---")
    st.markdown("✨ هذا هو المحتوى الحصري للمستخدمين المسجلين.")
else:
    st.markdown("📢 قم بتسجيل الدخول لعرض محتوى مخصص.")

if __name__ == "__main__":
    st.write("🔧 تأكد من تشغيل الخادم الخلفي: python backend.py")
