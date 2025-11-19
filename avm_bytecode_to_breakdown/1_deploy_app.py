from algosdk.account import generate_account
from algokit_utils import SigningAccount, AlgorandClient
from contract_files.TestClient import TestContractFactory
from dotenv import load_dotenv, set_key
import os

load_dotenv()
# sk, pk = generate_account()
# set_key('.env', 'SK', sk)
# set_key('.env', 'PK', pk)

# Fund account via https://bank.testnet.algorand.network/

sk = os.getenv('SK')
pk = os.getenv('PK')
signing_account = SigningAccount(
    private_key=sk,
    address=pk
)

test_factory = TestContractFactory(
    algorand=AlgorandClient.testnet(),
    default_sender=pk,
    default_signer=signing_account.signer,
)


app_client, deploy_response = test_factory.send.create.bare()

set_key('.env', 'app_id', str(app_client.app_id))