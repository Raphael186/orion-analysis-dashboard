#!/usr/bin/env python3
"""Gera uma imagem demonstrativa da dashboard usando somente dados sintéticos."""
from collections import Counter, defaultdict
from pathlib import Path
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "Vendas_demo_sinteticas.xlsx"
OUTPUT = ROOT / "assets" / "dashboard-preview-sintetica.png"

BG = "#0B1220"
SIDEBAR = "#0E1A2B"
PANEL = "#111E30"
PANEL_ALT = "#14253A"
GRID = "#26384E"
TEXT = "#F1F5F9"
MUTED = "#91A4BA"
CYAN = "#38BDF8"
TEAL = "#34D399"
GOLD = "#F5C451"
PURPLE = "#A78BFA"


def load_rows(sheet_name):
    wb = openpyxl.load_workbook(INPUT, data_only=True, read_only=True)
    sheet = wb[sheet_name]
    rows = sheet.iter_rows(values_only=True)
    headers = next(rows)
    result = [dict(zip(headers, row)) for row in rows]
    wb.close()
    return result


def money(value):
    return f"R$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def rounded_panel(ax, x, y, w, h, face=PANEL):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        transform=ax.transAxes, facecolor=face, edgecolor=GRID,
        linewidth=0.8, zorder=1))


