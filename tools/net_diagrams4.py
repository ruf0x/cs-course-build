"""Subnetting pictures. Run: python tools/net_diagrams4.py  ->  images/enterprise-networking/sub-*.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from net_diagrams import canvas, save, line, text, NAVY, BLUE, LINE, RED
from matplotlib.patches import Rectangle


def class_ranges():
    fig, ax = canvas(100, 22, (11.0, 2.4))
    segs = [("Class A", 0, 128, "#79A7CE", "1 - 126"), ("Class B", 128, 64, "#7FCB92", "128 - 191"),
            ("Class C", 192, 32, "#F0A93B", "192 - 223"), ("D", 224, 16, "#D98B73", "224-239"), ("E", 240, 16, "#A07CC9", "240-255")]
    sc = 100 / 256
    text(ax, 50, 20, "The first octet decides the class", 11, weight="bold")
    for n, a, w, col, rng in segs:
        x = a * sc
        ax.add_patch(Rectangle((x, 6), w * sc, 9, fc=col, ec=NAVY, lw=1.6))
        text(ax, x + w * sc / 2, 10.5, n, 11 if w >= 32 else 9, color="white", weight="bold")
        text(ax, x + w * sc / 2, 2.8, rng, 8.6 if w >= 32 else 6.6, weight="bold")
    save(fig, "sub-class-ranges.png")


def bits_split():
    fig, ax = canvas(100, 30, (11.0, 3.3))
    bits = "11000000" + "10101000" + "00001010" + "00000000"
    sub = {24: "#F0A93B", 25: "#F0A93B"}
    bw = 2.7
    x = 3.0
    xs = []
    for i, b in enumerate(bits):
        if i and i % 8 == 0:
            x += 1.4
        col = "#79A7CE" if i < 24 else ("#F0A93B" if i < 26 else "#7FCB92")
        ax.add_patch(Rectangle((x, 12), bw, 5.2, fc=col, ec=NAVY, lw=1.0))
        text(ax, x + bw / 2, 14.6, b, 9, color="white", weight="bold")
        xs.append(x)
        x += bw
    for k, lab in enumerate(("192", "168", "10", "0")):
        text(ax, xs[k * 8] + 4 * bw, 19.6, lab, 10, weight="bold")
    def brace(i0, i1, lab, col, ly=6):
        a, b = xs[i0], xs[i1 - 1] + bw
        line(ax, [(a, 10.5), (a, 9), (b, 9), (b, 10.5)], color=col, lw=1.6)
        text(ax, (a + b) / 2, ly, lab, 9.2, color=col, weight="bold")
    brace(0, 24, "network: 24 bits (kept)", "#2474D1")
    brace(24, 26, "subnet: 2 bits", "#D07A00", 2.6)
    brace(26, 32, "host: 6 bits", "#2E9B52")
    text(ax, 38, -0.6, "192.168.10.0 / 26  (the /24 network, with 2 bits borrowed from the host part)", 9, color=LINE)
    save(fig, "sub-bits.png")


def space_bar(blocks, name, title):
    """blocks: (label, start, size, color)  on a 0..255 line"""
    fig, ax = canvas(100, 30, (11.0, 3.3))
    sc = 94 / 256
    x0 = 3
    text(ax, 50, 27.5, title, 10.5, weight="bold")
    ax.add_patch(Rectangle((x0, 14), 256 * sc, 8, fc="#E4EDF8", ec=NAVY, lw=1.3))
    small = 0
    for lab, st, sz, col in blocks:
        ax.add_patch(Rectangle((x0 + st * sc, 14), sz * sc, 8, fc=col, ec=NAVY, lw=1.2))
        cx = x0 + (st + sz / 2) * sc
        if sz * sc >= 9:
            text(ax, cx, 18, lab, 8.4, color="white", weight="bold")
        else:
            yy = 9.2 - 3.6 * (small % 2)
            line(ax, [(cx, 14), (cx, yy + 1.4)], color=LINE, lw=0.8)
            text(ax, cx, yy, lab, 7.8, color=NAVY, weight="bold")
            small += 1
    for v in (0, 64, 128, 192, 255):
        text(ax, x0 + v * sc, 24.2, f".{v}", 7.6, color=LINE)
    save(fig, name)


if __name__ == "__main__":
    class_ranges(); bits_split()
    B, G, O, P, R2, GR = "#2474D1", "#2E9B52", "#D07A00", "#7C5AC9", "#C9364A", "#7B8794"
    space_bar([("Users /25", 0, 128, B), ("Servers /26", 128, 64, G), ("Printers /27", 192, 32, O), ("Link /30", 224, 4, R2)], "sub-vlsm1.png", "10.1.0.0/24: the addresses used by the 4 subnets (the rest is free)")
    space_bar([("LAN A /26", 0, 64, B), ("LAN B /27", 64, 32, G), ("C /28", 96, 16, O), ("WAN1", 112, 4, R2), ("WAN2", 116, 4, P)], "sub-vlsm2.png", "192.168.50.0/24: the addresses used by the 5 subnets (the rest is free)")
    print("ok")
