# Breadboarding Workshop 2026

Slides for **Introduction to Electronics and Breadboarding Circuits**, a FUBAR Labs × 4-H workshop. There are 36 slides: the basics of electricity, then hands-on projects with LEDs, resistors, capacitors, switches, sensors, transistors and motors. Slide 35 is a bonus logic-chip activity and slide 36 is a glossary of schematic symbols.

Everything runs from one 9V battery, except the bonus slide, which needs 5V.

## View the deck

**Online:** https://ricklon.github.io/breadboarding-workshop-2026/ (GitHub Pages, from `main`)

**Locally:**

```sh
python3 -m http.server 8765
# open http://localhost:8765/
```

Use the arrow keys to move between slides. The deck works offline because React is served from `vendor/`.

`Breadboarding Workshop 2026.pdf` is a 1920×1080 export with one slide per page and working links.

## Repository layout

| Path | What it is |
| --- | --- |
| `index.html` | The deck (from Claude Design; runtime in `vendor/`) |
| `images/` | Photos and Fritzing breadboard drawings |
| `fonts/` | Bricolage Grotesque and IBM Plex Mono |
| `schematics/` | Generated SVG schematics (don't edit by hand) |
| `schematics/glossary/` | Symbols for the glossary slide |
| `tools/schematics.py` | Draws every schematic |
| `tools/export-pdf.js` | Exports the PDF |

## Edit and rebuild

Schematics are code. To change a circuit, edit its function in `tools/schematics.py`, then:

```sh
pip install schemdraw matplotlib
python3 tools/schematics.py
```

To regenerate the PDF, start the server above, then:

```sh
npm install playwright   # or use a global install with NODE_PATH
node tools/export-pdf.js http://localhost:8765/ "Breadboarding Workshop 2026.pdf"
```

## Circuit notes

- **LED resistors are 330Ω.** Some older breadboard drawings show 220Ω, which overdrives an LED on 9V, so use 330Ω.
- **Slide 22, potentiometer:** a 330Ω resistor in series with the pot keeps the LED safe when the pot is turned all the way down.
- **Slide 23, RGB LED:** drawn as common cathode. A common-anode LED needs its common leg on + and the polarity reversed.
- **Slide 25, capacitor in series:** the LED flashes once while C1 charges, then goes dark. The 10kΩ resistor drains C1 so the demo can be repeated.
- **Slide 26, capacitor in parallel:** hold S1 to charge C1, then let go and the LED fades. The 1kΩ resistor stretches the glow so it's easy to see.
- **Slide 27, series vs. parallel:** two 1000µF capacitors. In parallel they make 2000µF and glow longer; in series they make 500µF and glow for a shorter time.
- **Slide 34, motor:** the 1N4001 across the motor absorbs the voltage spike when the motor turns off.
- **Slide 35, bonus:** use **5V only**, because 9V destroys the 74HC chips. Wire each chip's power pins, which the schematic leaves out: 74HC595 pin 16 → +5V and pin 8 → GND; 74HC14 pin 14 → +5V and pin 7 → GND. Tie the unused 74HC14 inputs to GND.

## Kit

### DIY kit (slide 6)

| Required | Qty | Required | Qty | Extras | Qty |
| --- | --- | --- | --- | --- | --- |
| Breadboard | 1 | Slide switch | 1 | Green LEDs | 3 |
| Wire kit | 1 | Tilt ball switch | 1 | Yellow LEDs | 3 |
| 9V battery | 1 | Reed switch | 1 | 10kΩ resistors | 3 |
| 9V snap connector | 1 | Magnet | 1 | 10µF capacitor, 25V | 2 |
| Red LEDs | 3 | Hall effect sensor | 1 | 10kΩ potentiometer (RGB mixing) | 2 |
| RGB LED | 1 | PN2222 transistor | 1 | | |
| 330Ω resistors | 3 | 1N4001 diode | 1 | | |
| 1kΩ resistor | 1 | DC toy motor | 1 | | |
| 10kΩ potentiometer | 1 | 1000µF capacitor, 25V | 2 | | |
| Buttons | 2 | 100µF capacitor, 25V | 1 | | |

**Bonus slide 35 needs extra parts:** a 74HC14, a 74HC595, 8 LEDs with 330Ω resistors, and a 5V supply such as a breadboard power module or USB. It also uses the kit's two buttons, a 10µF capacitor and 10kΩ resistors.

### ELEGOO ESP-32 Super Starter Kit option

The kit costs about $36 and covers most parts. To match this workshop, buy these separately:

- Capacitors: 1000µF ×2, 100µF, 10µF
- Reed switch
- Hall effect sensor
- Slide switch

That adds about $3–5 per student for a class of 5.

## Still to verify

- [ ] Update the Fritzing breadboard drawings on slides 25, 26 and 27 to match the new capacitor circuits
- [ ] Dry-run the slide 35 debounce circuit with real parts and confirm the raw button bounces visibly
- [ ] Time the capacitor glow on slides 26 and 27
- [ ] ELEGOO kit: RGB LED type (common anode or cathode); if it's common anode, redraw slide 23
- [ ] ELEGOO kit: 9V battery connector compatibility
- [ ] ELEGOO kit: resistor color bands (4 or 5; slide 21 covers both)
- [ ] ELEGOO kit: DC motor voltage rating on 9V
- [ ] Check the YouTube links (slides 9, 15, 24) and the resistor calculator (slide 21) still load
- [ ] Optional: a safety callout slide; an ELEGOO option on the parts slide

## Credits

Content from *Basic Electronics 2024* (FUBAR Labs). Deck designed with Claude Design. Breadboard drawings made with Fritzing.
