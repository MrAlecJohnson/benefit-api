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
    },
     {
        'ben_id': 2,
        'name': 'Attendance Allowance',
        'abbrev': 'aa'
    },
    {
        'ben_id': 3,
        'name': 'Jobseeker\'s Allowance',
        'abbrev': 'jsa'
    }
     
]

# I'll need to put these in MySQL or a proper database at some point
rates = [
    {
        'ben_id': 1,
        'element': 'housing',
        'date': datetime.date(2018,4,1),
        'amount': float(56.00),
        'id': 1
    },
    
     {
        'ben_id': 1,
        'element': 'disability', 
        'date': datetime.date(2018,4,1),
        'amount': float(96.00),
        'id': 2
    },
    {
        'ben_id': 1,
        'element': 'housing', 
        'date': datetime.date(2017,4,1),
        'amount': float(55.00),
        'id': 3
    },
    
    {
        'ben_id': 1,
        'element': 'disability', 
        'date': datetime.date(2017,4,1),
        'amount': float(95.00),
        'id': 4
        
    },
    {
        'ben_id': 2,
        'element': 'basic', 
        'date': datetime.date(2018,4,1),
        'amount': float(76.00,
        'id': 5
        
    },
    {
        'ben_id': 3,
        'element': 'newstyle', 
        'date': datetime.date(2018,4,1),
        'amount': float(42.00),
        'id': 6
        
    }



]

def findBenefit(abbrev):
    """Looks up a benefit abbreviation and returns that benefit's id
    So you can look it up in the rates table"""
    benefit = str(abbrev).lower()
    for x in benefits:
        if x['abbrev'] == benefit:
            return int(x['ben_id'])

@app.errorhandler(404)
def not_found(error):
    """Slightly clearer error reporting"""
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

@app.route('/benefits/api/v1/all-benefits/<string:order>/', methods = ['GET'])
@app.route('/benefits/api/v1/all-benefits/', defaults = {'order': 'name'}, methods = ['GET'])
def allBenefits(order):
    """Returns all benefits with abbreviations and IDs - order optional"""
    ordered = sorted(benefits, key = lambda x: x[order])
    return flask.jsonify(ordered)


@app.route('/benefits/api/v1/all-elements/<string:benefit>/<string:order>', methods = ['GET'])
@app.route('/benefits/api/v1/all-elements/<string:benefit>/', defaults = {'order': 'element'}, methods = ['GET'])
@app.route('/benefits/api/v1/all-elements/', defaults = {'benefit': None, 'order': 'element'}, methods = ['GET'])
def allElements(benefit, order):
    """Returns all the elements for a given benefit - order optional"""
    if benefit:
        ben_id = findBenefit(benefit)
        results = [e for e in rates if e['ben_id'] == ben_id]
        ordered = sorted(results, key = lambda x: x[order])
        return flask.jsonify(ordered)
    else:
        elements = {(e['element'], e['ben_id']) for e in rates}
        ordered = sorted(elements, key = lambda x: x[1])
        return flask.jsonify(ordered)

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
                    return str(round(x['amount'],2))
        else:
            results = {}
            for x in rates:
                if x['ben_id'] == ben_id and x['element'] == element:
                    results[x['date'].year] = str(round(x['amount'],2))
            return flask.jsonify(results)
    else:
        if year:
            results = {}
            for x in rates:
                if x['ben_id'] == ben_id and x['date'].year == year:
                    results[x['element']] = str(round(x['amount'],2))
            return flask.jsonify(results)
        else:
            results = {}
            for x in rates:
                if x['ben_id'] == ben_id:
                    results[x['date'].year] = results.get(x['date'].year,{})
                    results[x['date'].year][x['element']] = str(round(x['amount'],2))
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
                results[x['date']] = str(round(x['amount'],2))
        date = max([date for date in results.keys() if date <= datetime.date.today()])
        return str(results[date])
    else:
        for x in rates:
            if x['ben_id'] == ben_id:
                results[x['element']] = results.get(x['element'],{})
                results[x['element']][x['date']] = str(round(x['amount'],2))
        current = {}
        for e in results: 
            date = max([date for date in results[e] if date <= datetime.date.today()]) 
            current[e] = results[e][date]
        
        return flask.jsonify(current)

@app.route('/benefits/api/v1/new', methods = ['POST'])
def newRate():
    benefit = flask.request.args.get('benefit')
    element = flask.request.args.get('element')
    amount = flask.request.args.get('amount')
    date = flask.request.args.get('date')
    
    # check benefit
    ben_id = findBenefit(benefit)
    if ben_id not in [b['ben_id'] for b in benefits]:
        flask.abort(400)
    # check element
    elements = {e['element'] for e in rates if e['ben_id'] == ben_id}
    if element not in elements:
        flask.abort(400)
    # convert date - should be in 20180130 format
    if len(date) != 8:
        flask.abort(400)
    startDate = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    
    # check amount
    money = round(float(amount), 2)
    
    # check if it should be an update instead of a new entry
    datePlusElement = {(e['element'], e['date']) for e in rates if e['ben_id'] == ben_id}
    ids = [e['id'] for e in rates]
    if (element, startDate) in datePlusElement:
        flask.abort(406)
    else:
        # Not sure I need this - deletions will be rare
        for x in range(1, len(ids) + 2):
            if x not in ids:
                smallest = x
                break
        rates.append({'ben_id': ben_id, 'element': element, 'date': startDate, 'amount': money, 'id': smallest})
    
    return 'Added'

@app.route('/benefits/api/v1/update', methods = ['PUT'])
def changeRate():
    target = int(flask.request.args.get('id'))
    benefit = flask.request.args.get('benefit', default = None)
    element = flask.request.args.get('element', default = None)
    amount = round(float(flask.request.args.get('amount', default = None)), 2)
    date = flask.request.args.get('date', default = None)
    
    ids = [e['id'] for e in rates]
    index = ids.index(target)
    entry = rates.pop(index)
    if benefit:
        ben_id = findBenefit(benefit)
        entry['ben_id'] = ben_id
    if element:
        entry['element'] = element
    if amount:
        entry['amount'] = amount
    if date:
        if len(date) != 8:
            flask.abort(400)
        startDate = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))
        entry['date'] = startDate
    rates.append(entry)
    
    return 'Changed'

@app.route('/benefits/api/v1/delete/<int:rate_id>', methods = ['DELETE'])
def delRate(rate_id):
    ids = [e['id'] for e in rates]
    index = ids.index(rate_id)
    del rates[index]
    return 'Deleted'


if __name__ == '__main__':
    app.run(debug = True, port = 5000)
