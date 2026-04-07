from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple,Union

import re

class Users(BaseModel):
    email: Optional[str]=None
    password: Optional[str]=None
    created_at_dt: Optional[Any]=None


class ReadUsers(BaseModel):
    email: Optional[str]=None
    password: Optional[str]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class UploadSessions(BaseModel):
    filename: Optional[str]=None
    total_rows: Optional[Union[int, float]]=None
    added_count: Optional[Union[int, float]]=None
    skipped_count: Optional[Union[int, float]]=None
    uploaded_at_dt: Optional[Any]=None


class ReadUploadSessions(BaseModel):
    filename: Optional[str]=None
    total_rows: Optional[Union[int, float]]=None
    added_count: Optional[Union[int, float]]=None
    skipped_count: Optional[Union[int, float]]=None
    uploaded_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class UserRecords(BaseModel):
    upload_session_id: Optional[Union[int, float]]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    email: Optional[str]=None
    tag: Optional[str]=None
    created_at_dt: Optional[Any]=None


class ReadUserRecords(BaseModel):
    upload_session_id: Optional[Union[int, float]]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    email: Optional[str]=None
    tag: Optional[str]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True




class PostUploadSessions(BaseModel):
    filename: Optional[str]=None
    total_rows: Optional[Union[int, float]]=None
    added_count: Optional[Union[int, float]]=None
    skipped_count: Optional[Union[int, float]]=None
    uploaded_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutUploadSessionsId(BaseModel):
    id: Union[int, float] = Field(...)
    filename: Optional[str]=None
    total_rows: Optional[Union[int, float]]=None
    added_count: Optional[Union[int, float]]=None
    skipped_count: Optional[Union[int, float]]=None
    uploaded_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostUsers(BaseModel):
    email: Optional[str]=None
    password: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutUsersId(BaseModel):
    id: Union[int, float] = Field(...)
    email: Optional[str]=None
    password: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostUserRecords(BaseModel):
    upload_session_id: Optional[Union[int, float]]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    email: Optional[str]=None
    tag: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutUserRecordsId(BaseModel):
    id: Union[int, float] = Field(...)
    upload_session_id: Optional[Union[int, float]]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    email: Optional[str]=None
    tag: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostPlatformAuthPackageMaysonAuthUserLogin(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)

    class Config:
        from_attributes = True



class PostPlatformAuthPackageMaysonAuthUserRegister(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)

    class Config:
        from_attributes = True



# Query Parameter Validation Schemas

class GetUploadSessionsIdQueryParams(BaseModel):
    """Query parameter validation for get_upload_sessions_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetUsersIdQueryParams(BaseModel):
    """Query parameter validation for get_users_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteUploadSessionsIdQueryParams(BaseModel):
    """Query parameter validation for delete_upload_sessions_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteUsersIdQueryParams(BaseModel):
    """Query parameter validation for delete_users_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetUserRecordsIdQueryParams(BaseModel):
    """Query parameter validation for get_user_records_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteUserRecordsIdQueryParams(BaseModel):
    """Query parameter validation for delete_user_records_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True
