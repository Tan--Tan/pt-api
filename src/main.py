from fastapi import FastAPI
import uvicorn

from routers import credit_ratings

app = FastAPI()
app.include_router(credit_ratings.router, prefix="/v1/credit-ratings")


@app.get("/")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
