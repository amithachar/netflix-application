from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import uuid

app = FastAPI()

# ===============================
# Absolute Path Setup (Safe Mode)
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static + uploads
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

# ===============================
# In-Memory Movie Storage
# ===============================

movies = [
    {
        "title": "Night Teeth",
        "category": "Thriller",
        "thumbnail": "/uploads/Night Teeth.jpg"
    },
    {
        "title": "KPop Demon Hunters",
        "category": "Thriller",
        "thumbnail": "/uploads/KPop Demon Hunters.jpg"
    },
     {
        "title": "Red Notice",
        "category": "Thriller",
        "thumbnail": "/uploads/Red Notice.jpg"
    },
    {
        "title": "Don't Look Up",
        "category": "Thriller",
        "thumbnail": "/uploads/Don't Look Up.jpg"
    },
    {
        "title": "Dhurandhar",
        "category": "Thriller",
        "thumbnail": "/uploads/Dhurandhar.jpg"
    },
    {
        "title": "Carry-On",
        "category": "Thriller",
        "thumbnail": "/uploads/Carry-On.jpg"
    },
        {
        "title": "The Trial of the Chicago 7",
        "category": "Thriller",
        "thumbnail": "/uploads/The Trial of the Chicago 7.jpg"
    },
        {
        "title": "The Irishman",
        "category": "Thriller",
        "thumbnail": "/uploads/The Irishman.jpg"
    },    
    {
        "title": "Bird Box",
        "category": "Thriller",
        "thumbnail": "/uploads/Bird Box.jpg"
    },  
    {
        "title": "The Rip",
        "category": "Thriller",
        "thumbnail": "/uploads/The Rip.jpg"
    },
        {
        "title": "20th Century Girl",
        "category": "Romance",
        "thumbnail": "/uploads/20th Century Girl.jpg"
    },
            {
        "title": "The Life List",
        "category": "Romance",
        "thumbnail": "/uploads/The Life List.jpg"
    },
            {
        "title": "My Oxford Year",
        "category": "Romance",
        "thumbnail": "/uploads/My Oxford Year.jpg"
    },        {
        "title": "Our Souls at Night",
        "category": "Romance",
        "thumbnail": "/uploads/Our Souls at Night.jpg"
    },
    {
        "title": "The Perfect Find",
        "category": "Romance",
        "thumbnail": "/uploads/The Perfect Find.jpg"
    }, 
    {
        "title": "Always Be My Maybe",
        "category": "Romance",
        "thumbnail": "/uploads/Always Be My Maybe.jpg"
    },
    {
        "title": "Bones and All",
        "category": "Romance",
        "thumbnail": "/uploads/Bones and All.jpg"
    },
    {
        "title": "Crazy, Stupid, Love",
        "category": "Romance",
        "thumbnail": "/uploads/Crazy, Stupid, Love.jpg"
    },
    {
        "title": "Animal",
        "category": "Action",
        "thumbnail": "/uploads/Animal.jpg"
    },
        {
        "title": "Rebel Ridge",
        "category": "Action",
        "thumbnail": "/uploads/Rebel Ridge.jpg"
    },
        {
        "title": "Lift",
        "category": "Action",
        "thumbnail": "/uploads/Lift.jpg"
    },
        {
        "title": "Maharaja",
        "category": "Action",
        "thumbnail": "/uploads/Maharaja.jpg"
    },
     {
        "title": "Fighter",
        "category": "Action",
        "thumbnail": "/uploads/Fighter.jpg"
    },
     {
        "title": "Pushpa 2",
        "category": "Action",
        "thumbnail": "/uploads/Pushpa 2.jpg"
    },
     {
        "title": "RRR",
        "category": "Action",
        "thumbnail": "/uploads/RRR.jpg"
    },
     {
        "title": "Salt",
        "category": "Action",
        "thumbnail": "/uploads/Salt.jpg"
    },
         {
        "title": "Inside Job",
        "category": "Documentaries",
        "thumbnail": "/uploads/Inside Job.jpg"
    },
             {
        "title": "The Social Dilemma",
        "category": "Documentaries",
        "thumbnail": "/uploads/The Social Dilemma.jpg"
    },
             {
        "title": "Dirty Money",
        "category": "Documentaries",
        "thumbnail": "/uploads/Dirty Money.jpg"
    },
             {
        "title": "Downfall The Case Against Boeing",
        "category": "Documentaries",
        "thumbnail": "/uploads/Downfall The Case Against Boeing.jpg"
    },
             {
        "title": "The Great Hack",
        "category": "Documentaries",
        "thumbnail": "/uploads/The Great Hack.jpg"
    },

             {
        "title": "The Elephant Whisperers",
        "category": "Documentaries",
        "thumbnail": "/uploads/The Elephant Whisperers.jpg"
    },
             {
        "title": "Get Smart With Money",
        "category": "Documentaries",
        "thumbnail": "/uploads/Get Smart With Money.jpg"
    },
             {
        "title": "Descendant",
        "category": "Documentaries",
        "thumbnail": "/uploads/Descendant.jpg"
    },
             {
        "title": "Formula 1: Drive to Survive",
        "category": "Documentaries",
        "thumbnail": "/uploads/Formula 1 Drive to Survive.jpg"
    },
    {
        "title": "Ultraman Rising: A Contender for Best Animated Film",
        "category": "Anime",
        "thumbnail": "/uploads/Ultraman Rising.jpg"
    },
        {
        "title": "Ultraman Rising: A Contender for Best Animated Film",
        "category": "Anime",
        "thumbnail": "/uploads/Ultraman Rising.jpg"
    },
        {
        "title": "Ultraman Rising: A Contender for Best Animated Film",
        "category": "Anime",
        "thumbnail": "/uploads/Ultraman Rising.jpg"
    },
    
]


# ===============================
# Home Route
# ===============================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Group movies by category
    categories = {}
    for movie in movies:
        categories.setdefault(movie["category"], []).append(movie)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "categories": categories
        }
    )

# ===============================
# Upload Route
# ===============================

@app.post("/upload")
def upload_movie(
    title: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...)
):
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    movies.append({
        "title": title,
        "category": category,
        "thumbnail": f"/uploads/{filename}"
    })

    return {"message": "Uploaded successfully"}
