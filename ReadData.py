from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,Session, declarative_base

app=FastAPI()

DATABASE_URL="sqlite:///./save.db"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}

)

sessionLocal=sessionmaker(bind=engine)

Base =declarative_base()

class MyDetails(Base):
    __tablename__="Detail"

    Id = Column(Integer,primary_key=True,index=True)
    Name=Column(String)
    Mobile_No=Column(Integer)
    Vill=Column(String)
    District=Column(String)

Base.metadata.create_all(bind=engine)

def get_data():
    db =sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/DETAIL")
def post_data( Id:int, Name:str,Mobile_No:int,Vill:str,District:str,db : Session = Depends(get_data)):
    data = MyDetails(Id=Id,Name=Name,Mobile_No=Mobile_No,Vill=Vill,District=District)
    db.add(data)
    db.commit()
    db.refresh(data)
    return {
        "message":"success",
        "insert_data":data
    }
    
@app.get("/DETAIL")
def hello(db:Session=Depends(get_data)):
    data = db.query(MyDetails).all()

    return {
        "Total":len(data),
        "data1":data
    }

@app.get("/ENQUIRY/{Id}")
def tracker_data(Id=int,db:Session=Depends(get_data)):
    data =db.query(MyDetails).filter(MyDetails.Id ==Id).first()

    if not data:
        raise HTTPException(status_code=404,detail="Details not found")
    return data
