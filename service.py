from sqlalchemy.orm import Session, aliased
from database import SessionLocal
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException, status
from fastapi.responses import RedirectResponse
import models, schemas
import boto3
import jwt
from datetime import datetime
import requests
import math
import os
import random
import asyncio
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


def convert_to_datetime(date_string):
    if date_string is None:
        return datetime.now()
    if not date_string.strip():
        return datetime.now()
    if "T" in date_string:
        try:
            return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        except ValueError:
            date_part = date_string.split("T")[0]
            try:
                return datetime.strptime(date_part, "%Y-%m-%d")
            except ValueError:
                return datetime.now()
    else:
        # Try to determine format based on first segment
        parts = date_string.split("-")
        if len(parts[0]) == 4:
            # Likely YYYY-MM-DD format
            try:
                return datetime.strptime(date_string, "%Y-%m-%d")
            except ValueError:
                return datetime.now()

        # Try DD-MM-YYYY format
        try:
            return datetime.strptime(date_string, "%d-%m-%Y")
        except ValueError:
            return datetime.now()

        # Fallback: try YYYY-MM-DD if not already tried
        if len(parts[0]) != 4:
            try:
                return datetime.strptime(date_string, "%Y-%m-%d")
            except ValueError:
                return datetime.now()

        return datetime.now()


async def get_upload_sessions(request: Request, db: Session):

    query = db.query(models.UploadSessions)

    upload_sessions_all = query.all()
    upload_sessions_all = (
        [new_data.to_dict() for new_data in upload_sessions_all]
        if upload_sessions_all
        else upload_sessions_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"upload_sessions_all": upload_sessions_all},
    }
    return res


async def get_upload_sessions_id(request: Request, db: Session, id: Union[int, float]):

    query = db.query(models.UploadSessions)
    query = query.filter(and_(models.UploadSessions.id == id))

    upload_sessions_one = query.first()

    upload_sessions_one = (
        (
            upload_sessions_one.to_dict()
            if hasattr(upload_sessions_one, "to_dict")
            else vars(upload_sessions_one)
        )
        if upload_sessions_one
        else upload_sessions_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"upload_sessions_one": upload_sessions_one},
    }
    return res


async def post_upload_sessions(
    request: Request,
    db: Session,
    raw_data: schemas.PostUploadSessions,
):
    filename: str = raw_data.filename
    total_rows: Union[int, float] = raw_data.total_rows
    added_count: Union[int, float] = raw_data.added_count
    skipped_count: Union[int, float] = raw_data.skipped_count
    uploaded_at_dt: str = convert_to_datetime(raw_data.uploaded_at_dt)

    record_to_be_added = {
        "filename": filename,
        "total_rows": total_rows,
        "added_count": added_count,
        "skipped_count": skipped_count,
        "uploaded_at_dt": uploaded_at_dt,
    }
    new_upload_sessions = models.UploadSessions(**record_to_be_added)
    db.add(new_upload_sessions)
    db.commit()
    db.refresh(new_upload_sessions)
    upload_sessions_inserted_record = new_upload_sessions.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"upload_sessions_inserted_record": upload_sessions_inserted_record},
    }
    return res


async def put_upload_sessions_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutUploadSessionsId,
):
    id: Union[int, float] = raw_data.id
    filename: str = raw_data.filename
    total_rows: Union[int, float] = raw_data.total_rows
    added_count: Union[int, float] = raw_data.added_count
    skipped_count: Union[int, float] = raw_data.skipped_count
    uploaded_at_dt: str = convert_to_datetime(raw_data.uploaded_at_dt)

    query = db.query(models.UploadSessions)
    query = query.filter(and_(models.UploadSessions.id == id))
    upload_sessions_edited_record = query.first()

    if upload_sessions_edited_record:
        for key, value in {
            "id": id,
            "filename": filename,
            "total_rows": total_rows,
            "added_count": added_count,
            "skipped_count": skipped_count,
            "uploaded_at_dt": uploaded_at_dt,
        }.items():
            setattr(upload_sessions_edited_record, key, value)

        db.commit()

        db.refresh(upload_sessions_edited_record)

        upload_sessions_edited_record = (
            upload_sessions_edited_record.to_dict()
            if hasattr(upload_sessions_edited_record, "to_dict")
            else vars(upload_sessions_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"upload_sessions_edited_record": upload_sessions_edited_record},
    }
    return res


async def get_users(request: Request, db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_all": users_all},
    }
    return res


async def get_users_id(request: Request, db: Session, id: Union[int, float]):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_one": users_one},
    }
    return res


async def post_users(
    request: Request,
    db: Session,
    raw_data: schemas.PostUsers,
):
    email: str = raw_data.email
    password: str = raw_data.password
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "email": email,
        "password": password,
        "created_at_dt": created_at_dt,
    }
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_inserted_record": users_inserted_record},
    }
    return res


async def put_users_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutUsersId,
):
    id: Union[int, float] = raw_data.id
    email: str = raw_data.email
    password: str = raw_data.password
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "id": id,
            "email": email,
            "password": password,
            "created_at_dt": created_at_dt,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()

        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_edited_record": users_edited_record},
    }
    return res


