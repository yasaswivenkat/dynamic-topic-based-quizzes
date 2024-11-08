from flask import Flask, jsonify, request
from flask_cors import CORS
import openai

# Flask app setup
app = Flask(__name__)
CORS(app)  # Allow all domains or specify allowed domains

# Set your OpenAI API key here
openai.api_key = "your-openai-api-key"

def generate_questions_with_openai(topic, num_questions):
    try:
        prompt = f"Generate {num_questions} multiple-choice questions about {topic}."
        
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or use a different GPT model
            prompt=prompt,
            max_tokens=100 * num_questions,  # You can tweak this
            n=1,
            stop=None,
            temperature=0.7,
        )
        
        questions = response.choices[0].text.strip().split('\n')
        return questions
    except Exception as e:
        return str(e)

@app.route('/generate-quiz', methods=['GET'])
def generate_quiz():
    topic = request.args.get('topic')
    num_questions = int(request.args.get('num_questions'))

    if not topic or num_questions <= 0:
        return jsonify({"error": "Invalid topic or number of questions."}), 400
    
    questions = generate_questions_with_openai(topic, num_questions)
    
    if isinstance(questions, str):  # If an error message is returned
        return jsonify({"error": questions}), 500
    
    return jsonify({
        "topic": topic,
        "questions": questions
    })

if __name__ == "__main__":
    app.run(debug=True)
