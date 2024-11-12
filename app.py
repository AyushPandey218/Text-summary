
from flask import Flask, render_template, request, jsonify
from summary_logic import summarizer
from summary_logic import translate_text
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
        summary, original_txt, len_orig_txt, len_summary = summarizer(rawtext)
        return render_template('summary.html', summary=summary, original_txt=original_txt, len_orig_txt=len_orig_txt, len_summary=len_summary)
    
if __name__ == "__main__":
    app.run(debug=True)
