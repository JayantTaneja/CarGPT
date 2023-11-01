import streamlit as st

import json
import socket
from time import sleep

from .charts import *
from utils.car_definition import Car

def setup():
    st.session_state.car = Car()

    col1, col2, col3, col4 = st.columns([5, 1, 2, 1], gap="small")
    speed_gauge_fig = speed_gauge()
    tire_chart_fig = tire_pressure_anim()

    with col1:
        st.session_state.speed_gauge = st.plotly_chart(speed_gauge_fig, use_container_width=True)

    with col3:
        st.session_state.tire_display = st.plotly_chart(tire_chart_fig, use_container_width=True)

    col1, col2, col3, col4 = st.columns([5, 1, 2, 2], gap="small")
    with col3:
        air_con0 = air_con_gauge(25, 0)
        st.session_state.aircon_gauge0 = st.plotly_chart(air_con0, use_container_width=True)
    
    with col4:
        air_con1 = air_con_gauge(25, 1)
        st.session_state.aircon_gauge1 = st.plotly_chart(air_con1, use_container_width=True)
    
    with col3:
        air_con2 = air_con_gauge(25, 2)
        st.session_state.aircon_gauge2 = st.plotly_chart(air_con2, use_container_width=True)
    
    with col4:
        air_con3 = air_con_gauge(25, 3)
        st.session_state.aircon_gauge3 = st.plotly_chart(air_con3, use_container_width=True)
    
    blank_screen = Image.open('images/blank.png')
    with col1:
        st.session_state.infotainment_screen = st.image(blank_screen)

def update_air_con_gauges():
    car:Car = st.session_state.car
    air_con0 = air_con_gauge(car.climate_control.zones[0], 0)
    air_con1 = air_con_gauge(car.climate_control.zones[1], 1)
    air_con2 = air_con_gauge(car.climate_control.zones[2], 2)
    air_con3 = air_con_gauge(car.climate_control.zones[3], 3)

    st.session_state.aircon_gauge0.plotly_chart(air_con0)
    st.session_state.aircon_gauge1.plotly_chart(air_con1)
    st.session_state.aircon_gauge2.plotly_chart(air_con2)
    st.session_state.aircon_gauge3.plotly_chart(air_con3)

def update_speed_gauge():
    speed = st.session_state.car.curr_speed
    speed_gauge_fig = speed_gauge(speed)
    st.session_state.speed_gauge.plotly_chart(speed_gauge_fig, use_container_width = True)

def update_infotainment_cluster():
    car:Car = st.session_state.car
    
    playing = car.infotainment_system.playing
    
    if playing:
        song_title = car.infotainment_system.song
        singer_name = car.infotainment_system.singer
    
    else:
        song_title = "No Song Playing"
        singer_name = ""
    

    journey_state = car.navigation_control.journey_state

    if journey_state == "INACTIVE":
        start = "No location chosen"
        destination = "No location chosen"
    
    else:
        start = car.navigation_control.source
        destination = car.navigation_control.destination
    
    fig = infotainment_display(start, destination, song_title, singer_name)
    st.session_state.infotainment_screen.plotly_chart(fig, use_container_width = True)


def update_tire_pressure_display():
    car:Car = st.session_state.car
    fl = car.tire_manager.front_left
    fr = car.tire_manager.front_right
    rl = car.tire_manager.rear_left
    rr = car.tire_manager.rear_right

    fig = tire_pressure_anim(fl, fr, rl, rr)
    st.session_state.tire_display.plotly_chart(fig, use_container_width = True)

def show_startup():
    sleep(2)
    welcome_screen = Image.open("images/welcome_screen.png")
    st.session_state.infotainment_screen.image(welcome_screen)
    
    sleep(2)
    update_tire_pressure_display()
    sleep(1)
    
    update_air_con_gauges()
    sleep(2)
    
    update_infotainment_cluster()

    speed = 0
    acceleration = 1
    scale_factor = 1

    for _ in range(1000):
        speed += acceleration * scale_factor
        st.session_state.car.curr_speed = speed

        if speed >= 120:
            update_speed_gauge()
            break
        scale_factor *= 0.992
        update_speed_gauge()
        sleep(0.01)

def update_state(state_dict:dict):
    changed_property = state_dict['property']
    new_state = state_dict['new_state']

    if changed_property == 'speed':
        st.session_state.car.curr_speed = new_state['value']
        update_speed_gauge()
    
    elif changed_property == 'lane_assist':
        st.session_state.car.lane_assist_state = new_state['value']
        
    elif changed_property == 'climate_control':
        st.session_state.car.climate_control.load_state_dict(new_state)
        update_air_con_gauges()
    
    elif changed_property == 'tire_pressure':
        st.session_state.car.tire_manager.load_state_dict(new_state)
        update_tire_pressure_display()
    
    elif changed_property == 'navigation':
        st.session_state.car.navigation_control.load_state_dict(new_state)
        update_infotainment_cluster()
    
    elif changed_property == 'music_player':
        st.session_state.car.infotainment_system.load_state_dict(new_state)
        update_infotainment_cluster()

def send_reply(data_dict:dict, conn):
    property = data_dict['property']
    
    if property == 'car_state':
        car_state = st.session_state.car.generate_prompt()
        packet = json.dumps(car_state)
        conn.sendall(bytes(packet, encoding='utf-8'))
    
    elif property == 'diagnostics_data':
        diagnostics_data = st.session_state.car.get_diagnostics_data()
        packet = json.dumps(diagnostics_data)
        conn.sendall(bytes(packet, encoding='utf-8'))

def listen(HOST, PORT):
    reply = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("\n\nServer listening to port :", PORT)
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            data = conn.recv(4096)

            print("Recieved", data)
            data_dict = json.loads(data) 
            action = data_dict['action']

            if action == 'PUT':
                update_state(data_dict)
            
            elif action == 'GET':
                send_reply(data_dict, conn)

            elif action == 'TERMINATE-CONNECTION':
                reply = 'end'

    return reply

def start_server():
    HOST = "127.0.0.1"
    PORT = 65432

    while True:
        reply = listen(HOST, PORT)

        if reply == 'end':
            print('server process stopped')
            return        