from fastapi import FastAPI


app = FastAPI()


@app.get('/api/users/me')
def main():
    return {
        "result": "true",
        "user": {
            "id": 1,
            "name": "Maksim",
            "followers": [],
            "followings": []
        }
    }
