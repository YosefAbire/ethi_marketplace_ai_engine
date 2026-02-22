import os
import firebase_admin
from firebase_admin import auth, credentials
from fastapi import Header, HTTPException, Depends, status
from typing import Optional

# Initialize Firebase Admin SDK
# Try to load from environment variable first, then fallback to local file
service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "serviceAccountKey.json")

if not firebase_admin._apps:
    if os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    else:
        # In development/CI, we might not have a service account file
        # We can still initialize it, but token verification will fail
        # This allows the app to start even without the key
        print(f"WARNING: Firebase service account file not found at {service_account_path}")
        firebase_admin.initialize_app()

async def verify_firebase_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.split("Bearer ")[1]
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying Firebase token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency to get the current user from the token
async def get_current_user(decoded_token: dict = Depends(verify_firebase_token)):
    return decoded_token