async def delete_upload_sessions_id(
    request: Request, db: Session, id: Union[int, float]
):

    query = db.query(models.UploadSessions)
    query = query.filter(and_(models.UploadSessions.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        upload_sessions_deleted = record_to_delete.to_dict()
    else:
        upload_sessions_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"upload_sessions_deleted": upload_sessions_deleted},
    }
    return res


async def delete_users_id(request: Request, db: Session, id: Union[int, float]):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_deleted": users_deleted},
    }
    return res


async def get_user_records(request: Request, db: Session):

    query = db.query(models.UserRecords)

    user_records_all = query.all()
    user_records_all = (
        [new_data.to_dict() for new_data in user_records_all]
        if user_records_all
        else user_records_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_records_all": user_records_all},
    }
    return res


async def get_user_records_id(request: Request, db: Session, id: Union[int, float]):

    query = db.query(models.UserRecords)
    query = query.filter(and_(models.UserRecords.id == id))

    user_records_one = query.first()

    user_records_one = (
        (
            user_records_one.to_dict()
            if hasattr(user_records_one, "to_dict")
            else vars(user_records_one)
        )
        if user_records_one
        else user_records_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_records_one": user_records_one},
    }
    return res


async def post_user_records(
    request: Request,
    db: Session,
    raw_data: schemas.PostUserRecords,
):
    upload_session_id: Union[int, float] = raw_data.upload_session_id
    first_name: str = raw_data.first_name
    last_name: str = raw_data.last_name
    email: str = raw_data.email
    tag: str = raw_data.tag
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "tag": tag,
        "email": email,
        "last_name": last_name,
        "first_name": first_name,
        "created_at_dt": created_at_dt,
        "upload_session_id": upload_session_id,
    }
    new_user_records = models.UserRecords(**record_to_be_added)
    db.add(new_user_records)
    db.commit()
    db.refresh(new_user_records)
    user_records_inserted_record = new_user_records.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_records_inserted_record": user_records_inserted_record},
    }
    return res


async def put_user_records_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutUserRecordsId,
):
    id: Union[int, float] = raw_data.id
    upload_session_id: Union[int, float] = raw_data.upload_session_id
    first_name: str = raw_data.first_name
    last_name: str = raw_data.last_name
    email: str = raw_data.email
    tag: str = raw_data.tag
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.UserRecords)
    query = query.filter(and_(models.UserRecords.id == id))
    user_records_edited_record = query.first()

    if user_records_edited_record:
        for key, value in {
            "id": id,
            "tag": tag,
            "email": email,
            "last_name": last_name,
            "first_name": first_name,
            "created_at_dt": created_at_dt,
            "upload_session_id": upload_session_id,
        }.items():
            setattr(user_records_edited_record, key, value)

        db.commit()

        db.refresh(user_records_edited_record)

        user_records_edited_record = (
            user_records_edited_record.to_dict()
            if hasattr(user_records_edited_record, "to_dict")
            else vars(user_records_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_records_edited_record": user_records_edited_record},
    }
    return res


async def delete_user_records_id(request: Request, db: Session, id: Union[int, float]):

    query = db.query(models.UserRecords)
    query = query.filter(and_(models.UserRecords.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        user_records_deleted = record_to_delete.to_dict()
    else:
        user_records_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_records_deleted": user_records_deleted},
    }
    return res


async def get_platform_auth_package_mayson_sso_auth_me(request: Request, db: Session):

    # get auth header

    try:
        auth_header = request.headers.get("authorization").replace("Bearer ", "")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    import jwt

    try:
        user_profile = jwt.decode(
            auth_header,
            """TjeS-dNhRibKfuYA9-nbOEoAaKX1OVP9dCIzWUDTX0g=""",
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"message": user_profile},
    }
    return res


async def get_platform_auth_package_mayson_sso_auth_login_google(
    request: Request, db: Session
):

    # define client

    try:
        import httpx

        async def google_login():
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": "Bearer v4.public.eyJlbWFpbF9pZCI6ICJheXVzaHNvdGkwM0BnbWFpbC5jb20iLCAidXNlcl9pZCI6ICIxYjA3MmQ1ZjFkMGY0YWNhYWNmNmIxOWMxMGEyYWQwMSIsICJvcmdfaWQiOiAiTkEiLCAic3RhdGUiOiAic2lnbnVwIiwgInJvbGVfbmFtZSI6ICJOQSIsICJyb2xlX2lkIjogIk5BIiwgInBsYW5faWQiOiAiMTAxIiwgImFjY291bnRfdmVyaWZpZWQiOiAiMSIsICJhY2NvdW50X3N0YXR1cyI6ICIwIiwgInVzZXJfbmFtZSI6ICJBeXVzaFNvdGkiLCAic2lnbnVwX3F1ZXN0aW9uIjogMCwgInRva2VuX2xpbWl0IjogbnVsbCwgInRva2VuX3R5cGUiOiAiYWNjZXNzIiwgImV4cCI6IDE3NzYxNzMyNDAsICJleHBpcnlfdGltZSI6IDE3NzYxNzMyNDB94FdADbbPp9EzCeb-kytd2njkJSlgzqcqT7sGs3AIJrLvw89yAp0oJaQOjHl9GUqiegtNI6yiwS7dpRV3ib8_CQ",
                    "Content-Type": "application/json",
                }

                res = await client.get(
                    "https://cc1fbde45ead-in-south-01.mayson.dev/sigma/api/v1/sso/auth/google/login?collection_id=coll_c1d9d0085dfd4897aa14a5e290c32226",
                    headers=headers,
                )

            res.raise_for_status()

            try:
                response_obj = dict(res.json())
                final_url = response_obj.get("value")
                return final_url
            except Exception as e:
                return f"https://mayson.dev/not-found?reason={str(e)}"

        return RedirectResponse(url=await google_login())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"message": "success_response"},
    }
    return res


