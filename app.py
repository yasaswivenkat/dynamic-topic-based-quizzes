from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate-quiz', methods=['GET'])
def generate_quiz():
    topic = request.args.get('topic', 'default')
    num_questions = int(request.args.get('num_questions', 5))
    
    # Example: Generate dummy questions
    questions = [f"Question {i+1} on {topic}" for i in range(num_questions)]
    return jsonify({"topic": topic, "questions": questions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
