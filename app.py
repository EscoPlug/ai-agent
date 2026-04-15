from flask import Flask, render_template, request, jsonify
from agent import EmailAgent
from emailer import send_email
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Initialize agent globally
try:
    agent = EmailAgent()
except Exception as e:
    agent = None
    print(f"Error initializing agent: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    try:
        data = request.json
        name = data.get('name')
        role = data.get('role')
        email = data.get('email')
        context = data.get('context')

        if not agent:
            return jsonify({'success': False, 'message': 'Agent not initialized. Check server logs.'})

        # Generate Email
        draft = agent.generate_personalized_email(
            recipient_name=name,
            recipient_role=role,
            context=context
        )

        # Send Email
        success = send_email(email, draft["subject"], draft["body"])

        if success:
            return jsonify({
                'success': True, 
                'subject': draft['subject'], 
                'body': draft['body'],
                'message': 'Email generated and sent successfully!'
            })
        else:
            return jsonify({'success': False, 'message': 'SMTP Error: Failed to send email. Check .env credentials.'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    print("Starting Web UI on http://localhost:5000")
    app.run(debug=True, port=5000)
