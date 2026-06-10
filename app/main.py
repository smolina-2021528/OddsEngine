from fastapi import FastAPI

app = FastAPI(
    title="OddsEngine",
    description=(
        "REST Api for sports data collection, statistical odds calculation, "
        "and AI-assisted betting analysis"
    ),
    version="0.1.0",
)


@app.get("/", tags=["Root"])
async def read_root() -> dict[str, str]:
    return{
        "name": "OddsEngine",
        "status": "running",
    }