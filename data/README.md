# Planilha sintética para demonstração

O arquivo [`Vendas_demo_sinteticas.xlsx`](Vendas_demo_sinteticas.xlsx) contém dados inventados do zero. Ele reproduz apenas tipos gerais de campos descritos no projeto, sem copiar linhas, nomes, valores, produtos, SKUs ou identificadores da fonte real.

A pasta de trabalho tem quatro abas:

- **Origem_Bruta_Demo:** registros fictícios com formatos deliberadamente heterogêneos, como espaços, capitalização diferente, datas em representações distintas, valores numéricos/textuais e campos ausentes. Serve para ilustrar a etapa de limpeza.
- **Pedidos_PowerBI:** uma linha por pedido, com nomes de coluna padronizados e tipos consistentes.
- **Itens_PowerBI:** uma linha por item, com chave de pedido, produto demonstrativo, quantidade e valor de linha.
- **Leia-me_Dicionario:** descreve a granularidade e o uso de cada aba.

As abas limpas são exemplos da base que poderia ser carregada no Power BI após o tratamento. Relacione `Pedidos_PowerBI[pedido_id_demo]` a `Itens_PowerBI[pedido_id_demo]` (um para muitos) e evite somar o total de pedido repetido no grão de item. Os dados são sintéticos e não representam o desempenho de uma loja real.

Para recriar a planilha, execute `python3 scripts/gerar_planilha_sintetica.py` na raiz do repositório. O gerador usa uma semente fixa e não lê os arquivos originais.
