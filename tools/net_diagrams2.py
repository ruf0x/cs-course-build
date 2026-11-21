"""ARP and packet-flow diagrams. Run: python tools/net_diagrams2.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from net_diagrams import *  # noqa: F401,F403  (helpers: canvas, save, pc, switch, router, line, arrow, text, box ...)
from net_diagrams import canvas, save, pc, switch, router, server, line, arrow, text, box, NAVY, BLUE, RED, LINE, CARD, SKY


def arp_flow():
    fig, ax = canvas(120, 46, (10.4, 4.0))
    def panel(ox, title, req):
        text(ax, ox + 28, 43, title, 10.5, weight="bold")
        switch(ax, ox + 28, 28, s=1.2)
        pc(ax, ox + 6, 9, None, s=0.9); text(ax, ox + 6, 3.6, "PC-A\n.1.10", 8.5)
        pc(ax, ox + 22, 9, None, s=0.9); text(ax, ox + 22, 3.6, "PC-B\n.1.20", 8.5)
        pc(ax, ox + 38, 9, None, s=0.9); text(ax, ox + 38, 3.6, "PC-C\n.1.30", 8.5)
        pc(ax, ox + 54, 9, None, s=0.9); text(ax, ox + 54, 3.6, "PC-D\n.1.40", 8.5)
        for x in (6, 22, 38, 54):
            line(ax, [(ox + 28, 28), (ox + x, 12)], color=RED)
        if req:
            for x in (22, 38, 54):
                arrow(ax, (ox + 28 + (x - 28) * 0.35, 25), (ox + 28 + (x - 28) * 0.8, 14), color=BLUE, lw=1.8, ms=10)
            text(ax, ox + 28, 36.5, "Who has 192.168.1.20 ?  (broadcast)", 8.5, color=BLUE, weight="bold")
            text(ax, ox + 22, -2.5, "\"me!\"", 8.5, color=BLUE, weight="bold"); text(ax, ox + 38, -2.5, "ignores", 8.5); text(ax, ox + 54, -2.5, "ignores", 8.5)
        else:
            arrow(ax, (ox + 22, 13), (ox + 26, 25), color=BLUE, lw=1.4, ms=9)
            arrow(ax, (ox + 30, 25), (ox + 8, 13), color=BLUE, lw=1.8, ms=10)
            text(ax, ox + 28, 36.5, "192.168.1.20 is at BB:BB:BB:BB:BB:BB  (unicast)", 8.5, color=BLUE, weight="bold")
    panel(0, "1  ARP request", True)
    panel(62, "2  ARP reply", False)
    ax.set_ylim(-7, 46)
    save(fig, "arp-flow.png")


def gateway_lan():
    fig, ax = canvas(100, 52, (8.6, 4.5))
    box(ax, 2, 8, 60, 42, fc="#E4EDF8", ec="#9FB3CC", lw=1.2, r=3, z=0)
    text(ax, 32, 46, "LAN 192.168.1.0/24", 9.5, color=LINE)
    pc(ax, 12, 36, None, s=0.9); text(ax, 12, 42, "PC-A  .1.10\nGW = .1.1", 8.5); pc(ax, 52, 36, None, s=0.9); text(ax, 52, 42, "PC-B  .1.20\nGW = .1.1", 8.5)
    switch(ax, 32, 28, "SWITCH", s=1.1)
    line(ax, [(14, 36), (29, 29)], color=RED); line(ax, [(50, 36), (35, 29)], color=RED)
    line(ax, [(32, 27), (32, 20)], color=RED)
    router(ax, 32, 16, "ROUTER", s=0.9)
    text(ax, 40, 22, "G0/0  192.168.1.1", 8.5, ha="left", color=BLUE, weight="bold")
    text(ax, 40, 19, "= DEFAULT GATEWAY", 8.5, ha="left", color=BLUE)
    line(ax, [(34.5, 16), (84, 16)], color=RED); text(ax, 66, 13, "G1/0  10.0.0.1", 8.5)
    ax.add_patch(__import__("matplotlib.patches", fromlist=["Ellipse"]).Ellipse((90, 16), 18, 12, fc="#DCE6F2", ec=NAVY, lw=1.3))
    text(ax, 90, 16, "other networks\nInternet", 8.5)
    save(fig, "gateway-lan.png")


def gateway_decision():
    fig, ax = canvas(80, 46, (7.2, 4.1))
    def b(x, y, w, h, t, fc="white"):
        box(ax, x, y, w, h, fc=fc, r=1.2); text(ax, x + w / 2, y + h / 2, t, 8.8)
    b(18, 38, 44, 6, "PC wants to send to IP X", "#DCE6F2")
    b(16, 25, 48, 8, "Is X in MY network\n(same subnet)?", "#F8E58B")
    b(1, 5, 36, 14, "YES: ARP for X directly,\nsend to X's MAC", "#CFE8D5")
    b(43, 5, 36, 14, "NO: ARP for the GATEWAY's IP,\nsend to the GATEWAY's MAC\n(the destination IP stays X)", "#F6D0D5")
    arrow(ax, (40, 38), (40, 33)); arrow(ax, (30, 25), (19, 19)); arrow(ax, (50, 25), (61, 19))
    text(ax, 22, 22.5, "YES", 8.5, weight="bold"); text(ax, 58, 22.5, "NO", 8.5, weight="bold")
    save(fig, "gateway-decision.png")


# ---------------------------------------------------------------- packet-flow topology
NODES = {
    "X": (50, 52), "SW1": (28, 38), "SW4": (76, 38), "SW2": (14, 22), "SW3": (42, 22),
    "PC1": (7, 9), "PC2": (22, 9), "PC3": (34, 9), "PC4": (49, 9), "PC5": (76, 22),
}
EDGES = [("X", "SW1"), ("X", "SW4"), ("SW1", "SW2"), ("SW1", "SW3"), ("SW2", "PC1"), ("SW2", "PC2"), ("SW3", "PC3"), ("SW3", "PC4"), ("SW4", "PC5")]
IPS = {"PC1": "192.168.1.10", "PC2": "192.168.1.20", "PC3": "192.168.1.30", "PC4": "192.168.1.40", "PC5": "192.168.2.50"}


def pf_topology(path, name):
    fig, ax = canvas(100, 62, (9.0, 5.6))
    from matplotlib.patches import FancyBboxPatch
    box(ax, 1, -1, 56, 54, fc="#EEF3FA", ec="#9FB3CC", lw=1.0, r=3, z=0)
    box(ax, 62, 9, 36, 36, fc="#EEF3FA", ec="#9FB3CC", lw=1.0, r=3, z=0)
    text(ax, 3, 50.5, "LAN 1  192.168.1.0/24", 9, ha="left", color=LINE, weight="bold")
    text(ax, 64, 13.5, "LAN 2  192.168.2.0/24", 9, ha="left", color=LINE, weight="bold")
    hl = set()
    for a, b in zip(path, path[1:]):
        hl.add((a, b)); hl.add((b, a))
    for a, b in EDGES:
        on = (a, b) in hl
        line(ax, [NODES[a], NODES[b]], color=BLUE if on else "#8A97AA", lw=3.4 if on else 1.5, z=2)
    for n, (x, y) in NODES.items():
        if n == "X":
            router(ax, x, y, None, s=1.0)
            text(ax, x + 4, y + 0.5, "Router X", 9.5, ha="left", weight="bold")
            text(ax, x - 3.5, y - 5.2, "G0/0\n192.168.1.1", 7.5, ha="right")
            text(ax, x + 3.5, y - 5.2, "G0/1\n192.168.2.1", 7.5, ha="left")
        elif n.startswith("SW"):
            switch(ax, x, y, None, s=0.9)
            text(ax, x, y + 2.6, n, 8.5, weight="bold")
        else:
            pc(ax, x, y, None, s=0.85)
            text(ax, x, y - 5.4, f"{n}\n{IPS[n]}", 7.6, weight="bold" if n in path else "normal")
    for n in ((path[0], path[-1]) if path else ()):
        x, y = NODES[n]
        ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle((x, y + 0.4), 3.4, fc="none", ec=BLUE, lw=2.0, zorder=7))
    save(fig, name)


if __name__ == "__main__":
    arp_flow(); gateway_lan(); gateway_decision()
    pf_topology([], "pf-topology.png")
    pf_topology(["PC1", "SW2", "PC2"], "pf-path-pc2.png")
    pf_topology(["PC1", "SW2", "SW1", "SW3", "PC3"], "pf-path-pc3.png")
    pf_topology(["PC1", "SW2", "SW1", "X", "SW4", "PC5"], "pf-path-pc5.png")
    print("ok")
