#Name : Tejaswi Prakhya, Sapna Patil
#Flask: http://104.131.64.127:5000/
#################################################################################################
#################################################################################################
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_restful import reqparse
from flask import jsonify
from flask_cors import CORS, cross_origin

#from pymongo import MongoClient
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
from bson.objectid import ObjectId
from bson.son import SON

import datetime

import json
import urllib


import timeit

app = FlaskAPI(__name__)
CORS(app)

client = pymongo.MongoClient('localhost', 27017)

# change the following to fit your database configuration

db = client['mongo_db']   
businessdb = db['yelp.business']
review = db['yelp.review']
userdb = db['yelp.user']
testdb = db['yelp.test']
tipdb = db['yelp.tip']


parser = reqparse.RequestParser()
@cross_origin() # allow all origins all methods.
@app.route("/", methods=['GET'])
def index():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return func_list

@app.route("/business/<args>", methods=['GET'])
def business(args):

    args = myParseArgs(args)
    
    #data = []
    
    #result = businessdb.find({},{'_id':0}).limit(100)
    
    #for row in result:
        #data.append(row)
    

    return {"data":args}

#curl -X GET http://104.131.64.127:5000/most_likes/start=0:limit=20
""""@app.route("/most_likes/<args>", methods=['GET'])
def most_likes(args):
    args = myParseArgs(args)
    data = []
    start = int(args['start'])
    end = int(args['limit'])
    
    result = tipdb.find({},{"business_id":1,"name":1,"_id":0}).sort("likes",-1 ).limit(1)
    
    for row in result:
        
            data.append(row)
            
    return {"data":data}"""
@app.route("/most_likes/<args>", methods=['GET'])
def most_likes(args):
    args = myParseArgs(args)
    data = []
    if 'start' in args.keys():
        s = int(args['start'])
        val_start= s
        
    if 'limit' in args.keys():
        l= int(args['limit'])
        val_end = l
    
    if 'start' in args.keys() and 'limit' in args.keys():
        result = tipdb.find({},{"_id":0,"likes":1, "business_id":1}).sort("likes", -1).skip(val_start).limit(val_end)
    elif 'start' in args.keys():
        result = tipdb.find({},{"_id":0,"likes":1, "business_id":1}).sort("likes", -1).skip(val_start)
    elif 'limit' in args.keys():
        result = tipdb.find({},{"_id":0,"likes":1, "business_id":1}).sort("likes", -1).limit(val_end)
    else:
        result = tipdb.find({},{"_id":0,"likes":1, "business_id":1}).sort("likes", -1).limit(1)
    for row in result:
        print row
        data.append(row)
    
        
    return{"data":data}



#curl -X GET http://104.131.64.127:5000/review_count/
#{"data": [{"_id": 0, "avgreview_count": 25.757102115486575}]}root@5303-Advdb:~#

@app.route("/review_count/", methods=['GET'])
def review_count():
    data = []
    result = userdb.aggregate([{ "$group": { "_id" :"$name", "avgreview_count":{"$avg": "$review_count" } } } ])
    for row in result:
        data.append(row)


    return {"data":data}
    

#curl -X GET http://104.131.64.127:5000/city/city="Las%20Vegas":start=0:limit=20

@app.route("/city/<args>", methods=['GET'])
def city(args):

    args = myParseArgs(args)
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    city = args['city']
    data = []
    if 'start' in args.keys() and 'limit' in args.keys():
        result = businessdb.find( {"city" : city},{"name":1,"city":1,"_id":0} ).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = businessdb.find( {"city" : city},{"name":1,"_id":0} ).skip(args['start'])
    elif 'limit' in args.keys():
        result = businessdb.find( {"city" : city},{"name":1,"_id":0} ).limit(args['limit'])
    else:
        result = businessdb.find( {"city" : city},{"name":1,"_id":0} ).limit(10)  
    
    #result = businessdb.find( {"city" : city},{"full_address":1,"_id":0} )
    
    for row in result:
        
        data.append(row)
            
    

    return {"data":data}
#curl -X GET http://104.131.64.127:5000/closest/lon=-80.839186:lat=35.226504:start=0:limit=20

