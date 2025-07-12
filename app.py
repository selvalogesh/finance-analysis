import os
import hashlib
import subprocess
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.pdf'):
        file_hash = hashlib.sha256(file.read()).hexdigest()
        file.seek(0)
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_{file_hash}{ext}"

        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        
        output_csv_path = os.path.join('output', f"{os.path.splitext(new_filename)[0]}.csv")
        os.makedirs('output', exist_ok=True)

        if os.path.exists(pdf_path) and os.path.exists(output_csv_path):
            return jsonify({"message": f"File {name}{ext} already exists."}), 200

        file.save(pdf_path)

        try:
            command = f"python pdf_to_excel.py --csv {output_csv_path} {pdf_path}"
            subprocess.Popen(command, shell=True)
            return jsonify({"message": f"File upload successful. Conversion started for {new_filename}. Output will be at {output_csv_path}"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type, please upload a PDF"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
