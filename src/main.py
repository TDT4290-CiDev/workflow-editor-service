from http import HTTPStatus
from flask import Flask, jsonify, request
from pymongo import MongoClient

from workflow_collection import WorkflowCollection


app = Flask(__name__)

access_url = 'workflow-editor-datastore:27017'

workflow_collection = WorkflowCollection(MongoClient(access_url))


@app.route('/', methods=['GET'])
def get_all_workflows():
    workflows = workflow_collection.get_all_workflows()
    return jsonify({'data': workflows})


@app.route('/', methods=['POST'])
def add_workflow():
    workflow = request.get_json()
    wid = workflow_collection.add_workflow(workflow)
    return wid, HTTPStatus.CREATED


@app.route('/<wid>', methods=['GET'])
def get_one_workflow(wid):
    try:
        workflow = workflow_collection.get_one_workflow(wid)
        return jsonify({'data': workflow})
    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


@app.route('/<wid>', methods=['PUT'])
def update_one_workflow(wid):
    try:
        body = request.get_json()
        workflow_collection.update_one_workflow(wid, body)
        return '', HTTPStatus.NO_CONTENT
    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND

@app.route('/<wid>', methods=['DELETE'])
def delete_one_workflow(wid):
    try:
        workflow_collection.delete_one_workflow(wid)
        return '', HTTPStatus.NO_CONTENT
    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
