from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATTIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' %self.id


@app.route('/', methods=['POST', 'GET'])
@app.route('/hello_user')
def create_article():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        article = Article(name=name, email=email)
        exists = db.session.query(Article.id).filter_by(name=name).first()
        if exists is None:
            try:
                db.session.add(article)
                db.session.commit()
                return render_template("hello_user.html", article=article)
            except Exception:
                return "Произошла ошибка"
        return render_template("error_message.html", article=article)
    return render_template("create_article.html")


@app.route('/all_users')
def all_users():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("all_users.html", articles=articles)


@app.route('/all_users/<int:id>')
def user_info(id):
    article = Article.query.get(id)
    return render_template("user_info.html", article=article)


@app.route('/all_users/<int:id>/delete')
def user_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/all_users')
    except:
        return "При удалении статьи произошла ошибка!"


@app.route('/user')
def hello_user():
    return render_template("hello_user.html")


if __name__ == "__main__":
    app.run(debug=True)