import unittest
import mongomock
from bson.objectid import ObjectId

from workflow_collection import WorkflowCollection


class CollectionTest(unittest.TestCase):
    mock_coll = None
    initial_workflows = None

    def setUp(self):
        self.mock_coll = WorkflowCollection(mongomock.MongoClient())
        self.initial_workflows = [dict(title='workflow1'), dict(title='workflow2')]
        for f in self.initial_workflows:
            f['_id'] = str(self.mock_coll.db.workflow_collection.insert_one(f).inserted_id)

    def test_add_return_valid_id(self):
        add_response = self.mock_coll.add_workflow({"title": "test"})
        self.assertTrue(ObjectId.is_valid(add_response))

    def test_read_one(self):
        _id = self.initial_workflows[0]['_id']
        read_response = self.mock_coll.get_one_workflow(_id)
        self.assertEqual(read_response, self.initial_workflows[0])

    def test_read_all(self):
        all = self.mock_coll.get_all_workflows()
        self.assertEqual(all, self.initial_workflows)

    def test_update_no_return(self):
        _id = self.initial_workflows[0]['_id']
        update_res = self.mock_coll.update_one_workflow(_id, dict(new_title='Updated workflow1'))
        self.assertIsNone(update_res)

    def test_delete_no_return(self):
        _id = self.initial_workflows[0]['_id']
        deleteRes = self.mock_coll.delete_one_workflow(_id)
        self.assertIsNone(deleteRes)

    def test_invalid_id_format(self):
        inv_id = '0'
        with self.assertRaises(ValueError):
            self.mock_coll.get_one_workflow(inv_id)
        with self.assertRaises(ValueError):
            self.mock_coll.update_one_workflow(inv_id, {})
        with self.assertRaises(ValueError):
            self.mock_coll.delete_one_workflow(inv_id)

    def test_valid_but_nonexisting_id(self):
        # Creating an id of correct length, but with all 5s.
        inv_id = '5'*len(self.initial_workflows[0]['_id'])
        with self.assertRaises(ValueError):
            self.mock_coll.get_one_workflow(inv_id)
        with self.assertRaises(ValueError):
            self.mock_coll.update_one_workflow(inv_id, {})
        with self.assertRaises(ValueError):
            self.mock_coll.delete_one_workflow(inv_id)