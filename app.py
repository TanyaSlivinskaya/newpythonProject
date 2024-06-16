from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myproj.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # category = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/tasks", methods=['GET'])
def tasks():
    tasks = Post.query.all()
    task_id = request.args.get('id', type=int)
    return render_template('tasks.html', tasks=tasks, task_id=task_id)


@app.route("/create", methods=['POST','GET'])
def create():
    if request.method == 'POST':
        # category = request.form['category']
        title = request.form['title']
        text = request.form['text']

        post = Post( title=title, text=text )

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении задачи произошла ошибка!'
    else:
        return render_template('create.html')

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    task = Post.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/tasks')
        except:
            return 'При редактировании задачи произошла ошибка!'
    else:
        return render_template('edit.html', task=task)

@app.route("/delete_task/<int:id>", methods=['POST'])
def delete_task(id):
    task = Post.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/tasks')
    except:
        return 'При удалении задачи произошла ошибка!'




@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
