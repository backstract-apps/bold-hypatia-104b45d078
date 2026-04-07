

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(
     "sqlite+libsql:///embedded.db",
     connect_args={
         "sync_url": "libsql://coll-c1d9d0085dfd4897aa14a5e290c32226-mayson.aws-ap-south-1.turso.io",
         "auth_token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NzU1Njg0MTUsInAiOnsicm9hIjp7Im5zIjpbIjAxOWQ2ODFmLWQ2MDEtNzJhZS04NzEyLWRmNzJlOTNkMzA1MiJdfSwicnciOnsibnMiOlsiMDE5ZDY4MWYtZDYwMS03MmFlLTg3MTItZGY3MmU5M2QzMDUyIl19fSwicmlkIjoiZGVhZDM1MzAtMDAxMy00NDRhLTkwNTUtODEwNGZmMTE4MTM2In0.133gylAOqd2monxgdyS2WgiiPvnm4JD8OpI0OvK9xgupqJwdCO8FvJvIRzmxTnS3Mkz_mg3MPdJnX5uyimYvCA",
     },
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()

