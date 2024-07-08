import tkinter as tk
from tkinter import messagebox
import Pyro5.api

class TransferApp:
    def __init__(self, master):
        self.master = master
        master.title("Transferência de Fundos")

        # Define o URI do servidor Pyro5
        self.uri = "PYRO:example.transaction_manager@localhost:9090"
        # Cria um proxy para o gerenciador de transações
        self.transaction_manager = Pyro5.api.Proxy(self.uri)

        # Cria e posiciona os widgets da interface gráfica
        self.label_from = tk.Label(master, text="De (Conta):")
        self.label_from.grid(row=0, column=0)

        self.entry_from = tk.Entry(master)
        self.entry_from.grid(row=0, column=1)

        self.label_to = tk.Label(master, text="Para (Conta):")
        self.label_to.grid(row=1, column=0)

        self.entry_to = tk.Entry(master)
        self.entry_to.grid(row=1, column=1)

        self.label_amount = tk.Label(master, text="Quantia:")
        self.label_amount.grid(row=2, column=0)

        self.entry_amount = tk.Entry(master)
        self.entry_amount.grid(row=2, column=1)

        self.transfer_button = tk.Button(master, text="Transferir", command=self.transfer_funds)
        self.transfer_button.grid(row=3, column=0, columnspan=2)

    def transfer_funds(self):
        # Obtém os valores inseridos pelo usuário
        from_account = self.entry_from.get()
        to_account = self.entry_to.get()
        amount = self.entry_amount.get()

        try:
            # Converte o valor para float
            amount = float(amount)
            # Chama o método remoto para transferir fundos
            self.transaction_manager.transfer_funds(from_account, to_account, amount)
            # Exibe uma mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Transferência de {amount} de {from_account} para {to_account} bem-sucedida!")
        except ValueError as e:
            # Exibe uma mensagem de erro caso haja problemas de valor
            messagebox.showerror("Erro", f"Erro na transferência: {e}")
        except Exception as e:
            # Exibe uma mensagem de erro para outros tipos de problemas
            messagebox.showerror("Erro", f"Erro inesperado: {e}")

def main():
    root = tk.Tk()
    app = TransferApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
