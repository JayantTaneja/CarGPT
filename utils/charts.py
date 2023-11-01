from PIL import Image

import plotly.express as px
import plotly.graph_objects as go


def air_con_gauge(temp:int = 25, zone_id:int = 0):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        number = {'suffix': " °C", 'font': {'size': 15}},
        value = int(temp),
        domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [10, 35]},
            'steps' : [
                {'range': [10, 25], 'color': "blue"},
                {'range': [25, 30], 'color': "yellow"},
                {'range': [30, 35], 'color': "orange"}
            ]
            }
    ))

    fig.update_layout({
        'height' : 200,
        'margin' : {
            't' : 0,
            'r' : 10,
            'b' : 0,
            'l' : 20,
        },
    })

    fig.add_annotation(
        text = f"Zone {zone_id}", font = {'size': 15},
        showarrow=False
    )

    return fig

def speed_gauge(speed:int = 0):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        number = {'suffix': " Km/H", 'font': {'size': 30}},
        value = int(speed),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Speed", 'font' : {'size':15}},
            gauge = {'axis': {'range': [None, 250]},
            'steps' : [
                {'range': [0, 100], 'color': "lightgray"},
                {'range': [100, 200], 'color': "gray"}
            ],
            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 200}}
    ))

    fig.update_layout({
        'margin' : {
            't' : 0,
            'b' : 0
        },
    })

    return fig

def tire_pressure_anim(
    front_left = "",    
    front_right = "",    
    rear_left = "",    
    rear_right = "",    
    ):
    im = Image.open('images/wireframe.jpg')
    im = im.rotate(180)

    fig = px.imshow(im)
    fig.update_layout({
        'xaxis': {
            'showgrid': False,
            'zeroline': False,
            'visible': False, 
        }, 
        'yaxis': {
            'showgrid': False,
            'zeroline': False,
            'visible': False, 
        },
        'margin' : {
            't' : 0,
            'b':0
        },
    })

    fig.add_annotation(
        text=f"{front_left} PSI", align="left", font={"size":20},
        xanchor='right', yanchor='bottom',
        x = 125, y = 120, ax = -25, ay = -30,
        arrowhead=0,
    )

    fig.add_annotation(
        text=f"{front_right} PSI", align="right", font={"size":20},
        xanchor='left', yanchor='bottom',
        x = 345, y = 120, ax = 25, ay = -30,
        arrowhead=0,
    )

    fig.add_annotation(
        text=f"{rear_left} PSI", align="right", font={"size":20},
        xanchor='right', yanchor="top",
        x = 125, y = 475, ax = -25, ay = 30,
        arrowhead=0,
    )

    fig.add_annotation(
        text=f"{rear_right} PSI", align="right", font={"size":20},
        xanchor='left', yanchor="top",
        x = 345, y = 475, ax = 25, ay = 30,
        arrowhead=0,
    )

    return fig

def infotainment_display(
        start:str = "Your Location",
        dest:str = "No Dest Set",
        song:str = "Roar",
        singer:str = "Katy Perry"):
    
    if dest == "No Dest Set":
        dest = "No Destination Set"
        
    im = Image.open('images/infotainment.png')

    fig = px.imshow(im)
    fig.update_layout({
        'xaxis': {
            'showgrid': False,
            'zeroline': False,
            'visible': False, 
        }, 
        'yaxis': {
            'showgrid': False,
            'zeroline': False,
            'visible': False, 
        },
        'margin' :{
            't' : 0,
            'l' : 0,
            'b' : 0,
            'r' : 0,
        } 
    })

    fig.add_annotation(
        text=start.title(), align="right", font={"color" : "white", "size":15},
        x = 900, y = 85,
        showarrow= False,
        xanchor='left', yanchor='middle',
    )

    fig.add_annotation(
        text=f"Start", align="right", font={"color" : "lightgreen", "size":10},
        x = 900, y = 145,
        showarrow= False,
        xanchor='left', yanchor='middle',
    )

    fig.add_annotation(
        text=dest.title(), align="right", font={"color" : "white", "size":15},
        x = 900, y = 240, xanchor='left', yanchor='middle',
        showarrow= False,
    )

    fig.add_annotation(
        text=f"Dest", align="right", font={"color" : "lightgreen", "size":10},
        x = 900, y = 285, xanchor='left', yanchor='middle',
        showarrow= False,
    )

    fig.add_annotation(
        text=song.title(), align="left", font={"color" : "white", "size":15},
        x = 810, y = 402, xanchor='left', yanchor='middle',
        showarrow= False,
    )


    fig.add_annotation(
        text=singer.title(), align="left", font={"color" : "white", "size":10},
        x = 810, y = 455, xanchor='left', yanchor='middle',
        showarrow= False,
    )

    return fig
