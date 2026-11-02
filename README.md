# Orion Analysis — Análise de Vendas e Dashboard

> Projeto acadêmico de análise de dados: transformar planilhas operacionais em uma experiência de acompanhamento de vendas no Power BI.

![Diagrama conceitual do fluxo de dados da Orion Analysis](assets/fluxo-de-dados.svg)

## Visão geral

A Orion Analysis é uma empresa fictícia criada por um grupo de estudantes para apresentar uma solução de Business Intelligence a uma loja varejista de acessórios. O trabalho partiu de planilhas de vendas e descreveu um fluxo de preparação no Excel/Power Query, seguido da criação de páginas interativas no Power BI.

O objetivo do painel é tornar perguntas de negócio mais acessíveis: como as vendas evoluem ao longo do tempo, quais produtos têm maior participação e como os resultados se distribuem por região e canal. O projeto é uma entrega acadêmica e uma demonstração de portfólio — não um sistema de produção nem uma auditoria dos resultados da loja.

## O que foi desenvolvido

- Levantamento de necessidades para uma análise de vendas.
- Exploração e preparação dos dados no Excel e Power Query, conforme documentado no trabalho.
- Dashboard navegável no Power BI, com áreas de **Resumo**, **Mapa** e **Vendas**.
- Filtros descritos no projeto para período e dimensões comerciais, como estado, plataforma/canal e forma de entrega.
- Identidade conceitual e narrativa de serviço sob a marca fictícia Orion Analysis.

Veja a descrição das telas em [docs/dashboard.md](docs/dashboard.md) e o processo em [docs/metodologia.md](docs/metodologia.md).

## Fluxo conceitual

1. **Fonte:** exportação de pedidos e itens em planilha.
2. **Preparação:** revisão, padronização, filtragem e transformação no Power Query.
3. **Análise:** definição de dimensões e indicadores de vendas.
4. **Apresentação:** páginas interativas no Power BI para explorar os resultados.

O diagrama é esquemático; não contém dados, números ou capturas da loja.

## Estrutura do repositório

```text
.
├── assets/
│   └── fluxo-de-dados.svg
├── data/
│   └── README.md
├── docs/
│   ├── dashboard.md
│   ├── metodologia.md
│   ├── privacidade-e-publicacao.md
│   └── reproducibilidade.md
├── powerbi/
│   └── README.md
├── site/
│   └── README.md
├── .gitignore
└── README.md
```

## Tecnologias e competências demonstradas

**Microsoft Excel · Power Query · Power BI · preparação de dados · análise exploratória · visualização interativa · levantamento de requisitos · comunicação de resultados · privacidade por concepção**

## Limites desta publicação

Os arquivos originais recebidos incluem nomes de compradores e destinatários, localidades, anotações livres, identificadores de pedidos, itens/preços, documentos com nomes de integrantes/orientador e páginas de dashboard com métricas comerciais. Por isso, **a planilha bruta, o PBIX original, o relatório acadêmico integral e o banner original não foram incluídos neste repositório público**. O site foi mencionado na documentação, mas seus arquivos-fonte não foram enviados.

Em vez de publicar material identificável, este repositório apresenta o escopo, a metodologia e a estrutura da solução sem reproduzir registros ou indicadores reais. Consulte [docs/privacidade-e-publicacao.md](docs/privacidade-e-publicacao.md) antes de acrescentar qualquer material original.

## Como visualizar

Este repositório contém documentação e um diagrama conceitual; ele não contém um PBIX sanitizado nem dados de demonstração, então não é possível reproduzir ou atualizar o dashboard a partir do GitHub. O arquivo PBIX original continua sendo necessário para abrir o relatório completo no Power BI Desktop, mas deve ser revisado e sanitizado antes de qualquer compartilhamento.

## Contexto

Trabalho acadêmico da marca fictícia Orion Analysis, desenvolvido em 2023 por um grupo de estudantes de Técnico em Informática. O conteúdo deste repositório foi preparado como apresentação pública do projeto com foco em portfólio e minimização de dados.
