from flask import Flask, render_template, request, url_for
from gtts import gTTS
from werkzeug.utils import secure_filename
import os
import predict 

# Import your caption function
from predict import generate_caption

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
AUDIO_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():

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

        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        image.save(image_path)

        # Generate caption
        caption = generate_caption(image_path)

        # Generate audio only if caption exists
        if caption:

            audio_file = "caption.mp3"

            audio_path = os.path.join(
                app.config["AUDIO_FOLDER"],
                audio_file
            )

            try:
                tts = gTTS(text=caption, lang="en")
                tts.save(audio_path)

                print("Audio saved:", audio_path)
                print("Size:", os.path.getsize(audio_path), "bytes")

                audio_url = url_for(
                    "static",
                    filename=f"audio/{audio_file}"
                )

            except Exception as e:
                print("TTS Error:", e)

        image_url = url_for(
            "static",
            filename=f"uploads/{filename}"
        )

    return render_template(
        "index.html",
        caption=caption,
        image_path=image_url,
        audio_path=audio_url
    )


if __name__ == "__main__":
    app.run(debug=True)