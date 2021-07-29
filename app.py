from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from apriori import apr, ranList
import random

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "API"
app.config["MONGO_URI"] = "mongodb+srv://Derek:sciencemajic123@cluster0.xedr3.mongodb.net/API?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE"
CORS(app, resource = r'/api/*')
mongo = PyMongo(app)

@app.route('/')
def main():
    return 'Hello World'

#For updating the reccomendation. The list has to be a string, so must convert to a string with space between the mods
#For example 'CS2040EC1101" --> 'CS2040 EC1101'
@app.route('/api/recList/update/<list>',methods = ['PUT','GET'])
def add_rec(list):
    combi = list.split('_')
    for i in combi:
        i = i.upper()
    input = {'UI':combi}
    x = mongo.db.recList.insert_one(input)
    return "updated"

#For getting reccomended modules based on user inputs
@app.route('/api/recList/recs/<inp>',methods = ['GET'])
@cross_origin()
def get_rec(inp):
    if (inp != None):
        ulist = inp.split('_')
        collection = mongo.db.recList.find()
        data = {}
        counter = 0
        for i in collection:
            data[str(counter)] = i['UI']
            counter += 1
        uData = list(data.values())
        output = apr(uData, ulist)
        oD = {}
        oD['recs'] = []
        for i in output:
            oD['recs'].append(i)
        if (len(oD['recs']) == 0):
            collection1 = mongo.db.lessonList.find()
            output1 = []
            for mods in collection1:
                if (mods['_id'][0:2] == "GE"):
                    output1.append(mods['_id'])
            ran = random.randint(0, len(output1) - 1)
            mod = output1[ran]
            rec = {'recs': [mod]}
            return rec
        else:
            return oD

#For returning random GE mod
@app.route('/api/recList/recs/', methods = ["GET"])
def get_rec1():
    collection = mongo.db.lessonList.find()
    output = []
    for mods in collection:
        if (mods['_id'][0:2] == "GE"):
            output.append(mods['_id'])
    ran = random.randint(0,len(output)-1)
    mod = output[ran]
    rec = {'recs':[mod]}
    return rec


#For returning specific module information about the class
@app.route('/api/semD/<ID>', methods = ["GET"])
def get_mod_Class_Info(ID):
    input = ID.upper()
    document = mongo.db.semD.find_one({'_id':input})
    return document

#For returning the class types of the module
@app.route('/api/lessonType/schedule/<ID>', methods= ["GET"])
def get_mod_Types(ID):
    input = ID.upper()
    document2 = mongo.db.lessonList.find_one({'_id': input})
    return document2

#For returning the list of module codes
@app.route('/api/semD/modList/<letters>', methods = ['GET'])
def get_mod_codes(letters):
    length = len(letters)
    collection = mongo.db.lessonList.find()
    output = {}
    output['codes'] = []
    for mods in collection:
        if (mods['_id'][0:length] == letters.upper()):
            output['codes'].append({
                'value':mods['_id'],
                'label':mods['_id'],}
            )
    return output


#For returning the compulsory classes in the mod
@app.route('/api/comList/<ID>', methods=["GET"])
def get_com_class(ID):
    input = ID.upper()
    document3 = mongo.db.comList.find_one({'_id':input})
    return document3

#For generating random combinations to test for skewing
@app.route('/api/lessonType/rando/<length>', methods = ["GET"])
def get_rando(length):
    length = int(length)
    collection = mongo.db.lessonList.find()
    ind = ranList(length)
    holder = []
    output = {}
    for mods in collection:
        holder.append(mods['_id'])

    for i in ind:
        output[holder[i]] = {'value': holder[i], 'label': holder[i]}
    return output

#For getting the paired data
@app.route('/api/pairList/<code>', methods = ['GET'])
def get_pair(code):
    ID = code.upper()
    doc = mongo.db.pairList.find_one({'_id':ID})
    return doc

#For posting errors
@app.route('/api/error/1/<feedback>' , methods = ['GET','PUT'])
def sub_general(feedback):
    input = {'feedback': [feedback]}
    x = mongo.db.Data.insert_one(input)
    return 'updated'

#For posting errors
@app.route('/api/error/2/<feedback>' , methods = ['GET','PUT'])
def sub_preferences(feedback):
    input = {'feedback': [feedback]}
    x = mongo.db.Warning.insert_one(input)
    return 'updated'

#For posting errors
@app.route('/api/error/3/<feedback>' , methods = ['GET','PUT'])
def sub_data(feedback):
    input = {'feedback': [feedback]}
    x = mongo.db.Timetable.insert_one(input)
    return 'updated'

#For posting errors
@app.route('/api/error/4/<feedback>' , methods = ['GET','PUT'])
def sub_timetable(feedback):
    input = {'feedback': [feedback]}
    x = mongo.db.Others.insert_one(input)
    return 'updated'



if __name__ == "__main__":
    app.run(debug=True, port = 3230)

#To run this programme, just run this file and in the terminal there will be a link to the site you using
#That will look something like http://<random numbers>/, so to get the mod info data
#You just run http://<random numbers>/api/<Mod code>
#Random numbers shd look something like this <http://127.0.0.1:5000/>