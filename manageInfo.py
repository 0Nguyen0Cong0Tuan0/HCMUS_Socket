from MailLib import os, json, CONFIG_FILE

class ManagerInfoUser:
    # Mở file config để đọc
    @staticmethod
    def load_config():
        try:
            with open(CONFIG_FILE, 'r') as file:
                config_data = json.load(file)
            return config_data
        except FileNotFoundError:
            return None
    
    # Xóa (remove) một file config trong folder
    @staticmethod
    def delete_config_file():
        try:
            os.remove(CONFIG_FILE)
        except FileNotFoundError:
            return

            
    