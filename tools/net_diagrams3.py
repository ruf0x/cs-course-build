"""Gateway, ARP set-up and packet pictures. Run: python tools/net_diagrams3.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from net_diagrams import canvas, save, pc, switch, router, line, arrow, text, box, NAVY, BLUE, RED, LINE, CARD
from matplotlib.patches import Rectangle, Ellipse, Circle


def arp_setup():
    fig, ax = canvas(100, 44, (9.6, 4.2))
    switch(ax, 50, 32, None, s=1.6)
    text(ax, 50, 27.5, "SWITCH", 10, weight="bold")
    pcs = [(16, "PC-A", "192.168.1.10", "AA:AA:AA:AA:AA:AA", "Fa0/1"), (50, "PC-B", "192.168.1.20", "BB:BB:BB:BB:BB:BB", "Fa0/2"), (84, "PC-C", "192.168.1.30", "CC:CC:CC:CC:CC:CC", "Fa0/3")]
    for x, n, ip, mac, port in pcs:
        line(ax, [(50, 30), (x, 15)], color=RED, lw=1.8)
        pc(ax, x, 12, None, s=1.2)
        text(ax, x, 5.0, f"{n}\n{ip}\n{mac}", 8.6, weight="bold")
        fx = 50 + (x - 50) * 0.45
        text(ax, fx + (-1.5 if x < 50 else 1.5 if x > 50 else 2.5), 24, port, 8.8, ha="right" if x < 50 else "left", color=BLUE, weight="bold")
    text(ax, 50, 42.5, "192.168.1.0/24  ·  all the ARP tables and the switch MAC table are empty  ·  PC-A pings 192.168.1.20", 9.5, color=LINE, weight="bold")
    ax.set_ylim(-3, 44)
    save(fig, "arp-setup.png")


def gateway_exit():
    fig, ax = canvas(100, 44, (11.0, 4.85))
    box(ax, 1, 1, 68, 42, fc="#E4EDF8", ec="#9FB3CC", lw=1.4, r=3, z=0)
    text(ax, 4, 39.5, "LAN  192.168.1.0/24", 11, ha="left", color=LINE, weight="bold")
    pc(ax, 12, 31, None, s=1.4); text(ax, 12, 23, "PC-A\n192.168.1.10\ngateway: 192.168.1.1", 8.8)
    pc(ax, 12, 14, None, s=1.4); text(ax, 12, 6.6, "PC-B\n192.168.1.20\ngateway: 192.168.1.1", 8.8)
    switch(ax, 36, 22, None, s=1.7); text(ax, 36, 17.2, "SWITCH", 10, weight="bold")
    line(ax, [(15, 30), (32, 23.5)], color=RED, lw=2); line(ax, [(15, 15), (32, 20.5)], color=RED, lw=2)
    line(ax, [(40, 22), (60, 22)], color=RED, lw=2)
    router(ax, 64, 22, None, s=1.8)
    text(ax, 64, 29.5, "ROUTER", 10.5, weight="bold")
    text(ax, 64, 13.5, "G0/0  192.168.1.1", 9.5, color=BLUE, weight="bold")
    text(ax, 64, 10.3, "= the default gateway", 9.5, color=BLUE)
    line(ax, [(68.5, 22), (84, 22)], color=RED, lw=2)
    text(ax, 76, 24.3, "G0/1  10.0.0.1", 8.8)
    ax.add_patch(Ellipse((91, 22), 16, 20, fc="#DCE6F2", ec=NAVY, lw=1.5, zorder=3))
    text(ax, 91, 22, "other\nnetworks\nInternet", 9.5, weight="bold", zorder=4)
    save(fig, "gateway-exit.png")


def gateway_decide():
    fig, ax = canvas(100, 44, (11.0, 4.85))
    def b(x, y, w, h, t, fc="white", sz=11):
        box(ax, x, y, w, h, fc=fc, r=1.5); text(ax, x + w / 2, y + h / 2, t, sz, weight="bold")
    b(28, 37, 44, 6, "The PC wants to send to the IP X", "#DCE6F2")
    b(24, 23, 52, 9, "Is X in MY network?\n(same subnet, with my mask)", "#F8E58B")
    b(2, 1, 44, 15, "YES\nARP for X directly,\nsend to X's MAC", "#CFE8D5")
    b(54, 1, 44, 15, "NO\nARP for the GATEWAY's IP,\nsend to the GATEWAY's MAC\n(the destination IP stays X)", "#F6D0D5", 10.5)
    arrow(ax, (50, 37), (50, 32), lw=2); arrow(ax, (36, 23), (24, 16), lw=2); arrow(ax, (64, 23), (76, 16), lw=2)
    text(ax, 26.5, 20.5, "YES", 10, weight="bold"); text(ax, 73.5, 20.5, "NO", 10, weight="bold")
    save(fig, "gateway-decide.png")


MAC_C, IP_C, DATA_C = "#CFE0F7", "#D5EBD9", "#EEE9DA"
WIDTHS = [14, 14, 17, 17, 16]
LABELS = ["MAC dst", "MAC src", "IP src", "IP dst", ""]
FILLS = [MAC_C, MAC_C, IP_C, IP_C, DATA_C]


def packets(items, name):
    """items: ('sep', text, color) or ('pkt', link, [dstmac, srcmac, srcip, dstip, data], changed_indices)"""
    rowh, seph = 6.6, 4.8
    total = sum(rowh if it[0] == "pkt" else seph for it in items) + 2
    fig, ax = canvas(100, total, (11.5, total * 0.115))
    y = total - 0.5
    for it in items:
        if it[0] == "sep":
            y -= seph
            text(ax, 50, y + seph / 2, it[1], 9.5, color=it[2] if len(it) > 2 else NAVY, weight="bold")
            continue
        _, link, vals, changed = it
        y -= rowh
        text(ax, 1, y + 2.6, link, 9.5, ha="left", weight="bold")
        x = 22
        for k, (w, lab, fc) in enumerate(zip(WIDTHS, LABELS, FILLS)):
            on = k in changed
            ax.add_patch(Rectangle((x, y), w, 5.4, fc=fc, ec=RED if on else NAVY, lw=2.2 if on else 1.1, zorder=3))
            if lab:
                text(ax, x + w / 2, y + 4.3, lab, 6.6, color=LINE, zorder=4)
            text(ax, x + w / 2, y + (1.8 if lab else 2.7), vals[k], 8.8 if k < 4 else 8.2, color=RED if on else NAVY, weight="bold", zorder=4)
            x += w
    save(fig, name)


P1, P2, P3, P5 = "MAC-PC1", "MAC-PC2", "MAC-PC3", "MAC-PC5"
X0, X1 = "MAC-X0", "MAC-X1"
IP1, IP2, IP3, IP5 = "192.168.1.10", "192.168.1.20", "192.168.1.30", "192.168.2.50"
REQ, REP = "ICMP echo request", "ICMP echo reply"


def pk(link, dm, sm, si, di, data, ch=()):
    return ("pkt", link, [dm, sm, si, di, data], set(ch))


def build():
    packets([("sep", "Echo request"), pk("PC1 → SW2", P2, P1, IP1, IP2, REQ), pk("SW2 → PC2", P2, P1, IP1, IP2, REQ),
             ("sep", "Echo reply"), pk("PC2 → SW2", P1, P2, IP2, IP1, REP), pk("SW2 → PC1", P1, P2, IP2, IP1, REP)], "pf-pkts-pc2.png")
    packets([("sep", "Echo request: the packet is the same on every link")] +
            [pk(l, P3, P1, IP1, IP3, REQ) for l in ("PC1 → SW2", "SW2 → SW1", "SW1 → SW3", "SW3 → PC3")], "pf-pkts-pc3-req.png")
    packets([("sep", "Echo reply: the packet is the same on every link")] +
            [pk(l, P1, P3, IP3, IP1, REP) for l in ("PC3 → SW3", "SW3 → SW1", "SW1 → SW2", "SW2 → PC1")], "pf-pkts-pc3-rep.png")
    packets([("sep", "Echo request, in LAN 1 (to the gateway)"),
             pk("PC1 → SW2", X0, P1, IP1, IP5, REQ), pk("SW2 → SW1", X0, P1, IP1, IP5, REQ), pk("SW1 → Router X", X0, P1, IP1, IP5, REQ),
             ("sep", "Router X removes the old frame and builds a new one (TTL - 1): the MACs change, the IPs stay", RED),
             pk("Router X → SW4", P5, X1, IP1, IP5, REQ, (0, 1)), pk("SW4 → PC5", P5, X1, IP1, IP5, REQ, (0, 1))], "pf-pkts-pc5-req.png")
    packets([("sep", "Echo reply, in LAN 2 (to the gateway)"),
             pk("PC5 → SW4", X1, P5, IP5, IP1, REP), pk("SW4 → Router X", X1, P5, IP5, IP1, REP),
             ("sep", "Router X removes the old frame and builds a new one (TTL - 1): the MACs change, the IPs stay", RED),
             pk("Router X → SW1", P1, X0, IP5, IP1, REP, (0, 1)), pk("SW1 → SW2", P1, X0, IP5, IP1, REP, (0, 1)), pk("SW2 → PC1", P1, X0, IP5, IP1, REP, (0, 1))], "pf-pkts-pc5-rep.png")


if __name__ == "__main__":
    arp_setup(); gateway_exit(); gateway_decide(); build()
    print("ok")
