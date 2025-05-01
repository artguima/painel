# painel.py
import socket
import tkinter as tk
from tkinter import messagebox, ttk

class PainelControle:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Painel de Controle")
        self.root.geometry("350x300")

        self.prefixos = {
            "SEMFAZ": "SF",
            "PROTOCOLO/SEMFAZ": "P/SF",
            "FISCAL DE PLANTÃO": "FP",
            "SEMDUH": "SD",
            "VIGILÂNCIA SANITÁRIA": "VS",
        }


        tk.Label(self.root, text="Tipo de Atendimento:").pack(pady=5)
        self.tipo_combo = ttk.Combobox(self.root, values=list(self.prefixos.keys()), state="readonly")
        self.tipo_combo.current(0)
        self.tipo_combo.pack(pady=5)

        tk.Label(self.root, text="Guichê:").pack(pady=5)
        self.guiche_combo = ttk.Combobox(self.root, values=["Guichê 1", "Guichê 2", "Guichê 3", "Guichê 4", "Guichê 5", "Guichê 6", "Guichê 7", "Guichê 8"], state="readonly")
        self.guiche_combo.current(0)
        self.guiche_combo.pack(pady=5)

        self.botao = tk.Button(self.root, text="Chamar Próxima Senha", command=self.enviar_solicitacao)
        self.botao.pack(pady=20)

        self.status = tk.Label(self.root, text="", fg="green")
        self.status.pack()

        self.conectar()
        self.root.mainloop()

    def conectar(self):
        host = '192.168.1.113'  # <-- Coloque aqui o IP do servidor
        porta = 12345

        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((host, porta))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar: {e}")
            self.root.destroy()

    def enviar_solicitacao(self):
        tipo_nome = self.tipo_combo.get()
        guiche = self.guiche_combo.get()

        tipo = self.prefixos.get(tipo_nome, "A")

        mensagem = f"{tipo}|{guiche}"
        try:
            self.cliente.send(mensagem.encode())
            self.status.config(text=f"Solicitado: {tipo} ({guiche})")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar: {e}")

if __name__ == "__main__":
    PainelControle()
