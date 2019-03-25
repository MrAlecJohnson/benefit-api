#!flask/bin/python
import flask
import datetime

app = flask.Flask(__name__)

benefits = [
    {
        'ben_id': 1,
        'name': 'Universal Credit',
        'abbrev': 'uc'
    }
]

# I should probably move all these into MySQL
rates = [
    {
        'rate_id': 1,
        'ben_id': 1,
        'element': 'housing element', # what if I wanted to capitalise?
        'date': datetime.date(2018,4,1),
        'amount': 56
    },
    
        {
        'rate_id': 2,
        'ben_id': 1,
        'element': 'disability element', 
        'date': datetime.date(2018,4,1),
        'amount': 96
    },
                    {
        'rate_id': 1,
        'ben_id': 1,
        'element': 'housing element', 
        'date': datetime.date(2017,4,1),
        'amount': 56
    },
    
        {
        'rate_id': 2,
        'ben_id': 1,
        'element': 'disability element', 
        'date': datetime.date(2017,4,1),
        'amount': 96
    }

]

@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

@app.route('/benefits/api/v1/all-rates/<abbrev>', methods=['GET'])
def getAllRates(abbrev):
    """Returns all the rates for all the elements for a benefit"""
    name = str(abbrev).lower()
    try:
        benefit = [x['ben_id'] for x in benefits if x['abbrev'] == name][0]
    except:
        flask.abort(404)
    elements = [(rate['element'], rate['amount'], rate['date'].strftime("%-d %B %Y")) for rate in rates 
             if rate['ben_id'] == benefit]
    return flask.jsonify(elements)

@app.route('/benefits/api/v1/current-rates/<abbrev>', methods=['GET'])
def getCurrentRates(abbrev):
    """Returns just the current rates for all the elements for a benefit"""
    name = str(abbrev).lower()
    try:
        benefit = [x['ben_id'] for x in benefits if x['abbrev'] == name][0]
    except:
        flask.abort(404)
        
    elements = [rate for rate in rates if rate['ben_id'] == benefit]
    results = {}
    for x in elements:
        if results.get(x['element']):
            if results[x['element']][1] < x['date']:
                results[x['element']] = (x['amount'], x['date'])
        else:
            results[x['element']] = (x['amount'], x['date'])
    
    tidy = [(key, value[0]) for key, value in results.items()] 
    
    return flask.jsonify(tidy)


if __name__ == '__main__':
    app.run(debug = True)
