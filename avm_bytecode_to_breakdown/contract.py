from algopy import ARC4Contract, log
from algopy.arc4 import abimethod

class TestContract(ARC4Contract):
    def __init__(self) -> None:
        pass
    
    @abimethod
    def test(self) -> None:
        log("Test")