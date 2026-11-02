#!/usr/bin/env python3
"""Gera um arquivo XLSX demonstrativo usando somente dados sintéticos.

Nenhum registro, métrica, nome ou identificador da planilha real é reutilizado.
Reproduz apenas categorias gerais de campos vistas no esquema da origem.
"""
from __future__ import annotations

import random
from datetime import date, datetime, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

SEED = 20261102
OUT = Path(__file__).resolve().parents[1] / "data" / "Vendas_demo_sinteticas.xlsx"

STATES = ["SP", "RJ", "MG", "PR", "SC", "RS", "BA", "GO", "DF", "ES"]
CITIES = ["Cidade Demo A", "Cidade Demo B", "Cidade Exemplo C", "Município Fictício D"]
NEIGHBORHOODS = ["Bairro Exemplo 01", "Bairro Fictício 02", "Região Demo 03"]
PRODUCTS = [
    ("Colar modelo demonstração", 34.90),
    ("Brinco modelo demonstração", 22.50),
    ("Pulseira modelo demonstração", 28.75),
    ("Anel modelo demonstração", 19.90),
    ("Acessório modelo demonstração", 16.40),
    ("Conjunto modelo demonstração", 49.90),
    ("Tornozeleira modelo demonstração", 24.80),
]
CHANNELS = ["Loja virtual", "Marketplace fictício", "Canal social demo"]
DELIVERIES = ["Entrega padrão", "Entrega expressa", "Retirada"]
PAYMENTS = ["Cartão", "Pix", "Boleto"]
ORDER_STATUSES = ["Concluído", "Em processamento", "Cancelado"]
PAYMENT_STATUSES = ["Pago", "Pendente", "Estornado"]
SHIPPING_STATUSES = ["Entregue", "Em trânsito", "Não aplicável"]

RAW_HEADERS = [
    "Número do Pedido", "Data", "Status do Pedido", "Status do Pagamento",
    "Status do Envio", "Moeda", "Subtotal", "Desconto", "Valor do Frete",
    "Total", "Nome do comprador", "Nome para a entrega", "Bairro", "Cidade",
    "Estado", "País", "Forma de Entrega", "Forma de Pagamento",
    "Cupom de Desconto", "Anotações do Comprador", "Anotações do Vendedor",
    "Data de pagamento", "Data de envío", "Nome do Produto", "Valor do Produto",
    "Quantidade Comprada", "SKU", "Canal", "", "Identificador do pedido\n",
    "Produto Fisico",
]

ORDER_HEADERS = [
    "pedido_id_demo", "data_pedido", "status_pedido", "status_pagamento",
    "status_envio", "moeda", "subtotal_pedido", "desconto_pedido",
    "frete_pedido", "total_pedido", "cliente_demo_id", "destinatario_demo_id",
    "bairro_demo", "municipio_demo", "uf", "pais", "modalidade_entrega",
    "forma_pagamento", "cupom_demo", "observacao_cliente_demo",
    "observacao_vendedor_demo", "data_pagamento", "data_envio", "canal_demo",
]
ITEM_HEADERS = [
    "item_demo_id", "pedido_id_demo", "produto_demo", "sku_demo",
    "valor_unitario", "quantidade", "valor_linha", "produto_fisico",
]


def money_br(value: float) -> str:
    return "R$ " + f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def random_date(rng: random.Random) -> date:
    return date(2023, 1, 1) + timedelta(days=rng.randrange(365))


