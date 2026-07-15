from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..utils.resend import send_email
import os

router = APIRouter(prefix="/api/contact", tags=["contact"])

@router.get("/", response_model=List[schemas.ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).order_by(models.Contact.created_at.desc()).all()

@router.post("/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    # Send email notification
    try:
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        html_content = f"""
        <h2>New Contact Message</h2>
        <p><strong>Name:</strong> {contact.name}</p>
        <p><strong>Email:</strong> {contact.email}</p>
        <p><strong>Subject:</strong> {contact.subject}</p>
        <p><strong>Message:</strong></p>
        <p>{contact.message}</p>
        """
        send_email(admin_email, f"New Contact: {contact.subject}", html_content)
    except Exception as e:
        print(f"Email notification failed: {e}")
    
    return db_contact

@router.put("/{contact_id}/read")
def mark_as_read(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.is_read = True
    db.commit()
    return {"message": "Contact marked as read"}

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}