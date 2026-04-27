from flask import Flask, render_template, request, send_file, redirect, url_for
import pytesseract
from PIL import Image
import os
import io
import urllib.parse
from pdf2image import convert_from_path

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename != "":
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = ""

            try:
                # 📄 If PDF
                if file.filename.lower().endswith(".pdf"):
                    images = convert_from_path(filepath)

                    for img in images:
                        text += pytesseract.image_to_string(img) + "\n"

                # 🖼️ If Image
                else:
                    img = Image.open(filepath)
                    text = pytesseract.image_to_string(img)

            except Exception as e:
                text = f"Error processing file: {str(e)}"

            # redirect with text
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