# === app/schemas/client_schema.py ===

from app.models.client import Client
from marshmallow import Schema, fields, validate, post_load
from app.utils.jwt_helper import encode_auth_token

class ClientSchema(Schema):
    user_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    phone = fields.Str(validate=validate.Length(max=255))
    address = fields.Str(validate=validate.Length(max=255))
    vehicle_number = fields.Str(validate=validate.Length(max=255))

    @post_load
    def make_client(self, data, **kwargs):
        return Client(**data)
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)