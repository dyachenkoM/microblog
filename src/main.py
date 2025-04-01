from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get('/api/users/me')
async def main():
    return {
        "result": "true",
        "user": {
            "id": 1,
            "name": "Maksim",
            "followers": [],
            "followings": []
        }
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
