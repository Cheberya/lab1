def calculate(text):
    tokens = tokenize(text)
    pos = 0

    def expression():
        nonlocal pos
        result = term()

        while pos < len(tokens) and tokens[pos] in ('+', '-'):ы
            op = tokens[pos]
            pos += 1
            right = term()

            if op == '+':
                result += right
            else:
                result -= right

        return result

    def term():
        nonlocal pos
        result = factor()

        while pos < len(tokens) and tokens[pos] in ('*', '/'):
            op = tokens[pos]
            pos += 1
            right = factor()

            if op == '*':
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError('Деление на ноль')
                result /= right

        return result

    def factor():
        nonlocal pos

        if pos >= len(tokens):
            raise ValueError('Неожиданный конец выражения')

        token = tokens[pos]

        if token == '+':
            pos += 1
            return factor()

        if token == '-':
            pos += 1
            return -factor()

        if token == '(':
            pos += 1
            result = expression()

            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError('Не хватает закрывающей скобки')

            pos += 1
            return result

        if token == ')':
            raise ValueError('Лишняя закрывающая скобка')

        try:
            result = float(token)
        except ValueError:
            raise ValueError('Некорректное выражение')

        pos += 1
        return result

    result = expression()

    if pos != len(tokens):
        raise ValueError('Некорректное выражение')

    return result


try:
    text = input('Введите выражение: ')
    print('Результат:', calculate(text))
except (ValueError, ZeroDivisionError) as error:
    print('Ошибка:', error)
