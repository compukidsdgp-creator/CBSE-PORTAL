"""WHY? — Why do plants close their stomata during the day, even though they need CO₂?  (Class 10 Life Processes)"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do plants SHUT their pores on hot days?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "Plants need carbon dioxide to make food. So why do they shut their leaf pores on a hot afternoon?",
                "Plants NEED CO₂ to make food… so why shut their leaf pores on a hot afternoon?", 4.8),
    ("stomata", "These pores are stomata. Two guard cells swell to open them, and shrink to close them.",
                "These pores are STOMATA: two guard cells swell to OPEN, shrink to CLOSE.", 4.6),
    ("trade",   "When open, carbon dioxide comes in. But water vapour escapes too. That's transpiration.",
                "OPEN: CO₂ comes in… but WATER VAPOUR escapes too (transpiration).", 4.6),
    ("hot",     "On a hot, dry day, the leaf loses water faster than the roots can replace it. "
                "The guard cells go limp, and the pore closes. Water is saved.",
                "HOT & DRY: water lost faster than roots supply → guard cells go limp → pore CLOSES. Water saved!", 6.6),
    ("cost",    "Photosynthesis slows for a while. But wilting would be far worse.",
                "Photosynthesis slows for a while — but WILTING would be far worse.", 3.8),
    ("desert",  "Desert plants go further. They open their stomata at night, store the carbon dioxide, and use it in the day.",
                "DESERT plants open stomata at NIGHT, store CO₂, and use it in the day!", 5.2),
    ("math",    "Water first, food later.",
                "Water first, food later.", 2.8),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🌿 WHY? — Why do plants CLOSE their stomata on hot days, even though they need CO₂?

Stomata = tiny leaf pores, opened/closed by two guard cells.
Open → CO₂ in ✅ … but water vapour out ❌ (transpiration)

🔥 Hot, dry afternoon: water lost faster than roots can supply
→ guard cells go limp → stomata CLOSE → water saved 💧
Photosynthesis slows for a while — better than wilting!

🌵 Desert plants open stomata at NIGHT, store CO₂, use it by day.

Life Processes — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Stomata #Transpiration #Photosynthesis #Class10Science #CBSE #BoardExams"""


