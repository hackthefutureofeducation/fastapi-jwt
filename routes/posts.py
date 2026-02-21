from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from utils.database import get_db
from utils.models import Posts, PostsBase, Reactions
from .users import info

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/new")
def create_post(post:PostsBase, db = Depends(get_db), current_user: dict = Depends(info)):
    now = datetime.now()
    post_data = Posts(
        title=post.title,
        content=post.content,
        author_id=current_user.id,
        reaction_love=0,
        created_date=now,
        updated_date=now
    )
    db.add(post_data)
    db.commit()
    db.refresh(post_data)
    return post_data

@router.get("/all")
def get_all_posts(limit: int = 10, skip: int = 0, db = Depends(get_db)):
    posts = db.query(Posts).offset(skip).limit(limit).all()
    return posts

@router.get("/{id}")
def retrieve_post(id: int, db = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    return post

@router.put("/update/{id}", response_model=PostsBase)
def update_post(id:int, updated_post:PostsBase, db = Depends(get_db), current_user: dict = Depends(info)):
    post_query = db.query(Posts).filter(Posts.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    if current_user.id != post.author_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT THE OWNER")
    post_data = updated_post.dict()
    post_data['updated_date'] = datetime.now()
    post_query.update(post_data, synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/delete/{id}")
def remove_post(id:int, db = Depends(get_db), current_user:dict = Depends(info)):
    post_query = db.query(Posts).filter(Posts.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    if current_user.id != post.author_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="YOU ARE NOT THE OWNER")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Post deleted successfully"}

@router.post("/reactions/{id}")
def new_reaction(id:int, db = Depends(get_db), current_user:dict = Depends(info)):
    post_query = db.query(Posts).filter(Posts.id == id).first()
    if post_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    reaction_query = db.query(Reactions).filter(Reactions.post_id == id and Reactions.user_id == current_user.id).first()
    if reaction_query:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="You already liked that post, use delete to remove")
    
    reaction_data = Reactions(
        user_id=current_user.id,
        post_id=id
    )
    db.add(reaction_data)
    db.commit()
    db.refresh(reaction_data)
    return {"detail": "Added"}

@router.get("/reactions/{id}")
def get_reactions(id:int, db=Depends(get_db)):
    reactions = db.query(Reactions).filter(Reactions.post_id == id).all()
    return reactions

@router.delete("/reactions/{id}")
def delete_reactions(id: int, db=Depends(get_db), current_user:dict = Depends(info)):
    reaction = db.query(Reactions).filter(Reactions.post_id == id and Reactions.user_id == current_user.id)
    if reaction.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can't find reaction, please add it")
    reaction.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Post deleted successfully"}