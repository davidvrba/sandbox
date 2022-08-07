import os
import uvicorn
from fastapi import FastAPI, Depends, Request, Form
from .db import SessionLocal, engine
from .crud import get_zone_volume, get_zone_volume_today, get_volume_today, get_volume_per_zone_today

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path
from datetime import datetime, time

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get('/mainValveOn')
def close_main_valve():
    os.environ['irrigation_run'] = 'mainValveOn'
    return 'main valve is open.'

@app.get('/set_flow_rate')
def set_flow_rate(volume):
    os.environ['watter'] = str(float(os.environ.get('watter', '0')) + float(volume))
    return 'watter volume increased'

@app.get('/get_flow_rate')
def get_flow_rate():
    return os.environ.get('watter', '0')

@app.get('/get_zone_volume')
def get_zone(db = Depends(get_db)):
    return get_zone_volume(db, 1)

@app.get("/form")
def form_post(request: Request, db = Depends(get_db)):
    zone_1 = int(os.environ.get('zone_1', '0'))
    zone_2 = int(os.environ.get('zone_2', '0'))
    zone_3 = int(os.environ.get('zone_3', '0'))
    irrigation_start_hour = int(os.environ.get('irrigation_start_hour', 19))
    irrigation_start_minute = int(os.environ.get('irrigation_start_minute', 30))
    irrigation_start = time(hour=irrigation_start_hour, minute=irrigation_start_minute, second=0)

    irrigation_state = bool(os.environ.get('irrigation_state', 'True'))
    if irrigation_state:
        irrigation_on_checked = 'checked'
        irrigation_off_checked = ''
    else:
        irrigation_on_checked = ''
        irrigation_off_checked = 'checked'

    watter_source = int(os.environ.get('watter_source', '1'))
    if watter_source == 1:
        watter_source_watter_tank_checked = 'checked'
        watter_source_other_checked = ''
    else:
        watter_source_watter_tank_checked = ''
        watter_source_other_checked = 'checked'

    total_volume_today = get_volume_today(db)
    zone_volumes = get_volume_per_zone_today(db)
    return templates.TemplateResponse(
        'checkbox.html',
        context={
            'request': request,
            'zone_1': zone_1,
            'zone_2': zone_2,
            'zone_3': zone_3,
            'irrigation_start': irrigation_start,
            'total_volume_today': total_volume_today,
            'irrigation_on_checked': irrigation_on_checked,
            'irrigation_off_checked': irrigation_off_checked,
            'watter_source_watter_tank_checked': watter_source_watter_tank_checked,
            'watter_source_other_checked': watter_source_other_checked,
            'zone_volumes': zone_volumes
        }
    )

@app.post("/form")
def form_post(
        request: Request,
        zone_1: int = Form(...),
        zone_2: int = Form(...),
        zone_3: int = Form(...),
        irrigation_state: str = Form(...),
        watter_source: int = Form(...),
        irrigation_start: time = Form(...),
        db = Depends(get_db)
    ):
    if irrigation_state == 'True':
        irrigation_on_checked = 'checked'
        irrigation_off_checked = ''
    else:
        irrigation_on_checked = ''
        irrigation_off_checked = 'checked'

    if watter_source == 1:
        watter_source_watter_tank_checked = 'checked'
        watter_source_other_checked = ''
    else:
        watter_source_watter_tank_checked = ''
        watter_source_other_checked = 'checked'

    os.environ['zone_1'] = str(zone_1)
    os.environ['zone_2'] = str(zone_2)
    os.environ['zone_3'] = str(zone_3)
    os.environ['irrigation_start_hour'] = str(irrigation_start.hour)
    os.environ['irrigation_start_minute'] = str(irrigation_start.minute)
    os.environ['irrigation_on'] = str(irrigation_state)
    os.environ['watter_source'] = str(watter_source)

    total_volume_today = get_volume_today(db)
    zone_volumes = get_volume_per_zone_today(db)
    return templates.TemplateResponse(
        'checkbox.html',
        context={
            'request': request,
            'zone_1': zone_1,
            'zone_2': zone_2,
            'zone_3': zone_3,
            'irrigation_start': irrigation_start,
            'total_volume_today': total_volume_today,
            'irrigation_on_checked': irrigation_on_checked,
            'irrigation_off_checked': irrigation_off_checked,
            'watter_source_watter_tank_checked': watter_source_watter_tank_checked,
            'watter_source_other_checked': watter_source_other_checked,
            'zone_volumes': zone_volumes
        }
    )

@app.get('/esp/irrigation-input')
def get_irrigation_input(request: Request, db = Depends(get_db)):
    result = {
        'zone_1': os.environ.get('zone_1', '0'),
        'zone_2': os.environ.get('zone_2', '0'),
        'zone_3': os.environ.get('zone_3', '0'),
        'irrigation_start_hour': os.environ.get('irrigation_start_hour', 19),
        'irrigation_start_minute': os.environ.get('irrigation_start_minute', 30),
        'irrigation_on': os.environ.get('irrigation_on', 'True'),
        'watter_source': os.environ.get('watter_source', '1'),
    }
    return result

if __name__ == '__main__':
    uvicorn.run('src.api:app', host='0.0.0.0', port=int(os.getenv('PORT', 8000)), log_level='info')