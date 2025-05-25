from fastapi import FastAPI

from app.routery import wszystkie_routery

app = FastAPI(
    title="System Informacji Studenckiej USOS-like",
    description="API do zarządzania informacjami studenckimi",
    version="1.0.0",
)

for router in wszystkie_routery:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)