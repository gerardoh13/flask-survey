from functools import reduce
from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "cats_are_cool"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_homepage():
    return render_template('home.html', surveys=surveys)


@app.route('/start')
def show_instructions():
    survey = surveys[session['curr_survey']]
    return render_template('start.html', survey=survey)


@app.route('/survey', methods=["POST"])
def set_survey():
    survey = request.form['survey']
    print(survey)

    if request.cookies.get(f"completed_{survey}"):
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        flash("You've already completed that survey!")
        return redirect('/')
    session['curr_survey'] = survey
    session['responses'] = []
    for q in surveys[survey].questions:
        session['responses'].append(None)
    return redirect("/start")


@app.route('/questions/<int:q_idx>')
def show_questions(q_idx):
    curr_survey = surveys[session['curr_survey']]
    responses = session['responses']
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
    curr_survey = surveys[session['curr_survey']]
    responses = session['responses']
    answ = request.form['answer']
    idx = int(request.form['idx'])

    if curr_survey.questions[idx].allow_text:
        comment = request.form['comment']
        responses[idx] = (answ, comment)
    else:
        responses[idx] = answ
    session['responses'] = responses

    if (responses[-1] != None):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{idx + 1}")


@app.route('/complete')
def show_completion():
    if 'curr_survey' not in session or session['curr_survey'] == '':
        return redirect('/')
    else:
        curr_survey = surveys[session['curr_survey']]
        responses = session['responses']

    if None in responses:
        index = responses.index(None)
        flash('Please complete the survey')
        return redirect(f"/questions/{index}")
    else:
        html = render_template('complete.html', responses=responses,
                               questions=curr_survey.questions, length=len(responses))
        res = make_response(html)
        res.set_cookie(f"completed_{session['curr_survey']}", "yes", max_age=60)

        return res


@app.route('/clear')
def clear_vars():
    session['responses'] = []
    session['curr_survey'] = ""
    return redirect("/")
