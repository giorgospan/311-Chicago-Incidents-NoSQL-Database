# 311 Chicago Incidents NoSQL Database 

## About the project

This project is part of the _Database-Management-Systems_ course. We propose a NoSQL database solution to manage _311
Incidents_ data openly published by the city of Chicago. The database can be accessed through our REST API service.
Ouρ database design is simple yet efficient for all the queries we were asked to handle in this project. We experimented 
with various indexes which led us to performance gain in many cases.


## Built with

* ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
* ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
* ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
* ![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)


## Getting Started

* Download dataset from [Kaggle](https://www.kaggle.com/datasets/chicago/chicago-311-service-requests)
* Run [import_request.py](/import/import_request.py) to import the requests into the database
* Run [import_citizen.py](/import/import_citizen.py) to import the citizens into the database
* Create python virtual environment
   ```
   virtualenv -p python3 myenv
   ```
* Activate it
   ```
   source myenv/bin/activate
   ```
* Install project dependencies listed in [requirements.txt](requirements.txt) file
   ```
   pip3 install -r ./requirements.txt
   ```

## Usage

1. Run the flask application from the root directory of the project folder
    ```
    export FLASK_APP=flaskapp
    flask run
    ```
Development server should be up and running on http://127.0.0.1:5000/

## Database Design

Our NoSQL database consists of two collections, _request_ & _citizen_, which hold request and citizen documents respectively. 
Based on the principals of NoSQL databases, we settled for a non-normalized design. Thus, we avoided inefficient lookup queries between multiple collections. 

More specifically, all types of requests are stored in the _request_ collection. 
The schemaless design allows us to store requests with any number and any type of fields. 
The _citizen_ collection contains documents of the following form:
* id
* address
* username
* phone
* upvotes[]


The relationship between citizens and requests (i.e. incidents) is modelled by storing an array of requests in each citizen document. This array contains the ObjectId's of the requests that the user has upvoted.
Lastly, each request's location is stored as a  GeoJSON Point in order to leverage MongoDB's Geospatial query operators.


## Indexes

The following time measurements were reported by Postman. We ensured that MongoDB query optimizer uses the defined indexes 
by using the explain() function.

### Query1
Find the total requests per type that were created within a specified time range and sort them in descending order.

* No index: 2660ms
* Index(_creation_date_): **761ms**


### Query1  
Find the number of total requests per day for a specified request type and time range.  
* No index: 2430ms
* Index(_creation_date_): **657ms**
* Index(_request_type_): **614ms**
* CompoundIndex(_creation_date_,_request_type_): **110ms**
* CompoundIndex(_request_type_,_creation_date_): **73ms**

### Query3
Find the three most common service requests per zipcode for a specified day.
* No index: 2020ms
* Index(_zip_code_): **2020ms**
* Index(_creation_date_): <ins>**7ms**</ins>
* CompoundIndex(_creation_date_,_zip_code_): <ins>**7ms**</ins>

### Query4
Find the three least common wards with regard to a given service request type.
* No index: 2350ms
* Index(_request_type_): **347ms**

### Query5
Find the average completion time per service request for a specified date range.
* No index: 3030ms
* Index(_creation_date_): 1120ms
* CompoundIndex(_creation_date_,_request_type_): 1110ms


### Query6
Find the most common service request in a specified bounding box for a specified day. You are encouraged to use GeoJSON objects and Geospatial Query Operators.
* No index: 2060ms
* Index(2dsphere): 2080ms
* Index(_creation_date_): <ins>**5ms**</ins>

### Query7
Find the fifty most upvoted service requests for a specified day.
* No index: 33.31sec
* Index(_creation_date_): 31.34sec
* Index(upvotes) + Index(_creation_date_): <ins>**26ms**</ins>

### Query8
Find the fifty most active citizens, with regard to the total number of upvotes.
* No index: 101ms
* Index(upvotes): **96ms**


### Query9
Find the top fifty citizens, with regard to the total number of wards for which they have upvoted an incidents.
* No index: 30sec
* Index(upvotes): 30sec

### Query10
Find all incident ids for which the same telephone number has been used for more than one names.
* No index: 680ms
* Index(upvotes): 680ms
* Index(phone): 680ms
* CompoundIndex(upvotes,phone): 600ms
* CompoundIndex(phone,upvotes): 612ms


### Query11
Find all the wards in which a given name has cast a vote for an incident taking place in it.
* No index: 18ms
* Index(username): **15ms**


[Here](img/metrics) you can find screenshots with query results as shown in postman.

Queries implemented in this project can be found in [queries.sql](js/queries.js)

### Contact
- [George Panagiotopoulos](https://github.com/giorgospan)
- [George Michas](https://github.com/geooo109)
- Project link: [https://github.com/giorgospan/Database-Management-Systems-Project-II](https://github.com/giorgospan/Database-Management-Systems-Project-II)



 





