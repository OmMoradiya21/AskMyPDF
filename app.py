import os
from flask import Flask, render_template, request, jsonify
import pdfplumber
import docx

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(filename)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(filename)

        # Store extracted text in a global variable or database (for demo, we'll use a global variable)
        app.config['extracted_text'] = text

        return jsonify({'message': 'File uploaded and text extracted successfully!'})
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PDF or DOCX.'})

# Route to process question and get answer
@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form['question']
    context = app.config.get('extracted_text', '')

    if not context:
        return jsonify({'error': 'No document content available. Please upload a file first.'})

    # Use the QA model to find the answer

    return jsonify({'answer': result['answer']})

if __name__ == '__main__':
    app.run(debug=True)