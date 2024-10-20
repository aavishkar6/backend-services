from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from .blog.routers import router as blog_router
from .docChat.routers import router as docChat_router
from .personalWebsite.routers import router as personalWebsite_router
from .portalpeek.routers import router as portalpeek_router

app = FastAPI()

# # Define allowed origins
# allowed_origins = [
#     "http://localhost:3000",  # Example: your frontend URL
#     "https://your-frontend-domain.com",  # Add any other allowed domains
# ]

# Add CORS middleware to allow all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Define the database URL (modify with your actual credentials)
DATABASE_URL = "postgresql://postgres:Relative6#@localhost/test"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Include project-specific routers
app.include_router(blog_router, prefix="/api/blog")
app.include_router(docChat_router, prefix="/api/documentchat")
app.include_router(personalWebsite_router, prefix="/api/personal")
app.include_router(portalpeek_router, prefix="/api/portalpeek")

# Create database tables
# Base.metadata.create_all(bind=engine)

# Test route to check the database connection
@app.get("/test")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Perform a simple query to test the connection
        result = db.execute(text("SELECT 1")).fetchone()
        return {"status": "success", "result": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}