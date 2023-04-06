import socket as s
from common_ports import ports_and_services

def check_port(target, port):
    '''
    Return the port if successful connection, otherwise False
    '''
    print(f"Attempting to connect to: {target}:{port}")


    with s.socket(family=s.AF_INET, type=s.SOCK_STREAM) as soc:
        try:
            print("Connecting ...")
            soc.settimeout(2)
            soc.connect((target, port))
            print("Connected successfully")
        except:
            print("Exception raised, failed to connect")
            port = False
        finally:
            print("Closing connection")
            soc.close()
            print("Connection closed")
            print(f"Return a value of: {port}")
        return port


def pretty_print(open_ports):
    '''
    Produce the formatted string to be returned, example below:

    Open ports for {URL} ({IP address})
    PORT     SERVICE
    {port}       {service name}
    {port}       {service name}
    '''

    text_pairings = [f"{x}".ljust(9, " ") + f"{ports_and_services[x]}\n" for x in open_ports]
    return "".join(text_pairings)[:-1]


def get_open_ports(target, port_range, verbose=False):
    '''
    Check for open ports against a target adress (url or ip) and returning the ports that are open within the provided range
    '''
    print(f"Starting processing for {target}, with port/s {port_range}, and verbose set to {verbose}")

    try:
        print("Attempting to connect")
        info = s.gethostbyaddr(target)
    except s.herror:
        info = False
    except s.gaierror:
        print("Failed to connect")
        if target[0].isdigit():
            return "Error: Invalid IP address"
        else:
            return "Error: Invalid hostname"

    print("Producing open ports")
    port_range[1] += 1
    open_ports = [x for x in range(*port_range) if check_port(target, x)]

    if verbose:
        print("Building text intro")
        if info == False:
            text_intro = f"Open ports for {target}\nPORT     SERVICE\n"
        else:
            text_intro = f"Open ports for {info[0]} ({info[2][0]})\nPORT     SERVICE\n"

        print("Building pretty print")
        print(text_intro + pretty_print(open_ports))
        return text_intro + pretty_print(open_ports)

    else:
        print("Compiling list of open ports")
        print(open_ports)
        return open_ports
