## Example Output from 2_deconstruct_teal.py

*Prints the Teal Program*

```
#pragma version 11
intcblock 1
bytecblock 0x4141414141414141414141414141414141414141 0x54657374
txn ApplicationID
bnz label1
pushbytess 0x7a787a787a787a787a787a78 0x43434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343
app_global_put
pushbytes 0x7a787a787a787a787a787a787a787a787a78 // "zxzxzxzxzxzxzxzxzx"
bytec_0 // "AAAAAAAAAAAAAAAAAAAA"
app_global_put
pushbytes 0x7a787a787a787a787a787a787a787a787a787a787a787a78 // "zxzxzxzxzxzxzxzxzxzxzxzx"
bytec_0 // "AAAAAAAAAAAAAAAAAAAA"
app_global_put
pushbytes 0x7a787a787a787a787a787a787a787a787a787a787a78787a7a78787a7a78 // "zxzxzxzxzxzxzxzxzxzxzxxzzxxzzx"
bytec_0 // "AAAAAAAAAAAAAAAAAAAA"
app_global_put
pushbytes 0x7a787a787a787a787a787a787a787a787a787a787a78787a787a787a7a7a787a // addr PJ4HU6D2PB5HQ6TYPJ4HU6D2PB5HQ6TYPJ4HQ6TYPJ4HU6T2PB5NOSNYDE
bytec_0 // "AAAAAAAAAAAAAAAAAAAA"
app_global_put
pushbytes 0x7a787a787a787a787a787a787a787a787a78787a78787a787a787a7a7a787a787a78787a787a787a7a7a787a // "zxzxzxzxzxzxzxzxzxxzxxzxzxzzzxzxzxxzxzxzzzxz"
bytec_0 // "AAAAAAAAAAAAAAAAAAAA"
app_global_put
pushbytes 0x7a787a787a787a787a787a787a787a787a78787a78787a787a787a7a7a787a787a78787a787a787a7a7a787a787a78787a787a787a7a7a787a // "zxzxzxzxzxzxzxzxzxxzxxzxzxzzzxzxzxxzxzxzzzxzxzxxzxzxzzzxz"
bytec_0 // "AAAAAAAAAAAAAAAAAAAA"
app_global_put
label1:
txn NumAppArgs
bz label2
txn OnCompletion
!
assert
txn ApplicationID
assert
pushbytess 0x20254f91 0xf1908524 0xdf920f37 0x3d46345c
txna ApplicationArgs 0
match label3 label4 label5 label6
err
label6:
bytec_1 // "Test"
log
intc_0 // 1
return
label5:
bytec_1 // "Test"
log
intc_0 // 1
return
label4:
bytec_1 // "Test"
log
intc_0 // 1
return
label3:
bytec_1 // "Test"
log
intc_0 // 1
return
label2:
txn OnCompletion
!
txn ApplicationID
!
&&
assert
intc_0 // 1
return
```

*Detects log opcodes and value on the stack when logging*
```
Found log opcode, logs 0x54657374
Found log opcode, logs 0x54657374
Found log opcode, logs 0x54657374
Found log opcode, logs 0x54657374
```

*General Information:*
- *AVM Version*
- *Methods Available*
- *Method/Label Mapping*
- *Global state initial keys & values on deployment*
- *Bytecblock constants (Bytecblocks are used to optimize if a value is used more than once anywhere throughout the contract logic, and these constants are references with "bytec_0", "bytec_1", "bytec_2", "bytec_3" or "bytec N" opcodes)*
```
App Data:
App Version: 11
Methods: ['0x20254f91', '0xf1908524', '0xdf920f37', '0x3d46345c']
Method Label Mapping: {'label3': '0x20254f91', 'label4': '0xf1908524', 'label5': '0xdf920f37', 'label6': '0x3d46345c'}
Global States: {'0x7a787a787a787a787a787a78': '0x43434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343434343', '0x7a787a787a787a787a787a787a787a787a78': '0x4141414141414141414141414141414141414141', '0x7a787a787a787a787a787a787a787a787a787a787a787a78': '0x4141414141414141414141414141414141414141', '0x7a787a787a787a787a787a787a787a787a787a787a78787a7a78787a7a78': '0x4141414141414141414141414141414141414141', '0x7a787a787a787a787a787a787a787a787a787a787a78787a787a787a7a7a787a': '0x4141414141414141414141414141414141414141', '0x7a787a787a787a787a787a787a787a787a78787a78787a787a787a7a7a787a787a78787a787a787a7a7a787a': '0x4141414141414141414141414141414141414141', '0x7a787a787a787a787a787a787a787a787a78787a78787a787a787a7a7a787a787a78787a787a787a7a7a787a787a78787a787a787a7a7a787a': '0x4141414141414141414141414141414141414141'}
Bytecblock Constants: {0: '0x4141414141414141414141414141414141414141', 1: '0x54657374'}
```