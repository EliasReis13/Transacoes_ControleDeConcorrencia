import Pyro5.api

def main():
    # Define o URI do gerenciador de transações no servidor Pyro5
    uri = "PYRO:example.transaction_manager@localhost:9090"
    transaction_manager = Pyro5.api.Proxy(uri)

    # Define as contas e o valor para a simulação de transferência
    from_account = "João"
    to_account = "Maria"
    amount = 1000.0
    num_transfers = 5  # Número de transferências concorrentes

    # Chama a função de simulação de transferências concorrentes
    transaction_manager.simulate_concurrent_transfers(from_account, to_account, amount, num_transfers)

if __name__ == "__main__":
    main()
