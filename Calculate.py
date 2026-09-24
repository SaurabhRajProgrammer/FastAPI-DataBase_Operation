from fastapi import FastAPI,Depends
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,Session,declarative_base

app=FastAPI()

DATABASE_URL ="sqlite:///./put.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}

)

sessionLocal = sessionmaker(bind=engine)

Base =declarative_base()

class StudentDetail(Base):
    __tablename__="Detail"

    Id = Column(Integer,primary_key=True,index=True)
    Name=Column(String)
    Mobile_No=Column(Integer)
    CourseName=Column(String)

Base.metadata.create_all(bind=engine)

def get_data():
    db =sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/DETAIL")
def post_data( Id:int, Name:str,Mobile_No:int,CourseName:str,db : Session = Depends(get_data)):
    data = StudentDetail(Id=Id,Name=Name,Mobile_No=Mobile_No,CourseName=CourseName)
    db.add(data)
    db.commit()
    db.refresh(data)
    return {
        "message":"success",
        "insert_data":data
    }
    