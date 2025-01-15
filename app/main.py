from flask import Flask, request, make_response
import pdfkit
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

# needs to be setup on server as pat
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

#config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
path_wkhtmltopdf = "/usr/bin/wkhtmltopdf"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf) # because chatgpt said so

# Check documentation for more options
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}

# Post request handler
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    html_content = data.get('html', '') # get html part in json
    pdf_content = pdfkit.from_string(html_content, False, configuration=config, options=options) # conversion
    response = make_response(pdf_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=my_document.pdf'
    return response
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)