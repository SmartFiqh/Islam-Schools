from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)  # السماح بطلبات من Streamlit — قيّد هذا لنطاقك الفعلي في الإنتاج

# تخزين مؤقت للجلسات (في الإنتاج استخدم قاعدة بيانات فعلية؛ هذا القاموس
# يُفرَّغ بالكامل عند إعادة تشغيل الخادم)
sessions = {}


@app.route('/pi-auth', methods=['POST'])
def pi_auth():
    data = request.get_json(silent=True) or {}
    access_token = data.get('accessToken')
    if not access_token:
        return jsonify({'error': 'Missing access token'}), 400

    url = 'https://api.minepi.com/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 502

    if resp.status_code != 200:
        return jsonify({'error': 'Invalid token', 'details': resp.text}), 401

    # ✅ إصلاح: resp.json() يمكن أن يفشل إن أعادت Pi API استجابة غير
    # JSON (مثلاً صفحة خطأ HTML)، وكان هذا يتسبب سابقاً بخطأ 500 غير
    # معالَج بدل رسالة خطأ واضحة للعميل.
    try:
        user_data = resp.json()
    except ValueError:
        return jsonify({'error': 'Unexpected response format from Pi API'}), 502

    user_id = user_data.get('uid')
    if not user_id:
        return jsonify({'error': 'Pi API response missing uid'}), 502

    sessions[user_id] = user_data
    return jsonify({'status': 'success', 'user': user_data})


@app.route('/pi-user/<uid>', methods=['GET'])
def get_user(uid):
    user = sessions.get(uid)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


@app.route('/pi-logout', methods=['POST'])
def logout():
    data = request.get_json(silent=True) or {}
    uid = data.get('uid')
    if uid:
        sessions.pop(uid, None)
    return jsonify({'status': 'logged out'})


if __name__ == '__main__':
    # debug=True مناسب فقط للتطوير المحلي — يفتح ثغرة تنفيذ كود عن بُعد
    # (Werkzeug debugger) إن كان الخادم مكشوفاً على الشبكة. عطّله في الإنتاج.
    app.run(debug=True, port=5000)
