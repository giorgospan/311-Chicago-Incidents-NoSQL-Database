from flask import Blueprint

api = Blueprint('api', __name__)


@api.route('/')
def home():
    return '<h1> Welcome to our Chicago 311 Service </h1>'


"""
Find the total requests per type that were created within a specified time range and sort
them in a descending order.
"""


@api.route('/query1')
def query1():
    return


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
