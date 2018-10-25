from flask import Flask, jsonify, request
from workflow_collection import WorkflowCollection


app = Flask(__name__)

workflow_collection = WorkflowCollection()

@app.route('/', methods=['GET'])
def get_all_workflows():
    workflows = workflow_collection.get_all_workflows()
    return jsonify(workflows)

@app.route('/', methods=['POST'])
def add_workflow():
    workflow = request.get_json()
    workflow_collection.add_workflow(workflow)
    return 'Successfully inserted document'

@app.route('/<wid>', methods=['GET'])
def get_one_workflow(wid):
    workflow = workflow_collection.get_one_workflow(wid)
    return workflow


@app.route('/<wid>', methods=['PUT'])
def update_one_workflow(wid):
    workflow_collection.update_one_workflow(wid)
    return 'Successfully updated document'

@app.route('/<wid>', methods=['DELETE'])
def delete_one_workflow(wid):
    successfully_deleted = workflow_collection.delete_one_workflow(wid)
    if successfully_deleted:
        return '', 204
    else:
        return 'Workflow with id %d does not exist', 404


# Only for testing purposes - should use WSGI server in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
