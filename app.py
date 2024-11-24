from flask import Flask, render_template, request, jsonify
from summary_logic import summarizer, translate_text
from googletrans import LANGUAGES

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect_language', methods=['POST'])
def detect_language():
    data = request.json
    rawtext = data.get("rawtext")
    _, detected_lang = translate_text(rawtext)  # Detect language only
    detected_lang_full = LANGUAGES.get(detected_lang, "Unknown Language")
    return jsonify({"detected_lang": detected_lang_full})

@app.route('/analyse', methods=['POST'])
def analyse():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        
        # Get custom parameters from the form
        summary_ratio = float(request.form.get('summary_ratio', 0.3))  # Default to 0.3 if not provided
        max_sentences = request.form.get('max_sentences', None)
        
        # Convert max_sentences to an integer if provided
        if max_sentences:
            max_sentences = int(max_sentences)
        else:
            max_sentences = None  # Allow default ratio behavior
        
        # Get the summary from summarizer function
        summary, original_txt, len_orig_txt, len_summary = summarizer(rawtext, summary_ratio, max_sentences)
        
        # Return the results to the summary page
        return render_template('summary.html', summary=summary, original_txt=original_txt, 
                               len_orig_txt=len_orig_txt, len_summary=len_summary)

if __name__ == "__main__":
    app.run(debug=True)