@app.route("/closest/<args>", methods=['GET'])
def closest(args):

    args = myParseArgs(args)
    cities={}
    data = []
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    
    lon = float(args['lon'])
    lat = float(args['lat'])
    if 'start' in args.keys() and 'limit' in args.keys():
        result = businessdb.find(  { "loc": { "$geoWithin": { "$centerSphere": [ [lon,lat] , 100 / 3963.2 ] } } },{"full_address":1,"name":1,"_id":0} ).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = businessdb.find(  { "loc": { "$geoWithin": { "$centerSphere": [ [lon,lat] , 100 / 3963.2 ] } } },{"full_address":1,"_id":0} ).skip(args['start'])
    elif 'limit' in args.keys():
        result = businessdb.find(  { "loc": { "$geoWithin": { "$centerSphere": [ [lon,lat] , 100 / 3963.2 ] } } },{"full_address":1,"_id":0} ).limit(args['limit'])
    else:
        result = businessdb.find(  { "loc": { "$geoWithin": { "$centerSphere": [ [lon,lat] , 100 / 3963.2 ] } } },{"full_address":1,"_id":0} ).limit(10)  
    #result = businessdb.find(  { "loc": { "$geoWithin": { "$centerSphere": [ [lon,lat] , 100 / 3963.2 ] } } },{"full_address":1,"_id":0} )
    
    for row in result:
        
        data.append(row)
            
    

    return {"data":data}

# curl -X GET http://104.131.64.127:5000/closest_place/lon=-80.839186:lat=35.226504:start=0:limit=20

@app.route("/closest_place/<args>", methods=['GET'])
def closest_place(args):

    args = myParseArgs(args)
    counter=0
    data = []
    
    if 'limit' in args.keys():
        li = int(args['limit'])
        y=li
        
    if 'lon' in args.keys():
        lon = float(args['lon'])
        
    if 'lat' in args.keys():
        lat = float(args['lat'])
        
    if 'skip' in args.keys():    
        skip = int(args['skip'])
        x=skip
    
    distance = 0.004
    
    if 'skip' in args.keys() and 'limit' in args.keys():
        result = businessdb.find({ "loc":{ "$geoWithin": { "$center": [ [ lon,lat] , distance ] }}},{"name":1,"_id":0 } ).skip(x).limit(y)
    elif 'skip' in args.keys():
        result = businessdb.find({ "loc":{ "$geoWithin": { "$center": [ [ lon,lat] , distance ] }}},{"name":1,"_id":0 } ).skip(x)
    elif 'limit' in args.keys():
        result = businessdb.find({ "loc":{ "$geoWithin": { "$center": [ [ lon,lat] , distance ] }}},{"name":1,"_id":0 } ).limit(y)
    else:
        result = businessdb.find({ "loc":{ "$geoWithin": { "$center": [ [ lon,lat] , distance ] }}},{"name":1,"_id":0 } ).limit(10)
    
    
    for r in result:
        data.append(r)
    
    return {"data":data}


@app.route("/find_zip/<args>", methods=['GET'])
def find_zip(args):

    args = myParseArgs(args)
    zipval=[]

    if 'start' in args.keys():
        s = int(args['start'])
        start = s

    if 'limit' in args.keys():
        l = int(args['limit'])
        end = l
    if 'zip' in args.keys():
        zipval = args['zip']
        x=int(zipval[0])
        y=int(zipval[1])


    counter=0
    data = []
      
    result = businessdb.find({"$or": [{"full_address":{"$regex" : '.*' + 'x' + '.*'}},{"full_address":{"$regex" : '.*' + 'y' + '.*'}}]},{"name":1, "full_address":1,"_id":0}).skip(start).limit(end)

    for r in result:
        data.append(r)


    return {"data":data}



#curl -X GET http://104.131.64.127:5000/reviews/id=hB3kH0NgM5LkEWMnMMDnHw:start=0:limit=20

@app.route("/reviews/<args>", methods=['GET'])
def reviews(args):

    args = myParseArgs(args)
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    
    id= (args['id'])
    #result = review.find(  {"business_id" : id},{"text":1,"_id":0} )
    if 'start' in args.keys() and 'limit' in args.keys():
        result = review.find(  {"business_id" : id},{"text":1,"_id":0} )
    elif 'start' in args.keys():
        result = review.find(  {"business_id" : id},{"text":1,"_id":0} )
    elif 'limit' in args.keys():
        result = review.find(  {"business_id" : id},{"text":1,"_id":0} )
    else:
        result = review.find(  {"business_id" : id},{"text":1,"_id":0} ) 
    for row in result:
        
        data.append(row)
            
    

    return {"data":data}

