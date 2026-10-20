"""Draw the deck's schematics as SVG, themed to the deck colors.

Usage: python3 tools/schematics.py   (writes schematics/*.svg)
Requires: pip install schemdraw matplotlib

Every circuit runs from the kit's 9V battery. LEDs get 330 ohm unless noted.
"""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot  # noqa: E402
matplotlib.rcParams["svg.fonttype"] = "path"  # text as outlines: renders the same everywhere
import schemdraw
import schemdraw.elements as elm

INK = "#1E2A1F"
RED = "#D6402B"
GREEN = "#2E8B3E"
BLUE = "#2F5DA8"
OUT = os.path.join(os.path.dirname(__file__), "..", "schematics")

schemdraw.config(fontsize=15, lw=2.2, color=INK, font="DejaVu Sans")
schemdraw.use("matplotlib")


def save(d, name):
    d.save(os.path.join(OUT, name + ".svg"), transparent=True)
    matplotlib.pyplot.close("all")


def battery(d, length=3):
    """9V battery on the left edge, + at the top."""
    b = d.add(elm.Battery().up().length(length).reverse().label("9V", loc="bot", ofst=0.3))
    plus(d, b)
    return b


def plus(d, b):
    """Mark the + end of a battery, then carry on drawing from it."""
    d += elm.Label().at((b.end[0] - 0.45, b.end[1] - 0.45)).label("+", fontsize=18, color=RED)
    d.here = b.end


def led(**kw):
    return elm.LED(fill=RED, **kw)


# ---------------------------------------------------------------- symbols

def symbols():
    d = schemdraw.Drawing(show=False)
    d += elm.LED(fill=RED).right()
    save(d, "sym-led")

    d = schemdraw.Drawing(show=False)
    d += elm.Resistor().right()
    save(d, "sym-resistor")

    d = schemdraw.Drawing(show=False)
    d += elm.Capacitor(polar=True).right()
    save(d, "sym-capacitor-electrolytic")

    d = schemdraw.Drawing(show=False)
    d += elm.Capacitor().right()
    save(d, "sym-capacitor-ceramic")

    d = schemdraw.Drawing(show=False)
    d += elm.BjtNpn(circle=True).label("C", loc="collector").label("B", loc="base").label("E", loc="emitter")
    save(d, "sym-npn")

    d = schemdraw.Drawing(show=False)
    d += elm.Motor().right()
    save(d, "sym-motor")

    # RGB LED, common cathode: three LEDs sharing one leg
    d = schemdraw.Drawing(show=False)
    for i, (c, n) in enumerate(((RED, "R"), (GREEN, "G"), (BLUE, "B"))):
        d += elm.LED(fill=c).down().at((i * 1.6, 0)).label(n, loc="lft")
    d += elm.Line().at((0, -3)).right().length(3.2)
    d += elm.Line().at((1.6, -3)).down().length(1).label("common −", loc="end", ofst=0.15)
    save(d, "sym-rgb-led")


# ---------------------------------------------------------------- LED circuits

def led_circuit():
    d = schemdraw.Drawing(show=False)
    battery(d)
    d += elm.Line().right().length(0.5)
    d += elm.Resistor().right().label("330Ω")
    d += led().down().length(3).label("LED", loc="bot")
    d += elm.Line().left().tox(0)
    save(d, "led-circuit")


def series():
    d = schemdraw.Drawing(show=False)
    battery(d, 4)
    d += elm.Resistor().right().label("330Ω")
    d += led().right().label("LED1")
    d += elm.Resistor().right().label("330Ω")
    d += led().down().length(4).label("LED2", loc="bot")
    d += elm.Resistor().left().label("330Ω", loc="bot")
    d += led().left().label("LED3", loc="bot")
    d += elm.Line().left().tox(0)
    save(d, "series")


