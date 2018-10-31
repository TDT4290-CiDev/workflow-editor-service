from pymongo import MongoClient
from bson.objectid import ObjectId


access_url = 'workflow-editor-datastore:27017'


class WorkflowCollection:

    def __init__(self):
        self.client = MongoClient(access_url)
        self.db = self.client.cidev_db
        self.workflow_collection = self.db.workflow_collection

    def get_one_workflow(self, wid):
        workflow = self.workflow_collection.find_one(ObjectId(wid))
        if not workflow:
            return 'No results'
        workflow['_id'] = str(workflow['_id'])
        return workflow

    def get_all_workflows(self):
        with self.workflow_collection.find({}) as workflows:
            result = []
            for w in workflows:
                w['_id'] = str(w['_id'])
                result.append(w)
        return result

    def add_workflow(self, workflow):
        wid = self.workflow_collection.insert_one(workflow).inserted_id
        return str(wid)

    def update_one_workflow(self, wid, updates):
        updates = {'$set': updates}

        self.workflow_collection.update_one({'_id': ObjectId(wid)}, updates)

    def delete_one_workflow(self, wid):
        self.workflow_collection.delete_one({'_id': ObjectId(wid)})
        return True

    def delete_all_workflows(self):
        self.workflow_collection.delete_many({})
        return True
