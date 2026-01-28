from datetime import datetime
import pytz

def now_utc_from_local():
    local_tz = pytz.timezone("America/Mexico_City")
    return datetime.now(local_tz).astimezone(pytz.utc)
