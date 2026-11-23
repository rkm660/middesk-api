from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models import Address, Company

Base.metadata.create_all(engine)
app = FastAPI()


class CompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    state: str | None


class AddressOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company_id: int
    street: str
    city: str | None


@app.get("/companies", response_model=list[CompanyOut])
def list_companies(
    state: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = select(Company).order_by(Company.id)
    if state:
        q = q.where(Company.state == state)
    return db.scalars(q.limit(limit).offset(offset)).all()


@app.get("/companies/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.get(Company, company_id)
    if not company:
        raise HTTPException(404, "Company not found")
    return company


@app.get("/companies/{company_id}/addresses", response_model=list[AddressOut])
def list_addresses(company_id: int, db: Session = Depends(get_db)):
    q = select(Address).where(Address.company_id == company_id).order_by(Address.id)
    return db.scalars(q).all()
