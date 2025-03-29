from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrmUser(Base):
    __tablename__ = "users"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), index=True)
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    email = sa.Column(sa.String(), index=True)
    name = sa.Column(sa.String())
    surname = sa.Column(sa.String())
    is_admin = sa.Column(sa.Boolean(), default=False)
    is_deleted = sa.Column(sa.Boolean(), default=False)


class OrmExternalOauthType(Base):
    __tablename__ = "external_oauth_types"

    id = sa.Column(sa.SmallInteger(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), index=True)
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    name = sa.Column(sa.String(unique=True))


class OrmUserExternalOauth(Base):
    __tablename__ = "user_external_oauths"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), index=True)
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    user_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True)
    oauth_service_type_id = sa.Column(sa.SmallInteger(), sa.ForeignKey("external_oauth_types.id"), index=True)
    is_deleted = sa.Column(sa.Boolean(), default=False)


class OrmFiles(Base):
    __tablename__ = "files"
    
    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), index=True)
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    user_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True)
    name = sa.Column(sa.String(), nullable=False)
    