def create_records(rng: random.Random):
    orders, items, raw = [], [], []
    order_count = 120
    for order_idx in range(1, order_count + 1):
        order_id = f"DEMO-{900000 + order_idx}"
        buyer_id = f"CLIENTE-DEMO-{((order_idx - 1) % 55) + 1:03d}"
        order_date = random_date(rng)
        status = rng.choices(ORDER_STATUSES, weights=[82, 13, 5])[0]
        pay_status = rng.choices(PAYMENT_STATUSES, weights=[84, 12, 4])[0]
        ship_status = "Não aplicável" if status == "Cancelado" else rng.choice(SHIPPING_STATUSES[:2])
        state = rng.choice(STATES)
        city = rng.choice(CITIES)
        neighborhood = rng.choice(NEIGHBORHOODS)
        channel = rng.choice(CHANNELS)
        delivery = rng.choice(DELIVERIES)
        payment = rng.choice(PAYMENTS)
        coupon = "DEMO10" if rng.random() < 0.14 else ""
        notes_buyer = "Solicitação fictícia de embalagem para presente" if rng.random() < 0.07 else ""
        notes_seller = "Separação demo revisada" if rng.random() < 0.08 else ""
        line_count = rng.randint(1, 4)
        line_products = [(*rng.choice(PRODUCTS), rng.randint(1, 3)) for _ in range(line_count)]
        subtotal = round(sum(price * quantity for _, price, quantity in line_products), 2)
        discount = round(subtotal * (0.10 if coupon else 0.0), 2)
        freight = round(rng.choice([0.0, 7.90, 12.50, 16.90]), 2)
        total = round(subtotal - discount + freight, 2)
        paid_date = order_date + timedelta(days=rng.randint(0, 2)) if pay_status == "Pago" else None
        sent_date = order_date + timedelta(days=rng.randint(1, 5)) if ship_status in ("Entregue", "Em trânsito") else None
        order = {
            "pedido_id_demo": order_id, "data_pedido": order_date,
            "status_pedido": status, "status_pagamento": pay_status,
            "status_envio": ship_status, "moeda": "BRL",
            "subtotal_pedido": subtotal, "desconto_pedido": discount,
            "frete_pedido": freight, "total_pedido": total,
            "cliente_demo_id": buyer_id, "destinatario_demo_id": buyer_id,
            "bairro_demo": neighborhood, "municipio_demo": city, "uf": state,
            "pais": "Brasil", "modalidade_entrega": delivery,
            "forma_pagamento": payment, "cupom_demo": coupon,
            "observacao_cliente_demo": notes_buyer,
            "observacao_vendedor_demo": notes_seller,
            "data_pagamento": paid_date, "data_envio": sent_date,
            "canal_demo": channel,
        }
        orders.append(order)
        for item_idx, (product, unit_price, qty) in enumerate(line_products, start=1):
            # Item amounts reconcile exactly to the synthetic order subtotal.
            line_total = round(unit_price * qty, 2)
            sku = f"SKU-DEMO-{rng.randint(1, 250):03d}"
            item = {
                "item_demo_id": f"{order_id}-ITEM-{item_idx:02d}",
                "pedido_id_demo": order_id, "produto_demo": product,
                "sku_demo": sku, "valor_unitario": unit_price,
                "quantidade": qty, "valor_linha": line_total,
                "produto_fisico": True,
            }
            items.append(item)

            # Deliberately inconsistent source-like formatting, still entirely synthetic.
            raw_status = f" {status.upper()} " if rng.random() < 0.35 else status
            raw_channel = f" {channel.lower()} " if rng.random() < 0.3 else channel
            raw_order_date = order_date.strftime("%d/%m/%Y") if rng.random() < 0.5 else order_date.strftime("%Y-%m-%d")
            raw_payment_date = paid_date.strftime("%d/%m/%Y") if paid_date and rng.random() < 0.6 else paid_date
            raw_subtotal = money_br(subtotal) if rng.random() < 0.5 else subtotal
            raw_discount = money_br(discount) if rng.random() < 0.5 else discount
            raw_freight = money_br(freight) if rng.random() < 0.5 else freight
            raw_total = money_br(total) if rng.random() < 0.5 else total
            raw_product_price = money_br(unit_price) if rng.random() < 0.5 else unit_price
            raw.append([
                order_id, raw_order_date, raw_status,
                f" {pay_status.lower()} " if rng.random() < 0.25 else pay_status,
                ship_status, "brl" if rng.random() < 0.25 else "BRL",
                raw_subtotal, raw_discount, raw_freight, raw_total,
                f"Cliente fictício {buyer_id[-3:]} ", f" Cliente fictício {buyer_id[-3:]}",
                f" {neighborhood.lower()} " if rng.random() < 0.3 else neighborhood,
                city, state.lower() if rng.random() < 0.2 else state, "BR",
                delivery, payment, coupon or None, notes_buyer or None,
                notes_seller or None, raw_payment_date,
                sent_date.strftime("%Y-%m-%d") if sent_date and rng.random() < 0.5 else sent_date,
                product, raw_product_price, qty, sku, raw_channel, None,
                900000 + order_idx, "Sim",
            ])
    return orders, items, raw


