from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "cats_are_cool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
curr_survey = {}


@app.route('/')
def show_homepage():
    selected_surv = not not curr_survey
    return render_template('home.html', survey=curr_survey, surveys=surveys, selected=selected_surv)

@app.route('/survey')
def set_survey():
    survey = request.args['survey']

    global curr_survey
    curr_survey = surveys[survey]
    responses.clear()
    for q in surveys["satisfaction"].questions:
        responses.append(None)
    return redirect("/")

@app.route('/questions/<int:q_idx>')
def show_questions(q_idx):
    if None in responses:
        index = responses.index(None)
    elif None not in responses and len(responses) >= 1:
        flash("You've completed the survey!")
        return redirect("/complete")

    if q_idx > -1 and q_idx < len(curr_survey.questions):
        question = curr_survey.questions[q_idx]
    else:
        question = curr_survey.questions[index]

    if (index != q_idx):
        flash(f"Please answer question # {index + 1}.")

        return redirect(f"/questions/{index}")

    return render_template('questions.html', curr_q=question, idx=q_idx)


@app.route('/answer', methods=['POST'])
def get_answer():

    answ = request.form['answer']
    idx = int(request.form['idx'])
    
    if curr_survey.questions[idx].allow_text:
        comment = request.form['comment']
        responses[idx] = (answ, comment)
    else:
        responses[idx] = answ

    if (responses[-1] != None):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{idx + 1}")


@app.route('/complete')
def show_completion():
    if None in responses:
        index = responses.index(None)
        flash('Please complete the survey')
        return redirect(f"/questions/{index}")
    else:
        return render_template('complete.html', responses=responses, questions=curr_survey.questions, length=len(responses))

@app.route('/clear')
def clear_vars():
    responses.clear()
    global curr_survey
    curr_survey = {}
    return redirect("/")
