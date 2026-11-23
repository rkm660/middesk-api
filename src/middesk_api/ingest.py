import csv
import sys

from sqlalchemy import select

from db import Base, SessionLocal, engine
from models import Address, Company

Base.metadata.create_all(engine)


def ingest(path: str) -> None:
    with SessionLocal() as db, open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = row["company_name"].strip()
            if not name:
                continue

            street = row["street"].strip()
            city = row["city"].strip() or None
            state = row["state"].strip() or None

            company = db.scalar(select(Company).where(Company.name == name))
            if not company:
                company = Company(name=name, state=state)
                db.add(company)
                db.flush()  # so company.id is available for the address FK

            already = db.scalar(
                select(Address).where(
                    Address.company_id == company.id,
                    Address.street == street,
                )
            )
            if already:
                continue

            db.add(Address(company_id=company.id, street=street, city=city))
        db.commit()


if __name__ == "__main__":
    ingest(sys.argv[1])
