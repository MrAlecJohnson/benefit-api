import flask
import requests
import json

page = flask.Flask(__name__)

@page.route('/mockup', methods = ["GET"])
def index():

    return flask.render_template('mockup.html',
                                 rate1 = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/housing/').text,
                                 rate2 = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/disability/').text,
                                 housing2017 = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/uc/housing/2017').text,
                                 housing2018 = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/uc/housing/2018').text,
                                 attendance = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/housing/').text,
                                 jsa = requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/current/uc/disability/').text)

@page.route('/update', methods = ["GET"])
def form():
    benefitGet = json.loads(requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/all-benefits').text)
    elementGet = json.loads(requests.get('https://benefit-api.herokuapp.com/benefits/api/v1/all-elements').text)
    combined = []
    for x in benefitGet:
        x['elements'] = [e[0] for e in elementGet if e[1] == x['ben_id']]
        combined.append(x)
    return flask.render_template('update.html',
                             benefitTable = combined,
                             benefits = [b['name'] for b in benefitGet])
    
@page.route('/posting', methods = ['POST'])
def posting(benefit, element, rate, day, month, year):
    benefit = flask.request.args.get('benefit')
    element = flask.request.args.get('element')
    amount = flask.request.args.get('rate')
    day = str(flask.request.args.get('day'))
    month = str(flask.request.args.get('day'))
    year = str(flask.request.args.get('day'))
    date = day + month + year
    payload = None
    requests.post('https://benefit-api.herokuapp.com/benefits/api/v1/new', data = payload)

    return 'done'

if __name__ == '__main__':
    page.run(debug = True, port = 5000)
