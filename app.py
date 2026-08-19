import streamlit as st
import requests
import json

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

# عرض حالة المستخدم
if st.session_state.pi_user:
    st.success(f"✅ مرحباً {st.session_state.pi_user.get('username', 'مستخدم')} (UID: {st.session_state.pi_user.get('uid', 'N/A')})")
    if st.button("تسجيل الخروج"):
        st.session_state.pi_user = None
        st.rerun()
else:
    st.info("👋 لم تقم بتسجيل الدخول بعد. استخدم زر تسجيل الدخول أدناه.")

# ==========================================================
# تضمين واجهة HTML/JS لمصادقة Pi
# ==========================================================
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
        const BACKEND_URL = "http://localhost:5000";  // يجب أن يتطابق مع عنوان الخادم الخلفي

        // دالة للتعامل مع المدفوعات غير المكتملة (مطلوبة لكننا لا نستخدمها)
        function onIncompletePaymentFound(payment) {
            console.log('دفعة غير مكتملة:', payment);
            // يمكنك معالجتها إذا كنت تستخدم المدفوعات
        }

        // تشغيل المصادقة تلقائياً عند تحميل الصفحة
        window.addEventListener('load', async function() {
            try {
                // 1. تهيئة Pi SDK (sandbox: true للتطوير)
                await Pi.init({ version: '2.0', sandbox: true });

                // 2. استدعاء المصادقة
                const auth = await Pi.authenticate(['username'], onIncompletePaymentFound);

                // 3. إرسال التوكن إلى الخادم الخلفي
                const response = await fetch(BACKEND_URL + '/pi-auth', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ accessToken: auth.accessToken })
                });

                if (response.ok) {
                    const data = await response.json();
                    // تحديث واجهة Streamlit عبر إعادة التحميل مع تمرير بيانات المستخدم
                    // نستخدم window.parent.postMessage لإرسال البيانات إلى Streamlit
                    window.parent.postMessage({
                        type: 'pi_auth_success',
                        user: data.user
                    }, '*');
                    document.getElementById('status').innerHTML = '✅ تم تسجيل الدخول بنجاح! جاري تحديث الصفحة...';
                    document.getElementById('signInBtn').style.display = 'none';
                    // إعادة تحميل الصفحة بعد لحظة
                    setTimeout(() => { window.location.reload(); }, 1500);
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

        // زر تسجيل الدخول اليدوي
        document.getElementById('signInBtn')?.addEventListener('click', function() {
            window.location.reload();  // إعادة تحميل الصفحة لتشغيل المصادقة مرة أخرى
        });
    </script>
</body>
</html>
"""

# عرض HTML في Streamlit
st.components.v1.html(html_code, height=300)

# استقبال بيانات المستخدم من JavaScript (عبر استعلام أو session)
# في هذه النسخة، نعتمد على إعادة تحميل الصفحة بعد المصادقة.
# بدلاً من ذلك، يمكنك استخدام st.query_params أو st.session_state.

# إذا تم تمرير بيانات المستخدم عبر query params (اختياري)
params = st.query_params
if 'pi_user' in params:
    try:
        user = json.loads(params['pi_user'])
        st.session_state.pi_user = user
        # إزالة المعامل من الرابط
        st.query_params.clear()
        st.rerun()
    except:
        pass

# عرض معلومات إضافية بعد تسجيل الدخول
if st.session_state.pi_user:
    st.subheader("📋 معلومات حسابك")
    st.json(st.session_state.pi_user)

    # يمكنك إضافة المزيد من الميزات هنا (مثل عرض محتوى خاص)
    st.markdown("---")
    st.markdown("✨ هذا هو المحتوى الحصري للمستخدمين المسجلين.")
else:
    # عرض محتوى عام
    st.markdown("📢 قم بتسجيل الدخول لعرض محتوى مخصص.")

# تشغيل الخادم الخلفي (للاستخدام المحلي فقط)
if __name__ == "__main__":
    st.write("🔧 تأكد من تشغيل الخادم الخلفي: python backend.py")
