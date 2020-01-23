"""
This python script holds the Flask server and production AI code for the Digital Twins PoC.
This is the main python script called to return.
"""

from flask import Flask, make_response, jsonify
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS, cross_origin
from reverseModeling import max_prod

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)



float_package = None
smelt_package = None

parser = reqparse.RequestParser()
parser.add_argument('asset')
parser.add_argument('constraints')

def reverseModelingWrapper(asset, constraints, constraints_raw):
    opt_in, opt_out = max_prod(asset, constraints)

    # process return variable
    r = {}
    r['asset'] = str(asset)
    r['constraints'] = str(constraints_raw)
    r['opt_in'] = convertReturn(opt_in)
    r['opt_out'] = str(opt_out)

    return r

def parsePost(string):
    # Parsing values from post request

    ls = list(string.split(","))
    for i, l in enumerate(ls):
        ls[i] = str(l)
    for i, l in enumerate(ls):
        ls[i] = None if l == 'None' else l
    for i, l in enumerate(ls):
        ls[i] = float(l) if l != None else l

    return ls


def convertReturn(ls):
    # Converting values into format accepted by post requester

    string = ""
    for l in ls:
        string = string + str(l)
        if l != ls[-1]:
            string = string + ","

    return string


@app.route('/')
@cross_origin()
def index():
    return "Hello Flask"

@app.errorhandler(404)
def not_found(error):
    # Error Handler
    return make_response(jsonify({'error': 'Not found'}), 404)

class AI(Resource):
    def get(self):
        return {'resp': 'Hello Flask'}

    def post(self):
        args = parser.parse_args()
        args['constraints_raw'] = args['constraints']
        args['constraints'] = parsePost(args['constraints_raw'])
        r = reverseModelingWrapper(args['asset'], args['constraints'], args['constraints_raw'])  # main function
        # Return Branch CC
        return r, 201


api.add_resource(AI, '/flask/api')


if __name__ == '__main__':
    # Run the flask server
    # This function just responds to the browser ULR localhost:5000/
    app.run()

    # API Calls:
    # localhost:5000/flask/api?asset=float&constraints=56.2,14.8,397.5,9.76,1.67,2847.0,488.7,281.28,520.4
    # localhost:5000/flask/api?asset=smelt&constraints=65,1.67,0.21,5.3,5,650,280

    # Flotation Input and Output Parameters:
    # Inputs: '% Metal Concentrate Input','% Silica Feed','Ore Pulp Flow','Ore Pulp pH','Ore Pulp Density','Starch Flow','Nitrogen Flow','Flotation Column 01 Air Flow','Flotation Column 01 Level'
    # Output: '% Metal Concentrate Output'

    # Smelting Input and Output Parameters:
    # Inputs: "% Metal Concentrate Input","Gas Flow","Oxygen Flow","Coke Feed","RPM","Smelting Time","Smelt Level"
    # Output: '% Metal Concentrate Output'

