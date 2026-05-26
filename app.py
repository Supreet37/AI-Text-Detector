
import pickle
from flask import Flask, render_template, request
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter

nltk.download('punkt', quiet=True)
app = Flask(__name__)

# Load models
model = pickle.load(open('sentence_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
'''
def predict_paragraph(paragraph):
    sentences = sent_tokenize(paragraph)
    results = []
    
    for sentence in sentences:
        if len(sentence.split()) < 3:
            continue
        vec = vectorizer.transform([sentence])
        pred = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0]
        
        results.append({
            'sentence': sentence,
            'prediction': 'AI' if pred == 1 else 'Human',
            'confidence': round(max(prob) * 100, 2),
            'ai_probability': round(prob[1] * 100, 2),
            'human_probability': round(prob[0] * 100, 2)
        })
    
    if not results:
        return {'prediction': 'UNKNOWN', 'confidence': 0, 'sentence_results': []}
    
    predictions = [r['prediction'] for r in results]
    majority = Counter(predictions).most_common(1)[0]
    avg_ai = sum(r['ai_probability'] for r in results) / len(results)
    
    return {
        'prediction': majority[0],
        'confidence': round((majority[1] / len(predictions)) * 100, 2),
        'avg_ai_probability': round(avg_ai, 2),
        'total_sentences': len(sentences),
        'analyzed_sentences': len(results),
        'ai_sentence_count': predictions.count('AI'),
        'human_sentence_count': predictions.count('Human'),
        'sentence_results': results
    }
'''

def predict_paragraph(paragraph):
    # Detect content type FIRST
    content_type, content_conf = detect_content_type(paragraph)
    
    # Check if it's code
    if content_type == 'Code':
        return {
            'prediction': 'CODE',
            'confidence': content_conf,
            'avg_ai_probability': 0,
            'total_sentences': 1,
            'analyzed_sentences': 1,
            'ai_sentence_count': 0,
            'human_sentence_count': 0,
            'content_type': content_type,
            'content_type_confidence': content_conf,
            'sentence_results': [{
                'sentence': paragraph[:150],
                'prediction': 'CODE',
                'confidence': content_conf,
                'ai_probability': 0,
                'human_probability': 0
            }]
        }
    
    # Rest of your existing code for AI/Human detection...
    sentences = sent_tokenize(paragraph)
    results = []
    
    for sentence in sentences:
        if len(sentence.split()) < 3:
            continue
        vec = vectorizer.transform([sentence])
        pred = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0]
        
        results.append({
            'sentence': sentence,
            'prediction': 'AI' if pred == 1 else 'Human',
            'confidence': round(max(prob) * 100, 2),
            'ai_probability': round(prob[1] * 100, 2),
            'human_probability': round(prob[0] * 100, 2)
        })
    
    if not results:
        return {
            'prediction': 'UNKNOWN',
            'confidence': 0,
            'content_type': content_type,
            'content_type_confidence': content_conf,
            'sentence_results': []
        }
    
    predictions = [r['prediction'] for r in results]
    majority = Counter(predictions).most_common(1)[0]
    avg_ai = sum(r['ai_probability'] for r in results) / len(results)
    
    return {
        'prediction': majority[0],
        'confidence': round((majority[1] / len(predictions)) * 100, 2),
        'avg_ai_probability': round(avg_ai, 2),
        'total_sentences': len(sentences),
        'analyzed_sentences': len(results),
        'ai_sentence_count': predictions.count('AI'),
        'human_sentence_count': predictions.count('Human'),
        'content_type': content_type,
        'content_type_confidence': content_conf,
        'sentence_results': results
    }

def extract_features(text):
    words = text.split()
    is_code = any(x in text for x in ['def ', 'import ', 'class ', '#include'])
    
    complexity = 5
    if words:
        avg_len = sum(len(w) for w in words) / len(words)
        unique_ratio = len(set(words)) / len(words)
        if avg_len > 6: complexity += 1
        if unique_ratio > 0.7: complexity += 1
        if len(words) > 200: complexity += 1
        if len(words) < 20: complexity -= 1
    
    return {
        'word_count': len(words),
        'char_count': len(text),
        'sentence_count': text.count('.') + text.count('!') + text.count('?'),
        'avg_word_length': round(sum(len(w) for w in words) / len(words), 1) if words else 0,
        'type': 'Code' if is_code else 'Text',
        'language': 'Python' if 'def ' in text else 'English',
        'complexity_score': max(1, min(10, complexity))
    }

def detect_content_type(text):
    '''Manually detect content type based on keywords'''
    text_lower = text.lower()
    
    # News indicators
    news_keywords = ['breaking', 'reports say', 'according to sources', 'announced today', 'president', 'government', 'election', 'crisis', 'update']
    # Blog indicators  
    blog_keywords = ['in my opinion', 'i think', 'i believe', 'personally', 'my experience', 'i feel', 'thoughts on']
    # Academic indicators
    academic_keywords = ['research shows', 'study finds', 'according to research', 'hypothesis', 'methodology', 'findings indicate', 'literature review']
    # Product Review indicators
    review_keywords = ['highly recommend', 'stars', 'worth buying', 'excellent product', 'poor quality', 'battery life', 'customer service']
    # Creative Writing indicators
    creative_keywords = ['once upon a time', 'whispered', 'gazed', 'mysterious', 'adventure', 'dreamed', 'magical']
    # Technical/Code indicators
    code_keywords = ['def ', 'import ', 'class ', 'function(', 'var ', 'const ', 'console.log', 'print(', 'return ', '#include']
    
    # Check for code first
    for keyword in code_keywords:
        if keyword in text:
            return 'Code', 95
    
    # Check each category
    scores = {}
    
    for keyword in news_keywords:
        if keyword in text_lower:
            scores['News'] = scores.get('News', 0) + 10
    
    for keyword in blog_keywords:
        if keyword in text_lower:
            scores['Blog'] = scores.get('Blog', 0) + 10
    
    for keyword in academic_keywords:
        if keyword in text_lower:
            scores['Academic'] = scores.get('Academic', 0) + 10
    
    for keyword in review_keywords:
        if keyword in text_lower:
            scores['Product Review'] = scores.get('Product Review', 0) + 10
    
    for keyword in creative_keywords:
        if keyword in text_lower:
            scores['Creative Writing'] = scores.get('Creative Writing', 0) + 10
    
    # Also check length patterns
    word_count = len(text.split())
    if word_count > 500:
        scores['Academic'] = scores.get('Academic', 0) + 15
    elif 50 < word_count < 300:
        scores['Blog'] = scores.get('Blog', 0) + 10
    elif word_count < 50:
        scores['News'] = scores.get('News', 0) + 10
    
    if not scores:
        return 'General Text', 70
    
    # Get best match
    best_type = max(scores, key=scores.get)
    confidence = min(scores[best_type] + 50, 95)
    
    return best_type, confidence

@app.route('/')
def home():
    # New landing page
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Analysis dashboard (the old index.html)
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    if len(text.strip()) < 10:
        return render_template('result.html', error="Please enter at least 10 characters")
    
    result = predict_paragraph(text)
    features = extract_features(text)
    
    return render_template('result.html', result=result, features=features, original_text=text)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

# import os
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(debug=False, host='0.0.0.0', port=port)

if __name__ == '__main__':
    app.run()