def stoma(dax, cx, cy, openness, a, turgid=True, s=1.0):
    """Two bean-shaped guard cells; openness 0..1 controls the pore width."""
    gap = 0.08 + 0.45 * openness
    col = "#3ddc97" if turgid else "#8fae7a"
    for sx in (-1, 1):
        dax.add_patch(Ellipse((cx + sx * (gap / 2 + 0.38) * s, cy), 0.75 * s, 2.3 * s, facecolor=col,
                              edgecolor="#1f6b45", lw=3, alpha=a, zorder=6))
        dax.add_patch(Ellipse((cx + sx * (gap / 2 + 0.38) * s, cy), 0.3 * s, 1.5 * s, facecolor="#1f8a5a",
                              edgecolor="none", alpha=a * 0.6, zorder=7))
    dax.add_patch(Ellipse((cx, cy), gap * s, 1.6 * s, facecolor="#06101f", edgecolor="none", alpha=a, zorder=7))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    t = c.t
    a0 = ease(c.phase("hook", 0.05, 0.35))
    de = ease(c.phase("desert", 0.0, 0.25))
    ma = ease(c.phase("math", 0.0, 0.3))
    main = a0 * (1 - de)
    hot = ease(c.phase("hot", 0.25, 0.75))
    openness = (0.3 + 0.7 * ease(c.phase("stomata", 0.2, 0.6))) * (1 - hot)
    if c.at("cost"):
        openness = 0.0
    if main > 0.01:
        # leaf surface
        dax.add_patch(FancyBboxPatch((-3.3, -1.7), 6.6, 3.4, boxstyle="round,pad=0,rounding_size=0.3",
                                     facecolor="#1d4d33", edgecolor="#3ddc97", lw=2, alpha=main * 0.6, zorder=3))
        stoma(dax, 0, 0.0, openness, main, turgid=hot < 0.5)
        tr = ease(c.phase("trade", 0.1, 0.4))
        if tr > 0:
            for k in range(5):
                f = (k / 5 + 0.35 * t) % 1.0
                # CO2 in (from left, into the pore)
                dax.add_patch(Circle((lerp(-3.0, -0.1, f), 1.0 - 1.0 * f), 0.11, color=LTGREY, alpha=main * tr * openness,
                                     zorder=8))
                # H2O out (from pore, up to the right)
                dax.add_patch(Circle((lerp(0.1, 3.0, f), 0.0 + 1.6 * f), 0.11, color=CYAN, alpha=main * tr * openness,
                                     zorder=8))
            outline(dax.text(-2.3, 1.45, "CO₂ in", ha="center", fontsize=22, color=LTGREY, fontweight="bold",
                             alpha=main * tr, zorder=9))
            outline(dax.text(2.3, 1.95, "H₂O out", ha="center", fontsize=22, color=CYAN, fontweight="bold",
                             alpha=main * tr, zorder=9))
        if c.at("stomata") and not c.at("trade"):
            outline(dax.text(-2.2, -1.25, "guard cells", ha="center", fontsize=21, color=GREEN, fontweight="bold",
                             alpha=main * ease(c.phase("stomata", 0.2, 0.5)), zorder=9))
            outline(dax.text(2.2, -1.25, "pore", ha="center", fontsize=21, color=WHITE, fontweight="bold",
                             alpha=main * ease(c.phase("stomata", 0.4, 0.7)), zorder=9))
        ha = ease(c.phase("hot", 0.05, 0.3))
        if ha > 0:
            dax.add_patch(Circle((0.4, 2.2), 0.3, color=GOLD, alpha=main * ha, zorder=9))
            for k in range(8):
                ang = k * np.pi / 4
                dax.plot([0.4 + 0.38 * np.cos(ang), 0.4 + 0.52 * np.cos(ang)],
                         [2.2 + 0.38 * np.sin(ang), 2.2 + 0.52 * np.sin(ang)], color=GOLD, lw=3, alpha=main * ha, zorder=9)
            outline(dax.text(0, -2.2, "pore CLOSED → water saved", ha="center", fontsize=23, color=CYAN, fontweight="bold",
                             alpha=main * hot * (1 - ease(c.phase("cost", 0.0, 0.2))), zorder=9))
        ca = ease(c.phase("cost", 0.1, 0.4))
        if ca > 0:
            outline(dax.text(0, -2.2, "food-making slows… but no wilting", ha="center", fontsize=21, color=GOLD,
                             fontweight="bold", alpha=main * ca, zorder=9))
    if de > 0.01:
        d = de * (1 - ma)
        night = ease(c.phase("desert", 0.15, 0.4)) * (1 - ease(c.phase("desert", 0.6, 0.8)))
        day = ease(c.phase("desert", 0.6, 0.8))
        # cactus
        dax.add_patch(FancyBboxPatch((-0.35, -2.0), 0.7, 3.4, boxstyle="round,pad=0,rounding_size=0.35",
                                     facecolor="#2f8a4a", edgecolor="#1f6b35", lw=3, alpha=d, zorder=6))
        for sx in (-1, 1):
            dax.add_patch(FancyBboxPatch((sx * 0.35 - (0.9 if sx < 0 else 0), 0.0), 0.9, 0.45,
                                         boxstyle="round,pad=0,rounding_size=0.2", facecolor="#2f8a4a",
                                         edgecolor="#1f6b35", lw=3, alpha=d, zorder=5))
            dax.add_patch(FancyBboxPatch((sx * 1.1 - 0.22, 0.0), 0.45, 1.2, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#2f8a4a", edgecolor="#1f6b35", lw=3, alpha=d, zorder=5))
        if night > 0:
            dax.add_patch(Circle((-2.5, 2.0), 0.35, color="#e8e8ff", alpha=d * night, zorder=6))
            dax.add_patch(Circle((-2.35, 2.1), 0.3, color="#0b1530", alpha=d * night, zorder=7))
            outline(dax.text(2.1, 1.5, "night: open\nstore CO₂", ha="center", va="center", fontsize=22, color=CYAN,
                             fontweight="bold", alpha=d * night, zorder=8))
        if day > 0:
            dax.add_patch(Circle((2.5, 2.0), 0.38, color=GOLD, alpha=d * day, zorder=6))
            outline(dax.text(-2.1, 1.5, "day: closed\nuse stored CO₂", ha="center", va="center", fontsize=22,
                             color=GOLD, fontweight="bold", alpha=d * day, zorder=8))
    if ma > 0.01:
        outline(dax.text(0, 0.8, "water first", ha="center", fontsize=46, color=CYAN, fontweight="bold", alpha=ma, zorder=8))
        outline(dax.text(0, -0.4, "food later", ha="center", fontsize=46, color=GREEN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=8))
    c.steps([("open: CO₂ in, but water out", 0.0, WHITE),
             ("hot & dry → close to save water", 0.3, GOLD)], ys=(0.345, 0.285))
