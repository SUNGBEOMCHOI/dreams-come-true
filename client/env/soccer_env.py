import gym
import numpy as np
from gym import spaces
import cv2
import time

class SoccerEnv:
    def __init__(self,
        cfg,
        model,
        camera,
        communication,        
        ):

        super().__init__()

        env_cfg = cfg['env']
        self.mode = env_cfg['mode']
        self.crop_size = env_cfg['crop_size']
        self.robot_fps = env_cfg['robot_fps']

        self.model = model
        self.camera = camera
        self.communication = communication
        

        # Define the action space for the environment
        self.action_space = spaces.Discrete(cfg['num_actions'])  # e.g., 0: stop, 1: move forward, 2: move backward, 3: turn left, 4: turn right
        self.action_space.discrete = True

        # Define the observation space for the environment
        height, width = self.crop_size
        self.observation_space = spaces.Box(low=0, high=255, shape=(height, width), dtype=np.uint8)


    @property
    def action_space(self):
        space = self.env.action_space
        space.discrete = True
        return space
    
    def predict(self, obs):
        if self.mode == 'self_play':
            robot1_action, robot2_action = self.model.predict(obs) # return 2 integers
            return robot1_action, robot2_action
        elif self.model == 'human':
            robot1_action = self.model.predict(obs) # return 1 integer
            return robot1_action
        else:
            raise NotImplementedError

    def step(self, action):
        if self.mode == 'self_play':
            robot1_action, robot2_action = action
        elif self.mode == 'human':
            robot1_action = action
        else:
            raise NotImplementedError
        # Execute the action in the environment and update the environment state

        # TODO: send the action to the robot through Wi-Fi communication
        if self.mode == 'self_play':
            self.communication.send_action_to_robot('A', robot1_action)
            self.communication.send_action_to_robot('B', robot2_action)
        elif self.mode == 'human':
            self.communication.send_action_to_robot('A', robot1_action)

        # Determine if the episode has finished
        time.sleep(1/self.robot_fps) # wait for the robot to execute the action

        # Get the current camera frame
        obs, reward, done = self.camera.get_obs() # {image, self_position, opponent_position, ball_position}

        obs['image'] = cv2.resize(obs['image'], self.crop_size, interpolation=cv2.INTER_AREA)

        done = self.is_done()
        self.step += 1

        if done:
            self.done = True
        else:
            self.done = False
        

        return (
            {"image": obs['image'],
             'self_position':obs['self_position'],
             'opponent_position':obs['opponent_position'],
             'ball_position':obs['ball_position'],
             "is_terminal": self.done,
             "is_first": False},
            reward,
            self.done,
            {},
        )

    def reset(self):
        # Reset the environment state and return the initial observation
        print("After reset press Enter to continue...")
        input()
        print("Continuing...")
        self.camera.close()
        self.communication.connect()
        self.camera.camera_init()

        obs, reward, done = self.camera.get_obs()
        obs['image'] = cv2.resize(obs['image'], self.crop_size, interpolation=cv2.INTER_AREA)
        reward, done = 0, False
        self.step = 0
        if done:
            self.done = True
        else:
            self.done = False

        return (
            {"image": obs['image'],
             'self_position':obs['self_position'],
             'opponent_position':obs['opponent_position'],
             'ball_position':obs['ball_position'],
             "is_terminal": self.done,
             "is_first": True},
            reward,
            self.done,
            {},
        )

    def close(self):
        self.camera.close()
        self.communication.close()

    @property
    def action_space(self):
        space = self.env.action_space
        space.discrete = True
        return space