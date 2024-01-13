import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class ToDoList:
    def __init__(self, master, filename):
        self.master = master
        self.master.title("My To-Do List")
        self.filename = filename
        self.tasks = []
        self.load_tasks()

        self.task_var = tk.StringVar()
        self.task_entry = tk.Entry(self.master, textvariable=self.task_var, width=50)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.task_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, height=15, width=50)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = tk.Button(self.master, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10)

        self.complete_button = tk.Button(self.master, text="Mark as Completed", command=self.mark_completed)
        self.complete_button.grid(row=2, column=1, padx=10, pady=10)

        self.deadline_var = tk.StringVar()
        self.deadline_entry = tk.Entry(self.master, textvariable=self.deadline_var, width=20)
        self.deadline_entry.grid(row=3, column=0, padx=10, pady=10)

        self.set_deadline_button = tk.Button(self.master, text="Set Deadline", command=self.set_deadline)
        self.set_deadline_button.grid(row=3, column=1, padx=10, pady=10)

        self.save_button = tk.Button(self.master, text="Save Tasks", command=self.save_tasks)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.load_tasks_to_listbox()

    def add_task(self):
        task_text = self.task_var.get()
        if task_text:
            self.tasks.append({"task": task_text, "completed": False, "deadline": None, "subtasks": []})
            self.task_var.set("")
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks.pop(selected_index[0])
            self.load_tasks_to_listbox()

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]]["completed"] = True
            self.load_tasks_to_listbox()

    def set_deadline(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            deadline_text = self.deadline_var.get()
            try:
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d")
                self.tasks[selected_index[0]]["deadline"] = deadline.strftime("%Y-%m-%d")
                self.load_tasks_to_listbox()
            except ValueError:
                messagebox.showwarning("Warning", "Invalid deadline format. Use YYYY-MM-DD")

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                self.tasks = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            self.tasks = []

    def load_tasks_to_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_text = task["task"]
            if task["completed"]:
                task_text = "[Done] " + task_text
            if task["deadline"]:
                task_text += f" (Deadline: {task['deadline']})"
            self.task_listbox.insert(tk.END, task_text)

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file)

if __name__ == "__main__":
    root = tk.Tk()
    filename = "my_todo_list.json"
    todo_app = ToDoList(root, filename)
    root.mainloop()
