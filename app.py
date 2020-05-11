from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

# Global session variables need to be before app. items
CURRENT_RESPONSES = 'responses'
CURRENT_SURVEY_ID = 'survey_id'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return render_template('home.html', surveys=surveys.values())

@app.route('/', methods=["POST"])
def show_survey():
    survey_id = request.form["survey_id"]
    session[CURRENT_SURVEY_ID] = survey_id
    survey=surveys[survey_id]
    return render_template('survey-start.html', survey=survey)

@app.route("/question_start", methods=["POST"])
def start_survey():
    session[CURRENT_RESPONSES] = []
    return redirect("/questions/0")

@app.route('/questions/<int:q_num>')
def show_question(q_num):
    num_responses = len(session[CURRENT_RESPONSES])
    if q_num != num_responses:
        flash("Error trying to access an invalid question!", 'error')
        return redirect(f"/questions/{num_responses}")
    survey_id = session[CURRENT_SURVEY_ID]
    survey=surveys[survey_id]
    num_questions = len(survey.questions)
    if q_num <= num_questions - 1:
        question = survey.questions[q_num]
        return render_template("questions.html", question=question)
    else:
        return render_template("thanks.html")

@app.route('/answer', methods=["POST"])
def handle_answer():
    response_list = session[CURRENT_RESPONSES]
    if request.form.getlist('answer') != []:
        response = request.form['answer']
        text = request.form.get('text', "")
        response_list.append({"response":response,"text":text})
        session[CURRENT_RESPONSES] = response_list
    return redirect(f"/questions/{len(response_list)}")
