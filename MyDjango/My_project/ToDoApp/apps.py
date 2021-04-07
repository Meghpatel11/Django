from django.apps import AppConfig


class TodoappConfig(AppConfig):
    name = 'ToDoApp'

    def ready(self):
        import ToDoApp.signals