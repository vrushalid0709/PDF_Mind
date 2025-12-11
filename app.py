from flask import Flask, jsonify, request, render_template
from pdf_utils import extract_text
from ai_utils import get_ai_summary, analyze_sentiment,extract_keywords
from db_utils import save_document
 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-pdf', methods=['POST'])
def upload_file():
    print("Upload request received")

    try:
        # Validate file
        if 'file' not in request.files:
            raise ValueError("No file part in request")

        file = request.files['file']
        if file.filename == '':
            raise ValueError("No file selected")

        filename = file.filename
        full_text = extract_text(file)
        summary = get_ai_summary(full_text)
        sentiment_label = analyze_sentiment(summary)
        keywords = []

        # Save to DB 
        response_json = save_document(
            filename=filename,
            summary=summary,
            sentiment=sentiment_label,
            keywords=keywords
        )

        # return json response
        return jsonify(response_json)

    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({
            "error": f"Failed to process the file: {str(e)}",
            "status": "error"
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
