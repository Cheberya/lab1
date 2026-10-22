import math
 
 
def tokenize(text):
    tokens = []
    i = 0
    n = len(text)
 
    while i < n:
        ch = text[i]
 
        if ch.isspace():
            i += 1
        elif ch in '0123456789.':
            start = i
            while i < n and text[i] in '0123456789.':
                i += 1
            tokens.append(text[start:i])
        elif ch.isalpha():
            start = i
            while i < n and text[i].isalnum():
                i += 1
            tokens.append(text[start:i])
        elif ch in '+-*/()':
            tokens.append(ch)
            i += 1
        elif ch == '>':
            # единственный поддерживаемый оператор сравнения - ">="
            if i + 1 < n and text[i + 1] == '=':
                tokens.append('>=')
                i += 2
            else:
                raise ValueError('Одиночный ">" не поддерживается, используйте ">="')
        else:
            raise ValueError(f'Недопустимый символ: {ch!r}')
 
    return tokens
 
 
def calculate(text):
    tokens = tokenize(text)
    pos = 0
 
    def comparison():
        nonlocal pos
        result = expression()
 
        while pos < len(tokens) and tokens[pos] == '>=':
            pos += 1
            right = expression()
            # isclose учитывает погрешность float: 0.1 + 0.2 >= 0.3 -> 1.0
            if result >= right or math.isclose(result, right, rel_tol=1e-9, abs_tol=1e-12):
                result = 1.0
            else:
                result = 0.0
 
        return result
 
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
            result = comparison()
 
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError('Не хватает закрывающей скобки')
 
            pos += 1
            return result
 
        if token == 'log10':
            pos += 1
 
            if pos >= len(tokens) or tokens[pos] != '(':
                raise ValueError('После log10 ожидается "("')
 
            pos += 1
            argument = comparison()
 
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError('Не хватает закрывающей скобки')
 
            pos += 1
 
            if argument <= 0:
                raise ValueError('log10(x) определён только при x > 0')
            return math.log10(argument)
 
        if token == ')':
            raise ValueError('Ожидалось число, а найдена ")"')
 
        if token[0].isalpha():
            raise ValueError(f'Неизвестная функция или имя: {token}')
 
        if token in ('*', '/', '>='):
            raise ValueError(f'Ожидалось число, а найден оператор "{token}"')
 
        try:
            result = float(token)
        except ValueError:
            raise ValueError(f'Некорректное число: {token}')
 
        pos += 1
        return result
 
    result = comparison()
 
    if pos != len(tokens):
        if tokens[pos] == ')':
            raise ValueError('Лишняя закрывающая скобка')
        raise ValueError('Некорректное выражение')
 
    if not math.isfinite(result):
        raise ValueError('Результат выходит за допустимый диапазон')
 
    return result
 
 
def main():
    try:
        text = input('Введите выражение: ')
        print('Результат:', calculate(text))
    except (ValueError, ZeroDivisionError) as error:
        print('Ошибка:', error)
    except RecursionError:
        print('Ошибка: слишком глубокая вложенность выражения')
 
 
if __name__ == '__main__':
    main()
