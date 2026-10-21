import re


def tokenize(text):
    pattern = r'\d+(?:\.\d*)?|\.\d+|[+\-*/()]'
    tokens = re.findall(pattern, text)

    if ''.join(tokens).replace(' ', '') != text.replace(' ', ''):
        raise ValueError("Недопустимые символы в выражении")

    return tokens


def calculate(text):
    tokens = tokenize(text)
    pos = 0

    def expression():
        nonlocal pos
        result = term()

        while pos < len(tokens) and tokens[pos] in ('+', '-'):
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
                    raise ZeroDivisionError("Деление на ноль")
                result /= right

        return result

    def factor():
        nonlocal pos

        if pos >= len(tokens):
            raise ValueError("Неожиданный конец выражения")

        token = tokens[pos]

        if token == '-':
            pos += 1
            return -factor()

        if token == '+':
            pos += 1
            return factor()

        if token == '(':
            pos += 1
            result = expression()

            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Не хватает закрывающей скобки")

            pos += 1
            return result

        if token == ')':
            raise ValueError("Лишняя закрывающая скобка")

        if re.fullmatch(r'\d+(?:\.\d*)?|\.\d+', token):
            pos += 1
            return float(token)

        raise ValueError("Некорректное выражение")

    result = expression()

    if pos != len(tokens):
        raise ValueError("Некорректное выражение")

    return result


try:
    text = input("Введите выражение: ")
    result = calculate(text)
    print("Результат:", result)

except (ValueError, ZeroDivisionError) as error:
    print("Ошибка:", error)
