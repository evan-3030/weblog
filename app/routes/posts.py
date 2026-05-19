# app/routes/posts.py

from flask import request

from flask_restx import (
    Namespace,
    Resource,
    fields
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.services.post_service import PostService


posts_ns = Namespace(
    "posts",
    description="Posts APIs"
)

# Swagger request model
post_model = posts_ns.model("Post", {

    "title": fields.String(required=True),

    "body": fields.String(required=True),

    "tags": fields.List(fields.String)
})


@posts_ns.route("")
class PostListResource(Resource):

    # GET /posts
    def get(self):

        return PostService.get_posts()

    # POST /posts
    @jwt_required()
    @posts_ns.expect(post_model)
    def post(self):

        data = request.get_json()

        author_id = get_jwt_identity()

        return PostService.create_post(
            data,
            author_id
        ), 201


@posts_ns.route("/<string:post_id>")
class PostResource(Resource):

    # GET /posts/<id>
    def get(self, post_id):

        post = PostService.get_post(post_id)

        if not post:

            return {
                "message": "Post not found"
            }, 404

        return post

    # PUT /posts/<id>
    @jwt_required()
    @posts_ns.expect(post_model)
    def put(self, post_id):

        data = request.get_json()

        post = PostService.update_post(
            post_id,
            data
        )

        if not post:

            return {
                "message": "Post not found"
            }, 404

        return post

    # DELETE /posts/<id>
    @jwt_required()
    def delete(self, post_id):

        deleted = PostService.delete_post(
            post_id
        )

        if not deleted:

            return {
                "message": "Post not found"
            }, 404

        return {
            "message": "Post deleted"
        }