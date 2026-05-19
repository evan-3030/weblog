# app/routes/tags.py

from flask import request

from flask_restx import (
    Namespace,
    Resource,
    fields
)

from flask_jwt_extended import jwt_required

from app.services.tag_service import TagService


tags_ns = Namespace(
    "tags",
    description="Tags APIs"
)

# Swagger request model
tag_model = tags_ns.model("Tag", {

    "title": fields.String(required=True),

    "description": fields.String(required=True)
})


@tags_ns.route("")
class TagListResource(Resource):

    # GET /tags
    def get(self):

        return TagService.get_tags()

    # POST /tags
    @jwt_required()
    @tags_ns.expect(tag_model)
    def post(self):

        data = request.get_json()

        return TagService.create_tag(data), 201


@tags_ns.route("/<string:tag_id>")
class TagResource(Resource):

    # PUT /tags/<id>
    @jwt_required()
    @tags_ns.expect(tag_model)
    def put(self, tag_id):

        data = request.get_json()

        tag = TagService.update_tag(
            tag_id,
            data
        )

        if not tag:

            return {
                "message": "Tag not found"
            }, 404

        return tag

    # DELETE /tags/<id>
    @jwt_required()
    def delete(self, tag_id):

        deleted = TagService.delete_tag(
            tag_id
        )

        if not deleted:

            return {
                "message": "Tag not found"
            }, 404

        return {
            "message": "Tag deleted"
        }