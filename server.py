import Pyro5.api
import sqlite3
import threading

@Pyro5.api.expose
class TransactionManager(object):
    def __init__(self):
        # Inicializa a conexão com o banco de dados
        self.conn = sqlite3.connect('example.db', check_same_thread=False)
        # Inicializa um bloqueio para controle de concorrência
        self.lock = threading.Lock()

    def transfer_funds(self, from_account, to_account, amount):
        # Utiliza o bloqueio para garantir que a transação seja atômica
        with self.lock:
            print(f"Iniciando transferência: {amount} de {from_account} para {to_account}")
            try:
                # Começa uma transação com bloqueio imediato
                self.conn.execute('BEGIN IMMEDIATE')
                cursor = self.conn.cursor()

                # Verifica o saldo da conta de origem
                cursor.execute('SELECT balance FROM accounts WHERE name = ?', (from_account,))
                from_balance = cursor.fetchone()
                if from_balance is None:
                    raise ValueError(f"Conta {from_account} não encontrada")
                from_balance = from_balance[0]

                # Verifica o saldo da conta de destino
                cursor.execute('SELECT balance FROM accounts WHERE name = ?', (to_account,))
                to_balance = cursor.fetchone()
                if to_balance is None:
                    raise ValueError(f"Conta {to_account} não encontrada")
                to_balance = to_balance[0]

                # Verifica se há saldo suficiente para a transferência
                if from_balance < amount:
                    raise ValueError("Saldo insuficiente")

                # Atualiza os saldos das contas
                cursor.execute('UPDATE accounts SET balance = balance - ? WHERE name = ?', (amount, from_account))
                cursor.execute('UPDATE accounts SET balance = balance + ? WHERE name = ?', (amount, to_account))

                # Confirma a transação
                self.conn.commit()

                # Exibe os novos saldos
                cursor.execute('SELECT balance FROM accounts WHERE name = ?', (from_account,))
                new_from_balance = cursor.fetchone()[0]
                cursor.execute('SELECT balance FROM accounts WHERE name = ?', (to_account,))
                new_to_balance = cursor.fetchone()[0]
                print(f"Novo saldo de {from_account}: {new_from_balance}")
                print(f"Novo saldo de {to_account}: {new_to_balance}")

            except Exception as e:
                # Reverte a transação em caso de erro
                self.conn.rollback()
                print(f"Erro na transferência: {e}")
                raise e
            finally:
                cursor.close()

    def simulate_concurrent_transfers(self, from_account, to_account, amount, num_transfers):
        # Cria uma lista para armazenar os threads
        threads = []
        for _ in range(num_transfers):
            # Cria um thread para cada transferência
            t = threading.Thread(target=self.transfer_funds, args=(from_account, to_account, amount))
            threads.append(t)
            t.start()

        # Aguarda a conclusão de todos os threads
        for t in threads:
            t.join()

        print("Simulação de transferências concorrentes concluída.")

def main():
    print("Iniciando servidor PYRO...")
    # Inicia o servidor Pyro5
    Pyro5.api.Daemon.serveSimple(
        {
            TransactionManager: "example.transaction_manager"
        },
        host="localhost",
        port=9090,
        ns=False
    )

if __name__ == "__main__":
    main()
