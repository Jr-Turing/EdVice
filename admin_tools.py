import csv
import json
from typing import Iterable
from flask import current_app
from extensions import db
from models import College


def import_colleges_from_csv(csv_path: str) -> int:
    """Import colleges from a CSV file into the database.

    Expected columns (case-insensitive):
    name, state, city, type, courses (| separated), fees_range, facilities (| separated), cutoff_info, seats, scholarships, website

    Returns the number of upserted rows.
    """
    count = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get('name') or '').strip()
            if not name:
                continue
            state = (row.get('state') or '').strip()
            city = (row.get('city') or '').strip()
            ctype = (row.get('type') or '').strip()
            fees_range = (row.get('fees_range') or '').strip()
            cutoff_info = (row.get('cutoff_info') or '').strip()
            scholarships = (row.get('scholarships') or '').strip()
            website = (row.get('website') or '').strip()

            # Parse list-like fields
            def split_list(val: str) -> Iterable[str]:
                return [v.strip() for v in (val or '').split('|') if v.strip()]

            courses = json.dumps(split_list(row.get('courses') or ''))
            facilities = json.dumps(split_list(row.get('facilities') or ''))

            seats_raw = (row.get('seats') or '').strip().replace(',', '')
            try:
                seats = int(seats_raw) if seats_raw else None
            except ValueError:
                seats = None

            # Upsert by (name, state, city)
            college = College.query.filter_by(name=name, state=state, city=city).first()
            if not college:
                college = College(name=name, state=state, city=city, type=ctype)
                db.session.add(college)

            college.type = ctype or college.type
            college.courses = courses
            college.fees_range = fees_range
            college.facilities = facilities
            college.cutoff_info = cutoff_info
            college.seats = seats
            college.scholarships = scholarships
            college.website = website

            count += 1

        db.session.commit()
    return count
