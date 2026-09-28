import csv
import os


ESTOQUE_BAIXO = 5


def processar_estoque(arquivo_entrada):

    produtos = []

    with open(
        arquivo_entrada,
        "r",
        encoding="utf-8-sig"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)
        produtos = list(leitor)

    if not produtos:
        raise ValueError("O arquivo CSV está vazio.")

    produtos_validos = []
    produtos_vistos = set()
    duplicados = set()
    problemas = []

    valor_total = 0
    quantidade_total = 0

    valores_por_categoria = {}
    quantidades_por_categoria = {}
    produtos_estoque_baixo = []

    for produto in produtos:

        nome_original = produto.get(
            "Produto", ""
        ).strip()

        nome_chave = nome_original.casefold()

        preco_texto = produto.get(
            "Preço", ""
        ).strip()

        categoria = produto.get(
            "Categoria", ""
        ).strip()

        estoque_texto = produto.get(
            "Estoque", ""
        ).strip()

        produto_valido = True

        # PREÇO
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

        # ESTOQUE
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

        # CATEGORIA
        if not categoria:
            problemas.append(
                f"{nome_original}: categoria vazia"
            )
            produto_valido = False

        # DUPLICADO
        if nome_chave in produtos_vistos:
            duplicados.add(nome_original)
            produto_valido = False
        else:
            produtos_vistos.add(nome_chave)

        # PRODUTO VÁLIDO
        if produto_valido:

            produtos_validos.append(produto)

            valor_produto = preco * estoque

            valor_total += valor_produto
            quantidade_total += estoque

            if categoria not in valores_por_categoria:
                valores_por_categoria[categoria] = 0
                quantidades_por_categoria[categoria] = 0

            valores_por_categoria[categoria] += valor_produto
            quantidades_por_categoria[categoria] += estoque

            if estoque <= ESTOQUE_BAIXO:
                produtos_estoque_baixo.append(
                    (nome_original, estoque)
                )

    # ======================================
    # ARQUIVOS DE SAÍDA
    # ======================================

    pasta = os.path.dirname(
        os.path.abspath(arquivo_entrada)
    )

    arquivo_limpo = os.path.join(
        pasta,
        "estoque_limpo.csv"
    )

    arquivo_relatorio = os.path.join(
        pasta,
        "relatorio_estoque.txt"
    )

    # CSV LIMPO
    with open(
        arquivo_limpo,
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

    # RELATÓRIO
    with open(
        arquivo_relatorio,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write("=" * 55 + "\n")
        arquivo.write("RELATÓRIO DE ESTOQUE\n")
        arquivo.write("=" * 55 + "\n\n")

        arquivo.write("RESUMO GERAL\n")
        arquivo.write("-" * 55 + "\n")

        arquivo.write(
            f"Produtos analisados: {len(produtos)}\n"
        )

        arquivo.write(
            f"Produtos válidos: {len(produtos_validos)}\n"
        )

        arquivo.write(
            f"Produtos duplicados: {len(duplicados)}\n"
        )

        arquivo.write(
            f"Problemas encontrados: {len(problemas)}\n"
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

        arquivo.write("ESTOQUE POR CATEGORIA\n")
        arquivo.write("-" * 55 + "\n")

        for categoria in sorted(valores_por_categoria):

            arquivo.write(
                f"{categoria}: "
                f"{quantidades_por_categoria[categoria]} "
                f"unidades | "
                f"R$ {valores_por_categoria[categoria]:.2f}\n"
            )

        arquivo.write("\n")

        arquivo.write(
            f"PRODUTOS COM ESTOQUE BAIXO "
            f"(até {ESTOQUE_BAIXO} unidades)\n"
        )

        arquivo.write("-" * 55 + "\n")

        if produtos_estoque_baixo:

            for nome, estoque in produtos_estoque_baixo:
                arquivo.write(
                    f"- {nome}: {estoque} unidades\n"
                )

        else:
            arquivo.write(
                "Nenhum produto com estoque baixo.\n"
            )

        arquivo.write("\n")

        arquivo.write("PRODUTOS DUPLICADOS\n")
        arquivo.write("-" * 55 + "\n")

        if duplicados:

            for produto in sorted(duplicados):
                arquivo.write(f"- {produto}\n")

        else:
            arquivo.write(
                "Nenhum produto duplicado encontrado.\n"
            )

        arquivo.write("\n")

        arquivo.write("PROBLEMAS ENCONTRADOS\n")
        arquivo.write("-" * 55 + "\n")

        if problemas:

            for problema in problemas:
                arquivo.write(f"- {problema}\n")

        else:
            arquivo.write(
                "Nenhum problema encontrado.\n"
            )

        arquivo.write("\n")
        arquivo.write("=" * 55 + "\n")

    # ======================================
    # RETORNAR RESULTADOS PARA A INTERFACE
    # ======================================

    return {
        "produtos_analisados": len(produtos),
        "produtos_validos": len(produtos_validos),
        "duplicados": len(duplicados),
        "problemas": len(problemas),
        "quantidade_total": quantidade_total,
        "valor_total": valor_total,
        "arquivo_limpo": arquivo_limpo,
        "arquivo_relatorio": arquivo_relatorio
    }