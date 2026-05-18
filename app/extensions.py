from flask_jwt_extended import JWTManager
from elasticsearch import Elasticsearch
import os


jwt = JWTManager()


def create_es():
    return Elasticsearch(
        "https://localhost:9200",
        basic_auth=("elastic", "IIvYHWSHZYHI6DPkkoqg"),
        verify_certs=False
    )



#in the base for server should type password:

# def create_es():

#     base_dir = os.path.abspath(os.path.dirname(__file__))
#     cert_path = os.path.join(base_dir, "ca.crt")

#     print("cert_path",cert_path)


#     return Elasticsearch(
#         "https://localhost:9200",
#         basic_auth=("elastic", "1qaz2wsx"),
#         ca_certs=cert_path)



