from flask import Flask, request, render_template, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_DIR = "data"
# Check if upload dir exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
app = Flask(__name__)
app.config['DIR'] = UPLOAD_DIR


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        # Check if the extension is valid
        if '.' in f.filename:
            extension = f.filename.rsplit('.', 1)[1]
            # Check if the file is in  csv format
            if extension.lower() == "csv":
                # Duplicate file will be replaced directly
                f.save(os.path.join(app.config['DIR'], secure_filename(f.filename)))
                return "File is upload correctly"

    return "File does not upload"


if __name__ == "__main__":
    app.run(debug=True)
