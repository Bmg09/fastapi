from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session

from .. import schemas,model,database,oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session = Depends(database.get_db),current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="notfound")
    vote_query = db.query(model.Vote).filter(model.Vote.post_id == vote.post_id,model.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir==1):
        if(found_vote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Post with {vote.post_id} is already liked by user with {current_user.id} id")
        new_vote = model.Vote(post_id = vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"vote doesnt exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"Vote removed"}