from fastapi import APIRouter, HTTPException,Request
from app.models.linkedin_model import LinkedinConnect
from app.models.user_model import User
from bson import ObjectId
from app.schemas.linkedin_schema import LinkedinConnectCreate
from datetime import datetime

router = APIRouter()

# ✅ POST API (create a LinkedIn connection)
@router.post("/")
async def create_linkedin_connection(request: Request, data: LinkedinConnectCreate):
    user_data = request.state.user 
    user_id = ObjectId(user_data["sub"])
    user = await User.find_one({"_id": user_id}) 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    linkedin = LinkedinConnect(
        user_id=user_id,
        linkedin_id=data.linkedin_id,
        access_token=data.access_token,
        refresh_token=data.refresh_token,
        expires_in=data.expires_in
    ) 
    
    await linkedin.insert()
    
    user.is_linkedin_connected = True
    user.updated_at = datetime.now()
    await user.save()

    return {
        "message": "LinkedIn account connected successfully",
        "id": str(linkedin.id)
    }

# ✅ GET API (fetch by user_id)
@router.get("/")
async def get_linkedin_connection(request: Request):
    user_data = request.state.user  
    user_id = ObjectId(user_data["sub"])
    linkedin = await LinkedinConnect.find_one({"user_id": ObjectId(user_id)})
    if not linkedin:
        raise HTTPException(status_code=404, detail="LinkedIn connection not found")
    return linkedin
