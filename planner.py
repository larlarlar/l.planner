from questionary import select, text, confirm
import sys

class Task:
    def __init__(self, title):  # Исправлено: __init__ вместо init
        self.title = title
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __repr__(self):  # Исправлено: __repr__ вместо repr
        status = "✅" if self.completed else "❌"
        return f"[{status}] {self.title}"


class Planner:
    def __init__(self):  # Исправлено: __init__ вместо init
        self.tasks = []

    def add_task(self, title):
        task = Task(title)
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            return True
        return False

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            return True
        return False


def display_tasks(planner):
    print("\n--- Your Tasks ---")
    if not planner.tasks:
        print("No tasks yet!")
    else:
        for idx, task in enumerate(planner.list_tasks()):
            print(f"{idx + 1}. {task}")


def main():
    planner = Planner()

    while True:
        display_tasks(planner)

        choice = select(
            "Choose an action:",
            choices=[
                "Add a task",
                "Mark a task as completed",
                "Delete a task",
                "Exit"
            ]
        ).ask()

        if choice == "Add a task":
            task_title = text("Enter the task title:").ask()
            if task_title:
                planner.add_task(task_title)

        elif choice == "Mark a task as completed":
            if not planner.tasks:
                print("No tasks to mark as completed!")
                continue
                
            task_choices = [str(task) for task in planner.tasks]
            selected_task = select(
                "Which task did you complete?",
                choices=task_choices
            ).ask()
            
            index = planner.tasks.index([task for task in planner.tasks if str(task) == selected_task][0])
            planner.complete_task(index)

        elif choice == "Delete a task":
            if not planner.tasks:
                print("No tasks to delete!")
                continue
                
            task_choices = [str(task) for task in planner.tasks]
            selected_task = select(
                "Which task would you like to delete?",
                choices=task_choices
            ).ask()
            
            index = planner.tasks.index([task for task in planner.tasks if str(task) == selected_task][0])
            if confirm(f"Are you sure you want to delete '{selected_task}'?").ask():
                planner.delete_task(index)

        elif choice == "Exit":
            if confirm("Are you sure you want to exit?").ask():
                print("Goodbye!")
                sys.exit()


if __name__ == "__main__":  # Исправлено: __name__ и __main__
    main()
    