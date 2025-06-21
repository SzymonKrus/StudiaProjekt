from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os

app = Flask(__name__)

# Ensure data folder exists
os.makedirs('data', exist_ok=True)

# Initialize counter file if not exists
if not os.path.exists('data/counter.txt'):
    with open('data/counter.txt', 'w') as f:
        f.write('0')

@app.route('/')
def index():
    # Update visit counter
    with open('data/counter.txt', 'r+') as f:
        count = int(f.read()) + 1
        f.seek(0)
        f.write(str(count))
        f.truncate()
    return render_template('index.html', count=count)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = {
            "name": request.form['name'],
            "email": request.form['email']
        }
        try:
            with open('data/users.json', 'r') as f:
                users = json.load(f)
        except:
            users = []
        users.append(user)
        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=2)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        answers = [request.form.get('q1'), request.form.get('q2'), request.form.get('q3')]
        correct = ['a', 'b', 'c']
        score = sum([1 for i in range(3) if answers[i] == correct[i]])
        return render_template('result.html', score=score)
    return render_template('quiz.html')

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        entry = request.form['entry']
        with open('data/guestbook.txt', 'a') as f:
            f.write(entry + "\n")
    with open('data/guestbook.txt', 'r') as f:
        entries = f.readlines()
    return render_template('guestbook.html', entries=entries[::-1])

@app.context_processor
def inject_globals():
    return {'style': url_for('static', filename='style.css'), 'script': url_for('static', filename='script.js')}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))