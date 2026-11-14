"""ui/flame_lab.py - la fiamma animata (resa ILLUSTRATIVA, non una simulazione fisica).

build_html() e' una funzione pura (testabile senza Streamlit); render() la mostra nell'app.
Valori presi dal prototipo grafico del progetto.
"""

STAGE_H = 420

GRAVITY = {
    "earth": dict(name="Terra", g="1", w=118, h=236, br="50% 50% 50% 50% / 70% 70% 30% 30%", dur="1.05s",
                  anim="flicker", origin="50% 100%", bottom=58, mid_b=7, core_b=12, center=False,
                  outer="rgba(255,86,24,.82)", mid="#ffa238", core="#fff0bd", halo="rgba(255,110,40,"),
    "mars": dict(name="Marte", g="0,38", w=140, h=208, br="50% 50% 50% 50% / 64% 64% 36% 36%", dur="1.5s",
                 anim="flicker", origin="50% 100%", bottom=84, mid_b=7, core_b=12, center=False,
                 outer="rgba(255,100,50,.80)", mid="#ffb06a", core="#fff0d8", halo="rgba(255,115,60,"),
    "moon": dict(name="Luna", g="0,16", w=168, h=180, br="50% 50% 50% 50% / 56% 56% 44% 44%", dur="2.2s",
                 anim="flicker", origin="50% 100%", bottom=110, mid_b=8, core_b=14, center=False,
                 outer="rgba(255,120,110,.76)", mid="#ffc08a", core="#fff6ea", halo="rgba(255,130,120,"),
    "iss": dict(name="Microgravità", g="0", w=190, h=190, br="50%", dur="3.4s",
                anim="breathe", origin="50% 50%", bottom=0, mid_b=19, core_b=35, center=True,
                outer="rgba(70,140,255,.78)", mid="#7fd0ff", core="#effcff", halo="rgba(80,150,255,"),
}

O2_MIN, O2_MAX = 21.0, 85.0


def _fmt(n) -> str:
    return f"{n:g}".replace(".", ",")


def flame_params(gravity: str, o2: float, flow: float) -> dict:
    """Dimensioni e intensita' della fiamma per i parametri dati (usato anche nei test)."""
    g = GRAVITY[gravity]
    k = max(0.0, min(1.0, (o2 - O2_MIN) / (O2_MAX - O2_MIN)))
    f = 0.75 + k * 0.65
    w, h = round(g["w"] * f), round(g["h"] * f)
    bottom = round((STAGE_H - h) / 2) if g["center"] else g["bottom"]
    return {"k": k, "f": f, "w": w, "h": h, "bottom": bottom,
            "lean_deg": round(flow * 0.55, 1), "shift_px": round(flow * 1.6)}


_TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
html,body{margin:0;background:transparent;font-family:'JetBrains Mono',ui-monospace,monospace}
.stage{position:relative;height:__STAGE_H__px;border-radius:22px;overflow:hidden;border:1px solid rgba(255,255,255,.10);
 background:radial-gradient(ellipse at 50% 105%,rgba(255,120,60,.12),transparent 60%),rgba(3,6,16,.78)}
.lean{position:absolute;inset:0;transform-origin:50% 100%;transition:transform .6s ease}
.flame{position:absolute}
.layer{position:absolute}
.tag{position:absolute;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.75)}
.chips{position:absolute;left:18px;right:18px;bottom:14px;display:flex;flex-wrap:wrap;gap:8px}
.chip{padding:6px 11px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);
 font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.9)}
