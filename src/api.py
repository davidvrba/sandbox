import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return 'Main page'


@app.get('/get_value')
def get_state():
    return os.environ.get('irrigation_run', 'True')

@app.get('/set_true')
def set_state_true():
    os.environ['irrigation_run'] = "True"
    return 'The value was set to True.'

@app.get('/set_false')
def set_state_false():
    os.environ['irrigation_run'] = "False"
    return 'The value was set to False.'

@app.get('/openSlaveValvesOn')
def open_slave_valves():
    os.environ['irrigation_run'] = 'openSlaveValves'
    return 'All slave valves are open.'

@app.get('/closeSlaveValvesOn')
def close_slave_valves():
    os.environ['irrigation_run'] = 'closeSlaveValves'
    return 'All slave valves are closed.'

@app.get('/tomatoesValveOn')
def open_tomatoes_valve():
    os.environ['irrigation_run'] = 'tomatoesValveOn'
    return 'tomatoes valve is open.'

@app.get('/tomatoesValveOff')
def close_tomatoes_valve():
    os.environ['irrigation_run'] = 'tomatoesValveOff'
    return 'tomatoes valve is closed.'

@app.get('/herbsValveOn')
def open_herbs_valve():
    os.environ['irrigation_run'] = 'herbsValveOn'
    return 'herbs valve is open.'

@app.get('/herbsValveOff')
def close_herbs_valve():
    os.environ['irrigation_run'] = 'herbsValveOff'
    return 'herbs valve is closed.'

@app.get('/saladsValveOn')
def open_salads_valve():
    os.environ['irrigation_run'] = 'saladsValveOn'
    return 'salads valve is open.'

@app.get('/saladsValveOff')
def close_salads_valve():
    os.environ['irrigation_run'] = 'saladsValveOff'
    return 'salads valve is closed.'

@app.get('/mainValveOff')
def close_main_valve():
    os.environ['irrigation_run'] = 'mainValveOff'
    return 'main valve is closed.'

@app.get('/set_flow_rate')
def set_flow_rate(volume):
    os.environ['watter'] = str(float(os.environ.get('watter', '0')) + float(volume))
    return 'watter volume increased'

@app.get('/get_flow_rate')
def get_flow_rate():
    os.environ['watter'] = str(float(os.environ.get('watter', '0')) + float(volume))
    return os.environ.get('watter', '0')

if __name__ == '__main__':
    uvicorn.run('src.api:app', host='0.0.0.0', port=int(os.getenv('PORT', 8000)), log_level='info')
