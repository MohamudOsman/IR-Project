from flask import Flask, request, jsonify

import System

# from importlib_metadata import method_cache

port = 8000

app = Flask(__name__)

@app.route('/initialize', methods=['GET'])
def initialize():
    print("initialize")
    try:
        return jsonify(success=True)
    except:
        return jsonify(success=False)


@app.route('/search', methods=['GET'])
def search():
    print('search')
    try:
        data = request.get_json(force=True)
        if not System.selectDataSet(data['dataset'],System.getdataSetNow(),data['numResult']):
            return jsonify(success=False)
        res = System.query(data['query'],data['advantage'])
        print(res)
        return jsonify(res.to_json(orient ='index'))
    except:
        raise #TODO handle
        return jsonify(success=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)