from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)


#connect db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Bootstrap(app)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    date = db.Column(db.String(50))
    done = db.Column(db.Boolean)


with app.app_context():
    db.create_all()


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/info")
def info():
    done = List.query.filter_by(done=True).all()
    undone = List.query.filter_by(done=False).all()
    return render_template("info.html", done=done, undone=undone)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        text_data = request.form["text_data"]
        date = request.form["date"]
        new_task = List(
            text=text_data,
            date=date,
            done=False
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("info"))


@app.route("/complete")
def complete():
    end_data = request.args.get("id")
    complete_data = List.query.get(int(end_data))
    complete_data.done = True
    db.session.commit()
    return redirect(url_for("info"))


@app.route("/delete")
def delete():
    post_to_delete = request.args.get("id")
    delete_item = List.query.get(int(post_to_delete))
    db.session.delete(delete_item)
    db.session.commit()
    return redirect(url_for("info"))


if __name__ == "__main__":
    app.run(debug=True)