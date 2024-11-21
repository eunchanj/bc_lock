from flask import Flask, render_template, request, redirect, url_for
import datetime
from jinja2 import Environment

app = Flask(__name__)

# Define the attention grade categories
attention_grades = ['LOW', 'MEDIUM', 'HIGH']

# Define the default time blocks (1 hour or 30 minutes)
time_blocks_1h = [f"{str(hour).zfill(2)}:00-{str(hour+1).zfill(2)}:00" for hour in range(24)]
time_blocks_30m = [f"{str(hour).zfill(2)}:{minute:02d}-{str(hour if minute == 0 else hour + 1).zfill(2)}:{minute + 30 if minute == 0 else 0:02d}" for hour in range(24) for minute in (0, 30)]

# Define the schedule data (for simplicity, it's initialized in-memory)
schedule_data = {
    'Monday': [''] * len(time_blocks_1h),
    'Tuesday': [''] * len(time_blocks_1h),
    'Wednesday': [''] * len(time_blocks_1h),
    'Thursday': [''] * len(time_blocks_1h),
    'Friday': [''] * len(time_blocks_1h),
    'Saturday': [''] * len(time_blocks_1h),
    'Sunday': [''] * len(time_blocks_1h),
}

# Define tasks for each attention grade
tasks = {
    'LOW': [],
    'MEDIUM': [],
    'HIGH': []
}

@app.route('/')
def index():
    # Determine the current day to highlight
    current_day = datetime.datetime.now().strftime("%A")
    return render_template('index.html', 
                           time_blocks=time_blocks_1h, 
                           schedule_data=schedule_data, 
                           attention_grades=attention_grades, 
                           tasks=tasks,
                           current_day=current_day,
                           show_weekend=False,
                           enumerate=enumerate)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        grade = request.form.get('attention_grade')
        task = request.form.get('task')
        if grade in tasks:
            tasks[grade].append(task)
        return redirect(url_for('index'))
    return render_template('add_task.html', attention_grades=attention_grades)

@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    # Update the schedule based on the form data
    day = request.form.get('day')
    time_slot = int(request.form.get('time_slot'))
    task = request.form.get('task')
    schedule_data[day][time_slot] = task
    return redirect(url_for('index'))

@app.route('/toggle_time_blocks')
def toggle_time_blocks():
    # Toggle between 1-hour and 30-minute time blocks
    use_30_min_blocks = request.args.get('use_30_min_blocks', 'false') == 'true'
    time_blocks = time_blocks_30m if use_30_min_blocks else time_blocks_1h
    current_day = datetime.datetime.now().strftime("%A")
    return render_template('index.html', 
                           time_blocks=time_blocks, 
                           schedule_data=schedule_data, 
                           attention_grades=attention_grades, 
                           tasks=tasks,
                           current_day=current_day,
                           show_weekend=False,
                           enumerate=enumerate)

@app.route('/toggle_weekend', methods=['GET'])
def toggle_weekend():
    # Toggle weekend visibility
    show_weekend = request.args.get('show_weekend', 'false') == 'true'
    current_day = datetime.datetime.now().strftime("%A")
    return render_template('index.html', 
                           time_blocks=time_blocks_1h, 
                           schedule_data=schedule_data, 
                           attention_grades=attention_grades, 
                           tasks=tasks,
                           current_day=current_day,
                           show_weekend=show_weekend,
                           enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)
