from datetime import datetime, timedelta
from domain.event.event_schema import EventCreate, TimeRecord, UserShow, EventDetail, EventSummary, MyEvent
from models import TimeTable, User, EventInfo
from sqlalchemy.orm import Session
import json
#해당 유저 이벤트정보 모두 조회
def my_event(db: Session, _current_user : User):
    event_list = _current_user.events
    event_summary = []
    for event in event_list:
        all_time_slot =db.query(TimeTable).filter(TimeTable.event_id == event.event_id).all()
        event_name = event.event_name
        user_count = len(event.all_users)
        type = event.event_type
        start_date = all_time_slot[0].event_time
        end_date = all_time_slot[-1].event_time
        duration = start_date.strftime("%Y.%m.%d") + " ~ " + end_date.strftime("%Y.%m.%d")
        event_id = event.event_id
        info = EventSummary(event_name=event_name, duration= duration, user_count= user_count, type= type, event_id=event_id)
        event_summary.append(info)
    return event_summary
#Response body ex)
# [
#   {
#     "event_name": "test",
#     "duration": "2024.07.11 ~ 2024.07.11",
#     "user_count": 2,
#     "type": "미정",
#     "event_id": 1
#   },
#   {
#     "event_name": "test",
#     "duration": "2024.07.11 ~ 2024.07.13",
#     "user_count": 2,
#     "type": "미정",
#     "event_id": 2
#   }
# ]

#-----------------------------------------------------------------------------------------------

#이벤트 생성
def create_event(db : Session, event_create : EventCreate, user : User):
    dt_days = (event_create.end_day - event_create.start_day).days
    new_event = EventInfo(event_name = event_create.event_name,
                          event_type = event_create.event_type,
                          region= event_create.region,
                          admin=user,
                          all_users = [user])
    db.add(new_event)
    db.commit()
    current_day = event_create.start_day  #날짜 조정을 위해 만든 변수
    for i in range(dt_days + 1):
        start_time = current_day.replace(hour=event_create.start_hour, minute=0, second=0, microsecond=0)
        end_time = current_day.replace(hour=event_create.end_hour, minute=0, second=0, microsecond=0)
        while start_time <= end_time:
            schedule = TimeTable(event_time = start_time,
                                event = new_event,
                                users = [] #event 만들었다고 다 참여하는 거 아니잖아.
                                )
            db.add(schedule)
            db.commit()
            start_time += timedelta(minutes=30)
        current_day += timedelta(days=1)

#-----------------------------------------------------------------------------------------------

#get_event_time(?)
def get_eventtime(db : Session, userInput : TimeRecord):
    time_block = db.query(TimeTable).filter(TimeTable.event_id == userInput.event_id, TimeTable.event_time == userInput.event_time).first()
    return time_block

#-----------------------------------------------------------------------------------------------

#유저 삽입
def insert_user(db : Session, event_block : TimeTable, userInput : TimeRecord, _current_user : User):
        event_block.users+= [_current_user]
        db.add(event_block)
        db.commit()

#유저 제거
def delete_user(db : Session, event_block : TimeTable, userInput : TimeRecord, _current_user : User):
    event_block.users.remove(_current_user)
    db.add(event_block)
    db.commit()

#-----------------------------------------------------------------------------------------------

#이벤트 삭제
def delete_event(db : Session, event_id : int):
    all_time_slot = db.query(TimeTable).filter(TimeTable.event_id == event_id).all()
    #return all_time_slot
    for i in all_time_slot: #user_timetable_association에 있는 항목들 제거 -> 실패
        i.users.clear()
        db.add(i)
        db.commit()
    db.query(TimeTable).filter(TimeTable.event_id == event_id).delete() #해당하는 TimeTable 제거
    db.commit()
    event_slot = db.query(EventInfo).filter(event_id == event_id).first() #event_user_association에 있는 항목들 제거 -> 성공
    event_slot.all_users.clear()
    db.add(event_slot) 
    db.commit()
    db.query(EventInfo).filter(event_id == event_id).delete() # 해당하는 EventInfo제거
    db.commit()

#해당 시간 유저 조회(아마 event_detail함수 때문에 필요 없을 듯..?)
# def show_user(db : Session, event_block : TimeTable):
#     return event_block.users

def event_detail(db : Session, event_id : int, event_info : EventInfo, _current_user : User):
    _title = event_info.event_name
    _host = event_info.admin.username
    _type = event_info.event_type
    
    current_user_data = {"id":_current_user.id, "name":_current_user.username}
    current_user = UserShow.model_validate(current_user_data)
    _schedule = {}
    all_time_slot = db.query(TimeTable).filter(TimeTable.event_id == event_id).all()
    '''for slot in all_time_slot:
        date_info = slot.event_time.strftime("%Y.%m.%d %a")
        time_info = slot.event_time.strftime('%H:%M')
        if date_info not in _schedule:
            diff = 
            _schedule[date_info] = {time_info : }'''
    
    start_date = all_time_slot[0].event_time
    end_date = all_time_slot[-1].event_time

    dt_days = (end_date - start_date).days
    current_day = start_date
    for i in range(dt_days+1):
        start_time = current_day.replace(hour=start_date.hour, minute=0, second=0, microsecond=0)
        end_time = current_day.replace(hour=end_date.hour, minute=0, second=0, microsecond=0)
        date_info = start_time.strftime("%Y.%m.%d %a")
        if date_info not in _schedule:
            _schedule[date_info] = {}
        while start_time <= end_time:
            time_info = start_time.strftime('%H:%M')
            time_block =db.query(TimeTable).filter(TimeTable.event_id==event_id,TimeTable.event_time == start_time).first()
            time_slots =[]
            for user in time_block.users:
                user_data = {"id": user.id, "name": user.username}
                user_data =UserShow.model_validate(user_data)
                time_slots.append(user_data)
            _schedule[date_info][time_info] = time_slots
            start_time += timedelta(minutes=30)
        current_day += timedelta(days=1)

    detail = EventDetail(
        title=_title,
        host=_host,
        type=_type,
        current_user=current_user,
        schedule= _schedule
        )
    return detail


    '''start_time = start_date
    while start_time <= end_date:
        start_hour = start_time.replace(hour = start_time.hour, minute=0, second=0, microsecond=0)
        date_info = start_time.strftime("%Y.%m.%d %a")
        if date_info not in _schedule:
            _schedule[date_info] = {}
        while start_hour.hour != end_date.hour or start_hour.minute != end_date.minute:
            time_info = start_time.strftime('%H:%M')
            time_block =db.query(TimeTable).filter(TimeTable.event_id==event_id,TimeTable.event_time == start_time).first()
            time_slots = []
            for user in time_block.users:
                user =UserShow.model_validate(user)
                time_slots.append(user)
            _schedule[date_info][time_info] = time_slots
            start_time += timedelta(minutes=30)
        start_time += timedelta(days=1)'''


            






#--------------------------------------------------------------------------------------
#이벤트에 유저 입장
def enter_event(db: Session, event_block : EventInfo, _current_user : User):
    event_block.all_users = event_block.all_users + [_current_user]
    db.add(event_block)
    db.commit()



        

        





