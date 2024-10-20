from fastapi import APIRouter, Depends, HTTPException
import string
import random
from aiosmtplib import send
from email.message import EmailMessage
import asyncio
from pydantic import BaseModel

from .db import get_db
from .utils import validate_user

# Models for the user 
class Signup(BaseModel):
    name : str
    email : str
    classOf : int



# ----------
router = APIRouter()

@router.get("/")
async def get_status():
    return {"status": "portalpeek router status - OK"}

@router.post("/signup")
async def signup(user : Signup):
    # Validate user
    validate_user(user)

    # Add user to the database
    db = get_db()
    user_collection = db['users']

    try:
        result = user_collection.insert_one(dict(user))

        if result.inserted_id:
            return {"detail": "User added successfully"}
        else:
            raise HTTPException(status_code=500, detail="Database Error. Could not add User")
    except Exception as e:
        print("Error occured: ", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    

# This is the endpoint that will be called every 6 hours or so.
@router.get("/scrape")
async def scrape_data():
    # to scrape the data from the website and store it in the database.

    print("Setting up the driver")
    # driver = setup_driver()

    print("Logging into student portal")
    # login_to_student_portal(driver)

    print("Scraping data from student portal")
    # data = scrape_student_portal(driver)

    # Add to the database if not already added.
    # add_to_database(data)

    print("Scraping completed")
    # driver.quit()

    return {"status": "Scraping completed"}

def generate_otp(length = 6):

    digits = string.digits

    return ''.join(random.choice(digits) for i in range(length))

async def send_otp_email(user_email, otp):
    # Send OTP to the user via email
    """Send OTP to the recipient email address."""
    message = EmailMessage()
    message["From"] = "noreply@portalpeek.com"
    message["To"] = "ag8298@nyu.edu"
    message["Subject"] = "Your OTP Code"
    message.set_content(f"Your OTP code is {otp}. It will expire in 5 minutes.")

    # Send email via SMTP server (for example Gmail)
    await send(
        message, 
        hostname="smtp.gmail.com", 
        port=587, 
        start_tls=True, 
        username="aavishkargautam@gmail.com", 
        password="nfnx nzgi bing tcgh"
    )


# Endpoint for generating OTP and verifying it for the user.
@router.get("/otp/{user_email}")
async def send_otp_to_user(user_email):
    # Generate OTP
    otp = generate_otp()

    # Send OTP to the user
    send_otp_email(user_email, otp)

    return {"status": "OTP sent"}


if __name__ == "__main__":
    async def main():
        # Example usage
        otp = generate_otp()
        print(f"Generated OTP: {otp}")
        
        # Replace with the actual email address you want to send to
        await send_otp_email("ag8298@nyu.edu", otp)
    
    # Run the asynchronous main function
    asyncio.run(main())
