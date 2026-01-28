from datetime import timedelta
from utils.time import now_utc_from_local

def generate_schedule(days, hour, minutes=0, total_posts=10):
    """
    days: lista de enteros [0, 2 ,4]
    hour: hora de publicación (10)
    total_posts: cuantos posts generar

    """

    scheduled_dates = []
    current = now_utc_from_local()

    while len(scheduled_dates) < total_posts:
        current += timedelta(days=1)

        if current.weekday() in days:
            publish_date = current.replace(
                hour=hour,
                minute=minutes,
                second=0,
                microsecond=0
            )
            scheduled_dates.append(publish_date)

    return scheduled_dates