# curl -X GET http://104.131.64.127:5000/avg_elite/
#{"data": [{"_id": "0", "avg": 0.0}]}
@app.route("/avg_elite/", methods=['GET'])
def avg_elite():

    #args = myParseArgs(args)
    
    data = []
    #start = int(args['start'])
    #end = int(args['limit'])
    #id= (args['id'])
    result = userdb.aggregate([{"$group": {"_id":"$name","avg": { "$avg": { "$size" : "$elite" }}}}] )
    #result = userdb.aggregate({"$project":{"lengthofelite" : {"$size" : "$elite"}}}, {"$group": { "_id": 0,"avg": { "$avg": "$lengthofelite" }}} )

    for row in result:
        
        data.append(row)
            
    

    return {"data":data}

#curl -X GET http://104.131.64.127:5000/yelping/min_years=5:start=0:limit=20

@app.route("/yelping/<args>", methods=['GET'])
def yelping(args):

    args = myParseArgs(args)
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    
    minyears= int(args['min_years'])
    if 'start' in args.keys() and 'limit' in args.keys():
        result = userdb.find({ "yelping_since" : {"$lte":"2012-01"}}, {"yelping_since":1,"name" : 1,"_id":0}).limit(args['limit'])
    elif 'start' in args.keys():
        result = userdb.find({ "yelping_since" : {"$lte":"2012-01"}}, {"user_id":1,"_id":0}).skip(args['start'])
    elif 'limit' in args.keys():
        result = userdb.find({ "yelping_since" : {"$lte":"2012-01"}}, {"user_id":1,"_id":0}).limit(args['limit'])
    else:
        result = userdb.find({ "yelping_since" : {"$lte":"2012-01"}}, {"user_id":1,"_id":0})
    #result = userdb.find({ "yelping_since" : {"$lte":"2012-01"}}, {"user_id":1,"_id":0})
    
    for row in result:
        
        data.append(row)
            
    

    return {"data":data}

#curl -X GET http://104.131.64.127:5000/stars/id=hB3kH0NgM5LkEWMnMMDnHw:num_stars=5:start=0:limit=20

""""@app.route("/stars/<args>", methods=['GET'])
def stars(args):
    args = myParseArgs(args)
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])
    data = []
    
    star= int(args['num_stars'])
    if 'start' in args.keys() and 'limit' in args.keys():
        result = review.find(  {"stars" : star},{"text":1,"_id":0} ).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = review.find(  {"stars" : star},{"text":1,"_id":0} ).skip(args['start'])
    elif 'limit' in args.keys():
        result = review.find(  {"stars" : star},{"text":1,"_id":0} ).limit(args['limit'])
    else:
        result = review.find(  {"stars" : star},{"text":1,"_id":0} )  
    
    
    for row in result:
        
        data.append(row)
            
    
    return {"data":data}"""
@app.route("/stars/<args>", methods=['GET'])
def stars(args):

    args = myParseArgs(args)
    data = []
    
    if 'num_stars' in args.keys():
        star = int(args['num_stars'])
    
    if 'id' in  args.keys():
        bid = args['id']
        
    if 'start' in args.keys():
        s = int(args['start'])
        val_start= s
        
    if 'limit' in args.keys():
        l= int(args['limit'])
        val_end = l
        
    if 'skip' in args.keys() and 'limit' in args.keys() and 'num_stars' in args.keys() and 'id' in  args.keys():
        result = review.find({"stars": star, "business_id":bid},{"_id":0,"business_id":1,"text":1}).skip(val_start).limit(val_end)
    elif 'skip' in args.keys()and 'num_stars' in args.keys() and 'id' in  args.keys():
        result = review.find({"stars": star, "business_id":bid},{"_id":0,"business_id":1,"text":1}).skip(val_start)
    elif 'limit' in args.keys() and 'num_stars' in args.keys() and 'id' in  args.keys():
        result = review.find({"stars": star, "business_id":bid},{"_id":0,"business_id":1,"text":1}).limit(val_end)
    else:
        result = review.find({"stars": star, "business_id":bid},{"_id":0,"business_id":1,"text":1}).limit(10)    
    
    for r in result:
        data.append(r)
        
    return {"data":data}
 



