"""Router and static routing pictures. Run: python tools/net_diagrams5.py -> images/enterprise-networking/rt-*.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from net_diagrams import canvas, save, pc, switch, router, server, line, arrow, text, box, NAVY, BLUE, RED, LINE, CARD
from matplotlib.patches import Ellipse


def rt_intro():
    fig, ax = canvas(100, 36, (11.0, 4.0))
    pc(ax, 7, 20, "PC", s=1.2); switch(ax, 25, 20, None, s=1.5)
    router(ax, 52, 20, None, s=1.6); text(ax, 52, 13.5, "Router", 10, weight="bold")
    router(ax, 76, 20, None, s=1.4)
    server(ax, 93, 20, None, s=1.0); text(ax, 93, 12.5, "Google\n8.8.8.8", 9.5, weight="bold")
    for a, b in ((10, 22), (28, 49.5), (54.5, 73.5), (78.5, 91.5)):
        line(ax, [(a, 20), (b, 20)], color=RED, lw=2)
    text(ax, 44.5, 23.2, "G0/1", 9.5, weight="bold", color=BLUE); text(ax, 38, 15.5, "192.168.1.0/24", 9.5)
    text(ax, 60, 23.2, "G0/3", 9.5, weight="bold", color=BLUE); text(ax, 64.5, 15.5, "192.168.2.0", 9.5)
    ax.set_ylim(8, 30)
    save(fig, "rt-intro.png")


def rt_static():
    fig, ax = canvas(100, 44, (11.0, 4.85))
    router(ax, 28, 32, None, s=1.6); text(ax, 28, 26.2, "R1", 11, weight="bold")
    router(ax, 72, 32, None, s=1.6); text(ax, 72, 26.2, "R2", 11, weight="bold")
    line(ax, [(31, 32), (69, 32)], color=RED, lw=2.2)
    text(ax, 50, 36.5, "10.10.10.0/30", 10.5, weight="bold")
    text(ax, 36, 34.6, "Se0/0", 9, color=BLUE, weight="bold"); text(ax, 64, 34.6, "Se0/1", 9, color=BLUE, weight="bold")
    text(ax, 36, 29.2, ".1", 9); text(ax, 64, 29.2, ".2", 9)
    for x in (28, 72):
        line(ax, [(x, 29.5), (x, 14.5)], color=RED, lw=2.2)
        switch(ax, x, 12, None, s=1.4)
    text(ax, 33.2, 21, "G0/0", 9, color=BLUE, weight="bold", ha="left"); text(ax, 77.2, 21, "G0/0", 9, color=BLUE, weight="bold", ha="left")
    text(ax, 28, 7.4, "SW1", 9.5, weight="bold"); text(ax, 72, 7.4, "SW2", 9.5, weight="bold")
    text(ax, 28, 3.4, "192.168.1.0/24", 10.5, weight="bold"); text(ax, 72, 3.4, "172.16.1.0/24", 10.5, weight="bold")
    save(fig, "rt-static.png")


def rt_lb():
    fig, ax = canvas(100, 50, (11.0, 5.5))
    router(ax, 50, 42, None, s=1.4); text(ax, 50, 47.2, "R-top", 9.5, weight="bold")
    server(ax, 84, 42, None, s=0.9); text(ax, 84, 35.4, "10.10.10.0/24", 10, weight="bold")
    line(ax, [(52.5, 42), (81.5, 42)], color=RED, lw=2)
    router(ax, 22, 26, None, s=1.4); text(ax, 22, 20.5, "RA", 9.5, weight="bold")
    router(ax, 78, 26, None, s=1.4); text(ax, 78, 20.5, "RB", 9.5, weight="bold")
    router(ax, 50, 8, None, s=1.4); text(ax, 56, 8, "R1  (the LAN is behind)", 9.5, ha="left", weight="bold")
    for a, b in (((50, 42), (22, 26)), ((50, 42), (78, 26)), ((22, 26), (50, 8)), ((78, 26), (50, 8))):
        line(ax, [a, b], color=BLUE, lw=3)
    text(ax, 25, 11.8, "path 1: 5 packets", 10, color=BLUE, weight="bold", ha="right")
    text(ax, 75, 11.8, "path 2: 5 packets", 10, color=BLUE, weight="bold", ha="left")
    text(ax, 50, 2.0, "10 packets to 10.10.10.0/24: 5 on each path", 10.5, weight="bold")
    save(fig, "rt-lb.png")


def rt_decision():
    fig, ax = canvas(100, 56, (11.0, 6.2))
    def b(y, h, t, fc, sz=10.5):
        box(ax, 6, y, 88, h, fc=fc, r=1.5); text(ax, 50, y + h / 2, t, sz, weight="bold")
    items = [
        (49, 6, "A packet arrives: destination IP = D", "#DCE6F2"),
        (39, 7, "Which routes of the table match D ?  (no route matches: the packet is dropped)", "#F8E58B"),
        (28.5, 7.5, "1. LONGEST PREFIX: the most specific route wins (/32 > /24 > /16 ... /0)", "#CFE0F7"),
        (18, 7.5, "2. Same prefix, different sources: the lowest ADMINISTRATIVE DISTANCE wins", "#D5EBD9"),
        (7.5, 7.5, "3. Same source (same routing protocol): the lowest METRIC wins", "#F6D0D5"),
        (-3, 7.5, "4. Still a tie: the routes are equal, the packets are shared (LOAD BALANCING)", "#EEE9DA"),
    ]
    for y, h, t, c in items:
        b(y, h, t, c, 9.6)
    for y in (49, 39, 28.5, 18, 7.5):
        arrow(ax, (50, y), (50, y - 3.0), lw=2)
    ax.set_ylim(-4, 56)
    save(fig, "rt-decision.png")


def client_frame():
    from net_diagrams3 import packets
    packets([("pkt", "PC → switch → router", ["MAC-Router", "MAC-PC", "192.168.1.10", "8.8.8.8", "data"], {0})], "rt-client-frame.png")


if __name__ == "__main__":
    rt_intro(); rt_static(); rt_lb(); rt_decision(); client_frame()
    print("ok")
