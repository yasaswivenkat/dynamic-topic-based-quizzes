from flask import Flask, jsonify, request
from flask_cors import CORS
import openai

# Flask app setup
app = Flask(__name__)
CORS(app)  # Allow all domains or specify allowed domains

# Set your OpenAI API key here
openai.api_key = "your-openai-api-key"  # Replace with your actual API key

def generate_questions_with_openai(topic, num_questions):
    try:
        prompt = f"Generate {num_questions} multiple-choice questions about {topic}."
        
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can also try newer models like "gpt-3.5-turbo" if available
            prompt=prompt,
            max_tokens=150 * num_questions,  # Slightly increased to avoid truncation
            n=1,
            stop=None,
            temperature=0.7,
        )
        
        # Ensure questions are parsed correctly
        questions = [q.strip() for q in response.choices[0].text.strip().split('\n') if q.strip()]
        return questions
    except Exception as e:
        return str(e)

@app.route('/generate-quiz', methods=['GET'])
def generate_quiz():
    topic = request.args.get('topic')
    num_questions = request.args.get('num_questions')

    # Handle missing parameters
    if not topic or not num_questions:
        return jsonify({"error": "Please provide both 'topic' and 'num_questions' parameters."}), 400
    
    try:
        num_questions = int(num_questions)
        if num_questions <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid number of questions. Please provide a positive integer."}), 400

    questions = generate_questions_with_openai(topic, num_questions)
    
    if isinstance(questions, str):  # If an error message is returned
        return jsonify({"error": questions}), 500
    
    return jsonify({
        "topic": topic,
        "questions": questions
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
