from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrmApiLog(Base):
    __tablename__ = "api_logs"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), index=True)
    session_id = sa.Column(psql.UUID(as_uuid=True))
    uri = sa.Column(sa.String())
    method = sa.Column(sa.String(16))
    status_code = sa.Column(sa.SmallInteger())
    query = sa.Column(psql.JSONB())
    body = sa.Column(psql.JSONB())
    headers = sa.Column(psql.JSONB())
    cookies = sa.Column(psql.JSONB())
    traceback = sa.Column(sa.String())


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


class OrmUserExternalOauth(Base):
    __tablename__ = "user_external_oauths"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), index=True)
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    user_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True, nullable=False)
    external_id = sa.Column(sa.String(), index=True, nullable=False)


class OrmSession(Base):
    __tablename__ = "sessions"

    id = sa.Column(psql.UUID(as_uuid=True), default=uuid4, primary_key=True)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), index=True)
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    user_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True, nullable=False)
    expires_at = sa.Column(sa.DateTime(), nullable=False)
    ip = sa.Column(sa.String(64))
    user_agent = sa.Column(psql.JSONB())
    is_deactivated = sa.Column(sa.Boolean(), index=True)


class OrmFiles(Base):
    __tablename__ = "files"

    id = sa.Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime(), server_default=sa.func.now(), index=True)
    updated_at = sa.Column(sa.DateTime(), onupdate=sa.func.now())
    user_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True)
    name = sa.Column(sa.String(), nullable=False)
    path = sa.Column(sa.String(), nullable=False)
