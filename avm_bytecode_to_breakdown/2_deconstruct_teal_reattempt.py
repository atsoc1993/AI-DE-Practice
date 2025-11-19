from algokit_utils import AlgorandClient
from dotenv import load_dotenv
from base64 import b64encode
import os


load_dotenv()

algorand = AlgorandClient.testnet()

app_id = int(os.getenv('app_id'))

approval_program_b64_encoded = algorand.app.get_by_id(app_id).approval_program
compiled_teal = algorand.client.algod.disassemble(program_bytes=approval_program_b64_encoded)['result']
print(compiled_teal)
teal_split: str = compiled_teal.split('\n')
version_line = teal_split[0]
app_version = version_line.split(' ')[-1]

available_methods = None
for i, line in enumerate(teal_split):
    if line == 'txna ApplicationArgs 0':
        available_methods = (teal_split[i - 1].split(' ')[1:])
        method_labels = teal_split[i + 1].split(' ')[1:]


method_label_mapping = {}
reverse_method_label_mapping = {}
if available_methods == None:
    print(f'Failed to find available Methods')
else:
    for method, label in zip(available_methods, method_labels):
        method_label_mapping[label] = method
        reverse_method_label_mapping[method] = label

constants = {}

constants_counter = 0
for i, line in enumerate(teal_split):
    if line.startswith('bytecblock'):
        bytecblock = line.split(' ')[1:]
        for constant_ref in bytecblock:
            constants[constants_counter] = constant_ref
            constants_counter += 1

global_states = {}

# passed_method_declarations = False
for i, line in enumerate(teal_split):
    if line == 'app_global_put':
        #remove potential comment lines...
        trimmed_teal_line = teal_split[i - 1].split(' //')[0]
        try:
            initial_state_key, initial_state_value = trimmed_teal_line.split(' ')[1:]
        except:
            initial_state_key = teal_split[i - 2].split(' //')[0].split(' ')[-1]
            bytec_pointer = teal_split[i - 1].split(' //')[0]
            initial_state_value = constants[int(bytec_pointer[-1])]
        

        global_states[initial_state_key] = initial_state_value

    if line == 'txna ApplicationArgs 0':
        break




def itob(var: str):
    return int(var).to_bytes(8, 'big')

var_type_modifiers = {
    'itob': itob
}

stack_modifiers = ['pushbytes', 'pushbytess', 'pushint', 'dup', 'bytec']

fns = {
    'log': 'prints'
}

method_logic_mapping = {}

current_label = ''

print(constants)
stack = None
for i, line in enumerate(teal_split):
    if line == 'return':
        print(line)
        print('\n')
        current_label = ''

    if current_label:
        print(line)
        if any([line.startswith(key) for key in stack_modifiers]):
            if line.startswith('bytec'):
                constant_cursor = line.split(' //')[0]
                constant_cursor = constant_cursor[-1]
                stack.append(constants[int(constant_cursor)])
            elif line.startswith('dup'):
                stack.append(stack[-1])
            else:
                stack.append(line.split(' ')[1])
            
            print(stack)
        elif any([key == line for key in var_type_modifiers]):
            stack[-1] = var_type_modifiers[line](stack[-1])

        elif any([key == line for key in fns]):
            statement = f'{fns[line]} {stack[-1]}'
            print(statement)
            method_logic_mapping[current_label].append(statement)
            stack.pop()


    if any(label == line[:-1] for label in method_label_mapping):
        print(f'\n{line}')
        stack = []
        current_label = line[:-1]
        method_logic_mapping[current_label] = []

print(f'App Data:')
print(f'App Version: {app_version}')
print(f'Methods: {available_methods}')
print(f'Method Label Mapping: {method_label_mapping}')
print(f'Method Logic:')
for method in method_label_mapping:
    print(f'- {method}')
    for logic in method_logic_mapping[method]:
        print(f'- - {logic}')
print(f'Global States: {global_states}')
print(f'Bytecblock Constants: {constants}')

