from abc import ABC, abstractmethod
from Errors import ValidationError

class CommandNode(ABC):
    def __init__(self, name, value_type, action, line, char_pos, command_path, file):
        self._name = name  # Имя команды (ключ в JSON)
        self._value_type = value_type  # Ожидаемый тип значения (list, dict, int, str и т.д.)
        self._action = action  # Значение команды (то, что после ":")
        self._line = line  # Номер строки
        self._char_pos = char_pos  # Позиция символа
        self._command_path = command_path  # Путь к команде
        self._file = file  # Файл, откуда взята команда
        self._errors = []  # Список для хранения ошибок

    @abstractmethod
    def Errors(self):
        """Абстрактный метод для проверки ошибок. Должен быть реализован в наследниках."""
        pass

    def _collect_error_chain(self):
        """Собирает цепочку контекстов ошибок от корня до текущего узла.
        Сейчас нет явной структуры родителей, поэтому возвращаем только текущий узел.
        В будущем можно расширить, чтобы трассировать реальные вложенные файлы/контексты.
        """
        return [(self._file, self._line, self._char_pos, self._name)]

    def _format_error_line(self, file, line, pos, name, message):
        file_str = file if file is not None else "<неизвестен>"
        line_str = str(line) if line is not None else "<не найдена>"
        pos_str = str(pos) if pos is not None else "<не найдена>"
        return f"-Файл: \'{file_str}\'\n-Команда: {name}\n-Строка: {line_str}\n-Позиция: {pos_str}\n-Текст ошибки: {message}"

    def _log_error(self, message):
        """Создаёт ValidationError с информацией о местоположении и добавляет
        отформатированные строки в список ошибок узла.

        Логика для вычисления строки и позиции команды заимствована из
        `CommandPath.get_line_and_pos()`. Для вычисления позиции параметра
        используется модифицированный поиск элемента в карте скобок
        (аналог `find_command_element`). Метод не содержит блоков
        try/except и гарантирует числовые значения полей `param_substring`
        и `param_subposition` (по умолчанию 1 и 0 соответственно).
        """
        # Формируем структурированный путь (если есть CommandPath)
        
        chain = self._collect_error_chain()
        formatted_lines = ["Ошибка синтаксиса!" ]
        for file, line, pos, name in chain:
            formatted_lines.append(self._format_error_line(file, line, pos, name, message))
        formatted_lines.append("")  # пустая строка для разделения
        self._errors.extend(formatted_lines)
        
        """
        path = None
        if hasattr(self, '_command_path') and self._command_path is not None and hasattr(self._command_path, '_get_path'):
            p = self._command_path._get_path()
            if isinstance(p, list):
                path = p + [self._name]

        # Вычисляем строку и позицию команды через CommandPath.get_line_and_pos()
        line = None
        pos = None
        if hasattr(self, '_command_path') and self._command_path is not None and hasattr(self._command_path, 'get_line_and_pos'):
            lp = self._command_path.get_line_and_pos()
            if isinstance(lp, tuple) and len(lp) == 2:
                line, pos = lp

        # Если CommandPath не дал результат — используем значения из узла
        # НЕТ! Пусть вернет None для <не найдена>
        # В продакшне это не должно случаться, т.к. CommandPath должен быть всегда
        # if line is None:
        #     line = self._line
        # if pos is None:
        #     pos = self._char_pos

        # Подстрока параметра: первое целочисленное звено пути (1-based). По умолчанию 1.
        # ОШИБКА!!! может быть не только int!!!
        # Скорее я бы сказал, здесь нудо пропустить константу лексем
        param_substring = 1
        if isinstance(path, list):
            for step in path:
                if isinstance(step, int):
                    param_substring = int(step) + 1
                    break

        # Подпозиция параметра: ищем в карте скобок элемент по полному пути.
        # Если поиск даёт позицию (int) — используем её, иначе используем pos или 0.
        param_subposition = 0
        if isinstance(path, list) and hasattr(self._command_path, 'get_bracket_map') and hasattr(self._command_path, 'find_command_element'):
            bracket_map = self._command_path.get_bracket_map()
            if isinstance(bracket_map, list):
                reserved = getattr(self._command_path, '_commands', [])
                element = self._command_path.find_command_element(path, bracket_map, reserved)
                if isinstance(element, list) and len(element) >= 4 and isinstance(element[3], int):
                    param_subposition = int(element[3])
                    # print(param_subposition)

        # Если всё ещё не число — используем pos (если число) либо 0
        # В ПРОДАЖНЕ ЭТО НЕ ДОЛЖНО СЛУЧАТЬСЯ!!!
        if not isinstance(param_subposition, int):
            if isinstance(pos, int):
                param_subposition = int(pos)
            else:
                param_subposition = 0

        # Создаём ValidationError и добавляем его строки
        val_err = ValidationError(
            message,
            path=path,
            file=self._file,
            line=line,
            char_pos=pos,
            param_substring=param_substring,
            param_subposition=param_subposition,
            command=self._name,
        )
        self._errors.extend(val_err.format_lines())
        """
    def _type_check(self):
        """Проверка, соответствует ли тип значения ожидаемому."""
        if not isinstance(self._action, self._value_type):
            self._log_error(f"Ожидался тип команды {self._name} = {self._value_type}, получен {type(self._action)}.")
            return False
        return True

    def get_errors(self):
        """Возвращает список ошибок."""
        return self._errors
