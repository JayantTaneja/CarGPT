import json
import socket

from time import sleep


HOST = "127.0.0.1"
PORT = 65432

def send_packet(data):
    '''
    Transmits data packet to the server and returns the reply

    ### Params:
    - data : str
            The data packet to be sent to the server

    ### Returns  
    None

    '''

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes(data, encoding="utf-8"))
            
            reply = s.recv(10000)
    except Exception as e:
        print(e)
    
    finally:
        print("transaction complete!")
    
    return reply

def set_lane_assist_state(value:str = "OFF"):
    '''
    Sets the new state for Lane Assist Property

    ### Params
    - value : str
            The new state of lane assist
            Must be either "ON" or "OFF"
    
    ### Returns
    None
    
    '''

    data_dict = {
        'action' : 'PUT',
        'property' : 'lane_assist',
        'new_state' : {
            'value' : value
        }
    }
    send_packet(json.dumps(data_dict))

def set_ac_temp(new_temp:int, zone_id:int):
    '''
    Sets the new temp in climate control

    ### Params
    - new_temp : int
            Value of new temperature
        
    - zone_id : int
            Index (0-3) of the zone whose temp is to be changes
            Must one of [-1, 0, 1, 2, 3],
            
            -1 denotes all zones

    ### Returns
    None
    
    '''
    
    new_zones = [-1] * 4

    if zone_id == -1:
        new_zones = [int(new_temp)] * 4
    else:
        new_zones[zone_id] = int(new_temp)
    
    data_dict = {
        'action' : 'PUT',
        'property' : 'climate_control',
        'new_state' : {
            'new_zones' : new_zones
        }
    }

    send_packet(json.dumps(data_dict))

def update_tire_pressure(new_pressures:list):
    '''
    Updates the tire pressures of each tire

    ### Params
    - new_pressures : List[int]
            List of ints denoting new tire pressure of each wheel

    ### Returns
    None
    
    '''

    data_dict = {
        'action' : 'PUT',
        'property' : 'tire_pressure',
        'new_state' : {
            'front_left' : new_pressures[0],
            'front_right' : new_pressures[1],
            'rear_left' : new_pressures[2],
            'rear_right' : new_pressures[3]
        }
    }
    send_packet(json.dumps(data_dict))

def navigate(source:str, dest:str):
    '''
    Starts the navigation on the infotainment cluster

    ### Params
    - source : str
            The journey start point
    - dest : str
            The journey end point

    ### Returns
    None
    
    '''
    
    data_dict = {
        'action' : 'PUT',
        'property' : 'navigation',
        'new_state' : {
            'journey_state' : "ACTIVE",
            'source' : source,
            'destination' : dest
        }
    }
    send_packet(json.dumps(data_dict))

def quit_navigation():
    '''
    Stops the navigation

    ### Params
    None

    ### Returns
    None
    
    '''
    
    data_dict = {
        'action' : 'PUT',
        'property' : 'navigation',
        'new_state' : {
            'journey_state' : "INACTIVE",
            'source' : "",
            'destination' : ""
        }
    }
    send_packet(json.dumps(data_dict))

def play_song(song_title:str, by:str):
    '''
    Starts playing music on the infotainment cluster

    ### Params
    - song_title : str
            Name of the song to be played
    - by : str
            Name of the band/singer of the song to be played

    ### Returns
    None
    
    '''
    
    if song_title == "" and by != "":
        song_title = f"Shuffling Songs by {by}"
    data_dict = {
        'action' : 'PUT',
        'property' : 'music_player',
        'new_state' : {
            'playing' : True,
            'song' : song_title,
            'singer' : by
        }
    }
    send_packet(json.dumps(data_dict))

def stop_playing_song():
    '''
    Stops playing song, if playing already

    ### Params
    None

    ### Returns
    None
    
    '''
    
    data_dict = {
        'action' : 'PUT',
        'property' : 'music_player',
        'new_state' : {
            'playing' : False,
            'song' : "",
            'singer' : ""
        }
    }
    send_packet(json.dumps(data_dict))

def retrieve_diagnostics_data():
    '''
    Retrieves the diagnostics data from the car

    ### Params
    None

    ### Returns
    - diagnostics_data : dict
            Dictionary containing relevant diagnostics data with properties 
            including clutch oil level, engine temperature and tire pressures
    '''
    
    data_dict = {
        'action' : 'GET',
        'property' : 'diagnostics_data'
    }
    reply = send_packet(json.dumps(data_dict))

    return (reply)


def retrieve_car_state():
    '''
    Retrieves the current state of the car

    ### Params
    None

    ### Returns
    - car_state : dict
            Dict containing all the necessary details including :
            - current_speed
            - lane_assist_state
            - engine_temp
            - clutch_oil_level
            - climate_control_state
            - tires_pressure_state
            - navigation_state
            - infotainment_state
    '''

    data_dict = {
        'action' : 'GET',
        'property' : 'car_state'
    }
    reply = send_packet(json.dumps(data_dict))

    return json.loads(reply)

def no_func_needed():
    '''
    Dummy function to be called if no function
    needs to be called

    ### Params
    None

    ### Returns
    None
    '''

    return

def func_scheduler(func_name, func_arg_list, delay):
    sleep(delay)
    func_name(**func_arg_list)