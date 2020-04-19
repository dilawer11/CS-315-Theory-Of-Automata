import os

tests = [
    {'exp_output': "STANDARD OUTPUT\n5.4 True 2", 'test_name': 'standard_output'},
    {'exp_output': "start\n1 2.5\nFalse 0\nend\nRedeclarationError", 'test_name': 'variables'},
    {'exp_output':"theoryofautomata\n3.5\n11.0\n0.25\nTrue\nVariables of type 'int' and 'string' cannot use operator '+'", 'test_name': 'expressions'},
    {'exp_output': 'Wear down jacket', 'test_name': 'if_else'}
]
def match(output, exp_output):
    output_split = output.split('\n')
    exp_output_split = exp_output.split('\n')
    if len(output_split) != len(exp_output_split):
        return 'FAILED: Length Match Error'
    else:
        for i in range(0, len(output_split)):
            if output_split[i].rstrip() != exp_output_split[i]:
                return 'FAILED: ' + f'Line {i} not matched'
    return 'PASSED'
def main():
    for testcase in tests:
        filePath = os.path.join('test_cases', testcase['test_name'] + '.txt')
        os.system(f'python3 interpreter.py {filePath} > a.out')
        output = None
        with open('a.out', 'r') as f:
            _, output = f.read().split('OUTPUT:\n')
        output = output.rstrip()
        status = match(output, testcase['exp_output'])
        print(f"Test Case {testcase['test_name']}: {status}")

if __name__ == "__main__":
    main()