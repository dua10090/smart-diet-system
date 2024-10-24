import sqlite3
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, redirect, url_for
from train import train_agent
@app.route('/progress_plot/<int:user_id>')
def progress_plot(user_id):
    conn = get_db_connection()
    progress_data = conn.execute('SELECT date, current_weight FROM progress WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    dates = [row['date'] for row in progress_data]
    weights = [row['current_weight'] for row in progress_data]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, weights, marker='o')
    plt.title('Weight Progress Over Time')
    plt.xlabel('Date')
    plt.ylabel('Weight (kg)')
    plt.grid(True)

    # Save the plot to a byte stream
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('progress_plot.html', plot_url=plot_url)
app = Flask(brofit)
def calculate_reward(self):
    reward = 0
    
    # Reward for weight loss
    weight_diff = self.user_weight - self.target_weight
    if weight_diff < 0:
        reward += 1  # Positive reward for approaching the target weight
    else:
        reward -= 1  # Negative reward if weight is above the target

    # Reward for balanced macronutrient intake
    if self.daily_protein > 50:  # Assuming the user needs high protein
        reward += 0.5  # Bonus for hitting protein target
    else:
        reward -= 0.5  # Penalty for low protein

    # Reward for exercise completion
    if self.burned_calories > 500:
        reward += 0.5  # Bonus for meeting calorie burn targets
    else:
        reward -= 0.5

    return reward

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('scheduler.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page: enter user details
@app.route('/')
def index():
    return render_template('index.html')

# Route to register user details
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        weight = float(request.form['weight'])
        target_weight = float(request.form['target_weight'])
        dietary_pref = request.form['dietary_pref']

        # Store user data in the database
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, weight, target_weight, dietary_pref) VALUES (?, ?, ?, ?)',
                     (name, weight, target_weight, dietary_pref))
        conn.commit()
        conn.close()

        return redirect(url_for('track'))

# Track progress and display recommendations
@app.route('/track')
def track():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1').fetchone()  # Get latest user
    conn.close()

    # Use the latest user data to generate recommendations
    user_data = {
        'weight': user['weight'],
        'target_weight': user['target_weight'],
        'dietary_pref': user['dietary_pref'],
        'food_data': [{'calories': 300}, {'calories': 200}],  # Example data
        'exercise_data': [{'calories_burned_per_hour': 500}, {'calories_burned_per_hour': 300}]
    }

    # Call the train function
    recommendation = train_agent(user_data)

    return render_template('track.html', user=user, recommendation=recommendation)

# Save progress for a given day
@app.route('/progress', methods=['POST'])
def progress():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        date = request.form['date']
        current_weight = float(request.form['current_weight'])
        calories_consumed = float(request.form['calories_consumed'])
        calories_burned = float(request.form['calories_burned'])

        # Save progress to the database
        conn = get_db_connection()
        conn.execute('INSERT INTO progress (user_id, date, current_weight, calories_consumed, calories_burned) VALUES (?, ?, ?, ?, ?)',
                     (user_id, date, current_weight, calories_consumed, calories_burned))
        conn.commit()
        conn.close()

        return redirect(url_for('track'))

if __name__ == "__main__":
    app.run(debug=True)
