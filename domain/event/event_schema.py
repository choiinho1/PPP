import datetime

from pydantic import BaseModel
from typing import Dict, List
import json
from domain.user.user_schema import User

class EventCreate(BaseModel):
    event_name : str
    event_type : str
    start_day : datetime.datetime
    end_day : datetime.datetime
    region : str
    start_hour :int
    end_hour : int
    #admin : User | None #이벤트 만든 유저

class TimeRecord(BaseModel):
    event_id : int
    event_time : datetime.datetime

class UserShow(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# class ScheduleDay(BaseModel):
#     time_slots: Dict[str, List[TimeSlot]]

# class EventDetail(BaseModel):
#     title: str
#     host: str
#     type: str
#     current_user: UserShow
#     schedule: Dict[str, ScheduleDay]

class EventDetail(BaseModel):
    title: str
    host: str
    type: str
    current_user: UserShow
    schedule: Dict[str, Dict[str, List[UserShow]]]

    class Config:
        orm_mode = True


class EventSummary(BaseModel):
    event_name : str
    duration : str
    user_count : int
    type : str
    event_id : int

class MyEvent(BaseModel):
    event_list : List[EventSummary]