def parallel():
    d = schemdraw.Drawing(show=False)
    top = battery(d, 5).end
    d += elm.Line().right().length(1.5)
    for i in range(3):
        x = 1.5 + i * 2.5
        d += elm.Line().at((top[0] + 1.5 if i == 0 else x - 2.5, top[1])).right().length(2.5 if i else 0) if i else elm.Dot()
        d += elm.Resistor().down().at((x, top[1])).length(2.5).label("330Ω", loc="bot")
        d += led().down().length(2.5).label(f"LED{i+1}", loc="bot")
        d += elm.Dot() if i < 2 else elm.Line().length(0)
    d += elm.Line().left().at((6.5, top[1] - 5)).tox(0)
    d += elm.Dot().at((1.5, top[1]))
    d += elm.Dot().at((4, top[1]))
    save(d, "parallel")


def series_parallel():
    d = schemdraw.Drawing(show=False)
    top = battery(d, 6).end
    d += elm.Line().right().length(4).dot()
    a = d.here
    # branch A: one resistor, two LEDs in series
    d += elm.Resistor().down().length(2).label("330Ω", loc="bot")
    d += led().down().length(2).label("LED1", loc="bot")
    d += led().down().length(2).label("LED2", loc="bot").dot()
    d += elm.Line().left().tox(0)
    # branch B: one resistor, one LED
    d += elm.Line().right().at(a).length(3)
    d += elm.Resistor().down().length(3).label("330Ω", loc="bot")
    d += led().down().length(3).label("LED3", loc="bot")
    d += elm.Line().left().tox(a[0])
    save(d, "series-parallel")


def potentiometer():
    d = schemdraw.Drawing(show=False)
    battery(d, 4)
    d += elm.Resistor().right().label("330Ω")
    pot = d.add(elm.Potentiometer().right().label("10kΩ", loc="bot"))
    d += elm.Line().at(pot.tap).up().length(0.8)
    d += elm.Line().right().tox(pot.end[0])
    d += elm.Line().down().toy(pot.end[1]).dot()
    d += elm.Line().at(pot.end).right().length(1)
    d += led().down().length(4).label("LED", loc="bot")
    d += elm.Line().left().tox(0)
    save(d, "potentiometer")


def rgb():
    d = schemdraw.Drawing(show=False)
    top = battery(d, 6).end
    d += elm.Line().right().length(6.5)
    for i, (c, n) in enumerate(((RED, "R"), (GREEN, "G"), (BLUE, "B"))):
        x = 1.5 + i * 2.5
        if i < 2:
            d += elm.Dot().at((x, top[1]))
        d += elm.Resistor().down().at((x, top[1])).length(3).label("330Ω", loc="bot")
        d += elm.LED(fill=c).down().length(2).label(n, loc="bot")
        d += elm.Line().down().length(1)
    d += elm.Line().at((1.5, top[1] - 6)).right().length(5)
    d += elm.Dot().at((4, top[1] - 6))
    d += elm.Line().at((1.5, top[1] - 6)).left().tox(0)
    d += elm.Label().at((4, top[1] - 6.4)).label("common cathode (−)", loc="bot", fontsize=13)
    save(d, "rgb-led")


# ---------------------------------------------------------------- capacitors

def cap_series():
    """LED in series with a capacitor: it flashes while C1 charges, then goes dark.
    The 10k resistor across C1 drains it so the demo can be repeated."""
    d = schemdraw.Drawing(show=False)
    battery(d, 5)
    d += elm.Button().right().label("S1")
    d += elm.Resistor().right().label("330Ω")
    d += led().down().length(2).label("LED", loc="bot")
    d += elm.Line().down().length(0.5).dot()
    n = d.here
    d += elm.Capacitor(polar=True).down().length(2.5).label("1000µF", loc="bot").dot()
    b = d.here
    d += elm.Line().left().tox(0)
    d += elm.Line().right().at(n).length(2.5)
    d += elm.Resistor().down().length(2.5).label("10kΩ\n(drain)", loc="bot")
    d += elm.Line().left().tox(b[0])
    save(d, "cap-series")


def cap_parallel():
    """Hold S1 to charge C1 and light the LED. Let go and the LED fades as C1 drains."""
    d = schemdraw.Drawing(show=False)
    battery(d, 4)
    d += elm.Button().right().label("S1 (charge)")
    d += elm.Line().right().length(1).dot()
    n = d.here
    d += elm.Capacitor(polar=True).down().length(4).label("1000µF", loc="bot").dot()
    b = d.here
    d += elm.Line().left().tox(0)
    d += elm.Line().right().at(n).length(2.5)
    d += elm.Resistor().down().length(2).label("1kΩ", loc="bot")
    d += led().down().length(2).label("LED", loc="bot")
    d += elm.Line().left().tox(b[0])
    save(d, "cap-parallel")