.badge{color:#ffd2b3;border-color:rgba(255,170,120,.55)}
.streak{position:absolute;left:18px;width:90px;height:2px;border-radius:2px;
 background:linear-gradient(90deg,rgba(0,0,0,0),rgba(160,210,255,.9),rgba(0,0,0,0))}
@keyframes flicker{0%,100%{transform:scale(1,1) skewX(0deg)}20%{transform:scale(.96,1.05) skewX(1.6deg)}
 45%{transform:scale(1.03,.97) skewX(-1.2deg)}70%{transform:scale(.98,1.04) skewX(.8deg)}}
@keyframes breathe{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
@keyframes streak{0%{transform:translateX(-30px);opacity:0}25%{opacity:1}100%{transform:translateX(240px);opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style></head><body>
<div class="stage" role="img" aria-label="Fiamma illustrativa: __NAME__, __G__ g, ossigeno __O2__ percento">
__STREAKS__
<div class="lean" style="transform:translateX(__SHIFT__px) rotate(__LEAN__deg)">
  <div style="__HALO__"></div>
  <div class="flame" style="__FLAME__">
    <div class="layer" style="__OUTER__"></div>
    <div class="layer" style="__MID__"></div>
    <div class="layer" style="__CORE__"></div>
  </div>
</div>
<div class="tag" style="left:18px;top:16px">g = __G__</div>
<div class="tag" style="right:18px;top:16px">__NAME__</div>
<div class="tag" style="left:50%;top:16px;transform:translateX(-50%)"><span class="chip badge">Resa illustrativa · non CFD</span></div>
<div class="chips"><span class="chip">O₂ __O2__ %</span><span class="chip">P __P__ psia</span><span class="chip">Flusso __FLOW__ cm/s</span></div>
</div></body></html>"""


def build_html(gravity: str, o2: float, pressure: float, flow: float) -> str:
    if gravity not in GRAVITY:
        raise ValueError(f"gravita' sconosciuta: {gravity}")
    g = GRAVITY[gravity]
    p = flame_params(gravity, o2, flow)
    w, h, bottom, k = p["w"], p["h"], p["bottom"], p["k"]

    flame = (f"left:50%;margin-left:{-round(w / 2)}px;bottom:{bottom}px;width:{w}px;height:{h}px;"
             f"transform-origin:{g['origin']};animation:{g['anim']} {g['dur']} ease-in-out infinite;")
    outer = (f"inset:0;border-radius:{g['br']};background:radial-gradient(ellipse at 50% 72%,{g['mid']} 0%,"
             f"{g['outer']} 52%,rgba(0,0,0,0) 76%);filter:blur(9px);opacity:{0.62 + 0.38 * k:.2f}")
    mid = (f"left:20%;width:60%;height:62%;bottom:{g['mid_b']}%;border-radius:{g['br']};"
           f"background:radial-gradient(ellipse at 50% 70%,{g['core']} 0%,{g['mid']} 58%,rgba(0,0,0,0) 80%);filter:blur(5px)")
    core = (f"left:36%;width:28%;height:30%;bottom:{g['core_b']}%;border-radius:50%;"
            f"background:radial-gradient(ellipse at 50% 60%,#fff 0%,{g['core']} 62%,rgba(0,0,0,0) 100%);filter:blur(3px)")
    hs = round(max(w, h) * 2.4)
    halo = (f"position:absolute;left:50%;margin-left:{-round(hs / 2)}px;bottom:{round(bottom + h / 2 - hs / 2)}px;"
            f"width:{hs}px;height:{hs}px;border-radius:50%;"
            f"background:radial-gradient(circle,{g['halo']}{0.16 + 0.3 * k:.2f}) 0%,rgba(0,0,0,0) 62%)")

    sdur = max(0.9, 3.4 - flow * 0.09)
    sop = min(1.0, flow / 18)
    streaks = "".join(
        f'<div class="streak" style="top:{top};opacity:{sop:.2f};animation:streak {sdur:.2f}s linear {delay} infinite"></div>'
        for top, delay in (("30%", "0s"), ("48%", "0.7s"), ("66%", "1.4s")))

    values = {
        "__STAGE_H__": str(STAGE_H), "__STREAKS__": streaks, "__SHIFT__": str(p["shift_px"]),
        "__LEAN__": str(p["lean_deg"]), "__HALO__": halo, "__FLAME__": flame, "__OUTER__": outer,
        "__MID__": mid, "__CORE__": core, "__G__": g["g"], "__NAME__": g["name"],
        "__O2__": _fmt(o2), "__P__": _fmt(pressure), "__FLOW__": _fmt(flow),
    }
    html = _TEMPLATE
    for key, val in values.items():
        html = html.replace(key, val)
    return html


def render(gravity: str, o2: float, pressure: float, flow: float, height: int = STAGE_H + 10) -> None:
    """Mostra la fiamma nell'app Streamlit."""
    import streamlit.components.v1 as components
    components.html(build_html(gravity, o2, pressure, flow), height=height)
