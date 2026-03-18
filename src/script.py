# ============================================================
# TREASURE HUNT: CLASSICAL vs QUANTUM SEARCH
# ============================================================

!pip -q install imageio

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle, Circle, Polygon
from IPython.display import Image, display

# ============================================================
# CONFIGURAÇÕES
# ============================================================

rng = np.random.default_rng(21)

GIF_NAME = "treasure_hunt_6_vs_36_corrected.gif"
FPS = 24
DPI = 180
FIGSIZE = (16, 9)

ROWS, COLS = 6, 6
N = ROWS * COLS
TREASURE = rng.integers(0, N)

QUANTUM_FIND_STEP = 6
CLASSICAL_FIND_STEP = 36

FRAMES_PER_STEP = 6
HOLD_FINAL = 18

TOTAL_STEPS = CLASSICAL_FIND_STEP
MAIN_FRAMES = TOTAL_STEPS * FRAMES_PER_STEP
N_FRAMES = MAIN_FRAMES + HOLD_FINAL

BG = "#05070B"
PANEL = "#09111B"
FG = "#F4F7FF"
SUB = "#AABED5"
EDGE = "#162434"

CLASSICAL = "#64C8F2"
CLASSICAL_CURSOR = "#9EE7FF"

QUANTUM = "#D74D96"
QUANTUM_SOFT = "#2B1622"
QUANTUM_WAVE = "#FF6FB4"

TREASURE_GOLD = "#F4C35A"
TREASURE_EDGE = "#FCE6A2"

OPENED_CELL = "#132332"
DARK_CELL = "#182436"
DARKER = "#0F1722"
EMPTY_MARK = "#7FA9C9"

MEASURED = "#FFFFFF"

PAD = 0.12

WAVE_ALPHA = 0.18
WAVE_THICKNESS = 1.5

# ============================================================
# AUXILIARES
# ============================================================

def hex_to_rgb01(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)]) / 255.0

def rgb01_to_hex(rgb):
    rgb = np.clip(rgb, 0, 1)
    return "#{:02x}{:02x}{:02x}".format(*(rgb * 255).astype(int))

def blend(c1, c2, t):
    a = hex_to_rgb01(c1)
    b = hex_to_rgb01(c2)
    return rgb01_to_hex(a + (b - a) * np.clip(t, 0, 1))

def smootherstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * t * (t * (t * 6 - 15) + 10)

def draw_treasure_icon(ax, cx, cy, scale=0.22, alpha=1.0, color=TREASURE_GOLD, z=10):
    base = Rectangle(
        (cx - scale, cy - scale * 0.42),
        2 * scale, scale * 0.84,
        facecolor=color, edgecolor=TREASURE_EDGE,
        linewidth=1.0, alpha=alpha, zorder=z
    )
    lid = Rectangle(
        (cx - scale, cy + scale * 0.05),
        2 * scale, scale * 0.50,
        facecolor=blend(color, "#FFFFFF", 0.08),
        edgecolor=TREASURE_EDGE, linewidth=0.9,
        alpha=alpha, zorder=z + 1
    )
    lock = Circle(
        (cx, cy - scale * 0.02),
        radius=scale * 0.13,
        facecolor="#5B3D00", edgecolor="#FFF0B3",
        linewidth=0.7, alpha=alpha, zorder=z + 2
    )
    ax.add_patch(base)
    ax.add_patch(lid)
    ax.add_patch(lock)
    return [base, lid, lock]

def draw_empty_mark(ax, cx, cy, scale=0.16, alpha=0.65, color=EMPTY_MARK, z=8):
    l1 = ax.plot(
        [cx - scale, cx + scale],
        [cy - scale, cy + scale],
        color=color, lw=1.0, alpha=alpha, zorder=z
    )[0]
    l2 = ax.plot(
        [cx - scale, cx + scale],
        [cy + scale, cy - scale],
        color=color, lw=1.0, alpha=alpha, zorder=z
    )[0]
    return [l1, l2]

# ============================================================
# POSIÇÕES DA GRADE
# ============================================================

grid_positions = []
for r in range(ROWS):
    for c in range(COLS):
        grid_positions.append((c, ROWS - 1 - r))