def cap_compare():
    """Same charge-and-glow circuit twice: two 1000uF caps in parallel (2000uF, glows ~2x longer)
    vs. in series (500uF, ~half as long)."""
    d = schemdraw.Drawing(show=False)
    for ox, title, mode in ((0, "Parallel: 2000µF", "par"), (10, "Series: 500µF", "ser")):
        d += elm.Label().at((ox + 3.5, 5.6)).label(title, fontsize=17)
        plus(d, d.add(elm.Battery().up().at((ox, 0)).length(4).reverse().label("9V", loc="bot", ofst=0.3)))
        d += elm.Button().right().label("S1")
        d += elm.Line().right().length(0.5).dot()
        n = d.here
        if mode == "par":
            d += elm.Capacitor(polar=True).down().length(4).label("C1", loc="bot").dot()
            d += elm.Line().at(n).right().length(1.5)
            d += elm.Capacitor(polar=True).down().length(4).label("C2", loc="bot").dot()
            d += elm.Line().at((n[0] + 1.5, 4)).right().length(1.5)
        else:
            d += elm.Capacitor(polar=True).down().length(2).label("C1", loc="bot")
            d += elm.Capacitor(polar=True).down().length(2).label("C2", loc="bot").dot()
            d += elm.Line().at(n).right().length(3)
        d += elm.Resistor().down().length(2).label("1kΩ", loc="bot")
        d += led().down().length(2)
        d += elm.Line().left().tox(ox)
    save(d, "cap-compare")


# ---------------------------------------------------------------- switches & sensors

def switch_circuit(name, sw):
    d = schemdraw.Drawing(show=False)
    battery(d, 4)
    d += sw.right()
    d += elm.Resistor().right().label("330Ω")
    d += led().down().length(4).label("LED", loc="bot")
    d += elm.Line().left().tox(0)
    save(d, name)


def hall():
    """Open-collector Hall sensor (A3144 style): output pulls low near a magnet, lighting the LED."""
    d = schemdraw.Drawing(show=False)
    ic = d.add(elm.Ic(pins=[elm.IcPin(name="VCC", side="top", pin="1"),
                            elm.IcPin(name="GND", side="bot", pin="2"),
                            elm.IcPin(name="OUT", side="right", pin="3")],
                      size=(2.6, 2.2)).at((3, 0)))
    d += elm.Label().at((ic.GND[0], ic.GND[1] - 1.7)).label("Hall sensor (A3144)", fontsize=13)
    ytop, ybot, xr = ic.VCC[1] + 1.2, ic.GND[1] - 1.2, ic.OUT[0] + 3
    d += elm.Line().at(ic.VCC).up().toy(ytop).dot()
    d += elm.Line().at(ic.GND).down().toy(ybot)
    d += elm.Line().left().tox(0)
    bat = d.add(elm.Battery().up().toy(ytop).reverse().label("9V", loc="bot", ofst=0.3))
    plus(d, bat)
    d += elm.Line().right().tox(xr)
    d += elm.Resistor().down().length(1.6).label("330Ω", loc="bot")
    d += led().down().toy(ic.OUT[1]).label("LED", loc="bot")
    d += elm.Line().left().tox(ic.OUT[0])
    save(d, "hall-sensor")


def transistor():
    """Press S1: a small base current through 1k turns Q1 on and lights the LED."""
    d = schemdraw.Drawing(show=False)
    q = d.add(elm.BjtNpn(circle=True).at((6, 0)).anchor("base").label("PN2222", loc="right", ofst=(0.2, 0)))
    d += elm.Resistor().at(q.base).left().length(2.5).label("1kΩ")
    d += elm.Button().left().length(2).label("S1")
    d += elm.Line().up().toy(4)
    d += elm.Line().right().tox(q.collector[0])
    d += elm.Resistor().at((q.collector[0], 4)).down().toy(2).label("330Ω", loc="bot")
    d += led().down().to(q.collector).label("LED", loc="bot")
    d += elm.Line().at(q.emitter).down().toy(-3)
    d += elm.Line().left().tox(-1.5)
    plus(d, d.add(elm.Battery().up().toy(4).reverse().label("9V", loc="bot", ofst=0.3)))
    d += elm.Line().right().tox(1.5)
    d += elm.Dot().at((1.5, 4))
    d += elm.Dot().at((q.collector[0], 4))
    save(d, "transistor")


