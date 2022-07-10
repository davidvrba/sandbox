import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return 'Main page'


@app.get('/get_value')
def get_state():
    return os.environ['irrigation_run']

@app.get('/set_true')
def set_state_true():
    os.environ['irrigation_run'] = "True"
    return 'The value was set to True.'

@app.get('/set_false')
def set_state_false():
    os.environ['irrigation_run'] = "False"
    return 'The value was set to False.'

if __name__ == '__main__':
    uvicorn.run('src.api:app', host='0.0.0.0', port=int(os.getenv('PORT', 8000)), log_level='info')
