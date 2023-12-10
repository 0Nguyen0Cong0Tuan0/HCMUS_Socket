from MailLib import os, json, CONFIG_FILE

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
    def delete_config_file():
        try:
            os.remove(CONFIG_FILE)
        except FileNotFoundError:
            return

            
    