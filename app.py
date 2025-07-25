from flask import Flask, render_template, request
import http.client
import ssl
from urllib.parse import urlencode

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    color = "black"
    phone = ""
    body = ""

    if request.method == 'POST':
        phone = request.form['phone']
        body = request.form['message']

        if not phone or not body:
            message = "يرجى ملء جميع الحقول"
            color = "red"
        else:
            try:
                conn = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())
                params = {
                    'token': 'g1gbcvl22h3nola8',  
                    'to': phone,
                    'body': body
                }
                payload = urlencode(params)
                headers = { 'Content-Type': "application/x-www-form-urlencoded" }

                conn.request("POST", "/instance134983/messages/chat", payload, headers)
                res = conn.getresponse()
                data = res.read().decode("utf-8")

                if '"sent":true' in data:
                    message = "✅ تم الإرسال بنجاح"
                    color = "green"
                    phone = ""
                    body = ""
                else:
                    message = f"❌ فشل في الإرسال: {data}"
                    color = "red"

            except Exception as e:
                message = f"❌ خطأ: {str(e)}"
                color = "red"

    return render_template("index.html", message=message, color=color, phone=phone, body=body)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway provides this
    app.run(debug=False, host="0.0.0.0", port=port)