async def post_platform_auth_package_mayson_auth_user_login(
    request: Request,
    db: Session,
    raw_data: schemas.PostPlatformAuthPackageMaysonAuthUserLogin,
):
    email: str = raw_data.email
    password: str = raw_data.password

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == email))

    oneRecord = query.first()

    oneRecord = (
        (oneRecord.to_dict() if hasattr(oneRecord, "to_dict") else vars(oneRecord))
        if oneRecord
        else oneRecord
    )

    if oneRecord:
        from passlib.hash import md5_crypt

        password_hash = oneRecord["password"]
        password_valid = md5_crypt.verify(password, password_hash)
        if password_valid:
            validated_password = True
        else:
            validated_password = False
    else:
        validated_password = False

    login_status: str = "Login initiated"

    if validated_password:

        login_status = "Login success"

    else:

        raise HTTPException(status_code=401, detail="Bad credentials.")

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == email))

    user_record = query.first()

    user_record = (
        (
            user_record.to_dict()
            if hasattr(user_record, "to_dict")
            else vars(user_record)
        )
        if user_record
        else user_record
    )

    import jwt
    from datetime import timezone

    secret_key = """TjeS-dNhRibKfuYA9-nbOEoAaKX1OVP9dCIzWUDTX0g="""
    bs_jwt_payload = {
        "exp": int(datetime.now(timezone.utc).timestamp() + 86400),
        "data": user_record,
    }

    generated_jwt = jwt.encode(bs_jwt_payload, secret_key, algorithm="HS256")

    login_status = "Login successful"

    res = {
        "status": 200,
        "message": "Login successful",
        "data": {"jwt": generated_jwt, "login_status": login_status},
    }
    return res


async def get_platform_auth_package_mayson_sso_auth_callback(
    request: Request, db: Session
):

    user_identity: str = "i"

    user_password: str = "top_secret_area_51"

    from passlib.hash import md5_crypt

    encrypt_pass = md5_crypt.hash(user_password)

    # get user email from request

    try:
        param_obj = dict(request.query_params)

        not_found_page = "https://mayson.dev/not-found"
        user_identity = param_obj.get(
            "user_email", "no-user-identity-received-from-backend"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    record_to_be_added = {"email": user_identity, "password": encrypt_pass}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    post_user_record = new_users.to_dict()

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == user_identity))

    user_record = query.first()

    user_record = (
        (
            user_record.to_dict()
            if hasattr(user_record, "to_dict")
            else vars(user_record)
        )
        if user_record
        else user_record
    )

    import jwt
    from datetime import timezone

    secret_key = """TjeS-dNhRibKfuYA9-nbOEoAaKX1OVP9dCIzWUDTX0g="""
    bs_jwt_payload = {
        "exp": int(datetime.now(timezone.utc).timestamp() + 86400),
        "data": user_record,
    }

    generated_jwt = jwt.encode(bs_jwt_payload, secret_key, algorithm="HS256")

    # define client

    try:
        request_token = generated_jwt or "no-generated-jwt"
        request_provider = param_obj.get("provider", "no-provider-from-backend")
        final_url = f'{param_obj.get("frontend-redirect", not_found_page)}?token={request_token}&provider={request_provider}'

        return RedirectResponse(url=final_url)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"message": "success_response"},
    }
    return res


async def post_platform_auth_package_mayson_auth_user_register(
    request: Request,
    db: Session,
    raw_data: schemas.PostPlatformAuthPackageMaysonAuthUserRegister,
):
    email: str = raw_data.email
    password: str = raw_data.password

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == email))

    existing_record = query.first()

    existing_record = (
        (
            existing_record.to_dict()
            if hasattr(existing_record, "to_dict")
            else vars(existing_record)
        )
        if existing_record
        else existing_record
    )

    if existing_record:

        raise HTTPException(status_code=400, detail="User already exists.")
    else:
        pass

    from passlib.hash import md5_crypt

    encrypt_pass = md5_crypt.hash(password)

    record_to_be_added = {"email": email, "password": encrypt_pass}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    post_user_record = new_users.to_dict()

    res = {"status": 200, "message": "User registered successfully", "data": {}}
    return res
