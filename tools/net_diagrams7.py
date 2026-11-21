"""VLAN pictures. Run: python tools/net_diagrams7.py -> images/enterprise-networking/vlan-*.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from net_diagrams import canvas, save, pc, switch, router, server, line, arrow, text, box, NAVY, BLUE, RED, LINE
from matplotlib.patches import Rectangle, Ellipse

C10, C20, C30, C40 = "#CFE0F7", "#F9CFA9", "#CFE8D5", "#E7D3F2"
DK10, DK20, DK30, DK40 = "#2474D1", "#D07A00", "#2E9B52", "#7C5AC9"


def flat():
    fig, ax = canvas(100, 40, (10.5, 4.2))
    switch(ax, 50, 28, None, s=1.5); text(ax, 58, 31, "one switch", 9.5, weight="bold", ha="left")
    xs = [8, 24, 40, 60, 76, 92]
    for k, x in enumerate(xs):
        line(ax, [(50, 27), (x, 12)], color=RED)
        pc(ax, x, 9, None, s=0.9)
    arrow(ax, (8, 14), (36, 25), lw=2, color=BLUE, ms=11)
    for x in xs[1:]:
        arrow(ax, (50 + (x - 50) * 0.35, 23), (50 + (x - 50) * 0.85, 14), lw=1.6, color=BLUE, ms=9)
    text(ax, 3, 36, "a broadcast from the first PC reaches everybody", 9.5, color=BLUE, weight="bold", ha="left")
    text(ax, 50, 0.5, "all the devices are in the same broadcast domain", 9.5, weight="bold")
    ax.set_ylim(-2, 40)
    save(fig, "vlan-flat.png")


def sol1():
    fig, ax = canvas(100, 44, (10.5, 4.6))
    router(ax, 50, 36, None, s=1.4); text(ax, 58, 36, "Router", 9.5, ha="left", weight="bold")
    for x, lab in ((16, "IT"), (50, "HR"), (84, "Sales")):
        line(ax, [(50, 34), (x, 22)], color=RED, lw=2)
        switch(ax, x, 20, None, s=1.2)
        for dx in (-7, 0, 7):
            line(ax, [(x, 19), (x + dx, 9)], color=RED)
            pc(ax, x + dx, 7, None, s=0.65)
        text(ax, x, 13.2, lab, 9.5, weight="bold")
    text(ax, 50, -2.5, "one switch per department, and one router port per switch", 9.5, weight="bold")
    ax.set_ylim(-5, 44)
    save(fig, "vlan-sol1.png")


def building():
    fig, ax = canvas(100, 72, (8.4, 6.0))
    for x0, c, lab in ((38, C10, "VLAN 2 · IT" + chr(10) + "10.0.2.0/24"), (58, C20, "VLAN 3 · HR" + chr(10) + "10.0.3.0/24"), (78, C30, "VLAN 4 · Sales" + chr(10) + "10.0.4.0/24")):
        ax.add_patch(Rectangle((x0, 12), 19, 56, fc=c, ec="none", zorder=0))
        text(ax, x0 + 9.5, 7, lab, 9, weight="bold")
    for k, fl in enumerate(("Third floor", "Second floor", "First floor")):
        y = 58 - k * 19
        switch(ax, 14, y, None, s=1.1); text(ax, 14, y + 5, fl, 9, weight="bold")
        for x in (47, 67, 87):
            line(ax, [(17.5, y), (x - 2, y)], color=RED, lw=1.6)
            pc(ax, x, y, None, s=0.8)
    line(ax, [(14, 20), (14, 8)], color=RED, lw=2.2)
    router(ax, 14, 5, None, s=0.9)
    ax.set_ylim(-1, 72)
    save(fig, "vlan-building.png")


def virtual_switch():
    fig, ax = canvas(100, 36, (10.5, 3.8))
    box(ax, 4, 6, 92, 22, fc="#EEF3FA", r=2)
    text(ax, 50, 31.5, "one physical switch = several virtual switches", 10.5, weight="bold")
    groups = [(0, 0, 6, C10, DK10, "VLAN 10 · IT"), (6.6, 0, 4, C20, DK20, "VLAN 20 · RH"), (11.2, 0, 4, C30, DK30, "VLAN 30 · DG"), (0, 1, 8, C40, DK40, "VLAN 40 · Finance")]
    px, pw = 8, 5.2
    for c0, row, n, col, dk, lab in groups:
        y = 19 if row == 0 else 9.5
        x0 = px + c0 * pw
        ax.add_patch(Rectangle((x0 - 1, y - 2), n * pw + 0.4, 7.5, fc=col, ec=dk, lw=1.6, zorder=2))
        for k in range(n):
            ax.add_patch(Rectangle((x0 + k * pw + 0.4, y), 3.6, 3.6, fc="white", ec=NAVY, lw=1, zorder=3))
        text(ax, x0 - 1 + (n * pw + 0.4) / 2, y + 6.8, lab, 7.8, weight="bold", color=dk)
    ax.set_ylim(2, 34)
    save(fig, "vlan-virtual-switch.png")


def _pcs(ax, x, ys, side):
    for y, c, lab in ys:
        ax.add_patch(Ellipse((x, y), 11, 11, fc=c, ec="none", zorder=0))
        pc(ax, x, y, None, s=0.6)


def trunk_compare():
    fig, ax = canvas(100, 84, (10.5, 8.8))
    cols = [(C30, "#2E9B52", "Green VLAN"), (C20, "#D07A00", "Red VLAN"), (C10, "#2474D1", "Blue VLAN")]
    for base, title in ((60, "Without trunk: one link per VLAN"), (14, "With a trunk: one link for all the VLANs")):
        text(ax, 50, base + 20, title, 10.5, weight="bold")
        ys = [base + 11, base + 0, base - 11]
        for y, (c, dk, lab) in zip(ys, cols):
            ax.add_patch(Ellipse((14, y), 13, 10, fc=c, ec="none", zorder=0)); pc(ax, 14, y, None, s=0.6); text(ax, 4, y - 6.2, lab, 7.6)
            ax.add_patch(Ellipse((86, y), 13, 10, fc=c, ec="none", zorder=0)); pc(ax, 86, y, None, s=0.6); text(ax, 96, y - 6.2, lab, 7.6, ha="right")
            line(ax, [(18.5, y), (34, base)], color=dk, lw=1.4); line(ax, [(81.5, y), (66, base)], color=dk, lw=1.4)
        switch(ax, 37, base, None, s=1.1); switch(ax, 63, base, None, s=1.1)
        if base == 60:
            for dy, (c, dk, lab) in zip((2, 0, -2), cols):
                line(ax, [(41, base + dy), (59, base + dy)], color=dk, lw=2.2)
        else:
            import numpy as np
            xs = np.linspace(41, 59, 9)
            for k in range(8):
                line(ax, [(xs[k], base), (xs[k + 1] - 0.4, base)], color=cols[k % 3][1], lw=5)
    ax.set_ylim(-4, 84)
    save(fig, "vlan-trunk-compare.png")


def tag_frame():
    fig, ax = canvas(100, 36, (10.5, 3.8))
    text(ax, 3, 30, "Original frame", 10, weight="bold", ha="left")
    x = 3
    for lab, w in (("Dest", 13), ("Src", 13), ("Type", 14), ("Data", 22), ("FCS", 14)):
        ax.add_patch(Rectangle((x, 20), w, 6, fc="white", ec=NAVY, lw=1.6)); text(ax, x + w / 2, 23, lab, 10, weight="bold"); x += w
    text(ax, 3, 15, "Tagged frame (802.1Q)", 10, weight="bold", ha="left")
    x = 3
    for lab, w, fc in (("Dest", 13, "white"), ("Src", 13, "white"), ("Tag", 14, "#8FD0F5"), ("Type", 14, "white"), ("Data", 22, "white"), ("FCS", 14, "#D9D9D9")):
        ax.add_patch(Rectangle((x, 5), w, 6, fc=fc, ec=NAVY, lw=1.6)); text(ax, x + w / 2, 8, lab, 10, weight="bold"); x += w
    arrow(ax, (39, 20), (39, 12), lw=1.8, color=BLUE)
    text(ax, 54, 29.5, "(the FCS is recalculated)", 9, color=LINE, ha="left"); text(ax, 54, 14, "the tag: 4 bytes added", 9, color=BLUE, ha="left", weight="bold")
    ax.set_ylim(2, 34)
    save(fig, "vlan-tag-frame.png")


def two_switch():
    fig, ax = canvas(100, 40, (10.5, 4.2))
    switch(ax, 25, 28, None, s=1.4); text(ax, 25, 33.5, "SW1", 10, weight="bold")
    switch(ax, 75, 28, None, s=1.4); text(ax, 75, 33.5, "SW2", 10, weight="bold")
    line(ax, [(30, 28), (70, 28)], color=NAVY, lw=4); text(ax, 50, 31, "trunk", 10, weight="bold", color=NAVY)
    text(ax, 33, 25.5, "Fa0/3", 8.8, color=BLUE, weight="bold"); text(ax, 67, 25.5, "Fa0/3", 8.8, color=BLUE, weight="bold", ha="right")
    for sx in (25, 75):
        for dx, c, lab, vl in ((-9, C10, "Fa0/1", "VLAN 10"), (9, C20, "Fa0/2", "VLAN 20")):
            x = sx + dx
            line(ax, [(sx, 27), (x, 14)], color=RED, lw=1.8)
            ax.add_patch(Ellipse((x, 9), 14, 11, fc=c, ec="none", zorder=0)); pc(ax, x, 9, None, s=0.7)
            text(ax, x, 1.5, vl, 8.8, weight="bold")
            text(ax, sx + dx * 0.55 + (-3 if dx < 0 else 3), 21, lab, 8, color=BLUE, weight="bold", ha="right" if dx < 0 else "left")
    ax.set_ylim(-2, 40)
    save(fig, "vlan-two-switch.png")


def ros():
    fig, ax = canvas(100, 52, (10.5, 5.5))
    router(ax, 28, 44, None, s=1.3); text(ax, 22, 44, "R1", 10, ha="right", weight="bold")
    line(ax, [(30.5, 44), (58, 44)], color=RED, lw=2); ax.add_patch(Ellipse((70, 44), 22, 11, fc="#DCE6F2", ec=NAVY, lw=1.4, zorder=3)); text(ax, 70, 44, "Internet", 9.5, weight="bold", zorder=4)
    line(ax, [(28, 41.5), (28, 28)], color=NAVY, lw=4); text(ax, 31, 36, "Gi0/0", 9, color=BLUE, weight="bold", ha="left")
    text(ax, 31, 33, "trunk", 8.5, ha="left")
    switch(ax, 28, 25.5, None, s=1.3)
    for x, c, lab, ip in ((14, C10, "VLAN 10", "172.16.10.0/24"), (42, C20, "VLAN 20", "172.16.20.0/24")):
        line(ax, [(28, 24), (x, 14)], color=RED, lw=1.8)
        ax.add_patch(Ellipse((x, 9), 17, 11, fc=c, ec="none", zorder=0)); pc(ax, x, 9, None, s=0.7)
        text(ax, x, 1.6, f"{lab}\n{ip}", 8.4, weight="bold")
    # logical split of the router link
    ax.add_patch(Rectangle((66, 8), 30, 26, fc="#EEF3FA", ec="#9FB3CC", lw=1.2, zorder=0))
    text(ax, 81, 31, "Gi0/0 is divided into", 9, weight="bold"); text(ax, 81, 28.2, "2 logical sub-interfaces", 9, weight="bold")
    line(ax, [(69, 8), (69, 24)], color=DK10, lw=6); line(ax, [(93, 8), (93, 24)], color=DK20, lw=6)
    text(ax, 73, 16, "Gi0/0.10\nVLAN 10", 8, ha="left", weight="bold", color=DK10); text(ax, 90, 16, "Gi0/0.20\nVLAN 20", 8, ha="right", weight="bold", color=DK20)
    ax.set_ylim(-4, 52)
    save(fig, "vlan-ros.png")


def separate_if():
    fig, ax = canvas(100, 40, (10.5, 4.2))
    router(ax, 50, 33, None, s=1.2); text(ax, 57, 33, "Router", 9.5, ha="left", weight="bold")
    switch(ax, 50, 17, None, s=1.4)
    for dx, lab, ip in ((-3, "fa0/0", "10.1.10.1"), (3, "fa0/1", "10.1.20.1")):
        line(ax, [(50 + dx, 31), (50 + dx, 19)], color=RED, lw=2)
        text(ax, 50 + dx + (-1.5 if dx < 0 else 1.5), 27, f"{lab}\n{ip}", 8.4, color=BLUE, weight="bold", ha="right" if dx < 0 else "left")
    for x, c, lab, ip in ((14, C10, "VLAN 10", "10.1.10.100/24"), (86, C20, "VLAN 20", "10.1.20.100/24")):
        line(ax, [(50, 16), (x, 9)], color=RED, lw=1.8)
        ax.add_patch(Ellipse((x, 7), 22, 11, fc=c, ec="none", zorder=0)); pc(ax, x, 7, None, s=0.7)
        text(ax, x, -1.5, f"{lab}\n{ip}", 8.4, weight="bold")
    ax.set_ylim(-5, 40)
    save(fig, "vlan-separate-if.png")


def svi():
    fig, ax = canvas(100, 44, (10.5, 4.6))
    router(ax, 80, 36, None, s=1.1); text(ax, 80, 30.8, "other router", 8.8, weight="bold")
    box(ax, 12, 22, 52, 17, fc="#CFE0F7", r=1.5); text(ax, 38, 35.5, "Layer 3 (multilayer) switch", 9.5, weight="bold")
    text(ax, 38, 30.2, "ip routing", 9.5, color=BLUE, weight="bold")
    box(ax, 16, 23.5, 22, 4.2, fc=C10, r=0.6); text(ax, 27, 25.6, "interface vlan 10", 8, weight="bold")
    box(ax, 40, 23.5, 22, 4.2, fc=C20, r=0.6); text(ax, 51, 25.6, "interface vlan 20", 8, weight="bold")
    line(ax, [(64, 30), (77, 35)], color=RED, lw=2); text(ax, 68, 42, "Gi0/1 (no switchport) 192.168.1.1/30", 7.8, color=BLUE, weight="bold")
    for x, c, lab, ip in ((18, C10, "VLAN 10", "172.16.10.0/24"), (60, C20, "VLAN 20", "172.16.20.0/24")):
        line(ax, [(x + 10 if x < 40 else x - 4, 22), (x, 12)], color=RED, lw=1.8)
        ax.add_patch(Ellipse((x, 8), 22, 11, fc=c, ec="none", zorder=0)); pc(ax, x, 8, None, s=0.7)
        text(ax, x, 0.0, f"{lab}\n{ip}", 8.4, weight="bold")
    ax.set_ylim(-4, 44)
    save(fig, "vlan-svi.png")


def challenge():
    fig, ax = canvas(100, 40, (10.5, 4.2))
    switch(ax, 25, 28, None, s=1.4); text(ax, 25, 33.5, "SW1", 10, weight="bold")
    switch(ax, 75, 28, None, s=1.4); text(ax, 75, 33.5, "SW2", 10, weight="bold")
    line(ax, [(30, 28), (70, 28)], color=RED, lw=2.4)
    text(ax, 33, 25.5, "Fa0/24", 8.8, color=BLUE, weight="bold"); text(ax, 67, 25.5, "Fa0/20", 8.8, color=BLUE, weight="bold", ha="right")
    for sx, c, vl, port in ((25, C30, "PC (VLAN 30)", "Fa0/1"), (75, C20, "PC (VLAN 20)", "Fa0/2")):
        line(ax, [(sx, 27), (sx, 14)], color=RED, lw=1.8)
        ax.add_patch(Ellipse((sx, 9), 16, 11, fc=c, ec="none", zorder=0)); pc(ax, sx, 9, None, s=0.7)
        text(ax, sx, 1.5, vl, 8.8, weight="bold"); text(ax, sx + 2, 20.5, port, 8.4, color=BLUE, weight="bold", ha="left")
    ax.set_ylim(-2, 40)
    save(fig, "vlan-challenge.png")


def trunk_native():
    fig, ax = canvas(100, 50, (10.5, 5.2))
    CY = "#1E9BE0"
    sx, sy = 50, 42
    subs = [(14, "VLAN 1 + VLAN 2"), (38, "VLAN 3"), (62, "VLAN 1"), (86, "VLAN 5 + VLAN 6")]
    for x, lab in subs:
        line(ax, [(sx, sy - 1.5), (x, 24)], color=RED, lw=2.6)
        switch(ax, x, 22, None, s=1.1)
        text(ax, x, 13.5, lab, 8.6, weight="bold")
    switch(ax, sx, sy, None, s=1.3)
    text(ax, 22, 38, "802.1Q trunk", 8, color=RED, weight="bold"); text(ax, 36, 30, "802.1Q trunk", 8, color=RED, weight="bold", ha="right")
    text(ax, 78, 38, "802.1Q trunk", 8, color=RED, weight="bold"); text(ax, 74, 30, "802.1Q trunk", 8, color=RED, weight="bold", ha="left")
    # native VLAN path: a wide light-blue band under the trunk lines, with arrows
    ax.plot([14, 50], [24, 40.5], color=CY, lw=11, alpha=0.45, solid_capstyle="round", zorder=1)
    ax.plot([50, 62], [40.5, 24], color=CY, lw=11, alpha=0.45, solid_capstyle="round", zorder=1)
    arrow(ax, (20, 28.2), (29, 32), lw=3, color=NAVY, ms=14, z=8)
    arrow(ax, (53, 37), (57.5, 30), lw=3, color=NAVY, ms=14, z=8)
    box(ax, 2, 1, 48, 6, fc="white", r=0.6); text(ax, 26, 4, "blue band: native VLAN traffic, untagged", 8.6, weight="bold", color=CY)
    box(ax, 52, 1, 46, 6, fc="white", r=0.6); text(ax, 75, 4, "red: trunk, the other VLANs are tagged", 8.6, weight="bold", color=RED)
    ax.set_ylim(-1, 50)
    save(fig, "vlan-trunk-native.png")


def bc_example():
    fig, ax = canvas(100, 56, (10.5, 5.9))
    router(ax, 50, 46, None, s=1.3); text(ax, 56.5, 46, "Router", 9.5, ha="left", weight="bold")
    doms = [(22, "Network 1\n192.168.1.0/24", C10, DK10), (50, "Network 2\n192.168.2.0/24", C20, DK20), (78, "Network 3\n192.168.3.0/24", C30, DK30)]
    for x, lab, c, dk in doms:
        w = 40 if x == 22 else 24
        cx = 22 if x == 22 else x
        ax.add_patch(Ellipse((cx, 19), w - 1, 25, fc=c, ec=dk, lw=1.6, zorder=0))
    # domain 1: two switches linked
    for x, name in ((12, "SW1"), (32, "SW2")):
        switch(ax, x, 26, None, s=1.0); text(ax, x, 29.3, name, 8.6, weight="bold")
        for dx in (-5, 5):
            line(ax, [(x, 25), (x + dx, 13)], color=RED); pc(ax, x + dx, 11, None, s=0.6)
    line(ax, [(15, 26), (29, 26)], color=NAVY, lw=2.4)
    line(ax, [(47.5, 44.5), (22, 28)], color=RED, lw=2)
    text(ax, 33, 40, "interface 1", 8.2, color=BLUE, weight="bold")
    switch(ax, 50, 26, None, s=1.0); text(ax, 50, 29.3, "SW3", 8.6, weight="bold")
    for dx in (-5, 5):
        line(ax, [(50, 25), (50 + dx, 13)], color=RED); pc(ax, 50 + dx, 11, None, s=0.6)
    line(ax, [(50, 44), (50, 27.5)], color=RED, lw=2); text(ax, 52, 36, "interface 2", 8.2, color=BLUE, weight="bold", ha="left")
    switch(ax, 78, 26, None, s=1.0); text(ax, 78, 29.3, "SW4", 8.6, weight="bold")
    for dx in (-5, 5):
        line(ax, [(78, 25), (78 + dx, 13)], color=RED); pc(ax, 78 + dx, 11, None, s=0.6)
    line(ax, [(52.5, 44.5), (78, 28)], color=RED, lw=2); text(ax, 68, 40, "interface 3", 8.2, color=BLUE, weight="bold")
    for x, lab, c, dk in doms:
        text(ax, x if x != 22 else 22, 2.5, lab, 8.6, weight="bold", color=dk)
    ax.set_ylim(-1, 56)
    save(fig, "vlan-bc-example.png")


def native_hub():
    fig, ax = canvas(100, 40, (10.5, 4.2))
    switch(ax, 12, 26, None, s=1.3); text(ax, 12, 31, "Switch A (802.1Q)", 8.8, weight="bold")
    switch(ax, 88, 26, None, s=1.3); text(ax, 88, 31, "Switch B (802.1Q)", 8.8, weight="bold")
    box(ax, 38, 21, 24, 10, fc="#EEE9DA", r=1.0); text(ax, 50, 26, "HUB", 11, weight="bold")
    line(ax, [(17, 26), (38, 26)], color=NAVY, lw=3.4); line(ax, [(62, 26), (83, 26)], color=NAVY, lw=3.4)
    text(ax, 27.5, 28.4, "trunk", 8.4, weight="bold"); text(ax, 72.5, 28.4, "trunk", 8.4, weight="bold")
    line(ax, [(50, 21), (50, 12)], color=RED, lw=2); pc(ax, 50, 9, None, s=0.9)
    text(ax, 50, 2.5, "old PC: sends frames WITHOUT a tag", 8.8, weight="bold", color=RED)
    text(ax, 53, 15.5, "untagged frames", 8.2, color=RED, ha="left")
    text(ax, 50, 36.5, "untagged frames received on the trunk = native VLAN", 9, weight="bold", color=BLUE)
    ax.set_ylim(-1, 40)
    save(fig, "vlan-native-hub.png")


if __name__ == "__main__":
    flat(); sol1(); building(); virtual_switch(); trunk_native(); bc_example(); native_hub(); trunk_compare(); tag_frame(); two_switch(); ros(); separate_if(); svi(); challenge()
    print("ok")
