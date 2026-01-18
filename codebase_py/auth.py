import smtplib
from pymongo import MongoClient
from email.message import EmailMessage

import secrets
import time
class log_reg:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        
        # Select database
        self.db = self.client["lwnoteb"]
        # Select collection
        self.collection = self.db["user_log"]
    def login(self,_id,passw):
        return self.collection.find_one({"_id":_id,"password":passw})
    
     
class verify:
    def __init__(self):
        self.otp_store = {}

    def generate_otp(self,user_id):
        otp = str(secrets.randbelow(10**6)).zfill(6)  # 6-digit secure OTP
        expiry = time.time() + 300  # 5 minutes validity
        self.otp_store[user_id] = (otp, expiry)
        return otp

    def verify_otp(self,user_id, otp_input):
        if user_id not in self.otp_store:
            return "No OTP found. Please request a new one."
            
        otp, expiry = self.otp_store[user_id]
        if time.time() > expiry:
            del self.otp_store[user_id]
            return "OTP expired. Please request again."
            
        if otp_input == otp:
            del self.otp_store[user_id]  # Single-use OTP
            return True
        else:
            return "Invalid OTP."
    def send_mail(self,mail):
        print("here")
    
        otp=self.generate_otp(mail)
        SMTP_SERVER = "smtp.gmail.com"  # or "smtp.office365.com"
        SMTP_PORT = 587  # TLS port

        SENDER = "abc@gmail.com" 
        PASSWORD = "xxyz" 
        RECIPIENT = mail

        msg = EmailMessage()
        msg["From"] = SENDER
        msg["To"] = RECIPIENT
        msg["Subject"] = "Test email from Python"
        
        msg.set_content(f"This is a otp for your notebook {otp}. Ensure you dont share with anyone .it valid for 5 minutes .")

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.ehlo()
                smtp.starttls()          # secure the connection
                smtp.ehlo()
                smtp.login(SENDER, PASSWORD)
                smtp.send_message(msg)
            print("email sent")
            return otp
        except Exception as e:
            return "connection Failed"
   
if __name__=="__main__":
    mail=input("enter your mail id")
    obj=verify()
    obj.send_mail(mail)
    req=obj.verify_otp(mail,input("enter the otp"))
    if req==True:
        print("you are done")
    else:
        print(req)
    
    
        
                        
                    

               
                   


