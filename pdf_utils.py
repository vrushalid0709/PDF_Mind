from flask import Flask,jsonify,request
import PyPDF2

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    full_text = ""

    for page in reader.pages :

        text = page.extract_text()

        if text :
            full_text += text + "\n"
    return full_text