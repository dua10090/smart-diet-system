import numpy as np
import random
from collections import deque
from diet_exercise_env import DietExerciseEnv

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Replay memory
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.epsilon_decay = 0.995  # Decay rate for exploration probability
        self.model = self._build_model()  # Build the model

    def _build_model(self):
        # Implement your neural network model here (e.g., using TensorFlow/Keras or PyTorch)
        from keras.models import Sequential
        from keras.layers import Dense
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer='adam')  # Use Adam optimizer
        return model

    def act(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # Explore
        act_values = self.model.predict(state)  # Predict action values
        return np.argmax(act_values[0])  # Exploit

    def remember(self, state, action, reward, next_state, done):
        # Store experience in replay memory
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        # Train the model based on experiences from replay memory
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay  # Decay exploration rate


# Load your dataset
user_data = {
    'weight': 82,
    'target_weight': 75,
    'food_data': [{'calories': 300}, {'calories': 200}, {'calories': 400}],
    'exercise_data': [{'calories_burned_per_hour': 500}, {'calories_burned_per_hour': 300}]
}

env = DietExerciseEnv(user_data)
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
agent = DQNAgent(state_size, action_size)

episodes = 1000
batch_size = 32

for e in range(episodes):
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    
    for time in range(500):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])
        
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        
        if done:
            print(f"Episode {e + 1}/{episodes}, Score: {time}, Weight: {env.user_weight}")
            break
        
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)