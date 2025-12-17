from CommandNode import CommandNode

class CommandGameField(CommandNode):
    def __init__(self, name, value_type, action, line, char_pos, cmd_path):
        super().__init__(name, value_type, action, line, char_pos, cmd_path)

    def _not_empty_check(self):
        """Проверка, что значение не пустое."""
        if not self._action:
            self._log_error(f"Команда '{self._name}' не может быть пустой.")
            return False
        return True

    def _each_size_is_int(self):
        """Проверка, что каждое значение - число."""
        result = True
        if self._not_empty_check():
            for one_size in self._action:
                if not isinstance(one_size, int):
                    self._log_error(f"Тип поля \"размер\" (= \"{one_size}\") должен быть числом, получен '{type(one_size)}'.")
                    result = False
        return result

    def Errors(self):
        """Реализация метода Errors с локальными проверками."""
        if self._type_check():
            if self._not_empty_check():  # Проверка на пустоту
                self._each_size_is_int()  # Проверка типа каждого размера (должен быть int)
        return self.get_errors()
