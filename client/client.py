import time

from communication  import ClientCommunication
from camera import CameraModule

class Client:
    def __init__(self, cfg):
        """
        Class that manage everything on the client side

        Args:
            cfg: The configuration file for the client.    
        """
        self.frequency = cfg['frequency']
        self.camera_cfg = cfg['camera']
        self.communication_cfg = cfg['communication']

        self.camera = CameraModule(self.camera_cfg)
        self.communication = ClientCommunication(self.communication_cfg)

    def initialize(self):
        """
        initialize the connection to the robot, server and the camera
        """
        self.communication.connect()
        self.camera.camera_init()

    def run(self):
        """
        Run the client
        """
        while True:
            # Loop every 1/self.frequency seconds
            time.sleep(1/self.frequency)

            # Get observation from camera
            info = self.camera.get_info() # info = (observation, reward, done)
            _, _, done = info

            # Send observation to server
            self.communication.send_info_to_server(info)

            # If done in observation: break
            if done:
                break

            # Receive action from server
            robot, action = self.communication.receive_action_from_server()

            # Send action to robot
            self.communication.send_action_to_robot(robot, action)

    def close(self):
        """
        Close robot and server connection
        """
        self.communication.close()