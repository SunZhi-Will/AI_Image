from flask import Flask, request, jsonify, send_file
from gradio_client import Client
import io
import requests
from PIL import Image

app = Flask(__name__)

# 初始化 Gradio client
client = Client("radames/Real-Time-Text-to-Image-SDXL-Lightning")

@app.route('/generate_image', methods=['POST'])
def generate_image():
    # 從 POST 請求中獲取參數
    text = request.json.get('text')  # 假設傳入的 JSON 數據中有一個 'text' 鍵，代表文本內容

    result = client.predict(api_name="/get_random_value")
    # 使用 Gradio client 生成圖片
    result = client.predict(text, result, api_name="/predict")

    # 從服務器獲取圖片
    response = requests.get(client.src + "/file=" + result)
    image_bytes = io.BytesIO(response.content)
    img = Image.open(image_bytes)

    # 將圖片返回給客戶端
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route('/generate_image_url', methods=['POST'])
def generate_image():
    # 從 POST 請求中獲取參數
    text = request.json.get('text')  # 假設傳入的 JSON 數據中有一個 'text' 鍵，代表文本內容

    result = client.predict(api_name="/get_random_value")
    # 使用 Gradio client 生成圖片
    result = client.predict(text, result, api_name="/predict")

    
    
    
    return client.src + "/file=" + result

if __name__ == '__main__':
    app.run(debug=True)