def motor():
    """Transistor motor switch with a 1N4001 flyback diode across the motor."""
    d = schemdraw.Drawing(show=False)
    q = d.add(elm.BjtNpn(circle=True).at((6, 0)).anchor("base").label("PN2222", loc="right", ofst=(0.2, 0)))
    d += elm.Resistor().at(q.base).left().length(2.5).label("1kΩ")
    d += elm.Button().left().length(2).label("S1")
    d += elm.Line().up().toy(4.5)
    d += elm.Line().right().tox(q.collector[0])
    d += elm.Dot()
    top = d.here
    d += elm.Motor().down().to(q.collector)
    d += elm.Line().at(top).right().length(2)
    d += elm.Diode().down().length(4.5 - q.collector[1]).reverse().label("1N4001", loc="bot")
    d += elm.Line().left().tox(q.collector[0])
    d += elm.Dot().at(q.collector)
    d += elm.Line().at(q.emitter).down().toy(-3)
    d += elm.Line().left().tox(-1.5)
    plus(d, d.add(elm.Battery().up().toy(4.5).reverse().label("9V", loc="bot", ofst=0.3)))
    d += elm.Line().right().tox(1.5)
    d += elm.Dot().at((1.5, 4.5))
    save(d, "motor")


# ---------------------------------------------------------------- bonus: debounce

def debounce():
    """Count button bounces. Each rising edge on SRCLK shifts another 1 into the 74HC595,
    so the number of lit LEDs is the number of edges the button made. Move the jumper
    from RAW to CLEAN to send the button through an RC filter and a 74HC14 Schmitt trigger."""
    import schemdraw.logic as logic
    d = schemdraw.Drawing(show=False)
    # left pins are listed bottom to top
    ic = d.add(elm.Ic(pins=[elm.IcPin(name="OE", side="left", pin="13"),
                            elm.IcPin(name="SRCLR", side="left", pin="10"),
                            elm.IcPin(name="RCLK", side="left", pin="12"),
                            elm.IcPin(name="SRCLK", side="left", pin="11"),
                            elm.IcPin(name="SER", side="left", pin="14"),
                            elm.IcPin(name="QA–QH", side="right", pin="15, 1–7", anchorname="Q")],
                      pinspacing=1.2, edgepadW=3.2, label="74HC595").at((14, 0)))
    # SER high: every clock shifts in a 1
    d += elm.Line().at(ic.SER).left().length(1)
    d += elm.Vdd().label("+5V")
    # OE low: outputs always on
    d += elm.Line().at(ic.OE).left().length(0.6)
    d += elm.Ground()
    # RCLK tied to SRCLK so the LEDs update on every clock
    d += elm.Line().at(ic.RCLK).left().length(0.8).dot()
    d += elm.Line().up().toy(ic.SRCLK[1]).dot()
    clk = d.here
    d += elm.Line().right().to(ic.SRCLK)
    # SRCLR (active low): S2 clears the count, 10k holds it high
    d += elm.Line().at(ic.SRCLR).left().length(3).dot()
    clr = d.here
    d += elm.Button().down().length(2.4).label("S2 reset", loc="top")
    d += elm.Ground()
    d += elm.Resistor().at(clr).left().length(2.4).label("10kΩ", loc="bot")
    d += elm.Vdd().label("+5V")
    # Outputs: 8 LEDs, one drawn
    d += elm.Line().at(ic.Q).right().length(1)
    d += elm.Resistor().right().label("330Ω")
    d += led().down().length(2.5).label("LED ×8", loc="bot")
    d += elm.Ground()

    # Input: S1 with 10k pull-up
    bx = clk[0] - 11
    d += elm.Vdd().at((bx, clk[1] + 3.4)).label("+5V")
    d += elm.Resistor().down().length(1.6).label("10kΩ", loc="bot")
    d += elm.Dot()
    a = d.here
    d += elm.Button().down().length(1.8).label("S1", loc="bot")
    d += elm.Ground()
    d += elm.Line().at(a).right().length(1).dot()
    a2 = d.here
    # CLEAN path: RC filter then 74HC14
    d += elm.Resistor().right().length(2.4).label("10kΩ").dot()
    b = d.here
    d += elm.Capacitor(polar=True).down().length(1.8).label("10µF", loc="bot")
    d += elm.Ground()
    d += elm.Line().at(b).right().length(1.2)
    d += logic.SchmittNot().right().label("74HC14", loc="top")
    d += elm.Line().right().length(0.8).dot()
    clean = d.here
    d += elm.Label().at((clean[0], clean[1] + 0.45)).label("CLEAN", fontsize=12, color=GREEN)
    # RAW path: straight from the button
    d += elm.Line().at(a2).up().length(1.4)
    d += elm.Line().right().tox(clean[0]).dot()
    raw = d.here
    d += elm.Label().at((raw[0], raw[1] + 0.45)).label("RAW", fontsize=12, color=RED)
    # jumper: one wire picks RAW or CLEAN
    d += elm.Line().at((clk[0] - 2.2, clk[1])).right().tox(clk[0]).dot()
    j = (clk[0] - 2.2, clk[1])
    d += elm.Dot(open=True).at(j)
    d += elm.Line(ls="--", color=GREEN).at(j).to(clean)
    d += elm.Line(ls=":", color=RED).at(j).to(raw)
    d += elm.Label().at((j[0] - 0.2, j[1] - 0.6)).label("jumper", fontsize=12)
    save(d, "debounce")


