import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from models import Task
from scheduler import interval_schedule
from storage import save_tasks, load_tasks

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Inteligente")
        self.tasks = load_tasks()
        self.scheduled_tasks = []
        self.editing_index = None 

        self.setup_ui()
        self.update_tasks_list()
        self.update_scheduled_list()

    def setup_ui(self):
        input_frame = ttk.LabelFrame(self.root, text="Nova Tarefa", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Título:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1)

        ttk.Label(input_frame, text="Início (YYYY-MM-DD HH:MM):").grid(row=1, column=0, sticky="w")
        self.start_entry = ttk.Entry(input_frame, width=30)
        self.start_entry.grid(row=1, column=1)
        self.start_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))

        ttk.Label(input_frame, text="Término (YYYY-MM-DD HH:MM):").grid(row=2, column=0, sticky="w")
        self.end_entry = ttk.Entry(input_frame, width=30)
        self.end_entry.grid(row=2, column=1)
        self.end_entry.insert(0, (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"))

        ttk.Label(input_frame, text="Prioridade (1-5):").grid(row=3, column=0, sticky="w")
        self.priority_combobox = ttk.Combobox(input_frame, values=[1, 2, 3, 4, 5], width=5)
        self.priority_combobox.grid(row=3, column=1, sticky="w")
        self.priority_combobox.set(3)

        ttk.Button(input_frame, text="Adicionar", command=self.add_task).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(input_frame, text="Otimizar Agenda", command=self.schedule_tasks).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(input_frame, text="Excluir Selecionada", command=self.delete_task).grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(input_frame, text="Editar Selecionada", command=self.edit_task).grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(input_frame, text="Salvar Edição", command=self.save_edited_task).grid(row=8, column=0, columnspan=2, pady=5)

        self.tasks_frame = ttk.LabelFrame(self.root, text="Todas as Tarefas", padding=10)
        self.tasks_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tree = ttk.Treeview(self.tasks_frame, columns=("title", "start", "end", "priority"), show="headings")
        for col in ("title", "start", "end", "priority"):
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True)

        self.scheduled_frame = ttk.LabelFrame(self.root, text="Tarefas Agendadas (Otimizadas)", padding=10)
        self.scheduled_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.scheduled_tree = ttk.Treeview(self.scheduled_frame, columns=("title", "start", "end", "priority"), show="headings")
        for col in ("title", "start", "end", "priority"):
            self.scheduled_tree.heading(col, text=col.capitalize())
        self.scheduled_tree.pack(fill="both", expand=True)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

    def add_task(self):
        title = self.title_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        priority = int(self.priority_combobox.get())
        try:
            task = Task(title, start, end, priority)
            self.tasks.append(task)
            save_tasks(self.tasks)
            self.update_tasks_list()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para excluir.")
            return
        idx = self.tree.index(selected[0])
        del self.tasks[idx]
        save_tasks(self.tasks)
        self.update_tasks_list()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para editar.")
            return

        idx = self.tree.index(selected[0])
        task = self.tasks[idx]

        self.editing_index = idx
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, task.title)

        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, task.start_time.strftime("%Y-%m-%d %H:%M"))

        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, task.end_time.strftime("%Y-%m-%d %H:%M"))

        self.priority_combobox.set(task.priority)

    def save_edited_task(self):
        if self.editing_index is None:
            messagebox.showwarning("Aviso", "Nenhuma tarefa em edição.")
            return

        try:
            title = self.title_entry.get()
            start = self.start_entry.get()
            end = self.end_entry.get()
            priority = int(self.priority_combobox.get())

            edited_task = Task(title, start, end, priority)
            self.tasks[self.editing_index] = edited_task
            save_tasks(self.tasks)
            self.update_tasks_list()
            self.editing_index = None
            messagebox.showinfo("Sucesso", "Tarefa editada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update_tasks_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in sorted(self.tasks, key=lambda t: t.start_time):
            self.tree.insert("", "end", values=(
                task.title,
                task.start_time.strftime("%Y-%m-%d %H:%M"),
                task.end_time.strftime("%Y-%m-%d %H:%M"),
                task.priority
            ))

    def update_scheduled_list(self):
        for item in self.scheduled_tree.get_children():
            self.scheduled_tree.delete(item)
        for task in sorted(self.scheduled_tasks, key=lambda t: t.start_time):
            self.scheduled_tree.insert("", "end", values=(
                task.title,
                task.start_time.strftime("%Y-%m-%d %H:%M"),
                task.end_time.strftime("%Y-%m-%d %H:%M"),
                task.priority
            ))

    def schedule_tasks(self):
        self.scheduled_tasks = interval_schedule(self.tasks)
        self.update_scheduled_list()
        messagebox.showinfo("Sucesso", f"{len(self.scheduled_tasks)} tarefas agendadas com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
    