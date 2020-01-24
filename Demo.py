from flask import Flask,render_template,url_for
app=Flask(__name__)

posts=[
        {
        'author':'Chris Maghas',
        'title':'Blog Post 1',
        'content':'Second Post Content',
        'date_posted':'April 22,2018'
        },
        {
        'author':'Rose Mwangi',
        'title':'Blog Post 2',
        'content':'Second Post Content',
        'date_posted':'April 22,2018'
        }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts,title='Demo')


@app.route("/about")
def about():
    return render_template('about.html',title='about')

@app.route("/feedback")
def feedback():
    return render_template('feedback.html',posts=posts,title='feedback')

@app.route("/reports")
def reports():
    return render_template('reports.html',title='View Coda Reports')

if __name__ == '__main__':
    app.run(debug=True)
    