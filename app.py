import base64
import requests
import mimetypes
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# ✅ Load environment variables
load_dotenv() 
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    if 'image' not in request.files:
        return jsonify({"error": "❌ No image uploaded!"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "❌ No selected file!"}), 400

    # ✅ Read image from memory
    image_bytes = image.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    # Guess mime type
    mime_type = mimetypes.guess_type(image.filename)[0] or "image/jpeg"

    # Gemini Payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": base64_image
                        }
                    },
                    {
                        "text": (
                            "Generate 5 short, creative, engaging social media captions for this image. "
                            "Each caption should be expressive, one line only, and include emojis if appropriate. "
                            "List each on a separate line."
                        )
                    }
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    # ✅ Send request to Gemini API
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers, params=params)

    try:
        response_data = response.json()
        print("🔍 Gemini API raw response:", response_data)  # Debug log

        # Check if candidates exist
        if "candidates" not in response_data:
            return jsonify({
                "error": "❌ Gemini API did not return any caption candidates. Please check your API key or usage quota.",
                "details": response_data  # Helpful for debugging
            }), 500

        caption = response_data["candidates"][0]["content"]["parts"][0]["text"]

        # ✅ Return base64 image + multiple captions
        image_data_uri = f"data:{mime_type};base64,{base64_image}"
        return jsonify({
            "caption": caption,
            "image_url": image_data_uri
        })

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        return jsonify({"error": f"❌ Failed to generate caption. {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use port from environment or default to 5000
    app.run(host='0.0.0.0', port=port)
