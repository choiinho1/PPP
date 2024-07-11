from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import TimeTable, User, EventInfo
from starlette import status
import datetime as dt
from . import event_schema
from . import event_crud
from domain.user.user_router import get_current_user
router = APIRouter(
    prefix="/ppp/event"
)
#해당 유저가 속해있는 event list 갖다놓기
@router.get("/my_event")
def event_list(db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    _event_list = event_crud.my_event(db=db, _current_user= current_user)
    return _event_list

#이벤트 생성
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def event_create(_event_create : event_schema.EventCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    event_crud.create_event(db = db, event_create=_event_create, user=current_user)
    return {"message" : "Events created successfully"}

@router.patch("/insert_user")
def user_insert(_userInput : event_schema.TimeRecord, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    time_block = event_crud.get_eventtime(db = db, userInput= _userInput)
    eventInf = db.query(EventInfo).filter(EventInfo.event_id == _userInput.event_id).first()
    if current_user not in eventInf.all_users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="이벤트에 해당되는 사용자가 아닙니다.")
    if not time_block:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="데이터를 찾을수 없습니다.")
    if current_user in time_block.users:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="해당하는 사용자가 이미 존재합니다.")
    event_crud.insert_user(db = db, event_block= time_block, userInput= _userInput, _current_user= current_user)

@router.patch("/delete_user", status_code=status.HTTP_204_NO_CONTENT) #일단 이름 같으면 되게 구현. 나중에 id로 수정 필요
def user_delete(_userInput : event_schema.TimeRecord, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    time_block = event_crud.get_eventtime(db = db, userInput= _userInput)
    if not time_block:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="데이터를 찾을수 없습니다.")
    if current_user not in time_block.users:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="해당하는 사용자가 없습니다.")
    event_crud.delete_user(db = db, event_block= time_block, userInput= _userInput, _current_user= current_user)

@router.delete("/delete_event")
def event_delete(_event_id : int, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(EventInfo).filter(EventInfo.event_id == _event_id).first().admin_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="이벤트 삭제 권한이 없습니다.")
    event_crud.delete_event(db = db, event_id = _event_id)

#시간대 유저 나타내기
# @router.get("/show_user")
# def user_show(_event_name : str, _event_time : dt.datetime, db : Session = Depends(get_db)):
#     _userInput = event_schema.TimeRecord(event_name=_event_name, event_time=_event_time)
#     time_block = event_crud.get_eventtime(db= db, userInput=_userInput)
#     if not time_block:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                         detail="데이터를 찾을수 없습니다.")
#     user_list = event_crud.show_user(db=db, event_block=time_block)
#     return user_list

#이벤트 디테일 전송
@router.get("/event_detail")
def detail_event(_event_id : int, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    eventInf = db.query(EventInfo).get(_event_id)
    if current_user not in eventInf.all_users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="이벤트에 해당되는 사용자가 아닙니다.")
    info = event_crud.event_detail(db=db, event_id=_event_id, event_info=eventInf, _current_user= current_user)
    return info
    

#이벤트 입장(?)
@router.post("/enter_event")
def event_enter(_event_id : int, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    eventInf = db.query(EventInfo).get(_event_id)
    if not eventInf:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="데이터를 찾을수 없습니다.")
    if current_user in eventInf.all_users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="이미 해당 약속에 존재하는 사용자입니다.")
    event_crud.enter_event(db=db, event_block=eventInf, _current_user=current_user)
    


    
    

 
    

