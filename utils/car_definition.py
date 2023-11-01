import json
class TireManager:
    def __init__(self, curr_pressure:int, max_pressure:int) -> None:
        self.front_left = curr_pressure
        self.front_right = curr_pressure
        self.rear_left = curr_pressure
        self.rear_right = curr_pressure
        
        self.pressure_lim = max_pressure

        self.details = '''tire_pressure_limit specifies the safe limit for a tire pressure.
        Warn the user in case any tire exceeds this limit'''

    def get_state(self):
        curr_state = {
            "front_left_pressure" : self.front_left,
            "front_right_pressure" : self.front_right,
            "rear_left_pressure" : self.rear_left,
            "rear_right_pressure" : self.rear_right,
            "tire_pressure_limit" : self.pressure_lim,
        }

        return curr_state
    
    def generate_prompt(self):
        properties = self.get_state()
        context = self.details
        prompt = {
            "context" : context,
            "properties" : properties
        }

        return prompt
    
    def load_state_dict(self, new_state:dict):
        self.front_left = new_state['front_left']
        self.front_right = new_state['front_right']
        self.rear_left = new_state['rear_left']
        self.rear_right = new_state['rear_right']

        if 'pressure_lim' in new_state.keys():
            self.pressure_lim = new_state['pressure_lim']

class Navigator:
    def __init__(self) -> None:
        self.journey_state = "INACTIVE"
        self.source = None
        self.destination = None

    def get_state(self):
        curr_state = {
            "journey_state" : self.journey_state,
            "source" : self.source,
            "destination":self.destination
        }

        return curr_state
    
    def generate_prompt(self):
        return self.get_state()
    
    def load_state_dict(self, new_state:dict):
        self.journey_state = new_state['journey_state']
        self.source = new_state['source']
        self.destination = new_state['destination']
    
class ClimateControl:
    def __init__(self, temp:float = 30) -> None:
        self.zones = [temp, temp, temp, temp]
    
    def set_temp(self, zone_id:int, new_temp:float):
        self.zones[zone_id] = new_temp
    
    def get_state(self):
        curr_state = {
            "zone_0_temp" : self.zones[0],
            "zone_1_temp" : self.zones[1],
            "zone_2_temp" : self.zones[2],
            "zone_3_temp" : self.zones[3],
        }

        return curr_state

    def generate_prompt(self):
        context = '''zone 0 = front left, zone 1 = front right,
        zone 2 = rear left, zone 3 = rear right
        '''

        properties = self.get_state()

        prompt = {
            "context": context,
            "properties":properties
        }

        return dict(prompt)

    def load_state_dict(self, new_state:dict):
        new_zones = new_state['new_zones']        
        for id, new_temp in enumerate(new_zones):
            if new_temp != -1:
                self.zones[id] = new_temp

class InfotainmentCluster:
    def __init__(self) -> None:
        self.playing = False
        self.song = ""
        self.singer = ""
    
    def get_state(self):
        curr_state = {
            "playing" : self.playing,
            "song name" : self.song,
            "singer/band name" : self.singer
        }

        return curr_state
    
    def generate_prompt(self):
        properties = self.get_state()

        context = '''```playing``` denotes whether any song is playing or not. True if playing, otherwise False'''

        prompt = {
            "context" : context,
            "properties" : properties
        }

        return dict(prompt)
    
    def load_state_dict(self, new_state:dict):
        self.playing = new_state['playing']
        self.song = new_state['song']
        self.singer = new_state['singer']

class Car:
    def __init__(self) -> None:
        self.curr_speed = 0
        self.lane_assist = "OFF"
        self.engine_temp = 320
        self.clutch_oil_level = 50

        self.tire_manager = TireManager(
            curr_pressure = 55,
            max_pressure = 100
        )

        self.navigation_control = Navigator()
        self.climate_control = ClimateControl()
        self.infotainment_system = InfotainmentCluster()

    def get_state(self):
        curr_state = {
            "current_speed" : self.curr_speed,
            "lane_assist_state" : self.lane_assist,
            "engine_temp" : self.engine_temp,
            "clutch_oil_level" : self.clutch_oil_level,
            "climate_control_state":self.climate_control.generate_prompt(),
            "tires_pressure_state":self.tire_manager.generate_prompt(),
            "navigation_state" : self.navigation_control.generate_prompt(),
            "infotainment_state" : self.infotainment_system.generate_prompt(),
        }

        return curr_state

    def generate_prompt(self):
        properties = self.get_state()

        return dict(properties)
    
    def get_diagnostics_data(self):
        diagnostics_data = {
            'engine_temp' : {
                'curr_state' : self.engine_temp,
                'context' : '''The engine temp must be always less than 200 degrees'''
            },
            'clutch_oil_level' : {
                'curr_state' : self.clutch_oil_level,
                'context' : '''The clutch oil level must always be more than 20'''
            },
            'tire_pressures' : {
                'curr_state' : self.tire_manager.get_state(),
                'context' : self.tire_manager.details
            },
        }

        return diagnostics_data