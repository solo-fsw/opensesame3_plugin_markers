"""
Functions for serial communications.
"""

import serial
import json
import re
import sys
from serial.tools.list_ports import comports



except_factory = BaseException


def gen_com_filters(port_regex = '^.*$'
                , sn_regex = '^.*$'
                , com_dev_desc_regex = '^.*$'
                , com_dev_hwid_regex = '^USB VID:PID=2341:.*$'):

    # Return the COM filters:
    return { \
        "port_regex": port_regex
        , "sn_regex": sn_regex
        , "com_dev_desc_regex": com_dev_desc_regex
        , "com_dev_hwid_regex": com_dev_hwid_regex}




class Serial_Manager():

    FAKE_COM_ADDR = "FAKE"

    def __init__(self, com_port):

        parmarker_data_params = { "baudrate": 115200, "bytesize": 8
                                , "parity": 'N', "stopbits": 1
                                , "timeout": 2}
        self.serial = serial.Serial(com_port, **parmarker_data_params)

    
    def send(self, value):

        # Checks:
        if not (isinstance(self.serial, serial.serialwin32.Serial) \
            and self.serial.isOpen()):
            raise except_factory("No valid serial device.")
        if not isinstance(value, int):
            raise except_factory("Marker value must be an integer.")
        if (value < 0) or (value > 255):
            raise except_factory("Marker value must be 0 through 255.")

        # Send:
        self.serial.write(bytearray([value]))



def find_device(com_filters = gen_com_filters()):
    """ 
    This function finds the COM address of an Evert-style COM device.
    If can use filters, and will throw an error unless exactly one suitable 
    COM device can be connected to.
    """

    # Support a fake COM device request:
    info = {}
    if com_filters['port_regex'] == Serial_Manager.FAKE_COM_ADDR:
        info['device']['Serialno'] = '0000000'
        info["com_desc"] = "Fake COM device"
        info["com_port"] = Serial_Manager.FAKE_COM_ADDR
        return info
        
    # Params:
    parmarker_command_params ={ "baudrate": 4800, "bytesize": 8
                                , "parity": 'N', "stopbits": 1
                                , "timeout": 2}
    connected = False
    ser = None
    port_hit = False
    desc_hit = False
    hwid_hit = False
    serial_hit = False
    for port, desc, hwid in comports():
        
        # Check filters:
        port_matches_request = re.match(com_filters['port_regex'], port) != None
        com_dev_desc_matches = re.match(com_filters['com_dev_desc_regex'], desc) != None
        com_dev_hwid_matches = re.match(com_filters['com_dev_hwid_regex'], hwid) != None
        if port_matches_request:
            port_hit = True
        if com_dev_desc_matches:
            desc_hit = True
        if com_dev_hwid_matches:
            hwid_hit = True
        if not (port_matches_request \
                and com_dev_desc_matches \
                    and com_dev_hwid_matches):
            continue
        
        # Check device:
        com_dev_desc_matches = re.match(com_filters['com_dev_desc_regex'], desc) != None
        com_dev_hwid_matches = re.match(com_filters['com_dev_hwid_regex'], hwid) != None        
        
        if com_dev_desc_matches and com_dev_hwid_matches:
            # If a matching device is found, attempt to connect to it:
            try:
                ser = serial.Serial(port, **parmarker_command_params)
                
                # Ask for the info:
                ser.flushInput()
                ser.write("V".encode('UTF-8'))
                response_line = ser.readline().decode("utf-8").replace('\r\n', '')
                ser.close()
                
                # Check response:
                if response_line == "":
                    raise except_factory("Serial device did not respond.")
                try:
                    info['device'] = json.loads(response_line)
                except:
                    raise except_factory("COM device did not respond with JSON.")
                if not "Serialno" in info['device']:
                    raise except_factory("Serialno missing.")
                serialno_matches = re.match(com_filters['sn_regex'], info['device']['Serialno']) != None        
                if not serialno_matches:
                    continue
                serial_hit = True
                
                if connected:
                    except_factory("Multiple matching devices found.")
                info["com_desc"] = desc
                info["com_port"] = port
                connected = True
                
            except:
                try:
                    ser.close()
                except:
                    pass
                raise except_factory(f'Could not connect to "{desc}" because: {sys.exc_info()[1]}')
                
    if not port_hit:
        raise except_factory("No device matched the specified COM address.")
    if not desc_hit:
        raise except_factory("No device matched the specified COM description.")
    if not hwid_hit:
        raise except_factory("No device matched the specified HW ID.")
    if not serial_hit:
        raise except_factory("No device matched the specified serial number.")
    if not connected:
        raise except_factory("No suitable COM devices found.")
    
    return info
