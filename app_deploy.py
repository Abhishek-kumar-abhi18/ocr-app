from flask import Flask, render_template, request, send_file, redirect, url_for
import pytesseract
from PIL import Image
import os
import io
import urllib.parse
from pdf2image import convert_from_path

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = ""

            # 🔥 Check file type
            if file.filename.lower().endswith(".pdf"):
                images = convert_from_path(filepath)

                for img in images:
                    text += pytesseract.image_to_string(img) + "\n"

            else:
                img = Image.open(filepath)
                text = "OCR works on local system (not enabled online)"

            encoded_text = urllib.parse.quote(text)
            return redirect(url_for("result") + "?text=" + encoded_text)

    return render_template("index.html", extracted_text="")


@app.route("/result")
def result():
    text = request.args.get("text", "")
    decoded_text = urllib.parse.unquote(text)
    return render_template("index.html", extracted_text=decoded_text)


@app.route("/download", methods=["POST"])
def download():
    text = request.form.get("text", "")

    file = io.BytesIO()
    file.write(text.encode("utf-8"))
    file.seek(0)

    return send_file(
        file,
        as_attachment=True,
        download_name="extracted_text.txt",
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(debug=True)