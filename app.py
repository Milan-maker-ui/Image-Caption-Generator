from flask import Flask, render_template, request, url_for, send_file

from gtts import gTTS
from werkzeug.utils import secure_filename
import os

# DEBUG
print("Current Directory:", os.getcwd())
print("Templates Exists:", os.path.exists("templates/index.html"))
print("Templates Folder Exists:", os.path.exists("templates"))

if os.path.exists("templates"):
    print("Files in Templates:", os.listdir("templates"))

from predict import generate_caption

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
AUDIO_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER

latest_caption = ""

@app.route("/", methods=["GET", "POST"])
def index():

    global latest_caption
    caption = None
    image_url = None
    audio_url = None

    if request.method == "POST":

        if "image" not in request.files:
            return render_template("index.html")
        
        image = request.files["image"]

        if image.filename == "":
            return render_template("index.html")

        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)

        # Generate Caption
        caption = generate_caption(image_path)
        latest_caption = caption
        image_url = url_for("static", filename=f"uploads/{filename}")

        # Generate Audio
        if caption:
            audio_file = "caption.mp3"
            audio_path = os.path.join(app.config["AUDIO_FOLDER"], audio_file)

            try:
                tts = gTTS(text=caption, lang="en")
                tts.save(audio_path)
                audio_url = url_for("static", filename=f"audio/{audio_file}")

            except Exception as e:
                print("TTS Error:", e)

    return render_template("index.html", caption=caption, image_path=image_url, audio_path=audio_url)


@app.route("/download")
def download_caption():

    global latest_caption
    file_path = "caption.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(latest_caption)

    return send_file(file_path, as_attachment=True)

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response 


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True)
