from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes.user_auth import router as auth_router
from app.routes.task import router as task_router
import uvicorn

app = FastAPI(
    title="Task Manager API",
    description="A FastAPI-based backend for managing tasks and user authentication",
    version="1.0.0",
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

# Root endpoint for API information
@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Task Manager API.",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth/register and /auth/login",
            "tasks": "/tasks/ (create, read, update, delete tasks)"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)