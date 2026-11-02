# Metodologia

## Problema abordado

O trabalho parte de uma operação varejista que mantinha informações de pedidos e produtos em planilhas. Conforme o relato da equipe, a planilha recebida estava desorganizada, com campos e valores sem um padrão consistente. Antes de analisar ou criar gráficos, foi necessário limpar e padronizar os dados.

## Fluxo executado

### 1. Inspeção da planilha de origem

A equipe examinou a estrutura recebida para identificar cabeçalhos, formatos divergentes, campos vazios, valores inconsistentes e colunas sem utilidade para as perguntas do projeto. Como a fonte incluía informações pessoais e comerciais, também foi necessário considerar quais campos não deveriam seguir para a visualização.

### 2. Tratamento e padronização

Os dados foram transformados para seguir um padrão único antes de entrar no Power BI. O processo descrito no relatório inclui padronização de formatos, conversão de texto, remoção de campos pessoais ou desnecessários, tratamento de células em branco e organização das planilhas. O Power Query foi utilizado como ferramenta de preparação/ETL — extrair, transformar e carregar.

Em termos práticos, isso significa que valores equivalentes precisam ser representados de modo consistente, datas e números devem ter tipos coerentes, categorias não devem variar por espaços ou capitalização, e campos vazios precisam ser avaliados conforme seu significado. O objetivo é evitar que diferenças de formatação sejam interpretadas como categorias ou medidas diferentes.

### 3. Carga dos dados tratados no Power BI

Somente depois da etapa de tratamento a equipe utilizou as planilhas padronizadas como fonte para o Power BI. Essa ordem é importante: primeiro consolidar uma base coerente; em seguida, modelar os dados, definir indicadores e criar os visuais. O PBIX original recebido aponta para um conjunto de dados remoto, então não foi possível validar neste ambiente a atualização exata das consultas originais.

### 4. Construção das dashboards

O relatório organiza a navegação em **Resumo**, **Mapa** e **Vendas**, com filtros temporais e comerciais. As páginas apresentam informações agregadas como evolução das vendas, produtos, distribuição regional e métricas de pedidos, conforme descrito no trabalho.

### 5. Validação e comunicação

A equipe apresentou os resultados em páginas interativas destinadas a facilitar a exploração e a tomada de decisão. Este repositório documenta o processo relatado; não afirma que os resultados foram auditados nem que o sistema foi implantado em produção.

## Demonstração reprodutível

A pasta [`../data/Vendas_demo_sinteticas.xlsx`](../data/Vendas_demo_sinteticas.xlsx) contém uma aba **Origem_Bruta_Demo**, criada com inconsistências artificiais de formato, espaços e ausências, e as abas **Pedidos_PowerBI** e **Itens_PowerBI**, padronizadas para modelagem. Todos os dados foram gerados do zero e são fictícios.

A aba bruta ilustra por que uma etapa de limpeza é necessária. As abas limpas mostram um exemplo de saída consistente para carga. Elas são um material de demonstração, não uma cópia anonimizada nem uma reprodução dos registros reais. O script [`../scripts/gerar_planilha_sintetica.py`](../scripts/gerar_planilha_sintetica.py) recria o arquivo de forma determinística.

## Ferramentas

- **Excel:** formato de origem mencionado no projeto e contêiner da demonstração sintética.
- **Power Query:** limpeza, padronização, transformação e preparação ETL.
- **Power BI:** modelagem, medidas, filtros, navegação e visualização interativa.

## Nota de reprodutibilidade

Os materiais originais e os dados da loja não foram publicados por conterem informação pessoal/comercial. A planilha sintética é reprodutível, mas o PBIX original não foi recriado: sua conexão aponta para um dataset remoto e este ambiente não dispõe do Power BI Desktop necessário para gerar e validar um PBIX com a nova fonte. Consulte [`../powerbi/README.md`](../powerbi/README.md) para orientações de reconstrução local.
