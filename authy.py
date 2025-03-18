from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader

API_KEY = "123"
api_key_header = APIKeyHeader(name="X-API-KEY")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
