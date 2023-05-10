import time

from communication  import ClientCommunication
from camera import CameraModule
from env import SoccerEnv
import datetime
import pathlib
import numpy as np
import io
import uuid
import cv2

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
        self.env_cfg = cfg['env']

        self.camera = CameraModule(self.camera_cfg)
        self.communication = ClientCommunication(self.communication_cfg)
        self.model = None,
        self.env = SoccerEnv(
        self.env_cfg,
        self.model,
        self.camera,
        self.communication,
        )

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

    def collect_data(self, max_steps, directory='./train_dir'):
        """
        Collect data from the robot
        """
        directory = pathlib.Path(directory).expanduser()
        directory.mkdir(parents=True, exist_ok=True)
        steps = 0
        done = True
        while steps < max_steps:
            if done:
                obs, reward, done, _ = self.env.reset()
                transition = obs.copy()
                transition["reward"] = reward
                transition["discount"] = 1.0
                self.episode = [transition]
            else:
                if self.env.mode == 'self_play':
                    robot1_action, robot2_action = self.env.predict(obs)
                    obs, reward, done, _ = self.env.step((robot1_action, robot2_action))
                elif self.env.mode == 'human':
                    robot1_action = self.env.predict(obs)
                    obs, reward, done, _ = self.env.step(robot1_action)
                transition = obs.copy()
                transition["action"] = np.array(robot1_action)
                transition["reward"] = np.array(reward)
                transition["discount"] = np.array(0.0) if done else np.array(1.0)
                self.episode.append(transition)
                if done:
                    timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
                    episode = {k: [t[k] for t in self.episode] for k in self.episode[0]}
                    identifier = str(uuid.uuid4().hex)
                    length = len(episode["reward"])
                    filename = directory / f"{timestamp}-{identifier}-{length}.npz"
                    with io.BytesIO() as f1:
                        np.savez_compressed(f1, **episode)
                        f1.seek(0)
                        with filename.open("wb") as f2:
                            f2.write(f1.read())
                    # print filename
                    print(f"Episode steps: {length} saved to {filename}")
        
if __name__ == "__main__":
    cap = cv2.VideoCapture(1)
    timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = f"./data/{timestamp}-{identifier}-{length}.npz"
    with io.BytesIO() as f1:
        np.savez_compressed(f1, **episode)
        f1.seek(0)
        with filename.open("wb") as f2:
            f2.write(f1.read())
    # print filename
    print(f"Episode steps: {length} saved to {filename}")