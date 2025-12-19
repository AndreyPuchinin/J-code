from CommandNode import CommandNode

UNKNOWN_COMMAND_NAME = "UnknownCommand"

class CommandUnknown(CommandNode):
    def __init__(self, name, value_type, action, line, char_pos, cmd_path, file):
        # Независимо от переданного name, храним в _name значение 'UnknownCommand'
        self._action = action
        super().__init__(UNKNOWN_COMMAND_NAME, value_type, action, line, char_pos, cmd_path, file)

    def Errors(self):
        """Логируем неизвестную команду и возвращаем ошибки."""
        self._log_error(f"Неизвестная команда '{self._action}'.")
        return self.get_errors()
