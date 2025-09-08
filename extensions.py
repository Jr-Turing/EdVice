from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

# Shared SQLAlchemy instance for the app
# Import this as `from extensions import db`

db = SQLAlchemy(model_class=Base)
