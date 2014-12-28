
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

def get_ip_address_3():
    import socket
    ipaddr = socket.gethostbyname(socket.gethostname())
    return ipaddr

  
print(get_ip_address_2())
print(get_ip_address_3())
