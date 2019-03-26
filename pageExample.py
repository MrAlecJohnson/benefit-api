import flask
import requests

page = flask.Flask(__name__)

@page.route('/mockup', methods = ["GET"])
def index():
    
    return flask.render_template('mockup.html', 
                                 rate1 = requests.get('http://127.0.0.1:5000/benefits/api/v1/current/uc/housing/').text,
                                 rate2 = requests.get('http://127.0.0.1:5000/benefits/api/v1/current/uc/disability/').text,
                                 housing2017 = requests.get('http://127.0.0.1:5000/benefits/api/v1/current/uc/housing/2017').text,
                                 housing2018 = requests.get('http://127.0.0.1:5000/benefits/api/v1/current/uc/housing/2018').text,
                                 attendance = requests.get('http://127.0.0.1:5000/benefits/api/v1/current/uc/housing/').text,
                                 jsa = requests.get('http://127.0.0.1:5000/benefits/api/v1/current/uc/disability/').text)


if __name__ == '__main__':
    page.run(debug = True, port = 5001)
