import re
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "cats_are_cool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_homepage():
    responses.clear()
    return render_template('home.html', survey=surveys["satisfaction"])

@app.route('/questions/<int:question>')
def show_questions(question):
    q_idx=question
    curr_q=surveys["satisfaction"].questions[q_idx]

    return render_template('questions.html', curr_q=curr_q)

@app.route('/answer', methods=['POST'])
def get_answer():

    answ = request.form['answer']
    responses.append(answ)
    if (len(responses) == len(surveys["satisfaction"].questions)):
        print(responses)
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/complete')
def show_completion():
    return render_template('complete.html', responses=responses)