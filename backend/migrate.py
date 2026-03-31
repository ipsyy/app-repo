"""Runs on every terraform apply — creates tables if they don't exist."""
from database import engine, Base
import models  # noqa: F401 — registers models with Base

def run():
    print("Running migrations...")
    Base.metadata.create_all(bind=engine)
    print("Done — all tables created/verified.")

if __name__ == "__main__":
    run()