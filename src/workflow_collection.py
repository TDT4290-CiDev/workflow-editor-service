from bson.objectid import ObjectId
from bson.errors import InvalidId



def catch_invalid_id(form_operator):
    def catch_wrapper(*args):
        try:
            return form_operator(*args)
        except InvalidId:
            raise ValueError('{} is not a valid ID. '.format(args[1]))
    return catch_wrapper


class WorkflowCollection:

    def __init__(self, client):
        self.client = client
        self.db = self.client.cidev_db
        self.workflow_collection = self.db.workflow_collection

    @catch_invalid_id
    def get_one_workflow(self, wid):
        workflow = self.workflow_collection.find_one(ObjectId(wid))
        if not workflow:
            raise ValueError('Workflow with ID {} does not exist.'.format(wid))
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

    @catch_invalid_id
    def update_one_workflow(self, wid, updates):
        updates = {'$set': updates}
        update_res = self.workflow_collection.update_one({'_id': ObjectId(wid)}, updates)
        if update_res.matched_count == 0:
            raise ValueError('Workflow with ID {} does not exist.'.format(wid))

    @catch_invalid_id
    def delete_one_workflow(self, wid):
        del_res = self.workflow_collection.delete_one({'_id': ObjectId(wid)})
        if del_res.deleted_count == 0:
            raise ValueError('Workflow with ID {} does not exist.'.format(wid))


    def delete_all_workflows(self):
        self.workflow_collection.delete_many({})
        return True
