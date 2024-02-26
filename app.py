from flask import Flask, render_template, request
from text_summary import Extractive
from text_summary import Abstractive
from PyPDF2 import PdfReader
import re

app = Flask(__name__)

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()

    txt = text

    return txt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/abstractive')
def abstractive():
    return render_template('Abstractive.html')

@app.route('/extractive')
def extractive():
    return render_template('Extractive.html')

@app.route('/pdfextractive')
def pdfextractive():
    return render_template('pdf_ext.html')

@app.route('/pdfabstractive')
def pdfabstractive():
    return render_template('pdf_abst.html')

@app.route('/extractive_result', methods =['GET','POST'])
def result():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        summary, original_txt, len_orig_txt,len_summary = Extractive(rawtext)
        return render_template('extractive_result.html',summary=summary,original_txt = original_txt,len_orig=len_orig_txt,len_summ = len_summary)

@app.route('/abstractive_result', methods =['GET','POST'])
def result_abs():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        max_length = request.form['max']
        min_length = request.form['min']
        summary, original_text, length_org_txt, length_summary = Abstractive(rawtext,min_length,max_length)
        return render_template('abstractive_result.html',summary=summary,original_txt = original_text,org_len = length_org_txt,summ_len = length_summary)

@app.route('/extractiveresults', methods =['POST'])
def pdfextractiveres():
    if request.method == 'POST':
        rawtext = request.files['file']
        if rawtext:
            final = extract_text_from_pdf(rawtext)
            summary, original_txt, len_orig_txt,len_summary = Extractive(final)
            return render_template('extractive_result.html',summary=summary,original_txt = original_txt,len_orig=len_orig_txt,len_summ = len_summary)

@app.route('/abstractiveresults', methods =['POST'])
def pdfabstractiveres():
    if request.method == 'POST':
        rawtext = request.files['file']
        max_length = request.form['max']
        min_length = request.form['min']
        if rawtext:
            final = extract_text_from_pdf(rawtext)
            summary, original_text, length_org_txt, length_summary = Abstractive(final,min_length,max_length)
  
            return render_template('abstractive_result.html',summary=summary,original_txt = original_text,org_len = length_org_txt,summ_len = length_summary)
if __name__ == "__main__":
    app.run(debug=True)