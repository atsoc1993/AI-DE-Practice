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

fns = {
    'log': [-1]
}

method_logic_mapping = {}
for method in available_methods:
    logic_detected = []
    for i, line in enumerate(teal_split):
        if reverse_method_label_mapping[method] == line[:-1]:
            # print(line) #label start for a method
            next_line = None
            next_line_cursor = i
            while next_line != 'return':
                
                next_line_cursor += 1
                next_line = teal_split[next_line_cursor]
                if next_line in fns:
                    vars = []
                    for value in fns[next_line]:
                        fn_value = teal_split[next_line_cursor + value]
                        trimmed_fn_value = fn_value.split(' //')[0]
                        if 'bytec' in trimmed_fn_value:
                            trimmed_fn_value = constants[int(trimmed_fn_value[-1])]
                        vars.append(trimmed_fn_value)
                    method_logic_mapping[method] = f'Method ({reverse_method_label_mapping[method]}) logs {vars[0]} and returns'

print(f'App Data:')
print(f'App Version: {app_version}')
print(f'Methods: {available_methods}')
print(f'Method Label Mapping: {method_label_mapping}')
for method in reverse_method_label_mapping:
    print(method_logic_mapping[method])
print(f'Global States: {global_states}')
print(f'Bytecblock Constants: {constants}')