grid_positions = np.array(grid_positions, dtype=float)

# ============================================================
# CLÁSSICO
# ============================================================

classical_order = rng.permutation(N)
treasure_idx_in_order = np.where(classical_order == TREASURE)[0][0]
target_slot = CLASSICAL_FIND_STEP - 1
classical_order[treasure_idx_in_order], classical_order[target_slot] = (
    classical_order[target_slot],
    classical_order[treasure_idx_in_order]
)

# ============================================================
# QUÂNTICO
# ============================================================

q_target_probs = np.zeros(TOTAL_STEPS + 1)
for s in range(TOTAL_STEPS + 1):
    if s <= QUANTUM_FIND_STEP:
        t = s / QUANTUM_FIND_STEP
        q_target_probs[s] = 0.03 + 0.94 * smootherstep(t)
    else:
        q_target_probs[s] = 0.97

def quantum_distribution_for_step(step):
    p_target = q_target_probs[step]
    rest = (1.0 - p_target) / (N - 1)
    p = np.full(N, rest, dtype=float)
    p[TREASURE] = p_target
    return p

# ============================================================
# FIGURA
# ============================================================

plt.close("all")
fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=BG)
gs = fig.add_gridspec(
    3, 2,
    height_ratios=[12, 2.2, 2.0],
    width_ratios=[1, 1],
    wspace=0.08, hspace=0.10
)

ax_c = fig.add_subplot(gs[0, 0])
ax_q = fig.add_subplot(gs[0, 1])
ax_prob = fig.add_subplot(gs[1, :])
ax_work = fig.add_subplot(gs[2, :])

for ax in [ax_c, ax_q, ax_prob, ax_work]:
    ax.set_facecolor(PANEL)
    for s in ax.spines.values():
        s.set_visible(False)

for ax in [ax_c, ax_q]:
    ax.set_xlim(-0.35, COLS + 0.35)
    ax.set_ylim(-0.35, ROWS + 0.35)
    ax.set_xticks([])
    ax.set_yticks([])

for ax in [ax_prob, ax_work]:
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.text(
    0.5, 0.978,
    "Treasure Hunt: Classical vs Quantum Search",
    ha="center", va="top",
    color=FG, fontsize=22, fontweight="bold"
)

ax_c.set_title("Busca clássica", color="#C7D5E5", fontsize=14.5, pad=10)
ax_q.set_title("Busca quântica", color="#C7D5E5", fontsize=14.5, pad=10)

# ============================================================
# GRADE
# ============================================================

class_rects = []
quant_rects = []

for i in range(N):
    x, y = grid_positions[i]

    rc = Rectangle(
        (x + PAD/2, y + PAD/2), 1 - PAD, 1 - PAD,
        facecolor=DARK_CELL, edgecolor=EDGE, linewidth=0.9
    )
    rq = Rectangle(
        (x + PAD/2, y + PAD/2), 1 - PAD, 1 - PAD,
        facecolor=DARK_CELL, edgecolor=EDGE, linewidth=0.9
    )

    ax_c.add_patch(rc)
    ax_q.add_patch(rq)

    class_rects.append(rc)
    quant_rects.append(rq)

cursor = Rectangle((0, 0), 1 - PAD, 1 - PAD, fill=False, edgecolor=CLASSICAL_CURSOR, linewidth=2.2)
cursor_glow = Rectangle((0, 0), 1 - PAD, 1 - PAD, fill=False, edgecolor=CLASSICAL_CURSOR, linewidth=6.5, alpha=0.08)
ax_c.add_patch(cursor_glow)
ax_c.add_patch(cursor)

magnifier_ring = Circle((0, 0), radius=0.18, fill=False, edgecolor=CLASSICAL_CURSOR, linewidth=2.1, alpha=0.98)
magnifier_handle = ax_c.plot([], [], color=CLASSICAL_CURSOR, lw=2.0, alpha=0.98)[0]
ax_c.add_patch(magnifier_ring)

measure_box = Rectangle((0, 0), 1 - PAD, 1 - PAD, fill=False, edgecolor=MEASURED, linewidth=0.0, alpha=0.0)
measure_glow = Rectangle((0, 0), 1 - PAD, 1 - PAD, fill=False, edgecolor=MEASURED, linewidth=0.0, alpha=0.0)
ax_q.add_patch(measure_glow)
ax_q.add_patch(measure_box)

