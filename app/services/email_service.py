import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import Config


class EmailService:
    @staticmethod
    def send_verification_email(to_email: str, code: str, username: str) -> bool:
        """Send email verification code to user."""
        try:
            print("[EMAIL SERVICE] ========== STARTING EMAIL SEND ==========")
            print(f"[EMAIL SERVICE] To Email: {to_email}")
            print(f"[EMAIL SERVICE] Username: {username}")
            print(f"[EMAIL SERVICE] Code: {code}")
            print(f"[EMAIL SERVICE] MAIL_SERVER: {Config.MAIL_SERVER}")
            print(f"[EMAIL SERVICE] MAIL_PORT: {Config.MAIL_PORT}")
            print(f"[EMAIL SERVICE] MAIL_USERNAME: {Config.MAIL_USERNAME}")
            print(f"[EMAIL SERVICE] MAIL_USE_TLS: {Config.MAIL_USE_TLS}")
            print(f"[EMAIL SERVICE] MAIL_USE_SSL: {Config.MAIL_USE_SSL}")

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Verify Your Libris Account"
            msg["From"] = Config.MAIL_DEFAULT_SENDER
            msg["To"] = to_email

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .logo {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .logo h1 {{
                        color: #10b981;
                        font-size: 32px;
                        margin: 0;
                    }}
                    .code-box {{
                        background-color: #f0fdf4;
                        border: 2px solid #10b981;
                        border-radius: 8px;
                        padding: 20px;
                        text-align: center;
                        margin: 30px 0;
                    }}
                    .code {{
                        font-size: 36px;
                        font-weight: bold;
                        color: #10b981;
                        letter-spacing: 8px;
                    }}
                    .footer {{
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                        margin-top: 30px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="logo">
                        <h1>📚 Libris</h1>
                    </div>
                    <h2>Welcome to Libris, {username}!</h2>
                    <p>Thank you for signing up. Please verify your email
                    address by entering the code below:</p>
                    <div class="code-box">
                        <div class="code">{code}</div>
                    </div>
                    <p>This code will expire in <strong>10
                    minutes</strong>.</p>
                    <p>If you didn't create an account with Libris,
                    please ignore this email.</p>
                    <div class="footer">
                        <p>© 2025 Libris. All rights reserved.</p>
                        <p>Open the door to endless reading.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            print(
                f"[EMAIL SERVICE] Connecting to SMTP server "
                f"{Config.MAIL_SERVER}:{Config.MAIL_PORT}..."
            )

            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                print("[EMAIL SERVICE] Connected to SMTP server!")

                if Config.MAIL_USE_TLS:
                    print("[EMAIL SERVICE] Starting TLS...")
                    server.starttls()
                    print("[EMAIL SERVICE] TLS started!")

                print(
                    f"[EMAIL SERVICE] Logging in with username: "
                    f"{Config.MAIL_USERNAME}..."
                )

                if Config.MAIL_USERNAME and Config.MAIL_PASSWORD:
                    server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)

                print("[EMAIL SERVICE] Logged in successfully!")
                print("[EMAIL SERVICE] Sending message...")
                server.send_message(msg)
                print(f"[EMAIL SERVICE] Email sent successfully to {to_email}!")

            print("[EMAIL SERVICE] ========== EMAIL SEND COMPLETE ==========")
            return True

        except smtplib.SMTPAuthenticationError as e:
            print(f"[EMAIL SERVICE] AUTHENTICATION ERROR: {str(e)}")
            print(
                "[EMAIL SERVICE] Check your MAIL_USERNAME and " "MAIL_PASSWORD in .env"
            )
            import traceback

            traceback.print_exc()
            return False

        except smtplib.SMTPConnectError as e:
            print(f"[EMAIL SERVICE] CONNECTION ERROR: {str(e)}")
            print("[EMAIL SERVICE] Check MAIL_SERVER and MAIL_PORT in .env")
            import traceback

            traceback.print_exc()
            return False

        except Exception as e:
            print(f"[EMAIL SERVICE] UNEXPECTED ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return False

    @staticmethod
    def send_password_reset_email(to_email: str, code: str, username: str) -> bool:
        """Send password reset code to user."""
        try:
            print("[EMAIL SERVICE] ========== SENDING PASSWORD RESET EMAIL ==========")
            print(f"[EMAIL SERVICE] To Email: {to_email}")
            print(f"[EMAIL SERVICE] Username: {username}")
            print(f"[EMAIL SERVICE] Reset Code: {code}")

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Reset Your Libris Password"
            msg["From"] = Config.MAIL_DEFAULT_SENDER
            msg["To"] = to_email

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .logo {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .logo h1 {{
                        color: #10b981;
                        font-size: 32px;
                        margin: 0;
                    }}
                    .code-box {{
                        background-color: #fef3c7;
                        border: 2px solid #f59e0b;
                        border-radius: 8px;
                        padding: 20px;
                        text-align: center;
                        margin: 30px 0;
                    }}
                    .code {{
                        font-size: 36px;
                        font-weight: bold;
                        color: #f59e0b;
                        letter-spacing: 8px;
                    }}
                    .warning {{
                        background-color: #fee2e2;
                        border-left: 4px solid #ef4444;
                        padding: 15px;
                        margin: 20px 0;
                        border-radius: 4px;
                    }}
                    .footer {{
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                        margin-top: 30px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="logo">
                        <h1>📚 Libris</h1>
                    </div>
                    <h2>Password Reset Request</h2>
                    <p>Hello {username},</p>
                    <p>We received a request to reset your password. Use the code below to proceed:</p>
                    <div class="code-box">
                        <div class="code">{code}</div>
                    </div>
                    <p>This code will expire in <strong>10 minutes</strong>.</p>
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong><br>
                        If you didn't request a password reset, please ignore this email.
                        Your password will remain unchanged.
                    </div>
                    <div class="footer">
                        <p>© 2025 Libris. All rights reserved.</p>
                        <p>Open the door to endless reading.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                if Config.MAIL_USE_TLS:
                    server.starttls()

                if Config.MAIL_USERNAME and Config.MAIL_PASSWORD:
                    server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)

                server.send_message(msg)

            print(
                "[EMAIL SERVICE] ========== PASSWORD RESET EMAIL SENT "
                "SUCCESSFULLY =========="
            )
            return True

        except Exception as e:
            print(f"[EMAIL SERVICE] ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return False
