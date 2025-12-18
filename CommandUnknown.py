from CommandNode import CommandNode


class CommandUnknown(CommandNode):
    def __init__(self, name, value_type, action, line, char_pos, cmd_path, file):
        # Независимо от переданного name, храним в _name значение 'UnknownCommand'
        self._action = action
        super().__init__('UnknownCommand', value_type, action, line, char_pos, cmd_path, file)

    def Errors(self):
        """Логируем неизвестную команду и возвращаем ошибки."""
        self._log_error(f"Неизвестная команда '{self._action}'.")
        return self.get_errors()
