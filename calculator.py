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


def validate_expression_components(ops, numbers):
    if len(ops) == 0 and len(numbers) > 1:
        print('Invalid expression')
        return False
    for op in ops:
        if op is False:
            print('Invalid expression')
            return False
    return True


while True:
    user_input = input()
    if validate_commands(user_input) is False:
        continue
    if user_input == '/help':
        print('The program can add and subtract numbers')
        continue
    if user_input == '/exit':
        print('Bye!')
        break
    nums = list()
    operators = list()
    for item in user_input.split():
        try:
            nums.append(int(item))
        except ValueError:
            operators.append(evaluate_operator(item))
    nums.reverse()
    operators.reverse()
    if validate_expression_components(operators, nums) is False:
        continue
    while len(nums) != 1:
        num_1 = nums.pop()
        num_2 = nums.pop()
        operator = operators.pop()
        if operator == '-':
            nums.append(subtract(num_1, num_2))
        if operator == '+':
            nums.append(add(num_1, num_2))
    print(nums[0])
