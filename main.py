import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from PIL import Image, ImageTk

class ControleFinanceiroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle Financeiro")
        self.root.geometry("800x600")

        self.transacoes_selecionadas = set()

        self.criar_interface()
        self.exibir_transacoes()  # Exibe transações ao iniciar o programa

    def obter_todas_transacoes(self):
        conn = sqlite3.connect('controle_financeiro.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transacoes')
        transacoes = cursor.fetchall()
        conn.close()
        return transacoes

    def exibir_transacoes(self):
        transacoes = self.obter_todas_transacoes()

        self.text_area.delete(1.0, tk.END)  # Limpar a caixa de texto

        for transacao in transacoes:
            id_transacao = transacao[0]
            data = transacao[4]
            descricao = transacao[1]
            valor = transacao[2]
            tipo = transacao[3]

            # Adiciona a caixa de seleção para cada transação em uma nova linha
            checkbox = ttk.Checkbutton(self.text_area, command=lambda id_transacao=id_transacao: self.selecionar_transacao(id_transacao))
            self.text_area.window_create(tk.END, window=checkbox)
            self.text_area.insert(tk.END, " ")  # Adiciona um espaço entre a checkbox e a bolinha

            # Adiciona a bolinha colorida
            cor_bolinha = "green" if tipo == 'entrada' else "red"
            imagem_bolinha = self.criar_imagem_bolinha(cor_bolinha)
            bolinha = tk.Label(self.text_area, image=imagem_bolinha)
            bolinha.image = imagem_bolinha
            self.text_area.window_create(tk.END, window=bolinha)
            self.text_area.insert(tk.END, "  ")  # Adiciona espaços entre a bolinha e os detalhes

            detalhes = f"{data} - {descricao}: {tipo.capitalize()} - {valor:.2f}\n"

            # Adiciona os detalhes da transação
            self.text_area.insert(tk.END, detalhes)
            self.text_area.tag_add(tipo, self.text_area.index(tk.END) + f"-{len(detalhes)} chars", self.text_area.index(tk.END))
            self.text_area.tag_config(tipo, foreground='black')

        # Atualiza o resumo
        self.exibir_resumo()

    def criar_imagem_bolinha(self, cor):
        tamanho = 12
        imagem = Image.new("RGB", (tamanho, tamanho), cor)
        return ImageTk.PhotoImage(imagem)

       
    def criar_interface(self):
        # Estilo
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", background="#4CAF50", foreground="white")

        # Painel Superior
        self.painel_superior = ttk.Frame(self.root, style="TFrame")
        self.painel_superior.pack(fill=tk.X)

        ttk.Label(self.painel_superior, text="Total de Entradas:").grid(row=0, column=0, padx=10, pady=10)
        self.label_total_entradas = ttk.Label(self.painel_superior, text="0.00")
        self.label_total_entradas.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.painel_superior, text="Total de Saídas:").grid(row=0, column=2, padx=10, pady=10)
        self.label_total_saidas = ttk.Label(self.painel_superior, text="0.00")
        self.label_total_saidas.grid(row=0, column=3, padx=10, pady=10)

        ttk.Label(self.painel_superior, text="Saldo Atual:").grid(row=0, column=4, padx=10, pady=10)
        self.label_saldo_atual = ttk.Label(self.painel_superior, text="0.00")
        self.label_saldo_atual.grid(row=0, column=5, padx=10, pady=10)

        # Área de exibição
        self.text_area = tk.Text(self.root, height=20, width=80)
        self.text_area.pack(pady=10)

        # Botões de ação
        style.configure("TButton", background="#4CAF50", foreground="black")

        botao_adicionar = ttk.Button(self.root, text="Adicionar Transação", style="TButton", command=self.adicionar_transacao)
        botao_adicionar.pack(pady=10)

        botao_sair = ttk.Button(self.root, text="Sair", style="TButton", command=self.root.destroy)
        botao_sair.pack(pady=10)
        
        # Botão de exclusão
        botao_excluir = ttk.Button(self.root, text="Excluir Transações Selecionadas", style="TButton", command=self.excluir_transacoes_selecionadas)
        botao_excluir.pack(pady=10)

    def adicionar_transacao(self):
        def adicionar_com_valores(descricao, valor, tipo):
            valor = valor.replace(',', '.')  # Substituir vírgula por ponto

            try:
                valor = float(valor)
                self.inserir_transacao(descricao, valor, tipo)
                messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
                self.exibir_transacoes()  # Após adicionar, exibe novamente as transações
                janela.destroy()  # Fecha a janela após adicionar a transação
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido. Certifique-se de usar um formato numérico válido.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar transação: {str(e)}")

        janela = tk.Toplevel(self.root)
        janela.title("Adicionar Transação")

        ttk.Label(janela, text="Descrição:").grid(row=0, column=0, padx=10, pady=10)
        entry_descricao = ttk.Entry(janela)
        entry_descricao.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(janela, text="Valor:").grid(row=1, column=0, padx=10, pady=10)
        entry_valor = ttk.Entry(janela)
        entry_valor.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(janela, text="Tipo (entrada/saida):").grid(row=2, column=0, padx=10, pady=10)
        entry_tipo = ttk.Entry(janela)
        entry_tipo.grid(row=2, column=1, padx=10, pady=10)

        botao_adicionar = ttk.Button(janela, text="Adicionar", command=lambda: adicionar_com_valores(entry_descricao.get(), entry_valor.get(), entry_tipo.get()))
        botao_adicionar.grid(row=3, column=0, columnspan=2, pady=10)

    def selecionar_transacao(self, id_transacao):
        # Adiciona ou remove a transação da lista de transações selecionadas
        if id_transacao in self.transacoes_selecionadas:
            self.transacoes_selecionadas.remove(id_transacao)
        else:
            self.transacoes_selecionadas.add(id_transacao)

    def excluir_transacoes_selecionadas(self):
        if not self.transacoes_selecionadas:
            messagebox.showinfo("Aviso", "Nenhuma transação selecionada para excluir.")
            return

        try:
            # Conecta ao banco de dados
            conn = sqlite3.connect('controle_financeiro.db')
            cursor = conn.cursor()

            # Exclui as transações selecionadas do banco de dados
            for id_transacao in self.transacoes_selecionadas:
                cursor.execute('DELETE FROM transacoes WHERE id = ?', (id_transacao,))

            # Commit e fecha a conexão
            conn.commit()
            conn.close()

            # Limpa a lista de transações selecionadas
            self.transacoes_selecionadas.clear()

            # Atualiza a exibição após excluir as transações
            self.exibir_transacoes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir transações: {str(e)}")

    def inserir_transacao(self, descricao, valor, tipo):
        conn = sqlite3.connect('controle_financeiro.db')
        cursor = conn.cursor()
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO transacoes (descricao, valor, tipo, data) VALUES (?, ?, ?, ?)', (descricao, valor, tipo, data))
        conn.commit()
        conn.close()
        
    def exibir_resumo(self):
        transacoes = self.obter_todas_transacoes()

        entradas = sum(transacao[2] for transacao in transacoes if transacao[3] == 'entrada')
        saidas = sum(transacao[2] for transacao in transacoes if transacao[3] == 'saida')
        saldo_atual = entradas - saidas

        self.label_total_entradas.config(text=f"{entradas:.2f}")
        self.label_total_saidas.config(text=f"{saidas:.2f}")
        self.label_saldo_atual.config(text=f"{saldo_atual:.2f}")

    def criar_imagem_bolinha(self, cor):
        # Cria uma imagem de bolinha colorida
        imagem = Image.new("RGB", (10, 10), color=cor)
        return ImageTk.PhotoImage(imagem)

if __name__ == "__main__":
    root = tk.Tk()
    app = ControleFinanceiroApp(root)
    root.mainloop()
