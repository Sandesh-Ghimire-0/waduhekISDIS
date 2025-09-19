from flask import Flask, render_template, request, redirect
from datetime import datetime,timezone
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)

class Commentzzz(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    comment = db.Column(db.Text, nullable = False)
    date_commented = db.Column(db.DateTime, nullable = False, default = datetime.now(timezone.utc))

    def __repr__(self):
        return f"user={self.username}, comment: {self.comment}, date: {self.date_commented}"


@app.route('/', methods=['POST', 'GET'])
def comment():
    if request.method == 'POST':
        username = request.form['Username']
        comment = request.form['Comments']
        new_comment = Commentzzz(username=username, comment = comment)

        try:
            db.session.add(new_comment)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue with storing your comment."
    else:
        all_comments = Commentzzz.query.order_by(Commentzzz.date_commented).all()
        return render_template('index.html', all_comments = all_comments)

if (__name__=='__main__'):
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=False)
