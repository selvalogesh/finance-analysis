import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pdf_to_excel import pdf_to_excel

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
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)

        output_csv_path = os.path.join('output', f"{os.path.splitext(filename)[0]}.csv")
        os.makedirs('output', exist_ok=True)

        try:
            pdf_to_excel(pdf_path, csv_path=output_csv_path)
            return jsonify({"message": f"File successfully converted and saved to {output_csv_path}"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type, please upload a PDF"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
