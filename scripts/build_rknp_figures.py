#!/usr/bin/env python3
"""Build the six РКНП submission figures.

Every numeric value in this script is copied verbatim from the frozen analysis
artifacts and must not be edited without re-verifying against:

  results/final-pilot-v2-2-low/analysis/SCIENTIFIC_RESULTS_V2_2.md
  results/final-pilot-v2-2-low/analysis/C_vs_B.json
  data/manifests/SAMPLING_AUDIT_V2_2.md
  data/manifests/PATTERN_ANNOTATION_AGREEMENT_V2_2.md

Output: PDF (vector, for the document), SVG (vector, editable) and PNG (preview)
into paper/figures/rknp_final/.
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures" / "rknp_final"
OUT.mkdir(parents=True, exist_ok=True)

SYSFONTS = pathlib.Path("/System/Library/Fonts/Supplemental")
for _f in (
    "Times New Roman.ttf",
    "Times New Roman Bold.ttf",
    "Times New Roman Italic.ttf",
    "Times New Roman Bold Italic.ttf",
):
    if (SYSFONTS / _f).exists():
        fm.fontManager.addfont(str(SYSFONTS / _f))

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 9,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "black",
        "axes.labelcolor": "black",
        "text.color": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    }
)

# Grayscale-safe fills. Distinguishable in print, on screen and in photocopy.
FILL_B = "#d9d9d9"   # generic prior (light)
FILL_C = "#7f7f7f"   # pattern prior (dark)
FILL_NEUTRAL = "#f2f2f2"
FILL_ACCENT = "#e0e0e0"
EDGE = "black"

CM = 1 / 2.54


def save(fig, stem: str) -> None:
    for ext in ("pdf", "svg", "png"):
        fig.savefig(
            OUT / f"{stem}.{ext}",
            dpi=400 if ext == "png" else None,
            bbox_inches="tight",
            pad_inches=0.04,
        )
    plt.close(fig)
    print("wrote", stem)


def box(ax, x, y, w, h, text, fill=FILL_NEUTRAL, fontsize=8.2, weight="normal",
        lw=0.9, style="round,pad=0.012,rounding_size=0.012"):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h, boxstyle=style,
            linewidth=lw, edgecolor=EDGE, facecolor=fill, zorder=2,
        )
    )
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, fontweight=weight, zorder=3, linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, lw=1.0, style="-|>", ls="-", ms=7):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
            linewidth=lw, color="black", linestyle=ls, zorder=4,
            shrinkA=0, shrinkB=0,
        )
    )


def blank_axes(fig):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return ax


# --------------------------------------------------------------------------
# Рисунок 1 — концептуальная схема
# --------------------------------------------------------------------------
def figure_1() -> None:
    fig = plt.figure(figsize=(16.4 * CM, 9.6 * CM))
    ax = blank_axes(fig)

    xc, w, h = 0.055, 0.40, 0.115
    ys = [0.845, 0.665, 0.485, 0.305, 0.125]
    labels = [
        "Исходный код программы\nс логической ошибкой",
        "Алгоритмический паттерн\n(классифицированный тип алгоритма)",
        "Структурная подсказка:\nчек-лист вероятных мест сбоя",
        "Большая языковая модель",
        "Ранжированный список\nпредполагаемых строк ошибки",
    ]
    fills = [FILL_NEUTRAL, FILL_ACCENT, FILL_ACCENT, FILL_NEUTRAL, FILL_NEUTRAL]
    weights = ["normal", "bold", "bold", "normal", "normal"]

    for y, lab, fl, wt in zip(ys, labels, fills, weights):
        box(ax, xc, y, w, h, lab, fill=fl, weight=wt)
    for y0, y1 in zip(ys[:-1], ys[1:]):
        arrow(ax, xc + w / 2, y0, xc + w / 2, y1 + h, lw=1.1, ms=8)

    # Verified link marker
    ax.plot([xc - 0.022, xc - 0.022], [ys[2], ys[1] + h], color="black", lw=1.1)
    ax.plot([xc - 0.022, xc - 0.008], [ys[1] + h, ys[1] + h], color="black", lw=1.1)
    ax.plot([xc - 0.022, xc - 0.008], [ys[2], ys[2]], color="black", lw=1.1)
    ax.text(xc - 0.030, (ys[1] + h + ys[2]) / 2, "проверяемое\nзвено",
            ha="right", va="center", fontsize=7.6, style="italic", linespacing=1.3)

    # Side comparison panel
    px, pw = 0.545, 0.42
    ax.add_patch(
        FancyBboxPatch(
            (px, 0.245), pw, 0.665,
            boxstyle="round,pad=0.012,rounding_size=0.012",
            linewidth=0.9, edgecolor=EDGE, facecolor="white",
            linestyle=(0, (4, 2.5)), zorder=1,
        )
    )
    ax.text(px + pw / 2, 0.868, "Два варианта вставляемого блока подсказки",
            ha="center", va="center", fontsize=8.4, fontweight="bold")

    box(ax, px + 0.028, 0.648, pw - 0.056, 0.175,
        "Условие B — общая подсказка\n"
        "универсальные советы по отладке;\n"
        "одинакова для всех 30 программ",
        fill=FILL_B, fontsize=8.0)
    box(ax, px + 0.028, 0.348, pw - 0.056, 0.175,
        "Условие C — подсказка по паттерну\n"
        "содержание выведено из класса\n"
        "алгоритма данной программы",
        fill=FILL_C, fontsize=8.0)
    for t in ax.texts[-1:]:
        t.set_color("white")

    ax.text(px + pw / 2, 0.586,
            "согласованы по объёму, формату,\nтону и числу пунктов",
            ha="center", va="center", fontsize=7.4, style="italic", linespacing=1.3)

    ax.text(px + pw / 2, 0.292,
            "ПЕРВИЧНОЕ СРАВНЕНИЕ:  C против B",
            ha="center", va="center", fontsize=8.6, fontweight="bold")

    arrow(ax, px - 0.002, 0.586, xc + w + 0.006, 0.485 + h / 2, lw=1.0, ms=7)

    ax.text(xc + w / 2, 0.055,
            "сравнение с истинной ошибочной строкой  →  метрики Top-1, Top-3, Top-5 и EXAM*",
            ha="center", va="center", fontsize=7.8, style="italic")
    arrow(ax, xc + w / 2, ys[4], xc + w / 2, 0.078, lw=1.0, ms=7)

    save(fig, "fig1_concept")


# --------------------------------------------------------------------------
# Рисунок 2 — воронка формирования выборки
# --------------------------------------------------------------------------
def figure_2() -> None:
    """PRISMA-style eligibility funnel with the exact committed counts."""
    stages = [
        ("Полный корпус ConDefects-Python (985 задач)", "2864", None, False),
        ("Синтаксически корректные версии кода", "2863",
         "−1  синтаксическая ошибка", False),
        ("Длина исходника 25–300 строк", "1324",
         "−1539  длина вне диапазона", False),
        ("Исправление затрагивает ровно одну строку", "1008",
         "−316  исправление не однострочное", False),
        ("Выполнено динамическое условие: хотя бы один\nтест пройден и хотя бы один провален",
         "303", "−705  условие не выполнено", False),
        ("Одна программа на задачу\n(посеянная дедупликация) — рамка разметки", "232",
         "−71  повторы по задаче", True),
        ("Точное совпадение меток двух независимых\nслепых модельных аннотаторов", "182",
         "−50  аннотаторы разошлись", False),
        ("Согласованная метка внутри словаря паттернов", "157",
         "−25  паттерн вне словаря", False),
        ("Классы численностью не менее 7 программ", "130",
         "−27  класс слишком мал", False),
        ("Четыре крупнейших класса", "109",
         "−21  класс вне четырёх крупнейших", False),
        ("Итоговая выборка, квоты 8 / 8 / 7 / 7", "30",
         "−79  не отобраны посеянным жребием", True),
    ]

    n = len(stages)
    fig = plt.figure(figsize=(15.6 * CM, 16.6 * CM))
    ax = blank_axes(fig)

    top, bot = 0.985, 0.012
    slot = (top - bot) / n
    bh = slot * 0.62
    bx, bw = 0.045, 0.585

    for i, (label, count, excl, key) in enumerate(stages):
        y = top - (i + 1) * slot + (slot - bh) / 2
        ax.add_patch(
            FancyBboxPatch(
                (bx, y), bw, bh,
                boxstyle="round,pad=0.005,rounding_size=0.007",
                linewidth=1.5 if key else 0.9, edgecolor=EDGE,
                facecolor=FILL_ACCENT if key else FILL_NEUTRAL, zorder=2,
            )
        )
        ax.text(bx + 0.016, y + bh / 2, label, ha="left", va="center",
                fontsize=7.6, linespacing=1.3, zorder=3)
        ax.text(bx + bw - 0.016, y + bh / 2, f"n = {count}", ha="right",
                va="center", fontsize=8.8,
                fontweight="bold" if key else "normal", zorder=3)

        if i < n - 1:
            y_next = top - (i + 2) * slot + (slot - bh) / 2
            arrow(ax, bx + 0.085, y, bx + 0.085, y_next + bh, lw=1.0, ms=7)
            nxt = stages[i + 1]
            if nxt[2]:
                ym = (y + y_next + bh) / 2
                ax.plot([bx + 0.085, bx + bw - 0.010], [ym, ym], color="black",
                        lw=0.7, linestyle=(0, (3, 2)), zorder=1)
                arrow(ax, bx + bw - 0.010, ym, bx + bw + 0.006, ym, lw=0.7, ms=6)
                ax.text(bx + bw + 0.014, ym, nxt[2], ha="left", va="center",
                        fontsize=7.2, zorder=3)

    save(fig, "fig2_sampling_funnel")


# --------------------------------------------------------------------------
# Рисунок 3 — дизайн эксперимента
# --------------------------------------------------------------------------
def figure_3() -> None:
    fig = plt.figure(figsize=(17.2 * CM, 9.4 * CM))
    ax = blank_axes(fig)

    # Shared sample, on the left, spanning both lanes
    box(ax, 0.008, 0.230, 0.135, 0.640,
        "Одна\nи та же\nвыборка:\n\n30 программ\nConDefects-\nPython",
        fill=FILL_ACCENT, fontsize=8.2, weight="bold")

    lane_x, lane_w = 0.205, 0.665
    for y, name in ((0.585, "СЕССИЯ G"), (0.145, "СЕССИЯ P")):
        ax.add_patch(
            FancyBboxPatch(
                (lane_x, y), lane_w, 0.285,
                boxstyle="round,pad=0.010,rounding_size=0.010",
                linewidth=0.8, edgecolor="black", facecolor="white",
                linestyle=(0, (4, 2.5)), zorder=1,
            )
        )
        ax.text(lane_x + 0.016, y + 0.285 - 0.032, name, ha="left", va="center",
                fontsize=8.4, fontweight="bold")

    bw, bh = 0.245, 0.125
    xl, xr = 0.245, 0.585

    box(ax, xl, 0.615, bw, bh, "A_G — без блока\nподсказки",
        fill=FILL_NEUTRAL, fontsize=8.4)
    box(ax, xr, 0.615, bw, bh, "B — общая\nподсказка",
        fill=FILL_B, fontsize=8.8, weight="bold")
    box(ax, xl, 0.175, bw, bh, "A_P — без блока\nподсказки",
        fill=FILL_NEUTRAL, fontsize=8.4)
    box(ax, xr, 0.175, bw, bh, "C — подсказка\nпо паттерну",
        fill=FILL_C, fontsize=8.8, weight="bold")
    ax.texts[-1].set_color("white")

    for y in (0.615, 0.175):
        arrow(ax, xl + bw + 0.008, y + bh / 2, xr - 0.008, y + bh / 2,
              lw=0.9, style="<|-|>", ms=6)
        ax.text((xl + bw + xr) / 2, y + bh / 2 + 0.052,
                "вторичное\nсравнение", ha="center", va="center", fontsize=7.0,
                style="italic", linespacing=1.25)

    arrow(ax, 0.145, 0.678, xl - 0.006, 0.678, lw=1.0, ms=7)
    arrow(ax, 0.145, 0.238, xl - 0.006, 0.238, lw=1.0, ms=7)

    # Primary comparison — visually dominant
    xp = xr + bw / 2
    arrow(ax, xp, 0.615, xp, 0.175 + bh, lw=2.8, style="<|-|>", ms=15)
    ax.text(xp + 0.020, (0.615 + 0.175 + bh) / 2,
            "ПЕРВИЧНОЕ\nСРАВНЕНИЕ\nB ↔ C", ha="left", va="center",
            fontsize=9.6, fontweight="bold", linespacing=1.35)

    # Null control
    xn = xl + bw / 2
    arrow(ax, xn, 0.615, xn, 0.175 + bh, lw=1.0, style="<|-|>", ms=8,
          ls=(0, (4, 2.5)))
    ax.text(xn + 0.014, 0.505,
            "нулевой контроль:\nодно и то же условие,\nвыполненное дважды",
            ha="left", va="center", fontsize=7.2, style="italic",
            linespacing=1.3)

    ax.text(0.50, 0.075,
            "5 повторений в каждой ячейке «программа × условие»;  "
            "всего 600 обращений к модели",
            ha="center", va="center", fontsize=8.4)
    ax.text(0.50, 0.026,
            "Единица анализа — программа: исход Top-K агрегируется "
            "по большинству из пяти повторений",
            ha="center", va="center", fontsize=7.4, style="italic")

    save(fig, "fig3_design")


# --------------------------------------------------------------------------
# Рисунок 4 — Top-K
# --------------------------------------------------------------------------
def figure_4() -> None:
    groups = ["Top-1", "Top-3", "Top-5"]
    vals_b = [40.00, 50.00, 53.33]
    vals_c = [40.00, 60.00, 63.33]
    counts_b = ["12/30", "15/30", "16/30"]
    counts_c = ["12/30", "18/30", "19/30"]

    fig, ax = plt.subplots(figsize=(15.0 * CM, 9.4 * CM))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.30)

    xs = [0, 1, 2]
    bwd = 0.32
    for i, (x, vb, vc) in enumerate(zip(xs, vals_b, vals_c)):
        ax.bar(x - bwd / 2 - 0.012, vb, bwd, facecolor=FILL_B,
               edgecolor=EDGE, linewidth=0.9,
               label="B — общая подсказка" if i == 0 else None)
        ax.bar(x + bwd / 2 + 0.012, vc, bwd, facecolor=FILL_C,
               edgecolor=EDGE, linewidth=0.9,
               label="C — подсказка по паттерну" if i == 0 else None)

    for x, vb, vc, cb, cc in zip(xs, vals_b, vals_c, counts_b, counts_c):
        ax.text(x - bwd / 2 - 0.012, vb + 1.6, f"{vb:.2f}%", ha="center",
                va="bottom", fontsize=8.6, fontweight="bold")
        ax.text(x - bwd / 2 - 0.012, vb + 6.4, cb, ha="center", va="bottom",
                fontsize=7.4)
        ax.text(x + bwd / 2 + 0.012, vc + 1.6, f"{vc:.2f}%", ha="center",
                va="bottom", fontsize=8.6, fontweight="bold")
        ax.text(x + bwd / 2 + 0.012, vc + 6.4, cc, ha="center", va="bottom",
                fontsize=7.4)

    ax.set_xticks(xs)
    ax.set_xticklabels(groups, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylabel("доля программ, %", fontsize=9)
    ax.set_xlim(-0.62, 2.62)
    ax.yaxis.grid(True, linewidth=0.5, color="#bfbfbf", linestyle=(0, (2, 3)))
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    ax.legend(loc="upper left", frameon=False, fontsize=8.4,
              bbox_to_anchor=(0.0, 1.0))

    ax.annotate("первичная метрика:\n$p$ = 1.0, различий не обнаружено",
                xy=(0, 0), xytext=(0, -26), textcoords="offset points",
                xycoords=("data", "axes fraction"), ha="center", va="top",
                fontsize=7.6, fontweight="bold", linespacing=1.3)
    ax.annotate("вторичные, описательные;\nстатистическая значимость не достигнута",
                xy=(1.5, 0), xytext=(0, -26), textcoords="offset points",
                xycoords=("data", "axes fraction"), ha="center", va="top",
                fontsize=7.6, style="italic", linespacing=1.3)

    save(fig, "fig4_topk")


# --------------------------------------------------------------------------
# Рисунок 5 — EXAM*
# --------------------------------------------------------------------------
def figure_5() -> None:
    fig, ax = plt.subplots(figsize=(14.4 * CM, 5.6 * CM))
    fig.subplots_adjust(left=0.275, right=0.955, top=0.86, bottom=0.30)

    labels = ["B — общая подсказка", "C — подсказка по паттерну"]
    vals = [0.510798, 0.445055]
    ys = [1, 0]

    ax.barh(ys[0], vals[0], height=0.46, facecolor=FILL_B, edgecolor=EDGE,
            linewidth=0.9)
    ax.barh(ys[1], vals[1], height=0.46, facecolor=FILL_C, edgecolor=EDGE,
            linewidth=0.9)

    for y, v in zip(ys, vals):
        ax.text(v + 0.012, y, f"{v:.6f}", va="center", ha="left",
                fontsize=9.0, fontweight="bold")

    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, 1.0)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("средняя доля файла, просматриваемая до ошибочной строки\n"
                  "(0 = лучший возможный результат, 1 = худший)",
                  fontsize=8.4, linespacing=1.4)
    ax.set_ylim(-0.6, 1.6)
    ax.xaxis.grid(True, linewidth=0.5, color="#bfbfbf", linestyle=(0, (2, 3)))
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    ax.text(0.995, 1.055, "МЕНЬШЕ  —  ЛУЧШЕ", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=9.4, fontweight="bold")

    save(fig, "fig5_exam")


# --------------------------------------------------------------------------
# Рисунок 6 — гетерогенность по классам
# --------------------------------------------------------------------------
def figure_6() -> None:
    rows = [
        ("Полный перебор", 8, 25.0),
        ("Динамическое программирование", 8, -25.0),
        ("Бинарный поиск", 7, 0.0),
        ("Обход графа (DFS/BFS)", 7, 0.0),
    ]
    fig, ax = plt.subplots(figsize=(15.6 * CM, 7.8 * CM))
    fig.subplots_adjust(left=0.315, right=0.955, top=0.90, bottom=0.38)

    ys = list(range(len(rows)))[::-1]
    for y, (name, n, d) in zip(ys, rows):
        fill = FILL_C if d > 0 else (FILL_B if d < 0 else "#ffffff")
        ax.barh(y, d, height=0.5, facecolor=fill, edgecolor=EDGE, linewidth=0.9)
        if d == 0:
            ax.plot([0], [y], marker="|", color="black", markersize=11,
                    markeredgewidth=1.4)
        text = "0 п.п." if d == 0 else (f"+{d:.0f} п.п." if d > 0
                                        else f"\u2212{abs(d):.0f} п.п.")
        if d >= 0:
            ax.text(d + 2.0, y, text, va="center", ha="left",
                    fontsize=8.8, fontweight="bold")
        else:
            ax.text(d - 2.0, y, text, va="center", ha="right",
                    fontsize=8.8, fontweight="bold")
        ax.text(46.0, y, f"n = {n}", va="center", ha="right", fontsize=8.2)

    ax.axvline(0, color="black", linewidth=1.2)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.8)
    ax.set_xlim(-42, 47)
    ax.set_xticks([-30, -20, -10, 0, 10, 20, 30])
    ax.set_xlabel("изменение Top-1 при переходе от общей подсказки (B)\n"
                  "к подсказке по паттерну (C), процентные пункты",
                  fontsize=8.4, linespacing=1.4)
    ax.set_ylim(-0.7, len(rows) - 0.25)
    ax.xaxis.grid(True, linewidth=0.5, color="#bfbfbf", linestyle=(0, (2, 3)))
    ax.set_axisbelow(True)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)

    ax.text(-41, len(rows) - 0.52, "хуже, чем общая подсказка", fontsize=7.6,
            style="italic", ha="left", va="center")
    ax.text(35, len(rows) - 0.52, "лучше, чем общая подсказка", fontsize=7.6,
            style="italic", ha="right", va="center")

    ax.annotate("Описательные величины; не предназначены для подтверждающего вывода.\n"
                "При 8 программах в классе сдвиг 25 п.п. = разница в две программы. "
                "Инференциальные тесты\nна уровне класса не проводились.",
                xy=(0.5, 0), xytext=(0, -40), textcoords="offset points",
                xycoords="axes fraction", ha="center", va="top",
                fontsize=7.4, style="italic", linespacing=1.4)

    save(fig, "fig6_pattern_heterogeneity")


if __name__ == "__main__":
    figure_1()
    figure_2()
    figure_3()
    figure_4()
    figure_5()
    figure_6()
    print("figures ->", OUT)