def style_sheet(ws, widths=None):
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for cell in ws[1]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = PatternFill("solid", fgColor="17324D")
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 32
    if widths:
        for column, width in widths.items():
            ws.column_dimensions[column].width = width
    else:
        for col in range(1, ws.max_column + 1):
            ws.column_dimensions[get_column_letter(col)].width = 20


def main():
    rng = random.Random(SEED)
    orders, items, raw = create_records(rng)
    wb = Workbook()
    ws_raw = wb.active
    ws_raw.title = "Origem_Bruta_Demo"
    ws_raw.append(RAW_HEADERS)
    for row in raw:
        ws_raw.append(row)
    style_sheet(ws_raw)

    ws_orders = wb.create_sheet("Pedidos_PowerBI")
    ws_orders.append(ORDER_HEADERS)
    for record in orders:
        ws_orders.append([record.get(header) for header in ORDER_HEADERS])
    style_sheet(ws_orders)
    for row in ws_orders.iter_rows(min_row=2):
        for idx in (6, 7, 8, 9):
            row[idx].number_format = 'R$ #,##0.00'

    ws_items = wb.create_sheet("Itens_PowerBI")
    ws_items.append(ITEM_HEADERS)
    for record in items:
        ws_items.append([record.get(header) for header in ITEM_HEADERS])
    style_sheet(ws_items)
    for row in ws_items.iter_rows(min_row=2):
        for idx in (4, 6):
            row[idx].number_format = 'R$ #,##0.00'

    dictionary = [
        ("Aba", "Granularidade", "Uso recomendado"),
        ("Origem_Bruta_Demo", "Uma linha por item exportado", "Exemplo sintético com formatos inconsistentes, espaços e valores ausentes para demonstrar a etapa de tratamento."),
        ("Pedidos_PowerBI", "Uma linha por pedido", "Campos transacionais e de recorte já padronizados. Não some o total do pedido após relacionar diretamente a itens."),
        ("Itens_PowerBI", "Uma linha por item do pedido", "Produtos, quantidades e valores por linha. Use pedido_id_demo como relação com Pedidos_PowerBI."),
        ("IDs", "Identificadores fictícios", "CLIENTE-DEMO e DEMO-... são rótulos sintéticos, sem relação com clientes ou pedidos reais."),
        ("Geografia", "UF de exemplo", "As UFs servem apenas para demonstrar recortes; os registros são inventados e não representam vendas reais."),
        ("Medida sugerida", "Soma de valor_linha", "Valor bruto sintético dos itens. Não é faturamento da loja real e não incorpora descontos ou frete do pedido."),
    ]
    ws_dict = wb.create_sheet("Leia-me_Dicionario")
    for row in dictionary:
        ws_dict.append(row)
    style_sheet(ws_dict, {"A": 28, "B": 32, "C": 95})
    for row in ws_dict.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    ws_dict.sheet_view.showGridLines = False

    wb.properties.title = "Orion Analysis — planilha sintética de demonstração"
    wb.properties.subject = "Dados inteiramente fictícios para demonstração de preparação e análise"
    wb.properties.creator = "Orion Analysis — projeto acadêmico"
    wb.properties.description = "Todos os registros, valores, produtos, identificadores e dados de clientes desta pasta são sintéticos."
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"Arquivo criado: {OUT}")
    print(f"Pedidos sintéticos: {len(orders)}; itens sintéticos: {len(items)}")


if __name__ == "__main__":
    main()
