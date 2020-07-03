from graphic import graphic
from alerts import alerts
import requests
from pymongo import MongoClient
import pymongo
import json
from trading_efficiency import trading_efficiency

def clear_collection():
    client=MongoClient()
    database=client.get_database('database')
    database.drop_collection('collection') 

#returns a json archieve containing a determined indicator of a determined asset
def colectDataFromWeb(asset_name,WEB_indicator,JSON_indicator):
    try:
        raw_data=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo')#'https://www.alphavantage.co/query?function='+WEB_indicator+'&symbol='+asset_name+'&apikey=W0AG19EGTISKPZTL&datatype=json')
    except:
        print('requests error')
        return

    json_data=raw_data.json()

    if len(list(json_data.keys()))<=1:
        print('received JSON: ',json_data)
        return

    return json_data[JSON_indicator]

def remove_dots(processed_data):
    new_data={}
    for key,value in processed_data.items():
        key=key[3:]
        new_data[key]=value
    return(new_data)

#inserts data data into database
def insert_in_database(data,asset_name,indicator):
    for key,value in data.items():
        mongo_client=MongoClient()
        database=mongo_client.get_database('database')
        collection=database.get_collection('collection')
        new_data={
            'asset_name':asset_name,
            'indicator':indicator,
            'key':key,
            'value':remove_dots(value)
        }
        collection.insert_one(new_data)

def collect_from_database():
    mongo_client=MongoClient()
    database=mongo_client.get_database('database')
    collection=database.get_collection('collection')
    ordered_data= collection.find().sort('natural')#collects data in the same order it was entered
    return ordered_data

def render_graphics():
    pass

# #call all the functions to collect data from web and store them in database
def update_database():    
    try:
        data=colectDataFromWeb('MSFT','TIME_SERIES_INTRADAY','Time Series (5min)')
        if data is not None:
            insert_in_database(data,'MSFT','TIME_SERIES_INTRADAY')
            print('data inserted in database')
        else:
            print("the data was not inserted because it is in an invalid format")

    except Exception as ex:
        print("coudn't run insert_in_database:", type(ex).__name__)

#clears collection
clear_collection()

#sets windows
alerts_window=alerts()
indicators_graphic=graphic()

#updates database
update_database()

#get information from configuration.json
file=open('configuration.json','r')
json_file=json.load(file)
json_file=json_file['assets']
assets_json=list(json_file.keys())
assets_array=[]
for asset in assets_json:
    pass

#updates graphic with information contained in database
database_data=collect_from_database()
for data in database_data:
    close_value=data['value']
    close_value=close_value

#creates trading_efficiency script
trading_efficiency_object=trading_efficiency()
