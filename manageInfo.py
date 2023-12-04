from MailLib import json, CONFIG_FILE

class ManagerInfoUser:
    @staticmethod
    def load_config():
        try:
            with open(CONFIG_FILE, 'r') as file:
                config_data = json.load(file)
            return config_data
        except FileNotFoundError:
            return None
    
    @staticmethod
    def reset_config():
        try:
            with open(CONFIG_FILE, 'r') as file:
                config_data = json.load(file)
            
            erased_data = {key: "" for key in config_data}

            with open(CONFIG_FILE, 'w') as file:
                json.dump(erased_data, file)
        except FileNotFoundError:
            print(f"File '{CONFIG_FILE}' not found.")

            
    