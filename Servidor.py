import socket
import threading
import tkinter as tk
from PIL import Image, ImageTk
import os

class TelaServidor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Painel de Senhas")
        self.root.geometry("1920x1080")
        self.root.configure(bg="white")
        self.root.state('zoomed')           # Tela cheia
        self.root.overrideredirect(True)     # Sem borda

        self.ultima_senha = ""

        # Caminho base
        caminho_base = os.path.dirname(__file__)

        # Carregar logo
        logo_prefeitura = Image.open(os.path.join(caminho_base, "logo_prefeitura.png"))
        logo_prefeitura = logo_prefeitura.resize((300, 300))
        self.logo_prefeitura_img = ImageTk.PhotoImage(logo_prefeitura)

        # Frame topo
        topo_frame = tk.Frame(self.root, bg="white")
        topo_frame.pack(side="top", pady=10, fill="x")

        # Frame esquerda (logo + secretaria)
        esquerda = tk.Frame(topo_frame, bg="white")
        esquerda.pack(side="left", padx=50)

        logo_label = tk.Label(esquerda, image=self.logo_prefeitura_img, bg="white")
        logo_label.pack()

        texto_secretaria = tk.Label(esquerda, text="Secretaria Municipal de Fazenda", font=("Arial", 20, "bold"), fg="black", bg="white")
        texto_secretaria.pack(pady=10)

        # Espaço central vazio
        centro = tk.Frame(topo_frame, bg="white", width=500)
        centro.pack(side="left", expand=True)

        # Frame direita (Central de Atendimento)
        direita = tk.Frame(topo_frame, bg="white")
        direita.pack(side="right", padx=50)

        texto_central = tk.Label(direita, text="Central de Atendimento ao Contribuinte", font=("Arial", 30, "bold"), fg="black", bg="white")
        texto_central.pack(pady=100)

        # Label da senha atual
        self.label = tk.Label(self.root, text="Aguardando senha...", font=("Arial", 48, "bold"), fg="black", bg="white")
        self.label.pack(pady=40)

        # Label da última senha
        self.ultima_label = tk.Label(self.root, text="", font=("Arial", 24), fg="gray", bg="white")
        self.ultima_label.pack()

        # Contadores
        self.contadores = {"SF": 0, "P/SF": 0, "FP": 0, "SD": 0, "VS": 0}
        self.clientes = []

        threading.Thread(target=self.iniciar_servidor, daemon=True).start()

        self.root.mainloop()

    def iniciar_servidor(self):
        host = '0.0.0.0'
        porta = 12345

        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((host, porta))
        servidor.listen()

        print("Servidor ouvindo... Aceitando múltiplos painéis.")

        while True:
            conn, addr = servidor.accept()
            print(f"Conectado por {addr}")
            self.clientes.append(conn)
            threading.Thread(target=self.tratar_cliente, args=(conn,), daemon=True).start()

    def tratar_cliente(self, conn):
        while True:
            try:
                dados = conn.recv(1024).decode()
                if not dados:
                    break
                tipo, guiche = dados.split("|")
                senha = self.gerar_proxima_senha(tipo.strip())
                mensagem = f"{guiche.strip()} - Senha: {senha}"

                print(f"Chamando: {mensagem}")

                # Atualizar labels
                if self.label.cget("text") != "Aguardando senha...":
                    self.ultima_senha = self.label.cget("text").split(":")[-1].strip()

                self.label.config(text=mensagem)
                if self.ultima_senha:
                    self.ultima_label.config(text=f"Última senha: {self.ultima_senha}")
                else:
                    self.ultima_label.config(text="")

            except Exception as e:
                print(f"Erro: {e}")
                break
        conn.close()

    def gerar_proxima_senha(self, tipo):
        if tipo in self.contadores:
            self.contadores[tipo] += 1
            return f"{tipo}{self.contadores[tipo]:03d}"
        else:
            return "Tipo inválido"

if __name__ == "__main__":
    TelaServidor()
