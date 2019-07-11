from flask import Flask, request, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

tasks = []

@app.route('/', methods=['POST', 'GET'])
def todos():

    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)

    return render_template(
        'todos.html', 
        title='Get it Done!', 
        tasks=tasks,
        )

app.run()
