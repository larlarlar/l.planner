from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import pickle
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Необходимо для сессий

class Task:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        status = "✅" if self.completed else "❌"
        return f"[{status}] {self.title} - {self.description}"


class Planner:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, description=""):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        return self.tasks

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_tasks()
            return True
        return False

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
            return True
        return False

    def get_task(self, index):
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None
    
    def save_tasks(self):
        with open('tasks.pkl', 'wb') as f:
            pickle.dump(self.tasks, f)
    
    def load_tasks(self):
        if os.path.exists('tasks.pkl'):
            with open('tasks.pkl', 'rb') as f:
                self.tasks = pickle.load(f)

planner = Planner()

@app.route('/')
def index():
    return render_template('index.html', tasks=planner.list_tasks())

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        planner.add_task(title, description)
    return redirect(url_for('index'))

@app.route('/complete/<int:index>')
def complete_task(index):
    if not planner.complete_task(index):
        return "Task not found", 404
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_task(index):
    if not planner.delete_task(index):
        return "Task not found", 404
    return redirect(url_for('index'))

@app.route('/details/<int:index>')
def task_details(index):
    task = planner.get_task(index)
    if task is None:
        return "Task not found", 404
    return render_template('details.html', task=task, index=index)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_task(index):
    task = planner.get_task(index)
    if task is None:
        return "Task not found", 404
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title:
            task.title = title
            task.description = description
            planner.save_tasks()
            return redirect(url_for('index'))
    
    return render_template('edit.html', task=task, index=index)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_task(index):
    task = planner.get_task(index)
    if task is None:
        return "Task not found", 404
    
    # Проверяем, завершена ли задача
    if task.completed:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title:
            task.title = title
            task.description = description
            planner.save_tasks()
            return redirect(url_for('index'))
    
    return render_template('edit.html', task=task, index=index)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_task(index):
    task = planner.get_task(index)
    if task is None:
        return "Task not found", 404
    
    if task.completed:
        # Добавим flash-сообщение (не забудьте импортировать flash из flask)
        flash("Cannot edit completed tasks", "error")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title:
            task.title = title
            task.description = description
            planner.save_tasks()
            return redirect(url_for('index'))
    
    return render_template('edit.html', task=task, index=index)