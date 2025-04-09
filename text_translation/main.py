from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from text_translation import models, database, auth, schemas
from text_translation.database import engine
from text_translation.translation_service import TranslationService
from pydantic import BaseModel
from typing import Optional
from text_translation import config

# Initialize the translation service with a preferred model
translation_service = TranslationService()  # Example model

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Text Translation Service")

class TranslationRequest(BaseModel):
    text: str
    sender_type: str  # 'staff' or 'user'
    user_language: Optional[str] = None
    model_name: Optional[str] = None

# @app.post("/signup", status_code=status.HTTP_201_CREATED)
# async def signup(client: schemas.ClientCreate, db: Session = Depends(database.get_db)):
#     db_client = db.query(models.Client).filter(models.Client.email == client.email).first()
#     if db_client:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     hashed_password = auth.get_password_hash(client.password)
#     new_client = models.Client(organization_name=client.organization_name, email=client.email, hashed_password=hashed_password)
#     db.add(new_client)
#     db.commit()
#     db.refresh(new_client)
#     return {"message": "Client registered successfully"}

# @app.post("/token", response_model=schemas.Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     client = auth.authenticate_client(db, form_data.username, form_data.password)
#     if not client:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = auth.create_access_token(
#         data={"sub": client.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

@app.post("/translate/")
async def translate_text(request: TranslationRequest):
    try:
        # Detect the source language if not provided
        source_language = request.user_language or translation_service.detect_language(request.text)
        
        # Determine target language based on sender type
        if request.sender_type == 'staff':
            target_language = request.user_language or source_language
        else:  # sender_type == 'user'
            target_language = config.STAFF_LANGUAGE

        # Use default model if not specified
        model_name = request.model_name or config.DEFAULT_MODEL

        # Translate the text
        translated_text = translation_service.translate(request.text, model_name, target_language)
        
        return {
            "source_language": source_language,
            "target_language": target_language,
            "translated_text": translated_text,
            "model_used": model_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Text Translation Service!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