# ---------------------------------------------------------------- glossary

def glossary():
    """One small drawing per symbol for the glossary slide."""
    import schemdraw.logic as logic
    os.makedirs(os.path.join(OUT, "glossary"), exist_ok=True)

    def one(name, *els):
        d = schemdraw.Drawing(show=False)
        for e in els:
            d += e
        save(d, "glossary/" + name)

    one("resistor", elm.Resistor().right())
    one("potentiometer", elm.Potentiometer().right())
    one("capacitor", elm.Capacitor().right())
    one("capacitor-electrolytic", elm.Capacitor(polar=True).right())
    one("diode", elm.Diode().right())
    one("led", elm.LED(fill=RED).right())
    one("battery", elm.Battery().right().reverse())
    one("ground", elm.Line().down().length(1), elm.Ground())
    one("switch", elm.Switch().right())
    one("button", elm.Button().right())
    one("reed-switch", elm.SwitchReed().right())
    one("npn", elm.BjtNpn(circle=True))
    one("motor", elm.Motor().right())
    one("schmitt", logic.SchmittNot().right())
    one("ic", elm.Ic(pins=[elm.IcPin(side="left"), elm.IcPin(side="left"),
                           elm.IcPin(side="right"), elm.IcPin(side="right")], size=(1.6, 2)))
    d = schemdraw.Drawing(show=False)
    d += elm.Line().right().length(3)
    d += elm.Line().at((1.5, 1.2)).down().length(1.2).dot()
    save(d, "glossary/junction")
    d = schemdraw.Drawing(show=False)
    d += elm.Line().right().length(3)
    d += elm.Line().at((1.5, 1.2)).down().length(2.4)
    save(d, "glossary/crossing")
    one("supply", elm.Vdd().label("+5V"), elm.Line().down().length(1.2))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    symbols()
    led_circuit()
    series()
    parallel()
    series_parallel()
    potentiometer()
    rgb()
    cap_series()
    cap_parallel()
    cap_compare()
    switch_circuit("slide-switch", elm.Switch().label("slide switch"))
    switch_circuit("tilt-switch", elm.Switch().label("tilt switch"))
    switch_circuit("reed-switch", elm.SwitchReed().label("reed switch"))
    hall()
    transistor()
    motor()
    debounce()
    glossary()
    print("wrote", len(os.listdir(OUT)), "files to", os.path.abspath(OUT))
