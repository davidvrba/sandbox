from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from . import models
from datetime import date, timedelta

WATTER_SOURCES = {
    1: 'Rain tank',
    2: 'City pipe'
}

FLOW_RATE_CALIBRATION_CONSTANT = 60 * 6.6

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


def get_volume_history(db: Session):
    rows = (
        db.query(
            models.FlowRate,
            models.FlowRate.flow_timestamp.cast(Date).label("date"),
            models.FlowRate.zone.label("zone"),
            func.max(models.FlowRate.total_pulse_count).label("max")
        )
        .group_by(models.FlowRate.flow_timestamp.cast(Date), models.FlowRate.zone)
        .order_by(models.FlowRate.flow_timestamp.cast(Date))
        .all()
    )
    result = []
    for row in rows:
        result.append([row.date.strftime('%d.%m.%Y'), row.zone, int(row.max / (FLOW_RATE_CALIBRATION_CONSTANT))])

    rr = {}
    for r in result:
        if r[0] not in rr:
            rr[r[0]] = r[2]
        else:
            rr[r[0]] = rr[r[0]] + r[2]

    return list(rr.items())


def get_watter_source_distribution(db: Session):
    rows = (
        db.query(
            models.FlowRate,
            models.FlowRate.flow_timestamp.cast(Date).label("date"),
            models.FlowRate.watter_source.label("watter_source"),
            func.max(models.FlowRate.total_pulse_count).label("max")
        )
        .group_by(models.FlowRate.flow_timestamp.cast(Date), models.FlowRate.watter_source)
        .order_by(models.FlowRate.flow_timestamp.cast(Date))
        .all()
    )
    result = []
    for row in rows:
        result.append(
            [
                row.date.strftime('%d.%m.%Y'),
                WATTER_SOURCES[row.watter_source],
                int(row.max / (FLOW_RATE_CALIBRATION_CONSTANT))
            ]
        )

    rr = {}
    for r in result:
        if r[1] not in rr:
            rr[r[1]] = r[2]
        else:
            rr[r[1]] = rr[r[1]] + r[2]
    return list(rr.items())
