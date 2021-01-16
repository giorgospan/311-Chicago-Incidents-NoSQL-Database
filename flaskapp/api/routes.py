from bson import ObjectId
from bson.json_util import dumps
from flask import Blueprint, request
from datetime import datetime
from ..extensions import mongo
from ..utils.utils import *

api = Blueprint('api', __name__)

"""
Find the total requests per type that were created within a specified time range and sort
them in a descending order.
"""


@api.route('/query1')
def query1():
    fr = datetime.strptime(request.args.get('fr'), DATETIME_FORMAT)
    to = datetime.strptime(request.args.get('to'), DATETIME_FORMAT)
    result = mongo.db.request.find({'creation_date': {'$gte': fr, '$lt': to}})
    return dumps(result)


"""
Find the number of total requests per day for a specified request type and time range.
"""


@api.route('/query2')
def query2():
    return


"""
Find the three most common service requests per zipcode for a specified day.
"""


@api.route('/query3')
def query3():
    return


"""
Find the three least common wards with regards to a given service request type.
"""


@api.route('/query4')
def query4():
    return


"""
Find the average completion time per service request for a specified date range.
"""


@api.route('/query5')
def query5():
    return


"""
Find the most common service request in a specified bounding box for a specified day. You
are encouraged to use GeoJSON objects and Geospatial Query Operators.
"""


@api.route('/query6')
def query6():
    return


"""
Find the fifty most upvoted service requests for a specified day.
"""


@api.route('/query7')
def query7():
    return


"""
Find the fifty most active citizens, with regard to the total number of upvotes.
"""


@api.route('/query8')
def query8():
    return


"""
Find the top fifty citizens, with regard to the total number of wards for which they have
upvoted an incidents.
"""


@api.route('/query9')
def query9():
    return


"""
Find all incident ids for which the same telephone number has been used for more than one
names.
"""


@api.route('/query10')
def query10():
    return


"""
Find all the wards in which a given name has casted a vote for an incident taking place in it.
"""


@api.route('/query11')
def query11():
    return


"""
Insert a new incident
"""


@api.route('/insert-incident', methods=['POST'])
def insert_incident():
    data = request.get_json()

    error_message = is_valid(data)
    if error_message:

        return '<h1>Insertion Failed<h1>' + error_message

    data['creation_date'] = datetime.strptime(data['creation_date'], DATETIME_FORMAT)
    data['completion_date'] = datetime.strptime(data['completion_date'], DATETIME_FORMAT)
    mongo.db.request.insert(data)
    return '<h1> Successful insert </h1>'


"""
Cast an upvote. 
In case the same user casts a vote for the same incident a second time, the vote should be rejected.
"""


@api.route('/insert-upvote', methods=['POST'])
def insert_upvote():
    data = request.get_json()

    res = mongo.db.citizen.update_one(
        {"_id": ObjectId(data['citizen_id'])},
        {'$addToSet': {"upvotes": ObjectId(data['incident_id'])}}
    )

    if res.modified_count == 1:
        return '<h1> Successful upvote </h1>'
    else:
        return '<h1> Upvote already exists </h1>'
