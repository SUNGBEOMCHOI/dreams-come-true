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
        raise NotImplementedError

    def close(self):
        """
        Close robot and server connection
        """
        self.communication.close()