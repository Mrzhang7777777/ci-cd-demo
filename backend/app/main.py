from fastapi import FastAPI

from app.models import HealthResponse, HelloResponse


app = FastAPI(
    title="ci-cd-demo backend",
    description="用于学习 CI/CD 的最小 FastAPI 后端骨架。",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/api/hello", response_model=HelloResponse)
def get_hello() -> HelloResponse:
    return HelloResponse(message="hello from backend")
