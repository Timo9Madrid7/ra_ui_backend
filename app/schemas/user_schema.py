from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    # Dump only: only read
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    time_created = fields.Str(dump_only=True)


class UserUpdateSchema(Schema):
    username = fields.Str(allow_none=True, required=True)
    password = fields.Str(allow_none=True, required=True)
    roles = fields.List(cls_or_instance=fields.Int, required=True)


class UserSchema(PlainUserSchema):
    block = fields.Bool(dump_only=True)


class UserExportSchema(Schema):
    role_id = fields.Int(allow_none=True, required=True)
    search_content = fields.Str(allow_none=True, required=True)


class UserFilterSchema(UserExportSchema):
    page_size = fields.Int(allow_none=True, required=True)
    page = fields.Int(allow_none=True, required=True)


class UserPageSchema(Schema):
    results = fields.List(fields.Nested(UserSchema()))
    total_page = fields.Int()
    total_user = fields.Int()


class UserAndRoleSchema(Schema):
    message = fields.Str()


class RoleAndPermissionSchema(Schema):
    message = fields.Str()


class UpdateUserRoleSchema(Schema):
    roles = fields.List(cls_or_instance=fields.Int, required=True)


class UpdateBlockUserSchema(Schema):
    block = fields.Bool(required=True)


class CheckUserExistsSchema(Schema):
    email = fields.Str(required=True)


class UserLoginSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Nested(UserSchema)
