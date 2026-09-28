import os
import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from processamento import processar_estoque


arquivo_selecionado = ""


def selecionar_arquivo():

    global arquivo_selecionado

    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo CSV",
        filetypes=[
            ("Arquivo CSV", "*.csv"),
            ("Todos os arquivos", "*.*")
        ]
    )

    if caminho:

        arquivo_selecionado = caminho

        arquivo_label.config(
            text=os.path.basename(caminho)
        )

        status.config(
            text="Arquivo selecionado."
        )


def processar():

    if not arquivo_selecionado:

        messagebox.showwarning(
            "Atenção",
            "Selecione um arquivo CSV."
        )

        return

    try:

        resultado = processar_estoque(
            arquivo_selecionado
        )

        resultado_produtos.config(
            text=str(resultado["produtos_validos"])
        )

        resultado_duplicados.config(
            text=str(resultado["duplicados"])
        )

        resultado_problemas.config(
            text=str(resultado["problemas"])
        )

        resultado_quantidade.config(
            text=str(resultado["quantidade_total"])
        )

        resultado_valor.config(
            text=f'R$ {resultado["valor_total"]:.2f}'
        )

        status.config(
            text="Processamento concluído!"
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            f"Erro ao processar o arquivo:\n\n{erro}"
        )


def abrir_relatorio():

    if not arquivo_selecionado:
        messagebox.showwarning(
            "Atenção",
            "Primeiro selecione um arquivo."
        )
        return

    pasta = os.path.dirname(
        arquivo_selecionado
    )

    caminho = os.path.join(
        pasta,
        "relatorio_estoque.txt"
    )

    if os.path.exists(caminho):
        os.startfile(caminho)
    else:
        messagebox.showwarning(
            "Atenção",
            "O relatório ainda não foi criado."
        )


def abrir_csv_limpo():

    if not arquivo_selecionado:
        messagebox.showwarning(
            "Atenção",
            "Primeiro selecione um arquivo."
        )
        return

    pasta = os.path.dirname(
        arquivo_selecionado
    )

    caminho = os.path.join(
        pasta,
        "estoque_limpo.csv"
    )

    if os.path.exists(caminho):
        os.startfile(caminho)
    else:
        messagebox.showwarning(
            "Atenção",
            "O CSV limpo ainda não foi criado."
        )


# ==========================================
# JANELA
# ==========================================

janela = tk.Tk()

janela.title(
    "Analisador de Estoque"
)

janela.geometry(
    "700x600"
)

janela.resizable(
    False,
    False
)


# ==========================================
# TÍTULO
# ==========================================

ttk.Label(
    janela,
    text="ANALISADOR DE ESTOQUE",
    font=("Arial", 20, "bold")
).pack(
    pady=(30, 5)
)


ttk.Label(
    janela,
    text="Validação e análise automática de arquivos CSV",
    font=("Arial", 11)
).pack(
    pady=(0, 25)
)


# ==========================================
# ARQUIVO
# ==========================================

frame_arquivo = ttk.Frame(janela)

frame_arquivo.pack(
    padx=40,
    fill="x"
)


ttk.Button(
    frame_arquivo,
    text="Selecionar CSV",
    command=selecionar_arquivo
).pack(
    side="left"
)


arquivo_label = ttk.Label(
    frame_arquivo,
    text="Nenhum arquivo selecionado"
)

arquivo_label.pack(
    side="left",
    padx=15
)


# ==========================================
# PROCESSAR
# ==========================================

ttk.Button(
    janela,
    text="PROCESSAR ESTOQUE",
    command=processar
).pack(
    pady=25
)


# ==========================================
# RESUMO
# ==========================================

frame = ttk.LabelFrame(
    janela,
    text="Resumo do processamento"
)

frame.pack(
    padx=40,
    fill="x"
)


def criar_resultado(linha, texto):

    ttk.Label(
        frame,
        text=texto,
        font=("Arial", 11)
    ).grid(
        row=linha,
        column=0,
        padx=25,
        pady=12,
        sticky="w"
    )

    label = ttk.Label(
        frame,
        text="0",
        font=("Arial", 16, "bold")
    )

    label.grid(
        row=linha,
        column=1,
        padx=25
    )

    return label


resultado_produtos = criar_resultado(
    0,
    "Produtos válidos:"
)

resultado_duplicados = criar_resultado(
    1,
    "Duplicados:"
)

resultado_problemas = criar_resultado(
    2,
    "Problemas:"
)

resultado_quantidade = criar_resultado(
    3,
    "Quantidade em estoque:"
)

resultado_valor = criar_resultado(
    4,
    "Valor total:"
)

resultado_valor.config(
    text="R$ 0.00"
)


# ==========================================
# BOTÕES
# ==========================================

frame_botoes = ttk.Frame(janela)

frame_botoes.pack(
    pady=25
)


ttk.Button(
    frame_botoes,
    text="Abrir relatório",
    command=abrir_relatorio
).grid(
    row=0,
    column=0,
    padx=10
)


ttk.Button(
    frame_botoes,
    text="Abrir CSV limpo",
    command=abrir_csv_limpo
).grid(
    row=0,
    column=1,
    padx=10
)


# ==========================================
# STATUS
# ==========================================

status = ttk.Label(
    janela,
    text="Aguardando arquivo..."
)

status.pack(
    pady=10
)


janela.mainloop()