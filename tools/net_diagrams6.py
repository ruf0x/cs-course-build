"""ENARSI day 1 pictures and the 6-router lab. Run: python tools/net_diagrams6.py -> images/enterprise-networking/rt-*.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from net_diagrams import canvas, save, pc, switch, router, server, line, arrow, text, box, NAVY, BLUE, RED, LINE, CARD
from matplotlib.patches import Ellipse, Circle


def packet_path():
    fig, ax = canvas(100, 40, (11.0, 4.4))
    steps = [("Ingress\\ntraffic", "#DCE6F2"), ("Decryption\\n(optional)", "#EEE9DA"), ("Input ACL", "#F6D0D5"), ("Routing\\nlookup", "#CFE0F7"), ("NAT\\n(if any)", "#D5EBD9"),
             ("PBR\\n(route-map)", "#F8E58B"), ("Output ACL", "#F6D0D5"), ("Encryption\\n(optional)", "#EEE9DA"), ("Egress\\ntraffic", "#DCE6F2")]
    xs1 = [4 + k * 19.2 for k in range(5)]
    xs2 = [13.6 + k * 19.2 for k in range(4)]
    pos = [(x, 25) for x in xs1] + [(x, 5) for x in xs2]
    for (x, y), (t, c) in zip(pos, steps):
        box(ax, x, y, 16, 10, fc=c, r=1.2)
        text(ax, x + 8, y + 5, t.replace("\\n", "\n"), 9.2, weight="bold")
    for k in range(4):
        arrow(ax, (pos[k][0] + 16, 30), (pos[k + 1][0], 30), lw=2)
    line(ax, [(pos[4][0] + 8, 25), (pos[4][0] + 8, 20.5), (pos[5][0] + 8, 20.5)], lw=2)
    arrow(ax, (pos[5][0] + 8, 20.5), (pos[5][0] + 8, 15), lw=2)
    for k in range(5, 8):
        arrow(ax, (pos[k][0] + 16, 10), (pos[k + 1][0], 10), lw=2)
    ax.set_ylim(2, 40)
    text(ax, 50, 37.5, "The path of a packet through a router", 11, weight="bold")
    save(fig, "rt-packet-path.png")


def nat_acl():
    fig, ax = canvas(100, 36, (11.0, 4.0))
    pc(ax, 6, 14, None, s=1.1); pc(ax, 16, 14, None, s=1.1); text(ax, 6, 8.2, "10.0.0.1", 8.8); text(ax, 16, 8.2, "10.0.0.2", 8.8, weight="bold")
    switch(ax, 12, 22, None, s=1.3)
    line(ax, [(6, 16), (10, 21)], color=RED); line(ax, [(16, 16), (13.5, 21)], color=RED)
    router(ax, 42, 22, None, s=1.6); text(ax, 42, 15.4, "NAT router", 9.5, weight="bold")
    line(ax, [(15, 22), (39, 22)], color=RED, lw=2); line(ax, [(45, 22), (70, 22)], color=RED, lw=2)
    text(ax, 30, 25, "G0/1/0 (inside)", 8.8, color=BLUE, weight="bold"); text(ax, 56, 25, "G0/1/1 (outside)", 8.8, color=BLUE, weight="bold")
    ax.add_patch(Ellipse((84, 22), 24, 18, fc="#DCE6F2", ec=NAVY, lw=1.5, zorder=3)); text(ax, 84, 22, "Internet", 10, weight="bold", zorder=4)
    box(ax, 6, -3.5, 88, 5.5, fc="#F6D0D5", r=1.0)
    text(ax, 50, -0.75, "an OUTPUT ACL on G0/1/1 that denies 10.0.0.2 never matches: NAT changed the source first", 8.4, weight="bold")
    ax.set_ylim(-5, 31)
    save(fig, "rt-nat-acl.png")


def split_8020():
    fig, ax = canvas(100, 40, (11.0, 4.4))
    router(ax, 14, 20, None, s=1.5); text(ax, 14, 13.8, "R1", 10, weight="bold")
    router(ax, 86, 20, None, s=1.5); text(ax, 86, 13.8, "8.8.8.8", 10, weight="bold")
    router(ax, 50, 34, None, s=1.3); text(ax, 50, 38.6, "next hop 10.0.0.1", 9.2, weight="bold")
    router(ax, 50, 6, None, s=1.3); text(ax, 50, 0.4, "next hop 20.0.0.1", 9.2, weight="bold")
    line(ax, [(16.5, 21.5), (47.5, 33)], color=RED, lw=1.6); line(ax, [(52.5, 33), (83.5, 21.5)], color=RED, lw=1.6)
    line(ax, [(16.5, 18.5), (47.5, 7)], color=BLUE, lw=5); line(ax, [(52.5, 7), (83.5, 18.5)], color=BLUE, lw=5)
    text(ax, 26, 31.5, "20 %", 12, color=RED, weight="bold"); text(ax, 26, 8.5, "80 %", 12, color=BLUE, weight="bold")
    save(fig, "rt-8020.png")


def null_loop():
    fig, ax = canvas(100, 40, (11.0, 4.4))
    router(ax, 20, 22, None, s=1.5); text(ax, 20, 15.6, "Client", 10, weight="bold")
    router(ax, 55, 22, None, s=1.5); text(ax, 55, 15.6, "ISP", 10, weight="bold")
    ax.add_patch(Ellipse((86, 22), 24, 18, fc="#DCE6F2", ec=NAVY, lw=1.5, zorder=3)); text(ax, 86, 22, "Internet", 10, weight="bold", zorder=4)
    line(ax, [(22.5, 22), (52.5, 22)], color=RED, lw=2); line(ax, [(57.5, 22), (74, 22)], color=RED, lw=2)
    arrow(ax, (30, 28), (46, 28), lw=2, color=BLUE); text(ax, 38, 31, "default route 0.0.0.0/0", 8.8, color=BLUE, weight="bold")
    arrow(ax, (46, 18.4), (30, 18.4), lw=2, color=RED); text(ax, 38, 13, "ISP route to the pool 20.0.0.0/29", 8.8, color=RED, weight="bold")
    text(ax, 20, 8.2, "uses 20.0.0.1 to 20.0.0.4", 8.8)
    text(ax, 50, 3.0, "a packet for the unused 20.0.0.5 goes back and forth between the two routers: a loop", 9.2, weight="bold", color=RED)
    ax.set_ylim(0, 40)
    save(fig, "rt-null-loop.png")


def track():
    fig, ax = canvas(100, 44, (11.0, 4.85))
    router(ax, 14, 22, None, s=1.5); text(ax, 14, 15.8, "Source", 10, weight="bold")
    router(ax, 50, 36, None, s=1.4); text(ax, 50, 40.8, "next hop 10.0.0.1", 9.2, weight="bold")
    router(ax, 50, 8, None, s=1.4); text(ax, 50, 2.0, "next hop 20.0.0.1", 9.2, weight="bold")
    router(ax, 84, 22, None, s=1.5); text(ax, 90, 22, "8.8.8.8", 10, weight="bold", ha="left")
    line(ax, [(16.5, 23.5), (47.5, 35)], color=RED, lw=2.2); line(ax, [(52.5, 35), (81.5, 23.5)], color=RED, lw=2.2)
    line(ax, [(16.5, 20.5), (47.5, 9)], color=RED, lw=2.2); line(ax, [(52.5, 9), (81.5, 20.5)], color=RED, lw=2.2)
    text(ax, 68, 29.5, "X", 20, color=RED, weight="bold")
    text(ax, 80, 42, "the path is broken here,\nbut the interface of the source stays up", 8.8, color=RED, ha="center")
    box(ax, 1, 1, 40, 9, fc="#F8E58B", r=1.0); text(ax, 21, 5.5, "test: ping 8.8.8.8\nok: keep the static route\nfailed: remove it", 8.4, weight="bold")
    save(fig, "rt-track.png")


def lab6():
    fig, ax = canvas(100, 58, (11.0, 6.4))
    P = {"R1": (22, 48), "R2": (78, 48), "R3": (22, 30), "R4": (78, 30), "R5": (46, 14), "R6": (46, 2)}
    links = [("R1", "R3", "10.0.13.0/30", (12.5, 39)), ("R2", "R4", "10.0.24.0/30", (87.5, 39)), ("R1", "R4", "10.0.14.0/30", (40, 45.6)),
             ("R2", "R3", "10.0.23.0/30", (60, 45.6)), ("R3", "R5", "10.0.35.0/30", (30, 20)), ("R4", "R5", "10.0.45.0/30", (64, 20)), ("R5", "R6", "10.0.56.0/30", (55, 7.6))]
    for a, b, lab, (lx, ly) in links:
        line(ax, [P[a], P[b]], color=RED, lw=2)
        text(ax, lx, ly, lab, 8.2, weight="bold")
    for n, (x, y) in P.items():
        router(ax, x, y, None, s=1.5)
        text(ax, x, y + 4.4, n + (" (ISP)" if n == "R6" else ""), 10, weight="bold")
    # LANs
    def lan(x, y, rx, ry, label):
        switch(ax, x, y, None, s=1.1); pc(ax, x, y - 5.5, None, s=0.8)
        line(ax, [(rx - 2.4 if x < rx else rx + 2.4, ry), (x + (3.3 if x < rx else -3.3), y)], color=RED, lw=2)
        line(ax, [(x, y - 1), (x, y - 3.4)], color=RED)
        text(ax, x, y + (7.6 if y > 40 else -11.2), label, 8.6, weight="bold")
    lan(6, 48, 22, 48, "LAN-A\n192.168.10.0/24")
    lan(94, 48, 78, 48, "LAN-B\n192.168.20.0/24")
    lan(76, 14, 46, 14, "LAN-C\n192.168.30.0/24")
    ax.add_patch(Ellipse((15, 2), 28, 9, fc="#DCE6F2", ec=NAVY, lw=1.4, zorder=3)); text(ax, 15, 2, "Internet\n8.8.8.8 (loopback of R6)", 7.6, weight="bold", zorder=4)
    line(ax, [(43.6, 2), (29, 2)], color=RED, lw=2)
    ax.set_ylim(-5, 58)
    save(fig, "rt-lab6.png")


if __name__ == "__main__":
    packet_path(); nat_acl(); split_8020(); null_loop(); track(); lab6()
    print("ok")
