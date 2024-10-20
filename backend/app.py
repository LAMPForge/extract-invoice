import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from services.invoice_service import process_invoice

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}, 400)

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}, 400)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            result = process_invoice(filepath)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}, 500)


if __name__ == '__main__':
    app.run(debug=True)
