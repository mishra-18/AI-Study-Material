from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
from pdfReader import FlashCards, Quiz, QuestionBank
UPLOAD_FOLDER = os.getcwd() 
ALLOWED_EXTENSIONS = {'pdf'}
print("HOLA" , UPLOAD_FOLDER)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # Checks if the file's right!
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)
        # saves the pdf file in the working dir i.e. APP/
            file.save(file_path)
            return render_template('content.html', filename=filename)
    else:
        filename = None
    return render_template('upload.html', filename=filename)

# Rendering the Genereated MCQ Page
@app.route('/mcq/<filename>')
def mcq(filename):
    mcqs = Quiz(pdf=filename)
    return render_template('mcqs.html', filename=filename, mcqs=mcqs)

# Rendering the Generated Flashcards Page
@app.route('/flashcards/<filename>')
def flashcards(filename):

    #Get the resource type
    resourceType = request.args.get('resourceType', type=int)
    flashcards = FlashCards(pdf=filename, resourceType=resourceType)
    return render_template('flashcards.html', filename=filename, flashcards=flashcards)

# Rendering the Question Bank's page
@app.route('/questionbank/<filename>')
def question_bank(filename):
    
    #Get the resource type
    resourceType = request.args.get('resourceType', type=int)
    QnAs = QuestionBank(filename, resourceType=resourceType)
    return render_template('question_bank.html', filename=filename, QnAs=QnAs)

if __name__ == '__main__':
    app.run(debug=True)