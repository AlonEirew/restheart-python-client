import json
import urllib
import requests

ETAG_CONDITION = "If-Match"
CREATED_ON_TAG = "created_on"
CURRENT_DATE_TAG = "$currentDate";
DESCRIPTION_TAG = "description"
DEFAULT_LOCALHOST_URL = "http://127.0.0.1:8080/"


class RestHeartClientApi:

    mongo_url = DEFAULT_LOCALHOST_URL
    headers = {"content-type": "application/json"}


    def __init__(self, mongo_url):
        self.mongo_url = mongo_url

    def create_new_database(self, database_name, database_description=None):
        current_date = {CREATED_ON_TAG: True}
        data = {CURRENT_DATE_TAG: current_date}
        if database_description is not None:
            data[DESCRIPTION_TAG] = database_description
        url = self.mongo_url_builder(dbname=database_name)
        r = requests.put(url, headers=self.headers, json=data)
        print(r.status_code)
        return r

    def delete_data_base(self, database_name, database_etag):
        headers = self.create_headers_list(database_etag)
        url = self.mongo_url_builder(dbname=database_name)
        r = requests.delete(url, headers=headers)
        print(r.status_code)
        return r

    def create_new_collection(self, database_name, collection_name, collection_description=None):
        if collection_description is not None:
            json = {DESCRIPTION_TAG: collection_description}
        url = self.mongo_url_builder(dbname=database_name, collname=collection_name)
        r = requests.put(url, json=json)
        print(r.status_code)
        return r

    def insert_document_in_collection(self, database_name, collection_name, document_to_insert):
        url = self.mongo_url_builder(dbname=database_name, collname=collection_name)
        r = requests.post(url, headers=self.headers, json = document_to_insert)
        print(r.status_code)
        return r

    def delete_document_by_id(self, database_name, collection_name, document_id):
        url = self.mongo_url_builder(dbname=database_name, collname=collection_name, docid=document_id)
        r = requests.delete(url)
        print(r.status_code)
        return r

    def get_all_documents_from_collection(self, database_name, collection_name):
        url = self.mongo_url_builder(dbname=database_name, collname=collection_name)
        r = requests.get(url)
        print(r.status_code)
        return r

    def get_document_by_id(self, database_name, collection_name, document_id):
        url = self.mongo_url_builder(dbname=database_name, collname=collection_name, docid=document_id)
        r = requests.get(url)
        print(r.status_code)
        return r

    def get_documents_query(self, database_name, collection_name, query):
        encode = urllib.parse.quote_plus(query)
        url = self.mongo_url_builder(dbname=database_name, collname=collection_name) + "?" + encode
        r = requests.get(url)
        print(r.status_code)
        return r

    def create_headers_list(self, collETag):
        return {ETAG_CONDITION: collETag}

    def delete_collection(self, database_name, collection_name, collection_etag):
        headers = self.create_headers_list(collection_etag)
        url = self.mongo_url_builder(dbname=database_name, collname=collection_name)
        r = requests.delete(url, headers=headers)
        print(r.status_code)
        return r

    def mongo_url_builder(self, dbname=None, collname=None, docid = None):
        url = self.mongo_url + dbname
        if collname is not None:
            url += "/" + collname
            if docid is not None:
                url += "/" + docid
        return url


class RestHeartClientResponse():
    ETAG_LABEL = "ETag"
    LOCATION_LABEL = "Location"

    @staticmethod
    def get_etag(r):
        return r.headers[RestHeartClientResponse.ETAG_LABEL]

    @staticmethod
    def get_document_url_location(r):
        return r.headers[RestHeartClientResponse.LOCATION_LABEL]

    @staticmethod
    def get_status_code(r):
        return r.status_code

    @staticmethod
    def get_headers(r):
        return r.headers

    @staticmethod
    def get_content(r):
        return r.content

    @staticmethod
    def get_response_data_dict(r):
        return json.loads(r.content.decode("utf-8"))
