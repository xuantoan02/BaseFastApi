import uvicorn
from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
from security import reusable_oauth2,validate_token
from datetime import datetime, timedelta
import jwt
from typing import Union, Any

app = FastAPI(
    title='FastAPI JWT', openapi_url='/openapi.json', docs_url='/docs',
    description='fastapi jwt'
)


def verify_password(username, password):
    if username == 'admin' and password == 'admin':
        return True
    return False


class LoginRequest(BaseModel):
    username: str
    password: str

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

def generate_token(username) -> str:
    time_out = 123
    to_encode = {
        "exp": time_out, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


@app.post('/login')
def login(request_data: LoginRequest):
    print(f'[x] request_data: {request_data.__dict__}')
    if verify_password(username=request_data.username, password=request_data.password):
        token = generate_token(request_data.username)
        return {
            'token': token
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get('/books', dependencies=[Depends(validate_token)])
def list_books():
    return {'data': ['Sherlock Homes', 'Harry Potter', 'Rich Dad Poor Dad']}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
