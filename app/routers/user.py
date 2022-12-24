from .. import model, schemas, utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix="/users",tags=['Users']
)


#create a user and store it in the database check if the user already exists
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.userResponse)
def create_user(user:schemas.User,db: Session = Depends(get_db)):
    if db.query(model.User).filter(model.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    new_user = model.User(**user.dict())
    pwd_hash = utils.hash(user.password)
    new_user.password = pwd_hash
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#getting a user by id 
@router.get("/{id}",response_model=schemas.userResponse)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")    
    return user