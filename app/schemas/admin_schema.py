# === app/schemas/admin_schema.py ===
# app/schemas/admin_schema.py
from app.models.admin import Admin
from marshmallow import Schema, fields, validate, post_load


class AdminSchema(Schema):
    user_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    CREATE = fields.Boolean()
    UPDATE = fields.Boolean()
    READ = fields.Boolean()
    DELETE = fields.Boolean()

    @post_load
    def make_admin(self, data, **kwargs):
        return Admin(**data)
    
admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)
    
