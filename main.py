import csv


# ==========================================
# CONFIGURAÇÕES
# ==========================================

ARQUIVO_ENTRADA = "estoque.csv"
ARQUIVO_SAIDA = "estoque_limpo.csv"
ARQUIVO_RELATORIO = "relatorio_estoque.txt"

ESTOQUE_BAIXO = 5


# ==========================================
# VARIÁVEIS
# ==========================================

produtos = []

produtos_validos = []

produtos_vistos = set()
duplicados = set()
problemas = []

valor_total = 0
quantidade_total = 0

valores_por_categoria = {}
quantidades_por_categoria = {}

produtos_estoque_baixo = []


# ==========================================
# LER CSV
# ==========================================

try:

    with open(
        ARQUIVO_ENTRADA,
        "r",
        encoding="utf-8"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        produtos = list(leitor)

except FileNotFoundError:

    print(
        f"ERRO: o arquivo '{ARQUIVO_ENTRADA}' "
        "não foi encontrado."
    )

    exit()


# ==========================================
# VERIFICAR SE O CSV ESTÁ VAZIO
# ==========================================

if not produtos:

    print("ERRO: o arquivo CSV está vazio.")

    exit()


# ==========================================
# PROCESSAR PRODUTOS
# ==========================================

for produto in produtos:

    # --------------------------------------
    # PEGAR DADOS
    # --------------------------------------

    nome_original = produto.get(
        "Produto",
        ""
    ).strip()

    nome_chave = nome_original.casefold()

    preco_texto = produto.get(
        "Preço",
        ""
    ).strip()

    categoria = produto.get(
        "Categoria",
        ""
    ).strip()

    estoque_texto = produto.get(
        "Estoque",
        ""
    ).strip()


    produto_valido = True


    # --------------------------------------
    # VERIFICAR NOME
    # --------------------------------------

    if not nome_original:

        problemas.append(
            "Produto sem nome"
        )

        produto_valido = False


    # --------------------------------------
    # VERIFICAR CATEGORIA
    # --------------------------------------

    if not categoria:

        problemas.append(
            f"{nome_original}: categoria vazia"
        )

        produto_valido = False


    # --------------------------------------
    # VERIFICAR PREÇO
    # --------------------------------------

    try:

        preco = float(preco_texto)

        if preco < 0:

            problemas.append(
                f"{nome_original}: preço negativo"
            )

            produto_valido = False

    except ValueError:

        problemas.append(
            f"{nome_original}: preço inválido"
        )

        produto_valido = False

        preco = 0


    # --------------------------------------
    # VERIFICAR ESTOQUE
    # --------------------------------------

    try:

        estoque = int(estoque_texto)

        if estoque < 0:

            problemas.append(
                f"{nome_original}: estoque negativo"
            )

            produto_valido = False

    except ValueError:

        problemas.append(
            f"{nome_original}: estoque inválido"
        )

        produto_valido = False

        estoque = 0


    # --------------------------------------
    # VERIFICAR DUPLICADOS
    # --------------------------------------

    if nome_chave in produtos_vistos:

        duplicados.add(nome_original)

        produto_valido = False

    else:

        produtos_vistos.add(nome_chave)


    # --------------------------------------
    # GUARDAR PRODUTO VÁLIDO
    # --------------------------------------

    if produto_valido:

        produtos_validos.append(produto)

        valor_produto = preco * estoque

        valor_total += valor_produto

        quantidade_total += estoque


        # ----------------------------------
        # CATEGORIA
        # ----------------------------------

        if categoria not in valores_por_categoria:

            valores_por_categoria[categoria] = 0

        valores_por_categoria[categoria] += valor_produto


        if categoria not in quantidades_por_categoria:

            quantidades_por_categoria[categoria] = 0

        quantidades_por_categoria[categoria] += estoque


        # ----------------------------------
        # ESTOQUE BAIXO
        # ----------------------------------

        if estoque <= ESTOQUE_BAIXO:

            produtos_estoque_baixo.append(
                (nome_original, estoque)
            )


# ==========================================
# ESTATÍSTICAS
# ==========================================

produto_mais_caro = None
maior_valor = 0

produto_maior_estoque = None
maior_estoque = 0


for produto in produtos_validos:

    nome = produto["Produto"].strip()

    preco = float(
        produto["Preço"].strip()
    )

    estoque = int(
        produto["Estoque"].strip()
    )

    valor = preco * estoque


    # --------------------------------------
    # PRODUTO COM MAIOR VALOR
    # --------------------------------------

    if valor > maior_valor:

        maior_valor = valor

        produto_mais_caro = nome


    # --------------------------------------
    # PRODUTO COM MAIOR ESTOQUE
    # --------------------------------------

    if estoque > maior_estoque:

        maior_estoque = estoque

        produto_maior_estoque = nome


# ==========================================
# CRIAR CSV LIMPO
# ==========================================

with open(
    ARQUIVO_SAIDA,
    "w",
    newline="",
    encoding="utf-8"
) as arquivo:

    campos = [
        "Produto",
        "Preço",
        "Categoria",
        "Estoque"
    ]

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=campos
    )

    escritor.writeheader()

    for produto in produtos_validos:

        escritor.writerow(produto)


# ==========================================
# CRIAR RELATÓRIO
# ==========================================