wave_poly = Polygon(
    [[0, 0], [0, 0], [0, 0], [0, 0]],
    closed=True,
    facecolor=QUANTUM_WAVE,
    edgecolor="none",
    alpha=0.0,
    zorder=0.35
)
ax_q.add_patch(wave_poly)

class_info = ax_c.text(0.02, 0.96, "", transform=ax_c.transAxes, color=FG, fontsize=11.5, va="top")
quant_info = ax_q.text(0.02, 0.96, "", transform=ax_q.transAxes, color=FG, fontsize=11.5, va="top")
quant_phase = ax_q.text(0.98, 0.96, "", transform=ax_q.transAxes, color=SUB, fontsize=10.5, va="top", ha="right")

# ============================================================
# PAINÉIS INFERIORES
# ============================================================

ax_prob.text(5, 7.8, "Probabilidade de sucesso", color=FG, fontsize=14, fontweight="bold")

prob_bg_left = Rectangle((5, 4.0), 38, 1.55, facecolor=DARKER, edgecolor=EDGE, linewidth=1.0)
prob_bg_right = Rectangle((57, 4.0), 38, 1.55, facecolor=DARKER, edgecolor=EDGE, linewidth=1.0)
ax_prob.add_patch(prob_bg_left)
ax_prob.add_patch(prob_bg_right)

prob_fill_left = Rectangle((5, 4.0), 0, 1.55, facecolor=CLASSICAL, edgecolor="none")
prob_fill_right = Rectangle((57, 4.0), 0, 1.55, facecolor=QUANTUM, edgecolor="none")
ax_prob.add_patch(prob_fill_left)
ax_prob.add_patch(prob_fill_right)

ax_prob.text(5, 6.45, "Clássico", color=FG, fontsize=11.5, fontweight="bold")
ax_prob.text(57, 6.45, "Quântico", color=FG, fontsize=11.5, fontweight="bold")

prob_text_left = ax_prob.text(5, 1.7, "", color=CLASSICAL, fontsize=11.5)
prob_text_right = ax_prob.text(57, 1.7, "", color=QUANTUM, fontsize=11.5)

ax_work.text(5, 7.8, "Esforço usado", color=FG, fontsize=14, fontweight="bold")

work_bg_left = Rectangle((5, 4.0), 38, 1.55, facecolor=DARKER, edgecolor=EDGE, linewidth=1.0)
work_bg_right = Rectangle((57, 4.0), 38, 1.55, facecolor=DARKER, edgecolor=EDGE, linewidth=1.0)
ax_work.add_patch(work_bg_left)
ax_work.add_patch(work_bg_right)

work_fill_left = Rectangle((5, 4.0), 0, 1.55, facecolor=CLASSICAL, edgecolor="none")
work_fill_right = Rectangle((57, 4.0), 0, 1.55, facecolor=QUANTUM, edgecolor="none")
ax_work.add_patch(work_fill_left)
ax_work.add_patch(work_fill_right)

ax_work.text(5, 6.45, "Passos clássicos", color=FG, fontsize=11.5, fontweight="bold")
ax_work.text(57, 6.45, "Passos quânticos", color=FG, fontsize=11.5, fontweight="bold")

work_text_left = ax_work.text(5, 1.7, "", color=CLASSICAL, fontsize=11.5)
work_text_right = ax_work.text(57, 1.7, "", color=QUANTUM, fontsize=11.5)

bottom_message = ax_work.text(
    50, 0.9,
    "",
    ha="center",
    color="#DDE9F5",
    fontsize=13.2,
    fontweight="bold"
)

# ============================================================
# DINÂMICOS
# ============================================================

quant_treasure_artists = []
class_treasure_artists = []
class_empty_marks = []

def clear_artists(lst):
    for artist in lst:
        try:
            if isinstance(artist, list):
                for a in artist:
                    a.remove()
            else:
                artist.remove()
        except Exception:
            pass
    lst.clear()

# ============================================================
# UPDATE
# ============================================================

