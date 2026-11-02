# Power BI — demonstração sintética

## Por que o PBIX não está anexado

O PBIX original recebido registra uma conexão a um conjunto de dados remoto do Power BI. Substituir essa fonte e salvar uma cópia executável requer reconstruir o modelo e validar o relatório no Power BI Desktop. Esse aplicativo não está disponível neste ambiente Linux, portanto não foi possível produzir nem testar um PBIX fictício confiável. O arquivo original não foi republicado porque pode carregar dados e métricas da loja.

## Fonte fictícia para reconstrução local

Use [`../data/Vendas_demo_sinteticas.xlsx`](../data/Vendas_demo_sinteticas.xlsx), somente com registros inventados. As abas limpas estão prontas para importação:

- `Pedidos_PowerBI`: uma linha por pedido.
- `Itens_PowerBI`: uma linha por item.

Crie uma relação um-para-muitos entre `Pedidos_PowerBI[pedido_id_demo]` e `Itens_PowerBI[pedido_id_demo]`. Para analisar vendas por produto, use `valor_linha` em Itens. Para receita por pedido, use `total_pedido` em Pedidos; não some essa coluna no grão de item, pois o total do pedido aparece uma vez por pedido.

As medidas de partida estão em [`medidas-sinteticas.dax`](medidas-sinteticas.dax): contagem distinta de pedidos, itens vendidos, valor dos itens e total dos pedidos. Elas refletem apenas registros artificiais do workbook e não devem ser interpretadas como indicadores da loja real.

## Recriação

No Power BI Desktop, importe as abas limpas do XLSX, configure a relação indicada, crie as medidas e monte páginas equivalentes às descritas em [`../docs/dashboard.md`](../docs/dashboard.md). As cores, gráficos e interações exatos do arquivo original não foram reconstruídos nem validados aqui.
