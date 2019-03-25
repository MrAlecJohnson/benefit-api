#!flask/bin/python
import flask
import datetime

app = flask.Flask(__name__)

"""Do I need this?"""
benefits = [
    {
        'ben_id': 1,
        'name': 'Universal Credit',
        'abbrev': 'uc'
    }
]

# I'll need to put these in MySQL or a proper database at some point
rates = [
    {
        'rate_id': 1,
        'ben_id': 1,
        'element': 'housing',
        'date': datetime.date(2018,4,1),
        'amount': 56,
    },
    
        {
        'rate_id': 2,
        'ben_id': 1,
        'element': 'disability', 
        'date': datetime.date(2018,4,1),
        'amount': 96,
    },
                    {
        'rate_id': 1,
        'ben_id': 1,
        'element': 'housing', 
        'date': datetime.date(2017,4,1),
        'amount': 55,
    },
    
        {
        'rate_id': 2,
        'ben_id': 1,
        'element': 'disability', 
        'date': datetime.date(2017,4,1),
        'amount': 95,
        
    }

]

def findBenefit(abbrev):
    benefit = str(abbrev).lower()
    for x in benefits:
        if x['abbrev'] == benefit:
            return x['ben_id']

@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


@app.route('/benefits/api/v1/<string:benefit>/', defaults = {'element': None, 'year': None}, methods=['GET'])
@app.route('/benefits/api/v1/<string:benefit>/<string:element>/', defaults = {'year': None}, methods=['GET'])
@app.route('/benefits/api/v1/<string:benefit>/<int:year>/', defaults = {'element': None}, methods=['GET'])
@app.route('/benefits/api/v1/<string:benefit>/<string:element>/<int:year>', methods=['GET'])
def getValue(benefit, element, year):
    """Returns just the current rates for all the elements for a benefit"""
    ben_id = findBenefit(benefit)
    if element:
        element = str(element).lower()
        if year:
            for x in rates:
                if x['ben_id'] == ben_id and x['element'] == element and x['date'].year == year:
                    return str(x['amount'])
        else:
            results = {}
            for x in rates:
                if x['ben_id'] == ben_id and x['element'] == element:
                    results[x['date'].year] = x['amount']
            return flask.jsonify(results)
    else:
        if year:
            results = {}
            for x in rates:
                if x['ben_id'] == ben_id and x['date'].year == year:
                    results[x['element']] = x['amount']
            return flask.jsonify(results)
        else:
            results = {}
            for x in rates:
                if x['ben_id'] == ben_id:
                    results[x['date'].year] = results.get(x['date'].year,{})
                    results[x['date'].year][x['element']] = x['amount']
            return flask.jsonify(results)
            
@app.route('/benefits/api/v1/current/<string:benefit>/<string:element>/', methods=['GET'])
@app.route('/benefits/api/v1/current/<string:benefit>/', defaults = {'element': None}, methods=['GET'])
def getCurrent(benefit, element):
    ben_id = findBenefit(benefit)
    results = {}
    if element:
        element = str(element).lower()
        for x in rates:
            if x['ben_id'] == ben_id and x['element'] == element:
                results[x['date'].year] = x['amount']
        year = max([int(year) for year in results.keys()])
        return str(results[year])
    else:
        for x in rates:
            if x['ben_id'] == ben_id:
                results[x['element']] = results.get(x['element'],{})
                results[x['element']][x['date'].year] = x['amount']
        current = {}
        for e in results: 
            year = max([int(y) for y in results[e]]) 
            current[e] = results[e][year]
        
        return flask.jsonify(current)






if __name__ == '__main__':
    app.run(debug = True)
