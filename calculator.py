user_vars = dict()


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def evaluate_operator(string):
    if string != len(string) * string[0]:
        return False
    if '-' in string and len(string) % 2 != 0:
        return '-'
    return '+'


def validate_commands(string):
    commands = ['/help', '/exit']
    if string == '':
        return False
    if string.startswith('/') and string not in commands:
        print('Unknown command')
        return False
    return True


def validate_expression_components(numbers, ops):
    if len(numbers) < 1:
        return False
    if len(ops) == 0 and len(numbers) > 1:
        print('Invalid expression')
        return False
    for op in ops:
        if op is False:
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


def assign_variable_value(string, var_storage):
    var_key = string[0]
    var_value = string[1]
    var_storage[var_key] = var_value


def create_num_and_operator_stacks(input_values, var_list):
    numbers = list()
    ops = list()
    operations = ['-', '+']
    for item in input_values.split():
        try:
            numbers.append(int(item))
        except ValueError:
            if item in var_list.keys():
                numbers.append(var_list[item])
            elif item.isalpha():
                print('Unknown variable')
            elif item in operations:
                ops.append(evaluate_operator(item))
    numbers.reverse()
    ops.reverse()
    return numbers, ops


def calculate(numbers, ops):
    while len(numbers) != 1:
        num_1 = numbers.pop()
        num_2 = numbers.pop()
        operator = ops.pop()
        if operator == '-':
            nums.append(subtract(num_1, num_2))
        if operator == '+':
            nums.append(add(num_1, num_2))
    print(nums[0])


while True:
    user_input = input()
    if validate_commands(user_input) is False:
        continue
    if user_input == '/help':
        print('The program can add and subtract numbers; you can also store values in variables')
        continue
    if user_input == '/exit':
        print('Bye!')
        break
    if '=' in user_input:
        expression = user_input.replace(' ', '').split('=')
        try:
            expression[1] = int(expression[1])
        except ValueError:
            if expression[1] in user_vars.keys():
                expression[1] = user_vars[expression[1]]
            else:
                print('Invalid assignment')
                continue
        if not validate_assignment_expression(expression):
            continue
        else:
            assign_variable_value(expression, user_vars)
    else:
        nums, operators = create_num_and_operator_stacks(user_input, user_vars)
        if validate_expression_components(nums, operators):
            calculate(nums, operators)
