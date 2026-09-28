# 📊 Sistema de Análise de Estoque

Sistema desenvolvido em Python para automatizar a análise, validação e organização de arquivos de estoque em formato CSV.

## 🚀 Funcionalidades

* Leitura de arquivos CSV
* Validação de preços
* Validação de quantidade em estoque
* Identificação de produtos duplicados
* Normalização dos nomes dos produtos
* Identificação de estoque baixo
* Cálculo do valor total do estoque
* Análise de estoque por categoria
* Geração de CSV limpo
* Geração de relatório automático
* Interface gráfica para facilitar o uso

## 🖥️ Interface

O sistema possui uma interface gráfica onde o usuário pode:

1. Selecionar um arquivo CSV
2. Processar o estoque
3. Visualizar um resumo dos resultados
4. Abrir o relatório gerado
5. Abrir o CSV tratado

## 📁 Estrutura do projeto

```text
projeto_01_estoque/
│
├── main.py
├── interface.py
├── processamento.py
├── README.md
├── .gitignore
│
├── estoque.csv
├── estoque_limpo.csv
└── relatorio_estoque.txt
```

## 🛠️ Tecnologias utilizadas

* Python
* Tkinter
* CSV
* Manipulação de arquivos
* Validação e tratamento de dados

## ▶️ Como executar

Certifique-se de ter o Python instalado.

Abra o terminal na pasta do projeto e execute:

```bash
python interface.py
```

Depois:

1. Clique em **Selecionar CSV**
2. Escolha o arquivo de estoque
3. Clique em **PROCESSAR ESTOQUE**
4. Consulte os resultados na interface

## 📊 Formato do arquivo CSV

O arquivo deve possuir as seguintes colunas:

`
