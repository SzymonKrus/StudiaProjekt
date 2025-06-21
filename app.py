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
    questions = [
        {
            'question': 'Kiedy wybuchła II wojna światowa?',
            'options': ['a) 1939', 'b) 1945', 'c) 1918'],
            'answer': 'a'
        },
        {
            'question': 'Kto był pierwszym cesarzem Rzymu?',
            'options': ['a) Neron', 'b) Oktawian August', 'c) Juliusz Cezar'],
            'answer': 'b'
        },
        {
            'question': 'W którym roku Polska odzyskała niepodległość po zaborach?',
            'options': ['a) 1918', 'b) 1920', 'c) 1939'],
            'answer': 'a'
        },
        {
            'question': 'Jakie wydarzenie rozpoczęło rewolucję francuską?',
            'options': ['a) Bitwa pod Waterloo', 'b) Zdobycie Bastylii', "c) Zamach na Robespierre'a"],
            'answer': 'b'
        },
        {
            'question': 'Kim był Mieszko I?',
            'options': ['a) Pierwszym królem Polski', 'b) Pierwszym prezydentem RP', 'c) Pierwszym historycznym władcą Polski'],
            'answer': 'c'
        },
        {
            'question': 'W jakim roku miała miejsce bitwa pod Grunwaldem?',
            'options': ['a) 1410', 'b) 1492', 'c) 1385'],
            'answer': 'a'
        },
        {
            'question': 'Kto był wodzem Związku Radzieckiego podczas II wojny światowej?',
            'options': ['a) Lenin', 'b) Stalin', 'c) Chruszczow'],
            'answer': 'b'
        },
        {
            'question': 'Jakie państwo zbudowało piramidy w Gizie?',
            'options': ['a) Rzym', 'b) Grecja', 'c) Egipt'],
            'answer': 'c'
        },
        {
            'question': 'Kto odkrył Amerykę w 1492 roku?',
            'options': ['a) Wikingowie', 'b) Krzysztof Kolumb', 'c) Vasco da Gama'],
            'answer': 'b'
        },
        {
            'question': 'Jaki mur oddzielał Berlin w czasie zimnej wojny?',
            'options': ['a) Mur Chiński', 'b) Mur Hadriana', 'c) Mur Berliński'],
            'answer': 'c'
        }
    ]
    if request.method == 'POST':
        user_answers = [
            request.form.get(f'q{i+1}') for i in range(10)
        ]
        correct_answers = [q['answer'] for q in questions]
        score = sum(1 for i in range(10) if user_answers[i] is not None and user_answers[i] == correct_answers[i])
        return render_template('result.html', score=score, total=len(questions))
    return render_template('quiz.html', questions=questions)

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
