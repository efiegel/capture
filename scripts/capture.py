from capture import settings
from capture.vault import Vault

if __name__ == "__main__":
    text = input("add to vault: ")
    vault = Vault(settings.VAULT_DIRECTORY)
    vault.add(text)
