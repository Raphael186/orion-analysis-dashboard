# Reprodutibilidade e materiais de origem

## Materiais recebidos

Foram analisados uma planilha XLSX, um arquivo Power BI (`.pbix`), um relatório acadêmico Word e um banner PDF. Os arquivos-fonte do site não foram enviados.

## Demonstração pública

O arquivo [`../data/Vendas_demo_sinteticas.xlsx`](../data/Vendas_demo_sinteticas.xlsx) traz uma aba bruta de exemplo e duas tabelas padronizadas, todas com dados sintéticos. O script [`../scripts/gerar_planilha_sintetica.py`](../scripts/gerar_planilha_sintetica.py) recria o workbook com a mesma semente. Ele não abre nem consulta os arquivos reais.

A aba `Pedidos_PowerBI` tem uma linha por pedido; `Itens_PowerBI` tem uma linha por item. No Power BI, relacione as tabelas por `pedido_id_demo` e escolha a granularidade apropriada para cada medida.

## Por que não há um PBIX sintético pronto

O PBIX recebido aponta para um conjunto de dados remoto do Power BI. Substituí-lo por uma fonte Excel sintética exige reconstruir o modelo e salvar/testar o relatório no Power BI Desktop, que não está disponível neste ambiente Linux. Para não entregar um arquivo corrompido ou com dados reais, o PBIX original foi mantido fora do repositório. O diretório [`../powerbi/`](../powerbi/README.md) contém a configuração de modelo e as medidas iniciais para reconstrução local.

## Processo documentado

O processo relatado pela equipe foi: receber uma planilha despadronizada, tratar e padronizar os dados para que seguissem um único padrão, e só então carregar a planilha tratada no Power BI para criar as dashboards. O workbook sintético demonstra essa sequência, mas não replica transformações exatas ou valores da fonte real.
