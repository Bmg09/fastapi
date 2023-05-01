from .. import model, schemas,oauth2
from typing import List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#retrieve all posts
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):#limit is used as query string parameter
    # cursor.execute("SELECT * FROM posts")
    # post = cursor.fetchall()
    post = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    result  = db.query(model.Post,func.count(model.Vote.post_id).label("votes")).join(model.Vote,model.Post.id == model.Vote.post_id,isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(result)
    return result

#post request to the endpoint '/posts' here post is the class which extends pydantic BaseModel
#parameter post is object of the class post and is used to pass data through the request 
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    # **post.dict() is used to convert the pydantic object to a dictionary and unpack it to pass it as keyword arguments
    print(user.email)
    new_post = model.Post(owner_id =user.id, **post.dict())
    # new_post = model.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#get request a single post by id
@router.get("/{id}",response_model=schemas.PostOut)
#if the id is not integer then it throw a internal server error to avoid that we use id:int which 
#also converts the url string to integer
def get_post(id:int,db: Session = Depends(get_db),user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id),))
    # post = cursor.fetchone()
    # post = db.query(model.Post).filter(model.Post.id == id).first()
    post = db.query(model.Post,func.count(model.Vote.post_id).label("votes")).join(model.Vote,model.Post.id == model.Vote.post_id,isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post not found with {id}"}
    return post


#delete a post by id
#HTTPEXCEPTION 204 NO CONTENT is used in delete request
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *",(str(id),))
    # delete_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Post is registered by you")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update a post by id
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,upated_post:schemas.PostCreate,db: Session = Depends(get_db),user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found with id {id}")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Hmmm")
    post_query.update(upated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()