def main():
    orders = load_rows("Pedidos_PowerBI")
    items = load_rows("Itens_PowerBI")
    if not orders or not items:
        raise ValueError("As abas sintéticas de pedidos e itens não podem estar vazias.")

    monthly = defaultdict(float)
    by_state = defaultdict(float)
    by_payment = Counter()
    for row in orders:
        date = row["data_pedido"]
        if date is not None:
            monthly[date.month] += float(row["total_pedido"] or 0)
        by_state[str(row["uf"] or "N/I")] += float(row["total_pedido"] or 0)
        by_payment[str(row["forma_pagamento"] or "N/I")] += 1
    by_product = defaultdict(float)
    for row in items:
        by_product[str(row["produto_demo"])] += float(row["valor_linha"] or 0)

    revenue = sum(float(r["total_pedido"] or 0) for r in orders)
    avg_ticket = revenue / len(orders)
    units = sum(int(r["quantidade"] or 0) for r in items)
    months = list(range(1, 13))
    month_values = [monthly.get(m, 0) for m in months]
    state_values = sorted(by_state.items(), key=lambda kv: kv[1], reverse=True)[:5]
    product_values = sorted(by_product.items(), key=lambda kv: kv[1], reverse=True)[:5]
    payment_values = sorted(by_payment.items(), key=lambda kv: kv[1], reverse=True)[:5]

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "text.color": TEXT,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
    })
    fig = plt.figure(figsize=(16, 9), dpi=140, facecolor=BG)
    base = fig.add_axes([0, 0, 1, 1])
    base.set_axis_off()
    base.set_facecolor(BG)

    # Sidebar/navigation
    base.add_patch(FancyBboxPatch((0.015, 0.025), 0.16, 0.95,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        transform=base.transAxes, facecolor=SIDEBAR, edgecolor=GRID, linewidth=0.8))
    base.text(0.035, 0.92, "ORION", transform=base.transAxes,
        fontsize=18, fontweight="bold", color=TEXT, va="top")
    base.text(0.036, 0.885, "ANALYSIS", transform=base.transAxes,
        fontsize=8, fontweight="bold", color=CYAN, va="top")
    base.text(0.035, 0.82, "PAINEL", transform=base.transAxes,
        fontsize=8, fontweight="bold", color=MUTED, va="top")
    for i, label in enumerate(["Resumo", "Mapa", "Vendas"]):
        y = 0.77 - i * 0.055
        if i == 0:
            base.add_patch(FancyBboxPatch((0.027, y - 0.012), 0.135, 0.04,
                boxstyle="round,pad=0.008,rounding_size=0.01",
                transform=base.transAxes, facecolor=PANEL_ALT, edgecolor="none"))
        base.text(0.042, y + 0.006, label, transform=base.transAxes,
            fontsize=10, color=TEXT if i == 0 else MUTED, va="center")
    base.text(0.035, 0.12, "DEMONSTRAÇÃO", transform=base.transAxes,
        fontsize=8, fontweight="bold", color=TEAL, va="bottom")
    base.text(0.035, 0.085, "Dados sintéticos\nsem vínculo com a loja",
        transform=base.transAxes, fontsize=8, color=MUTED, va="bottom", linespacing=1.5)

    # Header and demo filters
    base.text(0.205, 0.945, "Visão geral de vendas", transform=base.transAxes,
        fontsize=21, fontweight="bold", color=TEXT, va="top")
    base.text(0.205, 0.907, "ORION ANALYSIS  /  PAINEL DE PORTFÓLIO",
        transform=base.transAxes, fontsize=8, fontweight="bold", color=CYAN, va="top")
    base.text(0.965, 0.938, "PRÉVIA ESTÁTICA  •  DADOS SINTÉTICOS",
        transform=base.transAxes, fontsize=8, fontweight="bold", color=GOLD,
        ha="right", va="top")
    for x, label, val, width in [
        (0.205, "PERÍODO", "Jan–Dez 2023", 0.20),
        (0.415, "UF", "Todas", 0.14),
        (0.565, "CANAL", "Todos", 0.20),
    ]:
        rounded_panel(base, x, 0.835, width, 0.052, face=PANEL)
        base.text(x + 0.012, 0.869, label, transform=base.transAxes,
            fontsize=6.5, fontweight="bold", color=MUTED, va="top")
        base.text(x + 0.012, 0.846, val, transform=base.transAxes,
            fontsize=9, color=TEXT, va="top")

    # KPI cards
    kpis = [
        ("VALOR TOTAL DOS PEDIDOS", money(revenue), CYAN),
        ("PEDIDOS", f"{len(orders):,}".replace(",", "."), TEAL),
        ("UNIDADES", f"{units:,}".replace(",", "."), PURPLE),
        ("TICKET MÉDIO", money(avg_ticket), GOLD),
    ]
    kpi_x = [0.205, 0.397, 0.589, 0.781]
    for (label, value, color), x in zip(kpis, kpi_x):
        rounded_panel(base, x, 0.704, 0.178, 0.105, face=PANEL)
        base.add_patch(FancyBboxPatch((x + 0.012, 0.725), 0.004, 0.063,
            boxstyle="round,pad=0.001,rounding_size=0.002",
            transform=base.transAxes, facecolor=color, edgecolor="none"))
        base.text(x + 0.027, 0.78, label, transform=base.transAxes,
            fontsize=7, fontweight="bold", color=MUTED, va="top")
        base.text(x + 0.027, 0.742, value, transform=base.transAxes,
            fontsize=16, fontweight="bold", color=TEXT, va="top")

    # Chart panels
    rounded_panel(base, 0.205, 0.408, 0.495, 0.26)
    rounded_panel(base, 0.715, 0.408, 0.25, 0.26)
    rounded_panel(base, 0.205, 0.105, 0.365, 0.27)
    rounded_panel(base, 0.585, 0.105, 0.38, 0.27)
    base.text(0.222, 0.645, "Vendas ao longo do ano", transform=base.transAxes,
        fontsize=11, fontweight="bold", color=TEXT, va="top")
    base.text(0.222, 0.617, "Valor total dos pedidos por mês • 2023",
        transform=base.transAxes, fontsize=8, color=MUTED, va="top")
    base.text(0.732, 0.645, "Distribuição por UF", transform=base.transAxes,
        fontsize=11, fontweight="bold", color=TEXT, va="top")
    base.text(0.732, 0.617, "Maiores valores no exemplo", transform=base.transAxes,
        fontsize=8, color=MUTED, va="top")
    base.text(0.222, 0.35, "Produtos em destaque", transform=base.transAxes,
        fontsize=11, fontweight="bold", color=TEXT, va="top")
    base.text(0.222, 0.322, "Valor das linhas de itens • dados fictícios",
        transform=base.transAxes, fontsize=8, color=MUTED, va="top")
    base.text(0.602, 0.35, "Formas de pagamento", transform=base.transAxes,
        fontsize=11, fontweight="bold", color=TEXT, va="top")
    base.text(0.602, 0.322, "Contagem de pedidos por modalidade",
        transform=base.transAxes, fontsize=8, color=MUTED, va="top")

    def prep(ax):
        ax.set_facecolor(PANEL)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.75)
        ax.tick_params(axis="both", labelsize=8, length=0)
        ax.set_axisbelow(True)

    ax1 = fig.add_axes([0.225, 0.435, 0.455, 0.155], facecolor=PANEL)
    prep(ax1)
    ax1.plot(months, month_values, color=CYAN, linewidth=2.5, marker="o",
        markersize=4, markerfacecolor=BG, markeredgewidth=1.5)
    ax1.fill_between(months, month_values, color=CYAN, alpha=0.12)
    ax1.set_xticks(months)
    ax1.set_xticklabels(["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"])
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:.1f}k"))
    ax1.grid(axis="x", visible=False)
    ax1.margins(x=0.02, y=0.2)

    ax2 = fig.add_axes([0.74, 0.435, 0.20, 0.155], facecolor=PANEL)
    prep(ax2)
    labels = [uf for uf, _ in reversed(state_values)]
    values = [v for _, v in reversed(state_values)]
    ax2.barh(labels, values, color=["#247CA8", "#258CAA", "#2697A3", "#2BA68E", TEAL], height=0.58)
    ax2.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
    ax2.tick_params(axis="y", labelsize=8)
    ax2.grid(axis="x", color=GRID, linewidth=0.7)
    ax2.grid(axis="y", visible=False)
    ax2.margins(x=0.24, y=0.12)

    ax3 = fig.add_axes([0.225, 0.135, 0.325, 0.165], facecolor=PANEL)
    prep(ax3)
    products = [name.replace(" modelo demonstração", " (demo)") for name, _ in reversed(product_values)]
    product_amounts = [v for _, v in reversed(product_values)]
    ax3.barh(products, product_amounts, color=["#4C6390", "#596F9B", "#6482AC", "#5B9AAF", CYAN], height=0.6)
    ax3.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
    ax3.tick_params(axis="y", labelsize=7)
    ax3.grid(axis="x", color=GRID, linewidth=0.7)
    ax3.grid(axis="y", visible=False)
    ax3.margins(x=0.22, y=0.15)

    ax4 = fig.add_axes([0.605, 0.135, 0.34, 0.165], facecolor=PANEL)
    prep(ax4)
    pays = [name for name, _ in reversed(payment_values)]
    counts = [count for _, count in reversed(payment_values)]
    ax4.barh(pays, counts, color=["#526783", "#617B9C", "#637EAF", "#5C95B7", PURPLE], height=0.6)
    ax4.set_xlabel("Pedidos", fontsize=7, color=MUTED, labelpad=3)
    ax4.tick_params(axis="y", labelsize=8)
    ax4.grid(axis="x", color=GRID, linewidth=0.7)
    ax4.grid(axis="y", visible=False)
    ax4.margins(x=0.2, y=0.15)

    base.text(0.965, 0.055,
        "Prévia ilustrativa com dados 100% sintéticos — não é captura nem resultado do dashboard original.",
        transform=base.transAxes, fontsize=7.5, color=MUTED, ha="right", va="center")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=140, facecolor=BG, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"Prévia sintética gerada: {OUTPUT}")
    print(f"Pedidos: {len(orders)} | Itens: {len(items)} | Total demonstrativo: {money(revenue)}")


if __name__ == "__main__":
    main()
