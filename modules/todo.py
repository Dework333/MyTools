import json
from general import data, print_status, print_warning

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import (
    Label,
    Checkbox,
    Static,
    Input,
    TabPane,
    TabbedContent,
)
from textual import on
from textual.binding import Binding
from textual.reactive import reactive



class TodoTab(Container):
    todo_list = reactive(dict, recompose = True)


    def __init__(self):
        super().__init__()
        self.todo_list = data.get("Todo", {})


    def add_task(self, task_name: str):
        output = self.query_one("#output", Static)

        if task_name in self.todo_list:
            output.update(print_status(False, "add", "Task", "exist"))
            return

        if task_name == 'all':
            output.update(print_status(False, "add", "Task", "incorrect"))
            return
        
        current_list = dict(self.todo_list)
        current_list[task_name] = False

        output.update(print_status(True, "add", "Task"))
        self.todo_list = current_list


    def delete_task(self, task_name: str):
        output = self.query_one("#output", Static)
        current_list = dict(self.todo_list)

        if task_name == 'all':
            output.update(print_warning())
            current_list.clear()

            output.update(print_status(True, 'delete', 'Task'))
            self.todo_list = current_list
            return

        if task_name not in current_list:
            output.update(print_status(False, "delete", "Task", "nexist"))
            return

        del current_list[task_name]

        output.update(print_status(True, 'delete', 'Task'))
        self.todo_list = current_list


    def done_task(self, task_name: str):
        output = self.query_one("#output", Static)
        current_list = dict(self.todo_list)

        if task_name == 'all':
            output.update(print_warning())
            for i in current_list:
                current_list[i] = True

            output.update(print_status(True, 'done', 'Task'))
            self.todo_list = current_list
            return

        if task_name not in current_list:
            output.update(print_status(False, 'done', 'Task', 'nexist'))
            return

        current_list[task_name] = True
        output.update(print_status(True, 'done', 'Task'))
        self.todo_list = current_list


    def undone_task(self, task_name: str):
        output = self.query_one("#output", Static)
        current_list = dict(self.todo_list)

        if task_name == 'all':
            output.update(print_warning())
            for i in current_list:
                cuurent_list[i] = False

            output.update(print_status(True, 'undone', 'Task'))
            self.todo_list = current_list
            return

        if task_name not in current_list:
            output.update(print_status(False, 'done', 'Task', 'nexist'))
            return

        current_list[task_name] = False
        output.update(print_status(True, 'done', 'Task'))
        self.todo_list = current_list


    command_list = {
            'add': add_task,
            'delete': delete_task,
            'del': delete_task,
            'done': done_task,
            'undone': undone_task,
        }


    def compose(self) -> ComposeResult:
        if not self.todo_list:
            yield Label("Task list is empty!", id = "empty-label")
        else:
            for i, todo_name in enumerate(self.todo_list):
                yield Checkbox(todo_name, classes = "tasks", id = f"task{i}")

        yield Static("", id = "output")

        inp = Input(placeholder = "enter command", id = "task-input")
        inp.display = False
        yield inp


    @on(Input.Submitted, "#task-input")
    def on_input_submitted(self, event: Input.Submitted):

        command = event.value.split(maxsplit = 1)

        if command[0] in self.command_list:
            self.command_list[command[0]](self, command[1])
        
        event.input.value = ""
        #event.input.display = False


    def show_add_input(self):
        inp = self.query_one("#task-input", Input)
        inp.display = not inp.display
        #inp.focus()



class MApp(App):
    BINDINGS = [
        Binding("ctrl+q", "quit"),
        Binding("ctrl+a", "add_task"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Tasks", id = "todo-tab"):
                yield TodoTab()

    def action_quit(self):
        self.exit()

    def action_add_task(self):
        todo_tab = self.query_one(TodoTab)
        todo_tab.show_add_input()


if __name__ == "__main__":
    MApp().run()