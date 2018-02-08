import unittest

from restheart_python_client.rest_heart_client import RestHeartClientResponse, RestHeartClientApi

get_etag = RestHeartClientResponse.get_etag
get_status_code = RestHeartClientResponse.get_status_code
get_document_url_location = RestHeartClientResponse.get_document_url_location
get_content = RestHeartClientResponse.get_content
get_response_data_dict = RestHeartClientResponse.get_response_data_dict
get_headers = RestHeartClientResponse.get_headers

db_name = "testDb"
coll_name = "testColl"
DEFAULT_LOCALHOST_URL = "http://127.0.0.1:8080/"

class TestRestHeartClient(unittest.TestCase):

    api = None
    mongo_url = DEFAULT_LOCALHOST_URL
    creation_response_db = None

    def setUp(self):
        self.api = RestHeartClientApi(self.mongo_url)
        self.create_data_base()

    def tearDown(self):
        self.drop_data_base()

    def test_create_and_delete_collection(self):
        new_collection = self.create_collection()
        r = self.api.delete_collection(db_name, coll_name, get_etag(new_collection))
        self.assertEqual(get_status_code(r), 204)

    def test_delete_doc_by_ID(self):
        self.create_collection()
        r = self.insert_doc_in_db()
        doc_url_loc = get_document_url_location(r)
        id_delete = get_id_from_url(doc_url_loc)
        r = self.api.delete_document_by_id(db_name, coll_name, id_delete)
        self.assertEqual(get_status_code(r), 204)

    def test_get_all_docs(self):
        self.create_collection()
        self.insert_doc_in_db()
        self.insert_doc_in_db()
        r = self.api.get_all_documents_from_collection(db_name, coll_name)
        self.assertIsNotNone(r)
        self.assertIsNotNone(get_content(r))
        self.assertTrue(get_response_data_dict(r)["_returned"] == 2)

    def test_test_get_doc_by_ID(self):
        self.create_collection()
        r = self.insert_doc_in_db()
        doc_url_loc = get_document_url_location(r)
        id_create = get_id_from_url(doc_url_loc)
        r = self.api.get_document_by_id(db_name, coll_name, id_create)
        self.assertIsNotNone(r)
        self.assertIsNotNone(get_content(r))
        self.assertEqual(get_response_data_dict(r)['_id']['$oid'], id_create)

    def test_get_doc_query(self):
        self.create_collection()
        self.insert_doc_in_db()
        self.insert_doc_in_db()

        query = 'filter={"name":"John"}'
        r = self.api.get_documents_query(db_name, coll_name, query)
        self.assertIsNotNone(r)
        self.assertIsNotNone(get_content(r))
        print(get_response_data_dict(r))
        self.assertTrue(get_response_data_dict(r)["_returned"] == 2)

    def create_data_base(self):
        self.creation_response_db = self.api.create_new_database(db_name, "this is a test")
        try:
            self.assertEqual(201, get_status_code(self.creation_response_db))
        except:
            self.tearDown()
        try:
            self.assertIsNotNone(get_etag(self.creation_response_db))
        except:
            self.tearDown()

    def create_collection(self):
        r = self.api.create_new_collection(db_name, coll_name, "this is a test collection")
        self.assertEqual(201, get_status_code(r))
        self.assertIsNotNone(get_etag(self.creation_response_db))
        return r

    def insert_doc_in_db(self):
        json = {"Name": "John", "Last": "Smith"}
        r = self.api.insert_document_in_collection(db_name, coll_name, json)
        self.assertIsNotNone(r)
        self.assertIsNotNone(get_headers(r))
        self.assertTrue(len(get_headers(r)) > 0)
        self.assertIsNotNone(get_etag(self.creation_response_db))
        return r

    def drop_data_base(self):
        r = self.api.delete_data_base(db_name, get_etag(self.creation_response_db))
        self.assertEqual(get_status_code(r), 204)

def get_id_from_url(doc_url_loc):
    return doc_url_loc.rsplit('/', 1)[-1]

if __name__ == '__main__':
    unittest.main()
