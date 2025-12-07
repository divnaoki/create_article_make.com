from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # フラッシュメッセージ用に必要

# 環境変数からWebhook URLを取得
WEBHOOK_URL = os.environ.get("MAKE_WEBHOOK_URL", "")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # フォームからデータを取得
        filename = request.form.get('filename')
        instruction = request.form.get('instruction')
        experience = request.form.get('experience')

        # バリデーション（空チェック）
        if not filename or not instruction or not experience:
            flash('全ての項目を入力してください', 'error')
            return redirect(url_for('index'))

        # Make.comへ送るJSONデータの作成
        # 以前のスクリプトと同じ構造にします
        payload = {
            "articles": [
                {
                    "filename": filename,
                    "instruction": instruction,
                    "experience": experience
                }
            ]
        }

        try:
            # Make.comへPOST送信
            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                flash(f'リクエストを送信しました！ Google Driveに "{filename}.md" が生成されるまでお待ちください。', 'success')
            else:
                flash(f'送信エラー: {response.status_code}', 'error')

        except Exception as e:
            flash(f'通信エラーが発生しました: {str(e)}', 'error')

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020)