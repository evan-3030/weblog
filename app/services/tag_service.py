# app/services/tag_service.py

from datetime import datetime

from flask import current_app

from elasticsearch import NotFoundError

from app.models.tag_model import TagModel


class TagService:

    # GET ALL TAGS
    @staticmethod
    def get_tags():

        es = current_app.extensions["es"]

        try:

            response = es.search(
                index=current_app.config["ELASTIC_INDEX_TAGS"],

                query={
                    "match_all": {}
                }
            )

            tags = []

            for hit in response["hits"]["hits"]:

                tags.append(hit["_source"])

            return tags

        except NotFoundError:

            return []

    # CREATE TAG
    @staticmethod
    def create_tag(data):

        es = current_app.extensions["es"]

        tag = TagModel.create_tag(data)

        es.index(
            index=current_app.config["ELASTIC_INDEX_TAGS"],

            id=tag["id"],

            document=tag
        )

        return tag

    # UPDATE TAG
    @staticmethod
    def update_tag(tag_id, data):

        es = current_app.extensions["es"]

        try:

            response = es.get(
                index=current_app.config["ELASTIC_INDEX_TAGS"],

                id=tag_id
            )

            tag = response["_source"]

            tag["title"] = data.get(
                "title",
                tag["title"]
            )

            tag["description"] = data.get(
                "description",
                tag["description"]
            )

            tag["updated_at"] = datetime.utcnow().isoformat()

            es.index(
                index=current_app.config["ELASTIC_INDEX_TAGS"],

                id=tag_id,

                document=tag
            )

            return tag

        except NotFoundError:

            return None

    # DELETE TAG
    @staticmethod
    def delete_tag(tag_id):

        es = current_app.extensions["es"]

        try:

            es.delete(
                index=current_app.config["ELASTIC_INDEX_TAGS"],

                id=tag_id
            )

            return True

        except NotFoundError:

            return False