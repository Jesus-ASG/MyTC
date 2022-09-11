import configparser
import socket
import os


class SystemConfig:
    def __init__(self):
        # Default configuration
        self.IP = self.get_ip()
        self.PORT = 6000
        self.BUFFER_SIZE = 1048576
        self.OP_SYS = self.get_os()
        self.SEP_SYSTEM = self.get_sep_system(self.OP_SYS)
        self.SEP_ENCODED = '<<<separator>>>'
        self.ROOT_DIR = '<<<root_dir>>>'
        self.receive_path = 'receive'
        self.send_path = 'send'

        # Custom configuration
        self.load_custom_configuration()

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = None
        finally:
            s.close()
        return ip

    @staticmethod
    def get_os():
        return 'WINDOWS' if os.name == 'nt' else 'LINUX'

    @staticmethod
    def get_sep_system(op_sys):
        if op_sys == 'WINDOWS':
            return '\\'
        else:
            return '/'

    def load_custom_configuration(self):
        config_file = 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_file)

        self.PORT = int(config['GENERAL']['PORT'])
        self.receive_path = config['GENERAL']['receive_path']
        self.send_path = config['GENERAL']['send_path']



