# app/services/post_service.py

from datetime import datetime

from flask import current_app
from elasticsearch import NotFoundError

from app.models.post_model import PostModel


class PostService:

    # Get all posts
    @staticmethod
    def get_posts():

        es = current_app.extensions["es"]

        try:

            response = es.search(
                index=current_app.config["ELASTIC_INDEX_POSTS"],

                query={
                    "match_all": {}
                }
            )

            posts = []

            for hit in response["hits"]["hits"]:

                posts.append(hit["_source"])

            return posts

        except NotFoundError:

            # If index does not exist yet
            return []

    # Get single post by id
    @staticmethod
    def get_post(post_id):

        es = current_app.extensions["es"]

        try:

            response = es.get(
                index=current_app.config["ELASTIC_INDEX_POSTS"],
                id=post_id
            )

            return response["_source"]

        except NotFoundError:

            return None

    # Create post
    @staticmethod
    def create_post(data, author_id):

        es = current_app.extensions["es"]

        post = PostModel.create_post(
            data,
            author_id
        )

        es.index(
            index=current_app.config["ELASTIC_INDEX_POSTS"],
            id=post["id"],
            document=post
        )

        return post

    # Update post
    @staticmethod
    def update_post(post_id, data):

        es = current_app.extensions["es"]

        try:

            response = es.get(
                index=current_app.config["ELASTIC_INDEX_POSTS"],
                id=post_id
            )

            post = response["_source"]

            post["title"] = data.get(
                "title",
                post["title"]
            )

            post["body"] = data.get(
                "body",
                post["body"]
            )

            post["tags"] = data.get(
                "tags",
                post["tags"]
            )

            post["updated_at"] = datetime.utcnow().isoformat()

            es.index(
                index=current_app.config["ELASTIC_INDEX_POSTS"],
                id=post_id,
                document=post
            )

            return post

        except NotFoundError:

            return None

    # Delete post
    @staticmethod
    def delete_post(post_id):

        es = current_app.extensions["es"]

        try:

            es.delete(
                index=current_app.config["ELASTIC_INDEX_POSTS"],
                id=post_id
            )

            return True

        except NotFoundError:

            return False