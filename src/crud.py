from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from . import models
from datetime import date, timedelta


def get_zone_volume(db: Session, zone_id: int):
    row = db.query(
        models.FlowRate,
        func.sum(models.FlowRate.increment).label("sum")
    ).filter(models.FlowRate.zone == zone_id).first()
    return row.sum


def get_zone_volume_today(db: Session, zone_id: int):
    row = (
        db.query(
            models.FlowRate,
            func.sum(models.FlowRate.increment).label("sum")
        )
        .filter(models.FlowRate.zone == zone_id)
        .filter(models.FlowRate.flow_timestamp.cast(Date) == date.today())
        .first()
    )
    return row.sum

def get_volume_per_zone_today(db: Session):
    rows = (
        db.query(
            models.FlowRate,
            models.FlowRate.zone,
            func.max(models.FlowRate.total_pulse_count).label("max")
        )
        .filter(models.FlowRate.flow_timestamp.cast(Date) == date.today())
        .group_by(models.FlowRate.zone)
        .all()
    )
    result = {}
    for row in rows:
        result[row.zone] = round(row.max / (6.6 * 60), 2)
    return result

def get_volume_today(db: Session):
    zones = get_volume_per_zone_today(db)
    total = 0
    for value in zones.values():
        total = total + value
    return round(total, 2)

def create_flowrate(db: Session, data):
    db_flow_rate = models.FlowRate(
        zone=data['zone'],
        increment=data['increment'],
        watter_source=data['watter_source'],
        flow_timestamp=data['flow_timestamp'],
        total_pulse_count=data['total_pulse_count']
    )
    db.add(db_flow_rate)
    db.commit()
