from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_cms.db'
db = SQLAlchemy(app)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)

@app.route('/')
def index():
    pages = Page.query.all()
    return render_template('home.html', pages=pages)

@app.route('/page/<int:page_id>')
def view_page(page_id):
    page = Page.query.get(page_id)
    return render_template('page.html', page=page)

@app.route('/admin')
def admin():
    pages = Page.query.all()
    return render_template('admin.html', pages=pages)

@app.route('/admin/create', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        page = Page(title=title, content=content) # type: ignore
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('create_page.html')
#comment to check the git aa 

if __name__ == '__main__':
    with app.app_context():
      db.create_all()
    app.run(debug=True)
