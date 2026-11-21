"""Redrawn network diagrams for topics/enterprise-networking/00-intro-to-networking.md
Run: python tools/net_diagrams.py   ->  images/enterprise-networking/*.png"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch, Ellipse

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "enterprise-networking")
os.makedirs(OUT, exist_ok=True)

NAVY, BLUE, MID, SKY, CARD, LINE, WARM, RED = "#0B1626", "#2474D1", "#4A9FE8", "#BFE0FA", "#F4F7FB", "#2A3B55", "#F6C99B", "#C9364A"
FONT = "DejaVu Sans Mono"


def canvas(w, h, size=(9, 5)):
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.set_aspect("equal"); ax.axis("off")
    fig.patch.set_facecolor(CARD)
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=130, bbox_inches="tight", facecolor=CARD, pad_inches=0.15)
    plt.close(fig)


def text(ax, x, y, s, size=10, color=NAVY, ha="center", va="center", weight="normal", **kw):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, family=FONT, **kw)


def line(ax, pts, color=LINE, lw=1.6, z=1, ls="-"):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, zorder=z, linestyle=ls, solid_capstyle="round")


def arrow(ax, a, b, color=NAVY, lw=1.5, style="-|>", ms=11, z=3, both=False):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="<|-|>" if both else style, mutation_scale=ms, color=color, lw=lw, zorder=z, shrinkA=0, shrinkB=0))


def box(ax, x, y, w, h, fc=CARD, ec=NAVY, lw=1.4, r=0.5, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))


# ----------------------------- device icons (centre x, y) -----------------------------
def pc(ax, x, y, label=None, s=1.0, below=True, size=9):
    ax.add_patch(FancyBboxPatch((x - 2.2 * s, y - 1.2 * s), 4.4 * s, 3.2 * s, boxstyle="round,pad=0,rounding_size=0.3", fc="#DCE6F2", ec=NAVY, lw=1.3, zorder=4))
    ax.add_patch(Rectangle((x - 1.7 * s, y - 0.7 * s), 3.4 * s, 2.2 * s, fc=NAVY, ec="none", zorder=5))
    ax.add_patch(Rectangle((x - 0.4 * s, y - 1.9 * s), 0.8 * s, 0.7 * s, fc="#DCE6F2", ec=NAVY, lw=1, zorder=4))
    ax.add_patch(Rectangle((x - 1.5 * s, y - 2.3 * s), 3.0 * s, 0.45 * s, fc="#DCE6F2", ec=NAVY, lw=1, zorder=4))
    if label:
        text(ax, x, y - (3.5 * s if below else -3.6 * s), label, size)


def switch(ax, x, y, label=None, s=1.0, size=9, below=True):
    ax.add_patch(FancyBboxPatch((x - 3 * s, y - 1.1 * s), 6 * s, 2.2 * s, boxstyle="round,pad=0,rounding_size=0.35", fc=BLUE, ec=NAVY, lw=1.3, zorder=4))
    for dy, dx in ((0.35, 1), (-0.45, -1)):
        arrow(ax, (x - 1.9 * s * dx, y + dy * s), (x + 1.9 * s * dx, y + dy * s), color="white", lw=1.4, ms=8, z=6)
    if label:
        text(ax, x, y - (2.3 * s if below else -2.4 * s), label, size)


def router(ax, x, y, label=None, s=1.0, size=9, below=True):
    ax.add_patch(Circle((x, y), 2.0 * s, fc=BLUE, ec=NAVY, lw=1.3, zorder=4))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        arrow(ax, (x + 0.35 * dx * s, y + 0.35 * dy * s), (x + 1.45 * dx * s, y + 1.45 * dy * s), color="white", lw=1.2, ms=7, z=6)
    if label:
        text(ax, x, y - (3.2 * s if below else -3.3 * s), label, size)


def server(ax, x, y, label=None, s=1.0, size=9, below=True):
    ax.add_patch(FancyBboxPatch((x - 1.6 * s, y - 2.4 * s), 3.2 * s, 4.8 * s, boxstyle="round,pad=0,rounding_size=0.25", fc="#DCE6F2", ec=NAVY, lw=1.3, zorder=4))
    for k in range(3):
        ax.add_patch(Rectangle((x - 1.1 * s, y + (1.2 - 1.0 * k) * s), 2.2 * s, 0.5 * s, fc="white", ec=NAVY, lw=0.8, zorder=5))
    if label:
        text(ax, x, y - (3.6 * s if below else -3.6 * s), label, size)


def laptop(ax, x, y, label=None, s=1.0, size=9):
    ax.add_patch(Rectangle((x - 1.8 * s, y - 0.3 * s), 3.6 * s, 2.4 * s, fc=NAVY, ec=NAVY, zorder=5))
    ax.add_patch(Polygon([(x - 2.4 * s, y - 0.3 * s), (x + 2.4 * s, y - 0.3 * s), (x + 2.0 * s, y - 1.1 * s), (x - 2.0 * s, y - 1.1 * s)], fc="#DCE6F2", ec=NAVY, zorder=4))
    if label:
        text(ax, x, y - 2.4 * s, label, size)


def printer(ax, x, y, label=None, s=1.0, size=9):
    ax.add_patch(FancyBboxPatch((x - 2 * s, y - 1 * s), 4 * s, 2 * s, boxstyle="round,pad=0,rounding_size=0.2", fc="#DCE6F2", ec=NAVY, lw=1.2, zorder=4))
    ax.add_patch(Rectangle((x - 1.2 * s, y + 1 * s), 2.4 * s, 1.1 * s, fc="white", ec=NAVY, lw=1, zorder=4))
    if label:
        text(ax, x, y - 2.2 * s, label, size)


def cloud(ax, x, y, w, h):
    ax.add_patch(Ellipse((x, y), w, h, fc="#E4EDF8", ec="#9FB3CC", lw=1.2, zorder=0))


# =================================== HANDWRITTEN NOTES ===================================
def notes_bus():
    fig, ax = canvas(60, 20, (8, 3.2))
    line(ax, [(2, 10), (58, 10)], lw=2.2)
    arrow(ax, (2, 10), (1, 10), ms=10); arrow(ax, (58, 10), (59, 10), ms=10)
    for x, up, n in ((10, False, "A"), (18, True, "B"), (26, True, "C"), (36, False, "D"), (46, True, "E"), (54, False, "F")):
        y2 = 15 if up else 5
        line(ax, [(x, 10), (x, y2)])
        ax.add_patch(Circle((x, y2 + (1 if up else -1)), 1.0, fc="white", ec=NAVY, lw=1.4, zorder=4))
        text(ax, x - 2.0, y2 + (2.4 if up else -2.4), n, 11, weight="bold")
    save(fig, "notes-bus.png")


def notes_star():
    fig, ax = canvas(70, 56, (7.4, 5.8))
    cx, cy = 35, 28
    subs = [(12, 42, [(-8, 5), (0, 8), (8, 5)]), (58, 42, [(-8, 5), (0, 8), (8, 5)]), (35, 12, [(-10, -4), (0, -7), (10, -4)])]
    for sx, sy, offs in subs:
        line(ax, [(cx, cy), (sx, sy)], lw=2)
    switch(ax, cx, cy, s=1.2)
    for sx, sy, offs in subs:
        switch(ax, sx, sy, s=0.9)
        for dx, dy in offs:
            line(ax, [(sx, sy), (sx + dx, sy + dy)])
            ax.add_patch(Circle((sx + dx, sy + dy), 1.5, fc="white", ec=NAVY, lw=1.4, zorder=4))
    text(ax, cx + 9, cy, "central switch", 8.5, color=LINE, ha="left")
    save(fig, "notes-star.png")


def _pent(ax, cx, cy, r):
    import math
    return [(cx + r * math.cos(math.radians(90 + 72 * k)), cy + r * math.sin(math.radians(90 + 72 * k))) for k in range(5)]


def _mesh(links, name):
    fig, ax = canvas(40, 36, (4.8, 4.3))
    pts = _pent(ax, 20, 18, 14)
    for i, j in links:
        line(ax, [pts[i], pts[j]], lw=1.6)
    for k, p in enumerate(pts):
        ax.add_patch(Circle(p, 2.4, fc="white", ec=NAVY, lw=1.6, zorder=5))
        text(ax, p[0], p[1], "ABCDE"[k], 10, weight="bold", zorder=6)
    save(fig, name)


def notes_mesh():
    _mesh([(i, j) for i in range(5) for j in range(i + 1, 5)], "notes-mesh.png")
    _mesh([(0, 1), (1, 2), (2, 3), (3, 4), (0, 2), (1, 4)], "notes-partial-mesh.png")


def notes_handshake():
    fig, ax = canvas(60, 26, (7, 3.2))
    text(ax, 5, 22, "Sender", 11, weight="bold"); text(ax, 55, 22, "Receiver", 11, weight="bold")
    line(ax, [(5, 19), (5, 2)], lw=1.2, ls="--"); line(ax, [(55, 19), (55, 2)], lw=1.2, ls="--")
    for y, a, b, lab in ((16, 5, 55, "SYN"), (10, 55, 5, "SYN ACK"), (4, 5, 55, "ACK")):
        arrow(ax, (a, y), (b, y), lw=1.8, ms=12)
        text(ax, 30, y + 2, lab, 10, weight="bold")
    save(fig, "notes-handshake.png")


def notes_frame():
    fig, ax = canvas(96, 28, (9.6, 2.8))
    cells = [("FCS", 0, 16), ("@src", 16, 14), ("@dst", 30, 14), ("message", 44, 28)]
    for lab, x, w in cells:
        ax.add_patch(Rectangle((8 + x, 10), w, 8, fc="white", ec=NAVY, lw=1.6, zorder=3))
        text(ax, 8 + x + w / 2, 14, lab, 10, weight="bold")
    text(ax, 16, 22, "Frame Check Sequence", 8.5, color=LINE)
    text(ax, 45, 22, "MAC", 10, weight="bold")
    line(ax, [(24, 8), (24, 6), (52, 6), (52, 8)], lw=1.2)
    text(ax, 38, 3, "headers", 9, color=LINE)
    text(ax, 91, 14, "Layer 2", 9.5, color=LINE)
    arrow(ax, (87, 14), (82, 14), lw=1.2, ms=9)
    save(fig, "notes-frame.png")


def notes_dns():
    fig, ax = canvas(100, 36, (9.4, 3.4))
    pc(ax, 8, 18, "User", s=1.0); server(ax, 50, 18, "DNS server", s=0.9); server(ax, 92, 18, "facebook.com web server", s=0.9)
    arrow(ax, (14, 24), (44, 24), lw=1.6); text(ax, 29, 27, "1  facebook.com ?", 9)
    arrow(ax, (44, 19), (14, 19), lw=1.6); text(ax, 29, 16, "2  IP address", 9)
    arrow(ax, (14, 32), (86, 32), lw=1.6, color=BLUE); text(ax, 50, 35, "3  the user connects to that IP address", 9, color=BLUE)
    save(fig, "notes-dns.png")


def osi_vs_tcpip():
    fig, ax = canvas(100, 78, (7.6, 6.0))
    text(ax, 24, 74, "OSI model", 13, weight="bold"); text(ax, 74, 74, "TCP/IP model", 13, weight="bold")
    osi = [("7", "Application", "#D98B73"), ("6", "Presentation", "#F0A93B"), ("5", "Session", "#8DB55A"), ("4", "Transport", "#7FCB92"),
           ("3", "Network", "#79A7CE"), ("2", "Data link", "#7C86C8"), ("1", "Physical", "#A07CC9")]
    h, gap = 8.4, 1.6
    ys = {}
    for i, (n, name, col) in enumerate(osi):
        y = 62 - i * (h + gap)
        ys[n] = y
        box(ax, 8, y, 34, h, fc=col, ec=NAVY, lw=1.3, r=0.8)
        text(ax, 25, y + h / 2, name, 10.5, color="white", weight="bold")
        ax.add_patch(Circle((3.2, y + h / 2), 2.2, fc="white", ec=NAVY, lw=1.2, zorder=4))
        text(ax, 3.2, y + h / 2, n, 9.5, weight="bold", zorder=5)
    groups = [("Application", ["7", "6", "5"], "#8DB55A"), ("Transport", ["4"], "#7FCB92"), ("Internet", ["3"], "#79A7CE"), ("Network access", ["2", "1"], "#7C86C8")]
    for name, ls, col in groups:
        top = ys[ls[0]] + h
        bot = ys[ls[-1]]
        box(ax, 58, bot, 34, top - bot, fc=col, ec=NAVY, lw=1.3, r=0.8)
        text(ax, 75, (top + bot) / 2, name, 10.5, color="white", weight="bold")
    save(fig, "osi-vs-tcpip.png")


def flooding():
    fig, ax = canvas(90, 44, (8.6, 4.2))
    sx, sy = 45, 26
    xs = [(8, "PC-A"), (32, "PC-B"), (58, "PC-C"), (82, "PC-D")]
    for k, (x, lab) in enumerate(xs):
        line(ax, [(sx, sy), (x, 9)], color=RED, lw=1.6)
        fx, fy = sx + (x - sx) * 0.3, sy + (9 - sy) * 0.3
        text(ax, fx + (-3 if x < sx else 3), fy + 1, f"Fa0/{k + 1}", 8.5, ha="right" if x < sx else "left")
        if k:
            arrow(ax, (sx + (x - sx) * 0.45, sy + (9 - sy) * 0.45), (sx + (x - sx) * 0.9, sy + (9 - sy) * 0.9), lw=1.8, color=BLUE, ms=10)
    switch(ax, sx, sy, s=1.5)
    for x, lab in xs:
        pc(ax, x, 6, lab, s=0.9, below=False)
    text(ax, 8, 0.5, "sends to PC-C", 8.5, color=LINE)
    text(ax, 32, 0.5, "ignores", 8.5, color=LINE); text(ax, 58, 0.5, "ACCEPTS", 9, color=BLUE, weight="bold"); text(ax, 82, 0.5, "ignores", 8.5, color=LINE)
    text(ax, 45, 38, "PC-C is unknown: FLOOD", 10, weight="bold")
    text(ax, 45, 35, "(out of every port except Fa0/1)", 8.5, color=LINE)
    save(fig, "flooding.png")


def forward_flow():
    fig, ax = canvas(80, 54, (7.2, 4.9))
    def b(x, y, w, h, t, fc="white"):
        box(ax, x, y, w, h, fc=fc, r=1.2); text(ax, x + w / 2, y + h / 2, t, 8.8)
    b(20, 46, 40, 6, "Frame arrives on port X", "#DCE6F2")
    b(14, 34, 52, 8, "Learn: write (X, source MAC)\nif it is not already in the table")
    b(20, 22, 40, 7, "Is the destination MAC\nin the table?", "#F8E58B")
    b(2, 4, 34, 11, "YES: send ONLY out of that\nport (drop it if it is port X)", "#CFE8D5")
    b(44, 4, 34, 11, "NO, or broadcast: FLOODING\nout of ALL ports except X", "#F6D0D5")
    arrow(ax, (40, 46), (40, 42)); arrow(ax, (40, 34), (40, 29)); arrow(ax, (30, 22), (19, 15)); arrow(ax, (50, 22), (61, 15))
    text(ax, 21, 19.5, "YES", 8.5, weight="bold"); text(ax, 59, 19.5, "NO", 8.5, weight="bold")
    save(fig, "forward-flow.png")


def _stack(ax, ox, oy, up_arrow, who):
    w = 12
    layers = ["Application", "Transport", "Internet", "Network Access"]
    for i, n in enumerate(layers):
        box(ax, ox, oy - i * 5, 26, 5, fc="#EEF3FA", r=0.2, ec=NAVY)
        text(ax, ox + 13, oy - i * 5 + 2.5, n, 9.5)
    arrow(ax, (ox - 2, oy + (-17.5 if up_arrow else 4.5)), (ox - 2, oy + (4.5 if up_arrow else -17.5)), lw=1.6, ms=11)
    return layers


def encap(name, receiver):
    fig, ax = canvas(120, 52, (10, 4.3))
    _stack(ax, 6, 36, receiver, "")
    bx = 42
    text(ax, 100, 48.5, "Receiver" if receiver else "Sender", 10, weight="bold")
    pc(ax, 100, 41, s=1.2)
    rows = [  # (y, headers present)
        (31, []), (26, ["L4"]), (21, ["L3", "L4"]), (16, ["L2", "L3", "L4"])]
    for y, hs in rows:
        x = bx + (3 - len(hs)) * 7
        for h in hs:
            ax.add_patch(Rectangle((x, y), 7, 5, fc=SKY, ec=NAVY, lw=1.2)); text(ax, x + 3.5, y + 2.5, f"{h}\nHDR", 7.5); x += 7
        if hs:
            ax.add_patch(Rectangle((x, y), 22, 5, fc=SKY, ec=NAVY, lw=1.2)); text(ax, x + 11, y + 2.5, "Other HDR", 9); x += 22
        ax.add_patch(Rectangle((x, y), 20, 5, fc=BLUE, ec=NAVY, lw=1.2)); text(ax, x + 10, y + 2.5, "User Data", 9, color="white")
        if len(hs) == 3:
            ax.add_patch(Rectangle((x + 20, y), 8, 5, fc=SKY, ec=NAVY, lw=1.2)); text(ax, x + 24, y + 2.5, "FCS", 9)
    box(ax, 88, 8, 24, 5, r=0.2); text(ax, 100, 10.5, "HDR = Header", 9)
    save(fig, name)


def peer():
    fig, ax = canvas(120, 42, (10, 3.6))
    layers = [("Application", "Data"), ("Transport", "Segment"), ("Network", "Packet"), ("Link", "Frame")]
    text(ax, 14, 39, "Sender", 10, weight="bold"); text(ax, 106, 39, "Receiver", 10, weight="bold")
    text(ax, 60, 39, "PDUs", 10, weight="bold")
    for i, (lay, pdu) in enumerate(layers):
        y = 28 - i * 6
        for x in (4, 76):
            box(ax, x, y, 36, 5.2, fc="#EEF3FA", r=0.2); text(ax, x + 18, y + 2.6, lay, 10)
        line(ax, [(40, y + 2.6), (76, y + 2.6)], lw=1.2, ls="--")
        text(ax, 58, y + 4.6, pdu, 9)
    arrow(ax, (2, 31), (2, 8), lw=1.6); arrow(ax, (118, 8), (118, 31), lw=1.6)
    arrow(ax, (14, 3), (106, 3), lw=1.6)
    save(fig, "peer-to-peer.png")


def lan():
    fig, ax = canvas(120, 46, (10, 3.9))
    cloud(ax, 25, 24, 46, 32); cloud(ax, 85, 24, 64, 40)
    switch(ax, 25, 33, s=0.9)
    for x in (13, 25, 37):
        line(ax, [(25, 33), (x, 20)], color=RED, lw=1.4)
    pc(ax, 13, 20, s=0.8); server(ax, 25, 19, s=0.7); pc(ax, 37, 20, s=0.8)
    text(ax, 25, 3, "Small Office LAN", 9.5)
    sw = [(85, 25), (68, 33), (102, 33), (70, 15), (100, 15)]
    for a, b in ((0, 1), (0, 2), (0, 3), (0, 4)):
        line(ax, [sw[a], sw[b]], color=RED, lw=1.4)
    for p in sw:
        switch(ax, *p, s=0.7)
    devs = [((61, 41), (68, 33), "pc"), ((75, 43), (68, 33), "pc"), ((110, 43), (102, 33), "lap"), ((112, 33), (102, 33), "pc"),
            ((58, 25), (68, 33), "pr"), ((59, 11), (70, 15), "pc"), ((72, 6), (70, 15), "srv"), ((111, 15), (100, 15), "pc")]
    for p, a, k in devs:
        line(ax, [a, p], color=RED, lw=1.3)
        {"pc": lambda: pc(ax, *p, s=0.65), "lap": lambda: laptop(ax, *p, s=0.65), "pr": lambda: printer(ax, *p, s=0.65), "srv": lambda: server(ax, *p, s=0.5)}[k]()
    text(ax, 85, 3, "Large Office LAN", 9.5)
    save(fig, "lan-types.png")


def lan_components():
    fig, ax = canvas(80, 50, (7, 4.4))
    sx, sy = 46, 26
    line(ax, [(sx, sy), (46, 42)], color=RED); line(ax, [(sx, sy), (18, 26)], color=RED)
    line(ax, [(sx, sy), (30, 8)], color=RED); line(ax, [(sx, sy), (66, 8)], color=RED)
    switch(ax, sx, sy, None, s=1.1); text(ax, sx + 5, sy + 0.2, "Switch", 10, ha="left")
    pc(ax, 46, 44, "PC", s=0.9, below=False); router(ax, 14, 26, "Router"); pc(ax, 30, 8, "PC", s=0.9); server(ax, 66, 10, "Server", s=0.9)
    save(fig, "lan-components.png")


def collision():
    fig, ax = canvas(100, 66, (8.5, 5.6))
    box(ax, 2, 2, 96, 62, fc="#D6EAFB", r=8, ec=NAVY, lw=1.6, z=0)
    text(ax, 50, 59, "Broadcast Domain", 10)
    switch(ax, 50, 46, s=1.1)
    box(ax, 6, 40, 34, 12, fc="#F3F0B8", r=2.5, z=1); pc(ax, 12, 46, s=0.8); text(ax, 28, 49, "Collision Domain 1", 8.5)
    box(ax, 60, 40, 34, 12, fc="#F3F0B8", r=2.5, z=1); pc(ax, 88, 46, s=0.8); text(ax, 73, 49, "Collision Domain 3", 8.5)
    box(ax, 41, 6, 18, 30, fc="#F3F0B8", r=2.5, z=1); server(ax, 50, 22, s=0.9); text(ax, 50, 9.5, "Collision\nDomain 2", 8.5)
    line(ax, [(12, 46), (47, 46)], color=RED); line(ax, [(53, 46), (88, 46)], color=RED); line(ax, [(50, 45), (50, 24)], color=RED)
    save(fig, "collision-domains.png")


def switch_functions():
    fig, ax = canvas(100, 40, (8.5, 3.4))
    switch(ax, 50, 30, "Switch", s=1.1, below=False)
    for p in ((6, 30), (94, 30), (26, 8), (74, 8)):
        line(ax, [(50, 30), p], color=RED)
    server(ax, 6, 28, s=0.9); server(ax, 94, 28, s=0.9); pc(ax, 26, 8, s=0.9); pc(ax, 74, 8, s=0.9)
    save(fig, "switch-star.png")


def cli_functions():
    fig, ax = canvas(60, 46, (5.2, 4))
    router(ax, 10, 40, s=1); switch(ax, 48, 40, s=1.1)
    line(ax, [(10, 38), (10, 30), (30, 30), (30, 16)], color=RED); line(ax, [(48, 39), (48, 34), (32, 34), (32, 16)], color=RED)
    pc(ax, 31, 12, "Console", s=1.1)
    save(fig, "cli-console.png")


def _mem(ax, x, y, title):
    text(ax, x + 7, y + 20, title, 11, weight="bold")
    ax.add_patch(Rectangle((x, y), 14, 18, fc="white", ec=NAVY, lw=1.6))
    ax.add_patch(Rectangle((x, y + 11), 14, 3.6, fc="#F08A32", ec=NAVY, lw=1.2)); text(ax, x + 7, y + 12.8, "Configuration", 7.5, color="white")


def cfg_backup():
    fig, ax = canvas(100, 56, (8.5, 4.7))
    _mem(ax, 4, 28, "RAM"); _mem(ax, 82, 28, "NVRAM")
    switch(ax, 50, 46, s=0.95); router(ax, 50, 39, s=0.8)
    text(ax, 50, 31, "tftp\nftp\nscp\nhttp\n...", 8.5)
    server(ax, 46, 10, s=1); text(ax, 62, 10, "External Server", 10, ha="left")
    arrow(ax, (18, 31), (42, 12), both=True, lw=1.4); arrow(ax, (82, 31), (56, 12), both=True, lw=1.4)
    save(fig, "cfg-backup.png")


def cfg_flows():
    fig, ax = canvas(110, 66, (9.3, 5.6))
    _mem(ax, 6, 34, "RAM"); _mem(ax, 86, 34, "NVRAM")
    arrow(ax, (24, 60), (84, 60), lw=1.4); arrow(ax, (84, 55), (24, 55), lw=1.4)
    text(ax, 54, 63, "copy running startup", 9); text(ax, 54, 52.3, "copy startup running  (merge)", 9)
    arrow(ax, (50, 45), (22, 45), lw=1.4); text(ax, 36, 47.7, "configure terminal (merge)", 9, ha="left")
    pc(ax, 62, 42, s=0.9)
    arrow(ax, (95, 22), (95, 33), lw=1.4); text(ax, 98, 27, "erase start", 9, ha="left")
    box(ax, 86, 8, 18, 13, r=0.3); text(ax, 95, 14.5, "Blank", 10)
    server(ax, 52, 14, s=0.9); text(ax, 52, 3.5, "TFTP Server", 10)
    line(ax, [(10, 34), (10, 16)]); line(ax, [(10, 16), (45, 16)]); arrow(ax, (40, 16), (46, 16), lw=1.4); text(ax, 12, 12.3, "copy run tftp:", 9, ha="left")
    line(ax, [(16, 34), (16, 22)]); arrow(ax, (16, 30), (16, 34), lw=1.4); line(ax, [(16, 22), (45, 22)]); arrow(ax, (46, 22), (16, 22), lw=1.4)
    text(ax, 18, 24.6, "copy tftp: running (merge)", 9, ha="left")
    line(ax, [(59, 22), (92, 22)]); arrow(ax, (59, 22), (90, 22), lw=1.4); line(ax, [(90, 22), (90, 34)]); arrow(ax, (90, 30), (90, 34), lw=1.4)
    text(ax, 64, 24.6, "copy tftp: start", 9, ha="left")
    arrow(ax, (86, 16), (59, 16), lw=1.4); text(ax, 62, 12.3, "copy start tftp:", 9, ha="left")
    save(fig, "cfg-flows.png")


def switch_ip():
    fig, ax = canvas(80, 20, (7, 2.1))
    pc(ax, 8, 10, "PC", s=1); switch(ax, 72, 10, "SwitchX", s=1.1)
    line(ax, [(11, 10), (67, 10)], color=RED); text(ax, 52, 13, "Console", 10)
    save(fig, "switch-ip.png")


def mac_casts():
    fig, ax = canvas(110, 56, (9.3, 4.7))
    def row(y, label, hi):
        text(ax, 10, y + 2, label, 11, ha="center")
        xs = [30, 52, 74, 96]
        for x in hi:
            ax.add_patch(Rectangle((xs[x] - 10, y - 8), 20, 17, fc="#F9CFA9", ec="none", zorder=0))
        line(ax, [(xs[0], y - 3), (xs[-1], y - 3)], color=RED)
        for i, x in enumerate(xs):
            pc(ax, x, y + 4, s=0.75); line(ax, [(x, y - 3), (x, y + 1)], color=RED)
    row(44, "Unicast", [2]); row(24, "Broadcast", [1, 2, 3]); row(4, "Multicast", [2, 3])
    text(ax, 85, -3, "Client Group", 9); ax.set_ylim(-6, 56)
    save(fig, "mac-casts.png")


def mac_structure():
    fig, ax = canvas(100, 36, (8.5, 3.1))
    ax.add_patch(Rectangle((4, 14), 46, 12, fc=BLUE, ec=NAVY, lw=1.6)); ax.add_patch(Rectangle((50, 14), 46, 12, fc=BLUE, ec=NAVY, lw=1.6))
    text(ax, 27, 20, "OUI", 13, color="white", weight="bold"); text(ax, 73, 20, "Vendor\nAssigned", 11, color="white", weight="bold")
    for x0, x1 in ((4, 50), (50, 96)):
        line(ax, [(x0 + 1, 28), (x0 + 1, 30), (x1 - 1, 30), (x1 - 1, 28)], lw=1.3); text(ax, (x0 + x1) / 2, 33, "24 Bits", 10)
    line(ax, [(5, 12), (5, 9), (95, 9), (95, 12)], lw=1.3); text(ax, 50, 5.5, "48 Bits", 10); text(ax, 50, 0.5, "MAC Address", 11, weight="bold")
    save(fig, "mac-structure.png")


def _sw_panel(ax, ox, oy, table, frames):
    sw = (ox + 28, oy + 20)
    pcs = {"A": (ox + 6, oy + 20, False), "B": (ox + 50, oy + 20, False), "C": (ox + 28, oy + 5, True)}
    for k, (px, py, bl) in pcs.items():
        line(ax, [sw, (px, py)], color=RED)
        pc(ax, px, py + (0 if k != "C" else 0), f"PC {k}", s=0.7, below=bl)
    switch(ax, *sw, s=0.9)
    text(ax, sw[0] - 4, sw[1] - 2.4, "1", 8.5, ha="right"); text(ax, sw[0] + 4, sw[1] - 2.4, "3", 8.5, ha="left"); text(ax, sw[0] + 1.5, sw[1] - 6, "2", 8.5, ha="left")
    box(ax, ox + 6, oy + 33, 34, 14, r=0.2, fc="white"); text(ax, ox + 7, oy + 45, "MAC Table", 8.5, ha="left")
    for i, t in enumerate(table):
        text(ax, ox + 7, oy + 41.5 - 2.9 * i, t, 7.5, ha="left")
    for (a, b, lab) in frames:
        arrow(ax, (ox + a[0], oy + a[1]), (ox + b[0], oy + b[1]), lw=1.4, ms=9)
        text(ax, ox + (a[0] + b[0]) / 2 + (-4 if a[0] == b[0] else 0), oy + (a[1] + b[1]) / 2 + (0 if a[0] == b[0] else 2.3), lab, 7.5, weight="bold", bbox=dict(fc="#F8E58B", ec=NAVY, lw=0.6, pad=1.2))


def switching(name, panels):
    fig, ax = canvas(124, 50, (10.6, 4.3))
    for ox, spec in zip((0, 66), panels):
        _sw_panel(ax, ox, 0, spec["table"], spec["frames"])
        for (x, y, n) in spec["steps"]:
            ax.add_patch(Circle((ox + x, y), 2.0, fc=BLUE, ec=NAVY, zorder=7)); text(ax, ox + x, y, n, 8.5, color="white", weight="bold", zorder=8)
    save(fig, name)


def duplex():
    fig, ax = canvas(60, 50, (4.5, 3.8))
    switch(ax, 40, 44, s=1.2, below=False); text(ax, 54, 44, "Switch", 11, ha="left")
    server(ax, 40, 10, s=1.1); text(ax, 52, 20, "Server", 11, ha="left")
    line(ax, [(40, 42), (40, 15)], color=RED, lw=2); arrow(ax, (36, 38), (36, 24), lw=1.5)
    save(fig, "duplex-half.png")


def duplex_cfg():
    fig, ax = canvas(110, 22, (9.3, 2.3))
    pc(ax, 8, 12, "PC1", s=0.9); switch(ax, 38, 12, "SwitchX", s=1.0); switch(ax, 76, 12, "SwitchY", s=1.0); pc(ax, 104, 12, "PC2", s=0.9)
    for a, b in ((11, 35), (41, 73), (79, 101)):
        line(ax, [(a, 12), (b, 12)], color=RED)
    for x, lab in ((24, "Fa0/5"), (45, "Fa0/1"), (69, "Fa0/1"), (92, "Fa0/3")):
        text(ax, x, 15.2, lab, 8.5)
    save(fig, "duplex-config.png")


if __name__ == "__main__":
    notes_bus(); notes_star(); notes_mesh(); notes_handshake(); notes_frame(); notes_dns(); flooding(); forward_flow(); osi_vs_tcpip()
    encap("encapsulation.png", False); encap("de-encapsulation.png", True)
    peer(); lan(); lan_components(); collision(); switch_functions(); cli_functions(); cfg_backup(); cfg_flows(); switch_ip()
    mac_casts(); mac_structure()
    A_tab = ["Port: 1: MAC PC A", "Port: 2: Empty", "Port: 3: Empty"]
    B_tab = ["Port: 1: MAC PC A", "Port: 2: Empty", "Port: 3: MAC PC B"]
    switching("switching-1.png", [
        dict(table=A_tab, frames=[((11, 23), (24, 23), "Frame")], steps=[(6, 12, "1"), (43, 44, "2")]),
        dict(table=A_tab, frames=[((33, 23), (45, 23), "Frame"), ((26, 17), (26, 9), "Frame")], steps=[(55, 12, "3")]),
    ])
    switching("switching-2.png", [
        dict(table=A_tab, frames=[((45, 23), (33, 23), "Frame")], steps=[(55, 12, "4"), (43, 44, "5")]),
        dict(table=B_tab, frames=[((24, 23), (11, 23), "Frame")], steps=[(6, 12, "6")]),
    ])
    duplex(); duplex_cfg()
    print("ok")
