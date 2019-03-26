import flask
import requests

page = flask.Flask(__name__)

@page.route('/mockup', methods = ["GET"])
def index():
    
    return flask.render_template('mockup.html', 
                                 rate1 = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/housing/').text,
                                 rate2 = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/disability/').text,
                                 housing2017 = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/housing/2017').text,
                                 housing2018 = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/housing/2018').text,
                                 attendance = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/housing/').text,
                                 jsa = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/disability/').text)


if __name__ == '__main__':
    page.run(debug = False, port = 5000)
