from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

# User와 TimeTable 간의 중간 테이블 정의
user_timetable_association = Table(
    'user_timetable_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('timetable_id', Integer, ForeignKey('TimeTable.id'))
)

# EventInfo와 User 간의 중간 테이블 정의
event_user_association = Table(
    'event_user_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('event_id', Integer, ForeignKey('EventInfo.event_id'))
)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    attending_event = relationship("TimeTable", secondary=user_timetable_association, back_populates="users")
    events = relationship("EventInfo", secondary=event_user_association, back_populates="all_users")

    
class TimeTable(Base):
    __tablename__ = "TimeTable"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("EventInfo.event_id"))
    event_time = Column(DateTime, nullable= False)
    event = relationship("EventInfo", back_populates="time_tables")
    users = relationship("User", secondary=user_timetable_association, back_populates="attending_event")


class EventInfo(Base):
    __tablename__ = "EventInfo"
    event_id = Column(Integer, primary_key= True)
    event_name = Column(String, nullable = False)
    event_type = Column(String, nullable= False)
    region = Column(String, nullable= False)
    admin_id = Column(Integer, ForeignKey("user.id"), nullable=True) #생성한 user 관련
    
    time_tables = relationship("TimeTable", back_populates="event")
    all_users = relationship("User", secondary=event_user_association, back_populates="events") #이벤트 안에 있는 모든 사람
    admin = relationship("User", foreign_keys=[admin_id]) #생성한 user 관련

    

    


