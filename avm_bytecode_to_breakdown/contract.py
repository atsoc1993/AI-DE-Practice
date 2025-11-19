from algopy import ARC4Contract, log, Bytes
from algopy.arc4 import abimethod

class TestContract(ARC4Contract):
    def __init__(self) -> None:
        self.zxzxzxzxzxzx= Bytes(b'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
        self.zxzxzxzxzxzxzxzxzx = Bytes(b'AAAAAAAAAAAAAAAAAAAA')
        self.zxzxzxzxzxzxzxzxzxzxzxzx = Bytes(b'AAAAAAAAAAAAAAAAAAAA')
        self.zxzxzxzxzxzxzxzxzxzxzxxzzxxzzx = Bytes(b'AAAAAAAAAAAAAAAAAAAA')
        self.zxzxzxzxzxzxzxzxzxzxzxxzxzxzzzxz = Bytes(b'AAAAAAAAAAAAAAAAAAAA')
        self.zxzxzxzxzxzxzxzxzxxzxxzxzxzzzxzxzxxzxzxzzzxz = Bytes(b'AAAAAAAAAAAAAAAAAAAA')
        self.zxzxzxzxzxzxzxzxzxxzxxzxzxzzzxzxzxxzxzxzzzxzxzxxzxzxzzzxz = Bytes(b'AAAAAAAAAAAAAAAAAAAA')
    
    @abimethod
    def test1(self) -> None:
        log("Test")
        
    @abimethod
    def test2(self) -> None:
        log("Test")

    @abimethod
    def test3(self) -> None:
        log("Test")

    @abimethod
    def test4(self) -> None:
        log("Test")