with open(
    ARQUIVO_RELATORIO,
    "w",
    encoding="utf-8"
) as arquivo:

    arquivo.write("=" * 55 + "\n")
    arquivo.write("RELATÓRIO DE ESTOQUE\n")
    arquivo.write("=" * 55 + "\n\n")


    # ======================================
    # RESUMO
    # ======================================

    arquivo.write("RESUMO GERAL\n")
    arquivo.write("-" * 55 + "\n")

    arquivo.write(
        f"Produtos analisados: "
        f"{len(produtos)}\n"
    )

    arquivo.write(
        f"Produtos válidos: "
        f"{len(produtos_validos)}\n"
    )

    arquivo.write(
        f"Produtos duplicados: "
        f"{len(duplicados)}\n"
    )

    arquivo.write(
        f"Problemas encontrados: "
        f"{len(problemas)}\n"
    )

    arquivo.write(
        f"Quantidade total em estoque: "
        f"{quantidade_total} unidades\n"
    )

    arquivo.write(
        f"Valor total do estoque: "
        f"R$ {valor_total:.2f}\n"
    )

    arquivo.write("\n")


    # ======================================
    # ESTATÍSTICAS
    # ======================================

    arquivo.write("ESTATÍSTICAS\n")
    arquivo.write("-" * 55 + "\n")

    if produto_mais_caro:

        arquivo.write(
            f"Produto com maior valor em estoque: "
            f"{produto_mais_caro}\n"
        )

        arquivo.write(
            f"Valor: R$ {maior_valor:.2f}\n"
        )

    else:

        arquivo.write(
            "Nenhum produto válido encontrado.\n"
        )


    if produto_maior_estoque:

        arquivo.write(
            f"Produto com maior quantidade: "
            f"{produto_maior_estoque}\n"
        )

        arquivo.write(
            f"Quantidade: {maior_estoque} unidades\n"
        )

    arquivo.write("\n")


    # ======================================
    # CATEGORIAS
    # ======================================

    arquivo.write("ESTOQUE POR CATEGORIA\n")
    arquivo.write("-" * 55 + "\n")

    if valores_por_categoria:

        for categoria in sorted(
            valores_por_categoria
        ):

            quantidade = (
                quantidades_por_categoria[
                    categoria
                ]
            )

            valor = (
                valores_por_categoria[
                    categoria
                ]
            )

            arquivo.write(
                f"{categoria}: "
                f"{quantidade} unidades | "
                f"R$ {valor:.2f}\n"
            )

    else:

        arquivo.write(
            "Nenhuma categoria encontrada.\n"
        )

    arquivo.write("\n")


    # ======================================
    # ESTOQUE BAIXO
    # ======================================

    arquivo.write(
        f"PRODUTOS COM ESTOQUE BAIXO "
        f"(até {ESTOQUE_BAIXO} unidades)\n"
    )

    arquivo.write("-" * 55 + "\n")

    if produtos_estoque_baixo:

        for nome, estoque in sorted(
            produtos_estoque_baixo
        ):

            arquivo.write(
                f"- {nome}: "
                f"{estoque} unidades\n"
            )

    else:

        arquivo.write(
            "Nenhum produto com estoque baixo.\n"
        )

    arquivo.write("\n")


    # ======================================
    # DUPLICADOS
    # ======================================

    arquivo.write("PRODUTOS DUPLICADOS\n")
    arquivo.write("-" * 55 + "\n")

    if duplicados:

        for produto in sorted(duplicados):

            arquivo.write(
                f"- {produto}\n"
            )

    else:

        arquivo.write(
            "Nenhum produto duplicado encontrado.\n"
        )

    arquivo.write("\n")


    # ======================================
    # PROBLEMAS
    # ======================================

    arquivo.write("PROBLEMAS ENCONTRADOS\n")
    arquivo.write("-" * 55 + "\n")

    if problemas:

        for problema in problemas:

            arquivo.write(
                f"- {problema}\n"
            )

    else:

        arquivo.write(
            "Nenhum problema encontrado.\n"
        )

    arquivo.write("\n")


    # ======================================
    # ARQUIVOS GERADOS
    # ======================================

    arquivo.write("ARQUIVOS GERADOS\n")
    arquivo.write("-" * 55 + "\n")

    arquivo.write(
        f"- {ARQUIVO_SAIDA}\n"
    )

    arquivo.write(
        f"- {ARQUIVO_RELATORIO}\n"
    )

    arquivo.write("\n")

    arquivo.write("=" * 55 + "\n")


# ==========================================
# RESULTADO NO TERMINAL
# ==========================================

print()
print("=" * 50)
print("PROCESSAMENTO CONCLUÍDO")
print("=" * 50)

print(
    f"Produtos analisados: "
    f"{len(produtos)}"
)

print(
    f"Produtos válidos: "
    f"{len(produtos_validos)}"
)

print(
    f"Produtos duplicados: "
    f"{len(duplicados)}"
)

print(
    f"Problemas encontrados: "
    f"{len(problemas)}"
)

print(
    f"Quantidade total: "
    f"{quantidade_total} unidades"
)

print(
    f"Valor total: "
    f"R$ {valor_total:.2f}"
)

print()

print(
    f"Arquivo criado: "
    f"{ARQUIVO_SAIDA}"
)

print(
    f"Relatório criado: "
    f"{ARQUIVO_RELATORIO}"
)

print("=" * 50)