def update(frame):
    global quant_treasure_artists, class_treasure_artists, class_empty_marks

    clear_artists(quant_treasure_artists)
    clear_artists(class_treasure_artists)
    clear_artists(class_empty_marks)

    if frame < MAIN_FRAMES:
        step_cont = frame / FRAMES_PER_STEP
    else:
        step_cont = TOTAL_STEPS

    # --------------------------------------------------------
    # CLÁSSICO
    # --------------------------------------------------------
    c_step_cont = min(step_cont, CLASSICAL_FIND_STEP)
    c_step_int = int(np.floor(c_step_cont))
    c_frac = c_step_cont - c_step_int
    checked_items = classical_order[:c_step_int]

    for r in class_rects:
        r.set_facecolor(DARK_CELL)
        r.set_edgecolor(EDGE)
        r.set_linewidth(0.9)

    for idx in checked_items:
        if idx != TREASURE:
            class_rects[idx].set_facecolor(OPENED_CELL)
            class_rects[idx].set_edgecolor(blend(OPENED_CELL, CLASSICAL, 0.26))
            x, y = grid_positions[idx]
            class_empty_marks.extend(draw_empty_mark(ax_c, x + 0.5, y + 0.5, alpha=0.42))

    current_idx = classical_order[min(c_step_int, N - 1)]
    found_classical = c_step_cont >= CLASSICAL_FIND_STEP

    if not found_classical:
        class_rects[current_idx].set_facecolor(blend(DARK_CELL, CLASSICAL, 0.18))
        class_rects[current_idx].set_edgecolor(CLASSICAL_CURSOR)

    start_idx = classical_order[max(c_step_int - 1, 0)]
    end_idx = classical_order[min(c_step_int, N - 1)]
    sx, sy = grid_positions[start_idx]
    ex, ey = grid_positions[end_idx]
    tt = smootherstep(c_frac)
    cx = (1 - tt) * sx + tt * ex
    cy = (1 - tt) * sy + tt * ey

    if found_classical:
        tx, ty = grid_positions[TREASURE]
        cx, cy = tx, ty
        class_rects[TREASURE].set_facecolor(blend("#59411B", TREASURE_GOLD, 0.96))
        class_rects[TREASURE].set_edgecolor(TREASURE_EDGE)
        class_rects[TREASURE].set_linewidth(2.4)
        class_treasure_artists = draw_treasure_icon(
            ax_c, tx + 0.5, ty + 0.5, scale=0.18, alpha=1.0, z=20
        )

    cursor.set_xy((cx + PAD/2, cy + PAD/2))
    cursor_glow.set_xy((cx + PAD/2, cy + PAD/2))

    magnifier_ring.center = (cx + 0.43, cy + 0.57)
    magnifier_handle.set_data(
        [cx + 0.56, cx + 0.74],
        [cy + 0.43, cy + 0.25]
    )

    class_info.set_text(
        f"passo: {min(c_step_cont, CLASSICAL_FIND_STEP):.1f}/36\n" +
        ("tesouro encontrado" if found_classical else "procurando")
    )

    p_class = min(c_step_cont / CLASSICAL_FIND_STEP, 1.0)

    # --------------------------------------------------------
    # QUÂNTICO
    # --------------------------------------------------------
    q_step_cont = min(step_cont, QUANTUM_FIND_STEP)
    q_step_floor = int(np.floor(q_step_cont))
    q_step_ceil = min(q_step_floor + 1, TOTAL_STEPS)
    alpha_q = smootherstep(q_step_cont - q_step_floor)

    p0 = quantum_distribution_for_step(q_step_floor)
    p1 = quantum_distribution_for_step(q_step_ceil)
    p_quant = (1 - alpha_q) * p0 + alpha_q * p1
    p_quant = p_quant / p_quant.sum()

    if q_step_cont < QUANTUM_FIND_STEP:
        prog = q_step_cont / QUANTUM_FIND_STEP
        center = -1.2 + (COLS + ROWS + 2.4) * prog

        s0 = center - WAVE_THICKNESS / 2
        s1 = center + WAVE_THICKNESS / 2
        pts = np.array([
            [-1.0, s0 + 1.0],
            [s0 + 1.0, -1.0],
            [s1 + 1.0, -1.0],
            [-1.0, s1 + 1.0],
        ])
        wave_poly.set_xy(pts)
        wave_poly.set_alpha(WAVE_ALPHA)
    else:
        wave_poly.set_alpha(0.0)

    pmax = p_quant.max()
    for i, r in enumerate(quant_rects):
        x, y = grid_positions[i]
        xc = x + 0.5
        yc = y + 0.5

        if q_step_cont < QUANTUM_FIND_STEP:
            diag_dist = abs((xc + yc) - center)
            wave_local = np.exp(-(diag_dist ** 2) / 0.55)
        else:
            wave_local = 0.0

        strength = p_quant[i] / max(pmax, 1e-12)
        base_mix = 0.08 + 0.12 * strength + 0.22 * wave_local

        r.set_facecolor(blend(DARK_CELL, QUANTUM_SOFT, base_mix))
        r.set_edgecolor(blend(EDGE, QUANTUM, 0.10 + 0.16 * wave_local))
        r.set_linewidth(0.9)

    q_found = q_step_cont >= QUANTUM_FIND_STEP

    if q_found:
        mx, my = grid_positions[TREASURE]
        measure_box.set_xy((mx + PAD/2, my + PAD/2))
        measure_glow.set_xy((mx + PAD/2, my + PAD/2))
        measure_box.set_alpha(1.0)
        measure_glow.set_alpha(0.18)
        measure_box.set_linewidth(3.2)
        measure_glow.set_linewidth(8.5)

        quant_rects[TREASURE].set_facecolor(blend(QUANTUM, TREASURE_GOLD, 0.92))
        quant_rects[TREASURE].set_edgecolor(MEASURED)
        quant_rects[TREASURE].set_linewidth(2.8)

        quant_treasure_artists = draw_treasure_icon(
            ax_q, mx + 0.5, my + 0.5, scale=0.18, alpha=1.0, z=20
        )

        quant_info.set_text("passo: 6.0/6\ntesouro encontrado")
        quant_phase.set_text("resultado final")
    else:
        measure_box.set_alpha(0.0)
        measure_glow.set_alpha(0.0)
        measure_box.set_linewidth(0.0)
        measure_glow.set_linewidth(0.0)

        quant_info.set_text(
            f"passo: {q_step_cont:.1f}/6\n"
            f"chance no alvo: {p_quant[TREASURE]:.3f}"
        )
        quant_phase.set_text("evolução global")

    if q_found:
        q_success = 1.0
    else:
        q_success = p_quant[TREASURE]

    q_work = min(q_step_cont / CLASSICAL_FIND_STEP, 1.0)

    # --------------------------------------------------------
    # PAINÉIS INFERIORES
    # --------------------------------------------------------
    prob_fill_left.set_width(38 * p_class)
    prob_fill_right.set_width(38 * q_success)

    prob_text_left.set_text(f"{p_class:.3f}")
    prob_text_right.set_text(f"{q_success:.3f}")

    c_work = min(c_step_cont / CLASSICAL_FIND_STEP, 1.0)
    work_fill_left.set_width(38 * c_work)
    work_fill_right.set_width(38 * q_work)

    work_text_left.set_text(f"{min(c_step_cont, CLASSICAL_FIND_STEP):.1f}")
    work_text_right.set_text(f"{min(q_step_cont, QUANTUM_FIND_STEP):.1f}")

    
    return (
        cursor, cursor_glow, magnifier_ring, magnifier_handle,
        measure_box, measure_glow, wave_poly,
        class_info, quant_info, quant_phase,
        prob_fill_left, prob_fill_right,
        prob_text_left, prob_text_right,
        work_fill_left, work_fill_right,
        work_text_left, work_text_right,
        bottom_message
    )

# ============================================================
# ANIMAÇÃO
# ============================================================

anim = FuncAnimation(
    fig,
    update,
    frames=N_FRAMES,
    interval=1000 // FPS,
    blit=False
)

anim.save(GIF_NAME, writer=PillowWriter(fps=FPS), dpi=DPI)
plt.close(fig)

print("GIF salvo como:", GIF_NAME)
display(Image(filename=GIF_NAME))
