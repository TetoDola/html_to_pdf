from flask import Flask, request, make_response, jsonify, url_for
import pdfkit
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# config
path_wkhtmltopdf = "/usr/bin/wkhtmltopdf"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Check documentation for more options
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}

PDF_STORAGE_DIR = 'pdf_storage'
os.makedirs(PDF_STORAGE_DIR, exist_ok=True)  # Create if it doesn't exist


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    html_content = data.get('html', '')  # Get HTML part in JSON
    filename = secure_filename(data.get('filename', 'document.pdf'))  # filename option
    filepath = os.path.join(PDF_STORAGE_DIR, filename)
    pdfkit.from_string(html_content, filepath, configuration=config, options=options) # conversion
    download_url = url_for('download_pdf', filename=filename, _external=True) # link generation
    return jsonify({"message": "PDF generated successfully", "download_url": download_url})


@app.route('/download-pdf/<filename>', methods=['GET'])
def download_pdf(filename):
    filepath = os.path.join(PDF_STORAGE_DIR, secure_filename(filename))
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return make_response(open(filepath, 'rb').read(), 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename={filename}'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
