import json
from general import data, print_status

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


class TodoTab(Container):
    def __init__(self):
        super().__init__()
        self.todo_list = data.get("Todo", {})


    def compose(self) -> ComposeResult:
        if not self.todo_list:
            yield Label("Task list is empty!", id="empty-label")
        else:
            for i, todo_name in enumerate(self.todo_list):
                yield Checkbox(todo_name, classes="tasks", id=f"task{i}")

        yield Static("", id="output")

        inp = Input(
            placeholder="enter new task",
            id="task-input"
        )
        inp.display = False
        yield inp


    @on(Input.Submitted, "#task-input")
    def on_input_submitted(self, event: Input.Submitted):
        output = self.query_one("#output", Static)

        if event.value in self.todo_list:
            output.update(print_status(False, "add", "Task", "exist"))
            return

        self.todo_list[event.value] = False
        output.update(print_status(True, "add", "Task"))

        event.input.value = ""
        event.input.display = False


    def show_add_input(self):
        inp = self.query_one("#task-input", Input)
        inp.display = True
        inp.focus()


    def reload_tasks(self):
    	pass


class MApp(App):
    BINDINGS = [
        Binding("ctrl+q", "quit"),
        Binding("ctrl+a", "add_task"),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Tasks", id="todo-tab"):
                yield TodoTab()

    def action_quit(self):
        self.exit()

    def action_add_task(self):
        todo_tab = self.query_one(TodoTab)
        todo_tab.show_add_input()


if __name__ == "__main__":
    MApp().run()