from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import sessionmaker,Session,declarative_base

app=FastAPI()

DATABASE_URL="sqlite:///./Updated_DataStore.db"

engine =create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}

)

sessionLocal=sessionmaker(bind=engine)

Base=declarative_base()

class Update_data(Base):
    __tablename__ ="CRUD"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    standard=Column(Integer)

Base.metadata.create_all(bind=engine)

def greet():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/USER")
def posted_data(id:int,name:str,standard:int,db:Session=Depends(greet)):
    update=Update_data(id=id,name=name,standard=standard)
    db.add(update)
    db.commit()
    db.refresh(update)
    return {
        "message":"successfully",
        "data":update
    }

@app.put("/USER/{id}")
def update_data(id:int, standard:int,db:Session =Depends(greet)):
    update=db.query(Update_data).filter(Update_data.id == id).first()

    if not update:
        raise HTTPException(status_code=404,deatail="NOT FOUND")

    update.standard = standard

    db.commit()

    return {
    "message":" updated successfully",
    "data":update
}
