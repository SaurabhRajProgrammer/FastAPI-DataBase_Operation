from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker,Session,declarative_base

app=FastAPI()

DATABASE_URL="sqlite:///./cutting.db"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

sessionLocal=sessionmaker(bind=engine)

Base=declarative_base()

class Material(Base):
    __tablename__ ="ADMISSION SLIP"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    age=Column(Integer)
    sem=Column(Integer)

Base.metadata.create_all(bind=engine)

def hello():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user")
def posted_data(id:int,name:str,age:int,sem:int,db:Session=Depends(hello)):
    create=Material(id=id,name=name,age=age,sem=sem)
    db.add(create)

    db.commit()

    db.refresh(create)
    return {
        "message":"successfully data posted",
        "data":create
    }  

@app.delete("/user/{id}")
def deleted_data(id:int,db:Session=Depends(hello)):
    create =db.query(Material).filter(Material.id==id).first()

    if  not create:
        raise HTTPException(status_code=404,detail="Not found")

    db.delete(create)
    db.commit()


    return {
        "message":"Data Deleted"
    }     