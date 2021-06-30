from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from apriori import apr, ranList

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "API"
app.config["MONGO_URI"] = "mongodb+srv://Derek:sciencemajic123@cluster0.xedr3.mongodb.net/API?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE"
CORS(app)
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
def get_rec(inp):
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
    return oD



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
    document2 = mongo.db.find_one({'_id': input})
    return document2

#For returning the list of module codes
@app.route('/api/semD/modList/<letters>', methods = ['GET'])
def get_mod_codes(letters):
    length = len(letters)
    collection = mongo.db.semD.find()
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

if __name__ == "__main__":
    app.run(debug=True, port = 3230)

#To run this programme, just run this file and in the terminal there will be a link to the site you using
#That will look something like http://<random numbers>/, so to get the mod info data
#You just run http://<random numbers>/api/<Mod code>
#Random numbers shd look something like this <http://127.0.0.1:5000/>