from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""

    if request.method == "POST":
        file = request.files.get("image")

        if file:
            text = "⚠️ OCR works only on local system.\nApp deployed successfully online."

            return redirect(url_for("result", text=text))

    return render_template("index.html", extracted_text=text)


@app.route("/result")
def result():
    text = request.args.get("text", "")
    return render_template("index.html", extracted_text=text)


# 👇 IMPORTANT FOR RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)