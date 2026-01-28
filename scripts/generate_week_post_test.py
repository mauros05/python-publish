from app import app
from scheduler.jobs import generate_week_post_test

if __name__=="__main__":
    generate_week_post_test(app)
