import smtplib
from email.mime.text import MIMEText


def send_mail(customer, employee, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '8496b7108c30fc'
    password = '7b4fd12a4c75c8'
    message = f"<h3> New Feedback Submission </h3><ul><li> Customer: {customer} </li><li> Employee: {employee} </li> <li> Rating: {rating} </li><li> Comments: {comments}</li></ul>"
    sender_email = 'test_sender@example.com'
    receiver_email = 'test_receiver@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Test Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
