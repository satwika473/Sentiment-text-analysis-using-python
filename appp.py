from flask import Flask, request, jsonify, render_template
import nltk
from textblob import TextBlob
from newspaper import Article

nltk.download('punkt')

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('m.html')
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    input_type = data.get('input_type')
    
    if input_type == 'url':
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        try:
            # Fetch and process the article from the URL
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            text = article.summary
        except Exception as e:
            return jsonify({'error': 'Failed to process the URL'}), 500

    elif input_type == 'text':
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

    # Perform sentiment analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    # Classify sentiment
    positive = 0
    neutral = 0
    negative = 0
    if sentiment > 0:
        positive = 1
    elif sentiment == 0:
        neutral = 1
    else:
        negative = 1

    return jsonify({
        'positive': positive,
        'neutral': neutral,
        'negative': negative
    })

if __name__ == '__main__':
    app.run(debug=True)
