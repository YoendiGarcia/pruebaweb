from fastapi import FastAPI, Request, Depends,status
from fastapi.responses import RedirectResponse, HTMLResponse
import models
from database import engine, get_db
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="templates"), "static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return templates.TemplateResponse("index.html", {"request": request,"tasks":tasks})


@app.post("/create", response_class=RedirectResponse)
async def create(request: Request, db: Session = Depends(get_db)):
    data = await request.form()
    task = data.get("title")
    if task != "":
        new_task = models.Task(title=task)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@app.post('/delete',response_class=HTMLResponse)
async def delete(request: Request, db: Session = Depends(get_db)):
    data = await request.form()
    id = data.get('id')
    delete_task = db.query(models.Task).filter(models.Task.id == id)
    delete_task.delete(synchronize_session=False)
    db.commit()
    return RedirectResponse('/',status_code=status.HTTP_303_SEE_OTHER)

if __name__ == "main":
    port = 8000
    uvicorn.run(app,host="0.0.0.0",port=port)

    
