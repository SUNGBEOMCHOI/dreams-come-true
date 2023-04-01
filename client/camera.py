import cv2
import numpy as np

class CameraModule:
    def __init__(self, cfg):
        """
        Camera module for the soccer environment.
        Return observations, reward and is_terminate from the camera.

        Args:
            cfg: The configuration file for the camera module.    
        """
        camera_cfg = cfg['camera']
        ball_template_path = camera_cfg['ball_template_path']
        robot_template_path = camera_cfg['robot_template_path']
        reward_condition = camera_cfg['reward_condition']
        done_condition = camera_cfg['done_condition']

        self.ball_tracker = BallTracker(ball_template_path)
        self.robot_tracker = RobotTracker(robot_template_path)
        self.reward_processor = RewardProcessor(reward_condition)
        self.done_processor = TerminationDetector(done_condition)

    def camera_init(self):
        """
        Initializes the camera.
        """
        # TODO : below is the example code for the camera initialization
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        raise NotImplementedError

    def get_frame(self):
        """
        Gets the current frame from the camera.

        Returns:
            The current frame from the camera.
        """
        raise NotImplementedError

    def get_info(self):
        """
        Gets the current observation, reward and done or not from the camera. 
        observation includes the preprocessed frame, the position of the ball in the 
            frame, and the position and angle of the robot in the frame.

        Returns:
            observation: The current observation from the camera.
            reward: The reward from the current frame.
            done: True if the episode has finished, False otherwise.
        """
        frame = self.get_frame()
        cropped_frame = self.crop_frame(frame)

        ball_position, robot_info = self.get_obs(cropped_frame)
        observation = [cropped_frame, ball_position, robot_info]
        done = self.done_processor.is_terminate(ball_position)
        reward = self.reward_processor.get_reward(ball_position, done)
        
        return observation, reward, done
    
    def get_obs(self, frame):
        """
        Gets the observation from the frame.

        Args:
            frame: The cropped frame to get the observation from.

        Returns:
            ball_position: The position of the ball in the frame.
            robot_info: The position of the robot in the frame.
        """
        raise NotImplementedError

    def crop_frame(self, frame, crop_size=(200, 200)):
        """
        Crops the frame to the specified size.
        
        Args:
            frame: The frame to crop.
            crop_size: The size of the frame to crop to. Should be a tuple of (width, height).

        Returns:
            The cropped frame.
        """
        raise NotImplementedError

class RewardProcessor:
    def __init__(self, reward_condition):
        """
        Reward module for the soccer environment.
        Calculates reward from the camera.

        Args:
            reward_condition: The condition to calculate the reward from.
        """
        self.reward_condition = reward_condition


    def get_reward(self, ball_position, done):
        """
        Gets the reward from the frame.

        Args:
            ball_position: The position of the ball in the frame.
            done: True if the episode has finished, False otherwise.

        Returns:
            The reward from the frame.
        """
        raise NotImplementedError

class TerminationDetector:
    def __init__(self, done_condition):
        """
        Detection module for the soccer environment.

        Args:
            done_condition: The condition to calculate if the episode should terminate from.
        """
        self.done_condition = done_condition

    def is_terminate(self, ball_position):
        """
        Checks if the episode should terminate.

        Args:
            ball_position: The position of the ball in the frame.

        """
        raise NotImplementedError

class BallTracker:
    def __init__(self, ball_template_path):
        """
        Module for tracking the ball in the frame.

        Args:
            ball_template_path: Path to the ball template image.        
        """
        self.ball_template = cv2.imread(ball_template_path)

    def track_ball(self, frame):
        """
        Tracks the ball in the frame.

        Args:
            frame: The frame to track the ball in.

        Returns:
            The position of the ball in the frame.
        """
        raise NotImplementedError

class RobotTracker:
    def __init__(self, robot_template_path):
        """
        Module for tracking the robot in the frame.

        Args:
            robot_template_path: Path to the robot template image.
        """
        self.robot_template = cv2.imread(robot_template_path)

    def track_robot(self, frame):
        """
        Tracks the robot in the frame.

        Args:
            frame: The frame to track the robot in.

        Returns:
            The position of the robot in the frame.
        """
        raise NotImplementedError