#curl -X GET http://104.131.64.127:5000/elite/start=0:limit=20

@app.route("/elite/<args>", methods=['GET'])
def elite(args):

    args = myParseArgs(args)
    
    
    if 'start' in args.keys():
        args['start'] = int(args['start'])
    if 'limit' in args.keys():
        args['limit'] = int(args['limit'])

    data = []
    if 'start' in args.keys() and 'limit' in args.keys():
        result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).skip(args['start']).limit(args['limit'])
    elif 'start' in args.keys():
        result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).skip(args['start'])
    elif 'limit' in args.keys():
        result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).limit(args['limit'])
    else:
        result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1}).limit(10)
    #result = userdb.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1})
    
    for row in result:
        
        data.append(row)
            
    return {"data":data}

#curl -X GET http://104.131.64.127:5000/long_elite/start=0:limit=20:sorted=reverse
#{"data": [{"max": {"lengthofelite": 12}, "_id": 0}]}
""""@app.route("/long_elite/<args>", methods=['GET'])
def long_elite(args):
    args = myParseArgs(args)
    sort = args['sorted']
    #return sort
    data = []
    start = int(args['start'])
    end = int(args['limit'])
    result = userdb.aggregate([{"$group": { "_id" :"$name","max": {"$max":{"lengthofelite" :{ "$size" : "$elite" }}}}}])
        #result = userdb.find({"elite":{"$ne":""}},{"_id":0,"name":1,"elite":1}).sort({"elite",-1}).limit(1)
    for row in result:
            
        data.append(row)
                
    return {"data":data}"""
# curl -X GET http://104.131.64.127:5000/longest_elite_user/start=0:limit=20:sorted=reverse
@app.route("/longest_elite_user/<args>",methods=['GET'])
def longest_elite_user(args):
    args = myParseArgs(args)
    data = []
            
    if 'start' in args.keys():
        s = int(args['start'])
        val_start= s
        
    if 'limit' in args.keys():
        l= int(args['limit'])
        val_end = l
        
    if 'sorted' in args.keys():
        x = -1
    
    if 'skip' in args.keys() and 'limit' in args.keys() and 'sorted' in args.keys():
        result = userdb.find({"elite":{"$ne":0}},{"_id":0,"name":1,"elite":1}).sort("elite", x).skip(val_start).limit(val_end)
    elif 'skip' in args.keys() and 'sorted' in args.keys():
          result = userdb.find({"elite":{"$ne":0}},{"_id":0,"name":1,"elite":1}).sort("elite", x).skip(val_start)
    elif 'limit' in args.keys() and 'sorted' in args.keys():
          result = userdb.find({"elite":{"$ne":0}},{"_id":0,"name":1,"elite":1}).sort("elite", x).limit(val_end)
    else:
         result = userdb.find({"elite":{"$ne":0}},{"_id":0,"name":1,"elite":1}).sort("elite", x).limit(10)
    for r in result:
        data.append(r)
        
    return{"data":data}



#curl -X GET http://104.131.64.127:5000/find_zips/zip=89117,89122:start=0:limit=20

@app.route("/find_zips/<args>", methods=['GET'])
def find_zips(args):

    args = myParseArgs(args)
    cond = 0
    data = []
    zip = []

    start = int(args['start'])
    end = int(args['limit'])
    zip = args['zip'].split(',')
    
    result = businessdb.find({},{"full_address":1,"_id":0,"name" : 1})

    #result = businessdb.find('(\d{5})([- ])?(\d{4})?',zip).group(0
    for r in result:
        parts = r['full_address'].split(' ')
        target = parts[-1]
        #return target
        if target in zip and start <= end :
            
            data.append(r)
            start = start +1  
    return {"data":data}


    
def myParseArgs(pairs=None):
    """Parses a url for key value pairs. Not very RESTful.
    Splits on ":"'s first, then "=" signs.
    
    Args:
        pairs: string of key value pairs
        
    Example:
    
        curl -X GET http://cs.mwsu.edu:5000/images/
        
    Returns:
        json object with all images
    """
    
    if not pairs:
        return {}
    
    argsList = pairs.split(":")
    argsDict = {}

    for arg in argsList:
        key,val = arg.split("=")
        argsDict[key]=str(val)
        
    return argsDict

if __name__ == "__main__":
    app.run(debug=True,host='104.131.64.127',port=5000)
