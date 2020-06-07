from io import StringIO
import tokenize
import re

user_vars = dict()
help_text = '''
The program solve expressions with (), +, -, * and /.
You can also store values in variables and use them in expression or get the variable value by typing its name.
'''


def tokenize_user_input(input_string):
    input_string = re.sub("\+\++", "+", input_string)
    input_string = re.sub("---", "-", input_string)
    input_string = re.sub("--+", "+", input_string)
    try:
        tokenized = [token[1] for token in tokenize.generate_tokens(StringIO(input_string).readline) if token[1]]
    except tokenize.TokenError:
        print('Invalid expression')
        return False
    return tokenized


def clean_tokenized_input(tokenized_user_input):
    clean_input = list()
    for item in tokenized_user_input:
        if is_number(item):
            clean_input.append(int(item))
        elif item.startswith('('):
            clean_input.append('(')
            clean_input.append(item[1:])
        elif item.endswith(')'):
            clean_input.append(item[:-1])
            clean_input.append(')')
        elif item.startswith(('+', '-', '*', '/')):
            clean_input.append(item)
        elif item in user_vars.keys():
            item = user_vars[item]
            clean_input.append(item)
    return clean_input


def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def validate_commands(string):
    commands = ['/help', '/exit']
    if string == '':
        return False
    if string.startswith('/') and string not in commands:
        print('Unknown command')
        return False
    return True


def validate_expression_stack(expression_stack):
    if len(expression_stack) < 2:
        print('Invalid expression')
        return False
    elif expression_stack.count('(') != expression_stack.count(')'):
        print('Invalid expression')
        return False
    return True


def validate_assignment_expression(contents):
    if not contents[0].isalpha():
        print('Invalid identifier')
        return False
    if len(contents) != 2:
        print('Invalid assignment')
        return False
    return True


def assign_user_variable(string):
    expression = string.replace(' ', '').split('=')
    try:
        expression[1] = int(expression[1])
    except ValueError:
        if expression[1] in user_vars.keys():
            expression[1] = user_vars[expression[1]]
        else:
            print('Invalid assignment')
            return False
    if not validate_assignment_expression(expression):
        return False
    else:
        assign_variable_value(expression, user_vars)
    return True


def assign_variable_value(string, var_storage):
    var_key = string[0]
    var_value = string[1]
    var_storage[var_key] = var_value


def convert_to_postfix(input_values):
    result = list()
    operator_stack = list()
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }
    for item in input_values:
        if is_number(item):
            result.append(int(item))
        elif item == '(':
            operator_stack.append(item)
        elif item == ')':
            while operator_stack[-1] != '(':
                result.append(operator_stack.pop())
            operator_stack.pop()
        elif item in precedence.keys():
            if len(operator_stack) == 0:
                operator_stack.append(item)
            else:
                while len(operator_stack) != 0 \
                        and operator_stack[-1] != '(' \
                        and precedence[operator_stack[-1]] >= precedence[item]:
                    result.append(operator_stack.pop())
                operator_stack.append(item)
    while len(operator_stack) > 0:
        result.append(operator_stack.pop())
    return result


def calculate(a, b, operator):
    temp_result = 'Calculation error'
    if operator == '-':
        temp_result = a - b
    elif operator == '+':
        temp_result = a + b
    elif operator == '*':
        temp_result = a * b
    elif operator == '/':
        temp_result = a / b
    return temp_result


def evaluate_expression(expression_stack):
    calculation_stack = list()
    for item in expression_stack:
        if isinstance(item, int):
            calculation_stack.append(item)
        elif item in ['+', '-', '*', '/']:
            num_1 = calculation_stack.pop()
            num_2 = calculation_stack.pop()
            calculation_stack.append(calculate(num_2, num_1, item))
    return calculation_stack[-1]


while True:
    user_input = input()
    if validate_commands(user_input) is False:
        continue
    elif user_input == '/help':
        print(help_text)
        continue
    elif user_input == '/exit':
        print('Bye!')
        break
    elif '=' in user_input:
        if assign_user_variable(user_input) is False:
            continue
        # print(user_vars)
    else:
        # convert input string to clean list of individual elements
        tokenized_input = tokenize_user_input(user_input)
        if tokenized_input is False:
            continue
        if len(tokenized_input) == 1 and tokenized_input[0] in user_vars.keys():
            print(user_vars[tokenized_input[0]])
            continue
        user_expression = clean_tokenized_input(tokenized_input)
        if user_expression is False:
            continue
        # convert to postfix
        postfix_stack = convert_to_postfix(user_expression)
        # validate expression
        if validate_expression_stack(postfix_stack):
            print(int(evaluate_expression(postfix_stack)))
