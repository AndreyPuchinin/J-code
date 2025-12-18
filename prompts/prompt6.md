Допиши в Линкер функцию print_bracket_map, задача которой - определить тип корневого json-объекта, сформировать к нему parent_path и вызвать root_cmd_path.print_bracket_map(file_path)

Параметры функции:
-file_path

Зависимость parent_path от типа корневого json-объекта:
{'dict': ...} -> ['dict']
[] -> [0]
else -> None -> msg about error! (работа нашей функции print_bracket_map в этом случае не дойдет до вызова root_cmd_path.print_bracket_map(file_path) - будет сразу вывод ошибки о содержимом file_path и завершение функции print_bracket_map) 