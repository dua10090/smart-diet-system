import numpy as np
import gym
from gym import spaces

class DietExerciseEnv(gym.Env):
    def __init__(self, user_data):
        super(DietExerciseEnv, self).__init__()
        
        # Action space: Recommend one meal and one exercise per step
        self.action_space = spaces.Discrete(len(user_data['food_data']) + len(user_data['exercise_data']))

        # Observation space: User's current state (weight, daily calories, burned calories)
        self.observation_space = spaces.Box(low=np.array([40, 0, 0]), high=np.array([150, 5000, 4000]), dtype=np.float32)

        # Initialize user state
        self.user_weight = user_data['weight']
        self.daily_calories = 0
        self.burned_calories = 0
        self.target_weight = user_data['target_weight']
    

    def step(self, action):
        reward = 0
        
        # Assume first half of actions are meals, second half are exercises
        if action < len(user_data['food_data']):
            meal = user_data['food_data'][action]
            self.daily_calories += meal['calories']
        else:
            exercise = user_data['exercise_data'][action - len(user_data['food_data'])]
            self.burned_calories += exercise['calories_burned_per_hour']
        
        # Calculate new weight based on calorie intake/output
        net_calories = self.daily_calories - self.burned_calories
        weight_change = net_calories / 7700  # 7700 calories = 1 kg of fat
        self.user_weight += weight_change
        
        # Reward: Weight loss towards target gets a positive reward
        if self.user_weight < self.target_weight:
            reward = 1
        else:
            reward = -1
        
        done = abs(self.user_weight - self.target_weight) < 0.5  # End if user is within 0.5kg of target weight
        obs = np.array([self.user_weight, self.daily_calories, self.burned_calories])

        return obs, reward, done, {}

    def reset(self):
        self.user_weight = user_data['weight']
        self.daily_calories = 0
        self.burned_calories = 0
        return np.array([self.user_weight, self.daily_calories, self.burned_calories])

    def render(self):
        print(f"Current weight: {self.user_weight}, Daily intake: {self.daily_calories}, Calories burned: {self.burned_calories}")
    