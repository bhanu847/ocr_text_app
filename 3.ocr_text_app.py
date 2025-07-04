from flask import Flask, request, render_template_string, flash, redirect
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import os
import io

# Set your tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
app.secret_key = "secret-key"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff", "webp"}

# HTML UI (Bootstrap 5)
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>OCR App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light py-5">
    <div class="container">
      <h1 class="text-center mb-4">OCR: Extract Text from Image</h1>

      {% with msgs = get_flashed_messages() %}
        {% if msgs %}
          <div class="alert alert-warning">{{ msgs[0] }}</div>
        {% endif %}
      {% endwith %}

      <form method="POST" enctype="multipart/form-data" class="card p-4 shadow-sm">
        <div class="mb-3">
          <input class="form-control" type="file" name="image" required>
        </div>
        <button class="btn btn-primary">Extract Text</button>
      </form>

      {% if ocr_text %}
      <div class="card mt-4 p-3 shadow-sm">
        <h5>Extracted Text:</h5>
        <pre style="white-space: pre-wrap;">{{ ocr_text }}</pre>
      </div>
      {% endif %}
    </div>
  </body>
</html>
"""


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    ocr_text = ""
    if request.method == "POST":
        file = request.files.get("image")
        if not file or file.filename == "":
            flash("No file selected.")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Unsupported file type.")
            return redirect(request.url)

        try:
            # Read image using PIL
            image = Image.open(io.BytesIO(file.read()))
            ocr_text = pytesseract.image_to_string(image)
        except Exception as e:
            flash(f"Error processing image: {e}")
            return redirect(request.url)

    return render_template_string(HTML_TEMPLATE, ocr_text=ocr_text)


if __name__ == "__main__":
    # pip install flask pillow pytesseract
    app.run(debug=True)
