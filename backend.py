from flask import Flask, request, jsonify, session
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)  # السماح بطلبات من Streamlit

# تخزين مؤقت للجلسات (في الإنتاج استخدم قاعدة بيانات)
sessions = {}

@app.route('/pi-auth', methods=['POST'])
def pi_auth():
    data = request.get_json()
    access_token = data.get('accessToken')
    if not access_token:
        return jsonify({'error': 'Missing access token'}), 400

    # التحقق من التوكن عبر Pi API
    url = 'https://api.minepi.com/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return jsonify({'error': 'Invalid token', 'details': resp.text}), 401

        user_data = resp.json()
        # تخزين معلومات المستخدم في جلسة (في الإنتاج استخدم قاعدة بيانات)
        user_id = user_data.get('uid')
        sessions[user_id] = user_data
        return jsonify({'status': 'success', 'user': user_data})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pi-user/<uid>', methods=['GET'])
def get_user(uid):
    user = sessions.get(uid)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/pi-logout', methods=['POST'])
def logout():
    # في تطبيق حقيقي، قم بحذف الجلسة أو التوكن
    return jsonify({'status': 'logged out'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
