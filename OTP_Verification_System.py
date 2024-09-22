import random
import smtplib
import re
from email.mime.text import MIMEText

class OTPVerification:
    def __init__(self):
        self.otp = None
        self.attempts = 0
        self.max_attempts = 3

    def is_valid_email(self, receiver_email):
        email_check1 = ["gmail", "hotmail", "yahoo", "outlook"]
        email_check2 = [".com", ".in", ".org", ".edu", ".co.in"]
        count = 0

        for domain in email_check1:
            if domain in receiver_email:
                count += 1
        for site in email_check2:
            if site in receiver_email:
                count += 1

        if "@" not in receiver_email or count != 2:
            print("Invalid email ID")
            new_receiver_email = input("Enter correct email ID: ")
            return self.is_valid_email(new_receiver_email)
        return receiver_email

    def generate_otp(self):
        # Generate a 6-digit OTP
        self.otp = ''
        for _ in range(6):
            self.otp += str(random.randint(0, 9))
        return self.otp

    def send_otp(self, email):
        try:
            otp = self.generate_otp()
            subject = "Your OTP Code"
            message = f"Your OTP code is {otp}. Please use this to verify your email."

            # Set up the SMTP server (e.g., Gmail)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "saunaksubudhi67@gmail.com"
            sender_password = "hljw rwpv xdda szbq"

            # Set up the MIMEText object
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = email

            # Send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())

            print(f"OTP has been sent to {email}.")
        except Exception as e:
            print(f"Failed to send OTP. Error: {str(e)}")

    def verify_otp(self, user_otp):
        return user_otp == self.otp

    def start_verification(self, email):
        email = self.is_valid_email(email)

        self.send_otp(email)
        while self.attempts < self.max_attempts:
            user_otp = input("Enter the OTP sent to your email: ")
            if self.verify_otp(user_otp):
                print("OTP verification successful!")
                return
            else:
                self.attempts += 1
                print(f"Invalid OTP. You have {self.max_attempts - self.attempts} attempt(s) left.")

        if self.attempts >= self.max_attempts:
            print("Maximum attempts reached. Would you like to resend the OTP? (yes/no)")
            resend = input().strip().lower()
            if resend == "yes":
                self.attempts = 0
                self.start_verification(email)
            else:
                print("OTP verification failed. Please try again later.")

if __name__ == "__main__":
    email = input("Enter your email address: ")
    otp_verification = OTPVerification()
    otp_verification.start_verification(email)