import socket

class ClientCommunication:
    def __init__(self, cfg):
        communication_cfg = cfg['communication']
        self.local_ip = communication_cfg['local_ip']
        self.server_ip = communication_cfg['server_ip']
        self.carA_ip = communication_cfg['carA_ip']
        self.carB_ip = communication_cfg['carB_ip']
        self.port = communication_cfg['port']

        self.Client2Server = Client2Server(self.local_ip, self.server_ip, self.port)
        self.Client2R = Client2Car(self.local_ip, self.carA_ip, self.port)

    def connect(self):
        """
        Connect to the car and server
        """
        # TODO: print for connected or not connected
        raise NotImplementedError

    def send_action_to_robot(self, robot, action):
        """
        Send action to robot

        Args:
            robot: robot name, It can be 'A' or 'B'
            action: action
        """
        raise NotImplementedError

    def send_obs_to_server(self, obs):
        """
        Send observation to server

        Args:
            obs: observation
        """
        raise NotImplementedError

    def receive_action_from_server(self):
        """
        Receive action from server
        """
        raise NotImplementedError

    def close(self):
        """
        Close robot and server connection
        """
        raise NotImplementedError



class Client2Car():
    def __init__(self, local_ip='127.0.0.1', car_a_ip='192.168.0.201', car_b_ip='192.168.0.202', port=1234):
        """
        UDP Client for communication with car
        
        Args:
            local_ip: local ip address
            car_a_ip: car A ip address
            car_b_ip: car B ip address
            port: port number        
        """
        self.local_ip = local_ip
        self.carA_ip = car_a_ip
        self.carB_ip = car_b_ip
        self.port = port
        self.server_init() # initialize server
        self.bufferSize = 1024

    def server_init(self):
        """
        Initialize UDP server
        """
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.local_ip, self.port))
        self.sock.setblocking(True)
        print('RC Server Initialized')
        print('--------------------------------')
        print(f'local ip : {self.local_ip}')
        print(f'carA ip : {self.carA_ip}')
        print(f'carB ip : {self.carB_ip}')
        print('--------------------------------')

    def send_action(self, robot='A', act=(0.0, 0.0)):
        """
        Send action to robot

        Args:
            robot: robot name, It can be 'A' or 'B'
            act: action (left wheel speed, right wheel speed)
        """
        speed = act
        message = str(f'{speed[0]}&{speed[1]}').encode()
        self.sock.sendto(message, (self.carA_ip, self.port))

class Client2Server:
    def __init__(self, local_ip, server_ip, port=1234):
        """
        TCP Client for communication with robot
        
        Args:
            local_ip: local ip address
            server_ip: server ip address
            port: port number        
        """
        self.local_ip = local_ip
        self.server_ip = server_ip
        self.port = port
        self.server_init() # initialize server
        
    def server_init(self):
        """
        Initialize TCP server
        """
        raise NotImplementedError
    
    def send_obs(self, obs):
        """
        Send observation to server

        Args:
            obs: observation
        """
        raise NotImplementedError
    
    def receive_action(self):
        """
        Receive action from server
        """
        raise NotImplementedError