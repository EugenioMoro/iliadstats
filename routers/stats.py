from fastapi import APIRouter, HTTPException
from iliadstats import IliadStats
import time

router = APIRouter()

# Initialize IliadStats with the path to the secrets file
iliad_stats = IliadStats(secrets_file_path='secrets.json')

@router.get("/used-data")
def get_used_data():
    try:
        used_data = iliad_stats.get_traffic_consumption()
        return {"used_data": used_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/traffic-endowment")
def get_traffic_endowment():
    try:
        endowment = iliad_stats.get_traffic_endowment()
        return {"traffic_endowment": endowment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/renewal-date")
def get_renewal_date():
    try:
        renewal_date = iliad_stats.get_renewal_date()
        return {"renewal_date": time.strftime("%Y-%m-%d", renewal_date)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))