from flask import Flask, jsonify, request
from pymongo import MongoClient


access_url = 'workflow-editor-datastore:27017'

class WorkflowCollection:

    def __init__(self):
        self.client = MongoClient(access_url)
        self.db = self.client.cwidev_db
        self.workflow_collection = self.db.workflow_collection

    def get_one_workflow(self, wid):
        workflow = self.workflow_collection.find_one({'_id': wid})
        if not workflow:
            return 'No results'
        return workflow

    def get_all_workflows(self):
        workflows = self.workflow_collection.find({})
        result = []
        for workflow in workflows:
            result.append(workflow)
        return result

    def add_workflow(self, workflow):
        self.workflow_collection.insert_one(workflow)
        return True

    def update_one_workflow(self, wid, updates={}):
        updates = {'$set': updates}
        self.workflow_collection.update_one({'_id': wid}, updates, True)

    def delete_one_workflow(self, wid):
        self.workflow_collection.delete_one({'_id': wid})
        return True

    def delete_all_workflows(self):
        self.workflow_collection.delete_many({})
        return True
