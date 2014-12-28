def get_ip_address_2():
    '''
    Source:
    http://commandline.org.uk/python/how-to-find-out-ip-address-in-python/
    '''
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ipaddr=s.getsockname()[0]

    return ipaddr


def send_email_2():
    import datetime
    import smtplib
    from email.mime.text import MIMEText
    today = datetime.date.today()

    addr_to = 'eunwho@naver.com'
    gmail_user     = 'fromeunwho@gmail.com'
    gmail_password = 'ii11ii11'
    smtpserver     = smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user,gmail_password)

    ipaddr = get_ip_address_2()

    my_ip = 'Your ip is %s' %  ipaddr
    msg = MIMEText(my_ip)
    msg['Subject'] = 'IP For RaspberryPi on %s' % today.strftime('%b %d %Y')
    msg['From'] = gmail_user
    msg['To'] = addr_to
    smtpserver.sendmail(gmail_user, [addr_to], msg.as_string())
    smtpserver.quit()

send_email_2()

