import flask

page = flask.Flask(__name__)

@page.route('/mockup', methods = ["GET"])
def index():
    
    return flask.render_template('mockup.html', rates = 'http://127.0.0.1:5000/benefits/api/v1/current/uc/housing/')


if __name__ == '__main__':
    page.run(debug = True)
