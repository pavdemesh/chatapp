from flask import Flask, render_template, request, session, redirect
import openai
import os
import secrets

app = Flask(__name__)

# generate a secret_key
secretk = secrets.token_hex(32)
app.secret_key = secretk

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to adjust text area height dynamically
@app.route('/')
def index():
    conversation = session.get('conversation', [])
    return render_template('index.html', conversation=conversation)

# Handle user input and chatbot interaction using GPT-3.5 Turbo
@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.form['prompt']
    conversation = session.get('conversation', [])
    conversation.append({'user': prompt})

    # Generate a bot reply using GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        # engine="text-davinci-003",  # GPT-3.5 Turbo engine
        model="gpt-3.5-turbo",
        # prompt=prompt,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3999,  # Adjust the response length as needed
        n=1,
        stop=None
    )

    # bot_reply = response.choices[0].text.strip()
    bot_reply = response.choices[0].message['content']
    conversation.append({'bot': bot_reply})
    session['conversation'] = conversation
    return redirect('/')

# Renew conversation (clear session data)
@app.route('/renew', methods=['POST'])
def renew():
    session.pop('conversation', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
