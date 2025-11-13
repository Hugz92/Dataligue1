# json_to_brevo_intro_modern.py
# ------------------------------------------------------------
# Version MODERNE 2.0 - Design glassmorphism épuré
# Palette sophistiquée, spacing généreux, typographie moderne
# ------------------------------------------------------------

import json
import re
import traceback
from pathlib import Path
from html import escape as html_escape
from typing import Any, Dict, List, Optional


# ====== LOGOS (HTTPS absolus) ======
CLUB_LOGO_URLS = {
    "DL1": "https://dataligue1.s3.sbg.io.cloud.ovh.net/DL1.png",
    "DL1_OFFICIEL": "https://dataligue1.s3.sbg.io.cloud.ovh.net/dl1-logo-officiel.png",
    "ANGERS":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/ANGERS.png",
    "AUXERRE":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/AUXERRE.png",
    "BREST":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/BREST.png",
    "LE HAVRE":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/LE%20HAVRE.png",
    "LENS":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/LENS.png",
    "LILLE":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/LILLE.png",
    "LORIENT":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/LORIENT.png",
    "LYON":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/LYON.png",
    "MARSEILLE":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/MARSEILLE.png",
    "METZ":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/METZ.png",
    "MONACO":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/MONACO.png",
    "NANTES":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/NANTES.png",
    "NICE":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/NICE.png",
    "PARIS FC":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/PARIS%20FC.png",
    "PSG":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/PSG.png",
    "RENNES":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/RENNES.png",
    "STRASBOURG":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/STRASBOURG.png",
    "TOULOUSE":"https://dataligue1.s3.sbg.io.cloud.ovh.net/logo/TOULOUSE.png",
}

# ====== PALETTE MODERNE 2.0 ======
MODERN = {
    # Backgrounds
    "bg_deep":     "#0A0E1A",  # Fond principal très sombre
    "bg_surface":  "#131829",  # Surface cards
    "bg_elevated": "#1A1F35",  # Surface surélevée
    "bg_glass":    "rgba(25, 32, 50, 0.7)",  # Glassmorphism

    # Primary colors
    "primary":     "#3B82F6",  # Blue moderne
    "primary_light": "#60A5FA",
    "accent":      "#06B6D4",  # Cyan
    "accent_light": "#22D3EE",

    # Semantic
    "success":     "#10B981",
    "warning":     "#F59E0B",
    "danger":      "#EF4444",

    # Text
    "text_primary":   "#F8FAFC",
    "text_secondary": "#CBD5E1",
    "text_muted":     "#94A3B8",

    # Borders & effects
    "border":      "rgba(255, 255, 255, 0.1)",
    "border_light": "rgba(255, 255, 255, 0.05)",
    "glow_blue":   "rgba(59, 130, 246, 0.3)",
    "glow_cyan":   "rgba(6, 182, 212, 0.3)",
}

# ====== CONFIG ======
IN_JSON = r"C:\Users\Utilisateur\Desktop\Newsletter DL1\data ligue 1 25-26 scraping\parisfc\parisfc lyon\2025-11-12-paris-fc-lyon.structured.json"


# ====== UTILS ======
def _coerce_str(v):
    if v is None: return ""
    if isinstance(v, (int,float)): return str(v)
    if isinstance(v, dict): return ""
    return str(v)

def norm_team(s: str) -> str:
    if not s: return ""
    return re.sub(r"\s+", " ", s).strip().upper()

def norm_display(name: str) -> str:
    name = _coerce_str(name)
    if not name: return ""
    out=[]
    for w in name.split():
        out.append(w.upper() if len(w)<=3 else w.capitalize())
    return " ".join(out)

def logo_img(team: str, size: int = 36, rounded: bool = True, alt: str = None) -> str:
    key = norm_team(team)
    url = CLUB_LOGO_URLS.get(key, "")
    if not url: return ""
    br = "50%" if rounded else "8px"
    alt_text = alt if alt is not None else key
    return (f'<img src="{url}" alt="{html_escape(alt_text)}" '
            f'style="max-width:{size}px;height:auto;display:block;margin:0 auto;border-radius:{br};" />')

def md_to_email_html(md: str, font_barlow=False) -> str:
    """Mini markdown pour email."""
    if not isinstance(md, str): return ""
    md = md.replace("\r\n","\n").replace("\r","\n")
    lines = md.split("\n")
    html, in_list = [], False

    for raw in lines:
        ln = (raw or "").strip()
        if not ln:
            if in_list: html.append("</ul>"); in_list=False
            continue
        if ln.startswith(("- ","* ")):
            if not in_list:
                html.append(f'<ul style="margin:12px 0 12px 20px;padding:0;color:{MODERN["text_secondary"]};list-style:none;">'); in_list=True
            item = html_escape(ln[2:].strip())
            item = re.sub(r"\*\*(.+?)\*\*", rf"<strong style='color:{MODERN['text_primary']};font-weight:600;'>\1</strong>", item)
            item = re.sub(r"\*(.+?)\*", rf"<em style='color:{MODERN['text_muted']};'>\1</em>", item)
            html.append(f"<li style='margin:8px 0;padding-left:16px;position:relative;font-size:14px;line-height:1.6;'>"
                       f"<span style='position:absolute;left:0;color:{MODERN['accent']};font-weight:700;'>•</span>{item}</li>")
        else:
            if in_list: html.append("</ul>"); in_list=False
            t = html_escape(ln)
            t = re.sub(r"\*\*(.+?)\*\*", rf"<strong style='color:{MODERN['text_primary']};font-weight:600;'>\1</strong>", t)
            t = re.sub(r"\*(.+?)\*", rf"<em style='color:{MODERN['text_muted']};'>\1</em>", t)
            html.append(f"<p style='margin:0 0 14px 0;color:{MODERN['text_secondary']};font-size:15px;line-height:1.7;'>{t}</p>")
    if in_list: html.append("</ul>")
    return "\n".join(html)

def parse_teams_score_from_meta(meta: dict):
    home_team = _coerce_str((meta.get("home") or {}).get("team"))
    away_team = _coerce_str((meta.get("away") or {}).get("team"))
    h_score   = (meta.get("home") or {}).get("score")
    a_score   = (meta.get("away") or {}).get("score")
    if home_team and away_team and (h_score is not None) and (a_score is not None):
        return home_team, f"{h_score}-{a_score}", away_team
    title = _coerce_str(meta.get("title"))
    t = re.sub(r"—.*$","", title).strip()
    m = re.search(r"(.+?)\s+(\d+\s*-\s*\d+)\s+(.+)$", t)
    if m:
        return m.group(1).strip(), m.group(2).strip().replace(" ",""), m.group(3).strip()
    return home_team or "", (f"{h_score}-{a_score}" if h_score is not None and a_score is not None else ""), away_team or ""

def find_intro_and_yc(sections: list):
    if not isinstance(sections, list): return "", ""
    for s in sections:
        title = (s.get("title") or s.get("id") or "").lower()
        if "intro" in title:
            intro_md, yc_md = "", ""
            for b in s.get("blocks", []):
                typ = (b.get("type") or "").lower()
                if typ in ("paragraph","text") and not intro_md:
                    intro_md = _coerce_str(b.get("text"))
                if typ in ("note","analysis_note") and not yc_md:
                    yc_md = _coerce_str(b.get("text"))
            return intro_md, yc_md
    return "", ""

def extract_scorers(facts: dict, meta: dict):
    """Timeline des buteurs."""
    def _format_minute(v):
        if v is None: return "—"
        if isinstance(v, (int, float)):
            return f"{int(v)}'"
        s = str(v).strip().replace("'", "'")
        if s.endswith("'"):
            return s
        return f"{s}'"

    home_name = norm_display((meta.get("home") or {}).get("team"))
    away_name = norm_display((meta.get("away") or {}).get("team"))

    items = []
    for t in facts.get("timeline") or []:
        player   = _coerce_str(t.get("player"))
        assist   = _coerce_str(t.get("assist")) or None
        minute_val = t.get("minute")

        if minute_val is None:
            m = re.match(r"^\s*(\d+\s*(?:\+\s*\d+)?)\s*'?[\s-]*", player)
            if m:
                minute_val = m.group(1)
                player = re.sub(r"^\s*\d+\s*(?:\+\s*\d+)?\s*'?[\s-]*", "", player).strip()

        minute_str = _format_minute(minute_val)

        side = None
        team = _coerce_str(t.get("team")).strip()
        if team:
            if norm_team(team) == norm_team(home_name):
                side = "home"
            elif norm_team(team) == norm_team(away_name):
                side = "away"
        if not side:
            sraw = (_coerce_str(t.get("side")) or "").lower()
            if sraw in ("home", "away"):
                side = sraw
        if not side:
            side = "center"

        try:
            sort_key = int(str(minute_val).split("+")[0]) if minute_val is not None else 999
        except Exception:
            sort_key = 999

        items.append({
            "minute": minute_str,
            "player": player,
            "assist": assist,
            "side": side,
            "_sort": sort_key
        })

    items.sort(key=lambda x: x["_sort"])
    for it in items:
        it.pop("_sort", None)
    return items

def extract_key_stats(facts: dict):
    """Stats clés."""
    res = {"Possession": ("—","—"), "xG": ("—","—"), "Tirs cadrés": ("—","—")}
    for row in facts.get("keyStats") or []:
        label = (row.get("label") or "").strip().lower()
        if "possession" in label:
            h = row.get("home_pct"); a = row.get("away_pct")
            if h is not None and a is not None:
                res["Possession"] = (f"{h:.0f}%", f"{a:.0f}%")
        elif label == "xg":
            h = row.get("home"); a = row.get("away")
            if h is not None and a is not None:
                res["xG"] = (f"{h:.2f}", f"{a:.2f}")
        elif "tirs" in label and "cadr" in label:
            h = row.get("home"); a = row.get("away")
            if h is not None and a is not None:
                res["Tirs cadrés"] = (str(h), str(a))
    return res

def extract_cards(data: dict):
    """Extraction cartons."""
    facts = data.get("facts") or {}
    cards = facts.get("cards")
    out = {"red": [], "yellow": []}

    if isinstance(cards, dict):
        for k in ("red", "yellow"):
            for it in cards.get(k, []) or []:
                out[k].append({
                    "player": (it.get("player") or "").strip(),
                    "team":   norm_display(it.get("team") or ""),
                    "note":   (it.get("note") or "").strip()
                })
        if out["red"] or out["yellow"]:
            return out

    sections = data.get("sections") or []
    intro_md = ""
    for s in sections:
        title = (s.get("title") or s.get("id") or "").lower()
        if "intro" in title:
            for b in s.get("blocks", []):
                if (b.get("type") or "").lower() in ("paragraph", "text"):
                    intro_md = (b.get("text") or "")
                    break
            break

    if intro_md:
        m = re.search(r"🟥[^\n]*\n(?P<block>(?:\s*[•\-].+\n?)+)", intro_md, flags=re.I)
        if m:
            for ln in (m.group("block") or "").splitlines():
                s = ln.strip().lstrip("•-").strip()
                mm = re.match(r"(.+?)\s*\((.+?)\)\s*(.*)$", s)
                if mm:
                    out["red"].append({
                        "player": mm.group(1).strip(),
                        "team":   norm_display(mm.group(2).strip()),
                        "note":   mm.group(3).strip()
                    })

        m2 = re.search(r"(🟨|jaunes)[^\n]*\n(?P<block>(?:\s*[•\-].+\n?)+)", intro_md, flags=re.I)
        if m2:
            for ln in (m2.group("block") or "").splitlines():
                s = ln.strip().lstrip("•-").strip()
                mm = re.match(r"(.+?)\s*\((.+?)\)\s*(.*)$", s)
                if mm:
                    out["yellow"].append({
                        "player": mm.group(1).strip(),
                        "team":   norm_display(mm.group(2).strip()),
                        "note":   mm.group(3).strip()
                    })

        if not out["yellow"]:
            mcount = re.search(
                r"(\d+)\s*cartons?\s+jaunes.*?\((\d+)\s+([^) ,]+(?:\s+[^) ,]+)*)\s*,\s*(\d+)\s+([^) ,]+(?:\s+[^) ,]+)*)\)",
                intro_md, flags=re.I
            )
            if mcount:
                total = int(mcount.group(1))
                c1 = int(mcount.group(2)); t1 = (mcount.group(3) or "").strip()
                c2 = int(mcount.group(4)); t2 = (mcount.group(5) or "").strip()

                meta = data.get("meta", {}) or {}
                home_name = norm_display(((meta.get("home") or {}).get("team")) or "")
                away_name = norm_display(((meta.get("away") or {}).get("team")) or "")

                def _norm(s): return re.sub(r"\s+", " ", s).strip().upper()
                if home_name and _norm(t1) == _norm(home_name):
                    home, away = c1, c2
                elif home_name and _norm(t2) == _norm(home_name):
                    home, away = c2, c1
                else:
                    home, away = c1, c2

                out["_yellow_counts"] = {
                    "total": total,
                    "home": home,
                    "away": away,
                    "home_name": home_name or "Équipe A",
                    "away_name": away_name or "Équipe B",
                }

    return out

def find_match_images_section(sections: list):
    if not isinstance(sections, list):
        return ("I. LE MATCH EN IMAGES", "", "")
    for s in sections:
        ttl = (s.get("title") or s.get("id") or "").lower()
        if "match en images" in ttl:
            title = s.get("title") or "I. LE MATCH EN IMAGES"
            intro_md, yc_md = "", ""
            for b in s.get("blocks", []):
                t = (b.get("type") or "").lower()
                if t in ("paragraph", "text") and not intro_md:
                    intro_md = _coerce_str(b.get("text"))
                if t in ("note", "analysis_note") and not yc_md:
                    yc_md = _coerce_str(b.get("text"))
            return (title, intro_md, yc_md)
    return ("I. LE MATCH EN IMAGES", "", "")

def get_section(sections, sec_id_or_slug):
    if not isinstance(sections, list):
        return None
    key = (sec_id_or_slug or "").lower()
    for s in sections:
        sid  = (s.get("id")   or "").lower()
        slug = (s.get("slug") or "").lower()
        if key in sid or key in slug:
            return s
    return None

def parse_section_ii(sections):
    out = {
        "title": "",
        "intro_md": "",
        "hist_title": "",
        "hist_md": "",
        "teams": {"home": "", "away": ""},
        "home": [],
        "away": [],
        "podiums": []
    }

    sec = get_section(sections, "ii-hommes")
    if not sec:
        return out

    out["title"] = sec.get("title") or "II. LES HOMMES DU MATCH"

    for b in sec.get("blocks") or []:
        typ = (b.get("type") or "").lower()
        if typ == "paragraph" and not out["intro_md"]:
            out["intro_md"] = (b.get("text") or "").strip()
        elif typ in ("subheading", "heading") and "histor" in (b.get("title") or "").lower():
            out["hist_title"] = b.get("title") or ""
        elif typ == "paragraph" and (
            "top 50" in (b.get("text") or "").lower() or "historique" in (b.get("text") or "").lower()
        ):
            out["hist_md"] = (b.get("text") or "").strip()

    for b in sec.get("blocks") or []:
        if (b.get("type") or "").lower() == "top_performers":
            data  = b.get("data") or {}
            teams = data.get("teams") or {}
            out["teams"]["home"] = teams.get("home") or out["teams"]["home"]
            out["teams"]["away"] = teams.get("away") or out["teams"]["away"]

            def _norm_list(lst):
                res = []
                for it in lst or []:
                    metrics = [it.get("metric_1") or "", it.get("metric_2") or "", it.get("metric_3") or ""]
                    metrics = [m for m in metrics if m]
                    res.append({
                        "rank":    it.get("rank"),
                        "player":  it.get("player") or "",
                        "minutes": it.get("minutes"),
                        "rating":  it.get("rating"),
                        "metrics": metrics
                    })
                try:
                    res.sort(key=lambda x: (x["rank"] if x.get("rank") is not None else 99))
                except Exception:
                    pass
                return res[:3]

            out["home"] = _norm_list(data.get("home"))
            out["away"] = _norm_list(data.get("away"))
            return out

    tables_any = sec.get("tables_any") or []
    for t in tables_any:
        club_title = (t.get("title") or "").strip()
        headers    = [h for h in (t.get("headers") or []) if isinstance(h, str)]
        values = []
        rows = t.get("rows") or []
        if rows and isinstance(rows[0], list):
            for cell in rows[0]:
                values.append("" if cell is None else str(cell))
        out["podiums"].append({
            "club_title": club_title,
            "headers": headers,
            "values": values
        })

    return out

def parse_section_iii(sections):
    sec = (
        get_section(sections, "iii-chiffres")
        or get_section(sections, "iii-ce-que-racontent-les-chiffres")
        or get_section(sections, "ce-que-racontent")
    )
    out = {"title": "", "intro_md": "", "yc_md": "", "tables": []}
    if not sec:
        return out

    out["title"] = sec.get("title") or "III. CE QUE RACONTENT LES CHIFFRES"

    for b in (sec.get("blocks") or []):
        typ = (b.get("type") or "").lower()
        if typ == "paragraph" and not out["intro_md"]:
            out["intro_md"] = (b.get("text") or "").strip()
        elif typ == "note":
            out["yc_md"] = (b.get("text") or "").strip()

    for t in (sec.get("tables_any") or []):
        title   = t.get("title") or ""
        headers = [h for h in (t.get("headers") or []) if isinstance(h, str)]
        rows    = [r for r in (t.get("rows") or []) if isinstance(r, list)]
        teams   = t.get("teams") or {}
        out["tables"].append({"title": title, "headers": headers, "rows": rows, "teams": teams})

    return out

_LWB_PATTERNS = [
    "erreur", "carton", "hors-jeux", "hors jeux", "csc", "contre son camp",
    "fautes", "faute", "tirs concédés"
]

def lower_is_better(metric_name: str) -> bool:
    n = (metric_name or "").lower()
    return any(p in n for p in _LWB_PATTERNS)

def _try_float(x):
    try:
        return float(str(x).replace(",", ".").replace("%", "").strip())
    except Exception:
        return None

def _is_percent_metric(metric_name: str) -> bool:
    return "%" in (metric_name or "")

def format_metric_value(metric_name: str, value):
    v = _try_float(value)
    if v is None:
        return html_escape(str(value)), None

    if _is_percent_metric(metric_name):
        return f"{v:.1f}%", v
    if abs(v - int(v)) < 1e-9:
        return f"{int(v)}", v
    return f"{v:.1f}", v

def compare_values(metric_name: str, home_val, away_val):
    h = _try_float(home_val)
    a = _try_float(away_val)
    if h is None or a is None:
        return None
    if lower_is_better(metric_name):
        if h < a: return "home"
        if a < h: return "away"
        return None
    else:
        if h > a: return "home"
        if a > h: return "away"
        return None


# ====== RENDERERS MODERNE 2.0 ======

def render_header():
    """Header minimaliste avec logos et titre épuré."""
    left_logo  = logo_img("DL1", 48)
    right_logo = logo_img("DL1_OFFICIEL", 48)

    return f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:32px;">
  <tr>
    <td style="background:{MODERN['bg_surface']};
               padding:24px;
               border-radius:16px;
               border:1px solid {MODERN['border']};
               box-shadow:0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td style="width:20%;text-align:center;vertical-align:middle;padding:0 12px;">{left_logo}</td>
          <td style="width:60%;text-align:center;vertical-align:middle;padding:0 12px;">
            <div style="color:{MODERN['text_primary']};
                        font-size:22px;
                        font-weight:700;
                        letter-spacing:0.5px;
                        margin-bottom:4px;
                        text-transform:uppercase;">
              Analyse Data Ligue 1
            </div>
            <div style="color:{MODERN['text_muted']};
                        font-size:13px;
                        font-weight:500;
                        letter-spacing:0.3px;">
              Newsletter Match
            </div>
          </td>
          <td style="width:20%;text-align:center;vertical-align:middle;padding:0 12px;">{right_logo}</td>
        </tr>
      </table>
    </td>
  </tr>
</table>
""".strip()


def render_scoreline(home, score, away, league):
    """Score moderne avec glassmorphism."""
    h_logo = logo_img(home, 48)
    a_logo = logo_img(away, 48)
    league = league or "Ligue 1"

    return f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
  <tr>
    <td style="background:{MODERN['bg_surface']};
               padding:28px 20px;
               border-radius:16px;
               border:1px solid {MODERN['border']};
               box-shadow:0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(59,130,246,0.1);">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td style="width:38%;text-align:center;vertical-align:middle;padding:0 8px;">
            <div style="margin-bottom:12px;">{h_logo}</div>
            <div style="color:{MODERN['text_primary']};
                        font-size:16px;
                        font-weight:600;
                        letter-spacing:0.3px;">
              {html_escape(norm_display(home))}
            </div>
          </td>
          <td style="width:24%;text-align:center;vertical-align:middle;padding:0 8px;">
            <div style="background:{MODERN['bg_elevated']};
                        border:1px solid {MODERN['border']};
                        border-radius:12px;
                        padding:14px 20px;
                        box-shadow:inset 0 2px 8px rgba(0,0,0,0.3);">
              <div style="color:{MODERN['text_primary']};
                          font-size:32px;
                          font-weight:700;
                          line-height:1;
                          margin-bottom:6px;">
                {html_escape(score or '—')}
              </div>
              <div style="color:{MODERN['text_muted']};
                          font-size:10px;
                          font-weight:600;
                          text-transform:uppercase;
                          letter-spacing:0.5px;">
                {html_escape(league)}
              </div>
            </div>
          </td>
          <td style="width:38%;text-align:center;vertical-align:middle;padding:0 8px;">
            <div style="margin-bottom:12px;">{a_logo}</div>
            <div style="color:{MODERN['text_primary']};
                        font-size:16px;
                        font-weight:600;
                        letter-spacing:0.3px;">
              {html_escape(norm_display(away))}
            </div>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
""".strip()


def render_timeline(scorers):
    """Timeline minimaliste et élégante."""
    if not scorers:
        return ""

    rows = []
    for s in scorers:
        minute = html_escape(s["minute"])
        assist = (
            f"<div style='color:{MODERN['text_muted']};font-size:12px;margin-top:4px;'>⚙️ {html_escape(s['assist'])}</div>"
            if s.get("assist") else ""
        )

        if s["side"] == "home":
            left = f"""
            <div style="display:inline-block;
                        background:{MODERN['bg_elevated']};
                        border:1px solid {MODERN['border']};
                        padding:10px 14px;
                        border-radius:12px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.2);">
              <div style="color:{MODERN['text_primary']};
                          font-size:14px;
                          font-weight:600;">
                ⚽ {html_escape(s['player'])}
              </div>
              {assist}
            </div>"""
            right = ""
            pill = f"""<div style="display:inline-block;
                                   background:{MODERN['primary']};
                                   color:#ffffff;
                                   padding:6px 12px;
                                   border-radius:8px;
                                   font-weight:700;
                                   font-size:13px;
                                   min-width:40px;
                                   text-align:center;
                                   box-shadow:0 2px 8px {MODERN['glow_blue']};">
                        {minute}
                      </div>"""
        elif s["side"] == "away":
            left = ""
            right = f"""
            <div style="display:inline-block;
                        background:{MODERN['bg_elevated']};
                        border:1px solid {MODERN['border']};
                        padding:10px 14px;
                        border-radius:12px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.2);">
              <div style="color:{MODERN['text_primary']};
                          font-size:14px;
                          font-weight:600;">
                {html_escape(s['player'])} ⚽
              </div>
              {assist}
            </div>"""
            pill = f"""<div style="display:inline-block;
                                   background:{MODERN['accent']};
                                   color:#ffffff;
                                   padding:6px 12px;
                                   border-radius:8px;
                                   font-weight:700;
                                   font-size:13px;
                                   min-width:40px;
                                   text-align:center;
                                   box-shadow:0 2px 8px {MODERN['glow_cyan']};">
                        {minute}
                      </div>"""
        else:
            left, right = "", f"""
            <div style="display:inline-block;
                        background:{MODERN['bg_elevated']};
                        border:1px solid {MODERN['border']};
                        padding:10px 14px;
                        border-radius:12px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.2);">
              <div style="color:{MODERN['text_primary']};
                          font-size:14px;
                          font-weight:600;">
                ⚽ {html_escape(s['player'])}
              </div>
              {assist}
            </div>"""
            pill = f"""<div style="display:inline-block;
                                   background:{MODERN['bg_elevated']};
                                   border:1px solid {MODERN['border']};
                                   color:{MODERN['text_primary']};
                                   padding:6px 12px;
                                   border-radius:8px;
                                   font-weight:700;
                                   font-size:13px;
                                   min-width:40px;
                                   text-align:center;">
                        {minute}
                      </div>"""

        rows.append(f"""
        <tr>
          <td style="width:42%;text-align:left;padding:10px 8px;">{left}</td>
          <td style="width:16%;text-align:center;padding:10px 8px;">{pill}</td>
          <td style="width:42%;text-align:right;padding:10px 8px;">{right}</td>
        </tr>""")

    body = "\n".join(rows)
    return f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
  <tr>
    <td style="background:{MODERN['bg_surface']};
               border-radius:16px;
               border:1px solid {MODERN['border']};
               box-shadow:0 4px 24px rgba(0,0,0,0.3);">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td colspan="3"
              style="background:{MODERN['bg_elevated']};
                     padding:14px 16px;
                     border-radius:16px 16px 0 0;
                     border-bottom:1px solid {MODERN['border']};
                     text-align:center;">
            <div style="color:{MODERN['text_primary']};
                        font-size:14px;
                        font-weight:600;
                        text-transform:uppercase;
                        letter-spacing:0.5px;">
              ⚡ Le fil du match
            </div>
          </td>
        </tr>
        {body}
      </table>
    </td>
  </tr>
</table>
""".strip()


def render_key_stats_panel(meta: dict, facts: dict) -> str:
    """Stats clés moderne avec barres de progression élégantes."""
    home = (meta.get("home") or {}).get("team") or "ÉQUIPE A"
    away = (meta.get("away") or {}).get("team") or "ÉQUIPE B"

    def _e(s):
        from html import escape as esc
        return esc(str(s)) if s is not None else ""

    def _fmt(v):
        if v is None: return "—"
        try:
            f = float(v)
            return f"{f:.2f}".rstrip("0").rstrip(".")
        except Exception:
            return str(v)

    def _num(v):
        try:
            return float(v)
        except Exception:
            return None

    key_stats = facts.get("keyStats") or []
    def _sort_key(s):
        lab = (s.get("label") or "").lower()
        return (0 if "possession" in lab else 1, lab)
    key_stats = sorted(key_stats, key=_sort_key)

    rows_html = ""
    for idx, s in enumerate(key_stats):
        label_raw = (s.get("label") or "").strip()
        low = label_raw.lower()

        if "possession" in low:
            h = _num(s.get("home_pct"))
            a = _num(s.get("away_pct"))
            h = 0.0 if h is None else max(0.0, min(100.0, h))
            a = (100.0 - h) if s.get("away_pct") is None else (0.0 if a is None else max(0.0, min(100.0, a)))

            left_style  = f"font-weight:700;color:{MODERN['text_primary']};"  if h > a else f"font-weight:600;color:{MODERN['text_secondary']};"
            right_style = f"font-weight:700;color:{MODERN['text_primary']};"  if a > h else f"font-weight:600;color:{MODERN['text_secondary']};"

            bar = f"""
            <table border="0" cellpadding="0" cellspacing="0" width="100%"
                   style="background:{MODERN['bg_deep']};
                          border:1px solid {MODERN['border_light']};
                          border-radius:999px;
                          overflow:hidden;">
              <tr>
                <td width="{h:.0f}%" style="background:{MODERN['primary']};
                           height:8px;line-height:0;font-size:0;">&nbsp;</td>
                <td width="{a:.0f}%" style="background:{MODERN['accent']};
                           height:8px;line-height:0;font-size:0;">&nbsp;</td>
              </tr>
            </table>"""

            row_html = f"""
            <tr>
              <td style="width:33%;text-align:center;padding:16px 12px;{left_style}font-size:15px;">{h:.0f}%</td>
              <td style="width:34%;text-align:center;padding:16px 12px;">
                <div style="color:{MODERN['text_secondary']};
                            font-weight:600;
                            font-size:12px;
                            letter-spacing:0.5px;
                            text-transform:uppercase;
                            margin-bottom:8px;">
                  Possession
                </div>
                {bar}
              </td>
              <td style="width:33%;text-align:center;padding:16px 12px;{right_style}font-size:15px;">{a:.0f}%</td>
            </tr>"""

        else:
            h_val = s.get("home") or s.get("home_pct")
            a_val = s.get("away") or s.get("away_pct")

            hn = _num(h_val)
            an = _num(a_val)

            label_center = label_raw
            if low == "xg":
                label_center = "🎯 xG"
            elif ("tirs" in low and "cadr" in low):
                label_center = "🥅 Tirs cadrés"

            if (hn is not None) and (an is not None):
                left_style  = f"font-weight:700;color:{MODERN['text_primary']};"  if hn > an else f"font-weight:600;color:{MODERN['text_secondary']};"
                right_style = f"font-weight:700;color:{MODERN['text_primary']};"  if an > hn else f"font-weight:600;color:{MODERN['text_secondary']};"
            else:
                left_style = right_style = f"font-weight:600;color:{MODERN['text_secondary']};"

            row_html = f"""
            <tr>
              <td style="width:33%;text-align:center;padding:16px 12px;{left_style}font-size:15px;">{_e(_fmt(h_val))}</td>
              <td style="width:34%;text-align:center;padding:16px 12px;
                         color:{MODERN['text_secondary']};
                         font-weight:600;
                         font-size:12px;
                         letter-spacing:0.5px;
                         text-transform:uppercase;">
                {_e(label_center)}
              </td>
              <td style="width:33%;text-align:center;padding:16px 12px;{right_style}font-size:15px;">{_e(_fmt(a_val))}</td>
            </tr>"""

        rows_html += row_html
        if idx < len(key_stats) - 1:
            rows_html += f"""
        <tr>
          <td colspan="3" style="height:1px;line-height:0;font-size:0;background:{MODERN['border_light']};">&nbsp;</td>
        </tr>"""

    return f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
  <tr>
    <td style="background:{MODERN['bg_surface']};
               border-radius:16px;
               border:1px solid {MODERN['border']};
               box-shadow:0 4px 24px rgba(0,0,0,0.3);">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td colspan="3" style="background:{MODERN['bg_elevated']};
                                  padding:14px 16px;
                                  border-radius:16px 16px 0 0;
                                  border-bottom:1px solid {MODERN['border']};
                                  text-align:center;">
            <div style="color:{MODERN['text_primary']};
                        font-size:14px;
                        font-weight:600;
                        text-transform:uppercase;
                        letter-spacing:0.5px;">
              📊 Statistiques clés
            </div>
          </td>
        </tr>
        <tr>
          <td colspan="3" style="padding:12px 16px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td style="width:33%;text-align:center;padding:8px;">
                  <span style="display:inline-block;
                               background:{MODERN['bg_elevated']};
                               border:1px solid {MODERN['border']};
                               border-radius:8px;
                               padding:6px 12px;
                               color:{MODERN['text_secondary']};
                               font-weight:600;
                               font-size:11px;
                               letter-spacing:0.3px;
                               text-transform:uppercase;">
                    🏠 {_e(home)}
                  </span>
                </td>
                <td style="width:34%;text-align:center;padding:8px;">
                  <span style="display:inline-block;
                               background:{MODERN['primary']};
                               color:#ffffff;
                               border-radius:8px;
                               padding:6px 14px;
                               font-weight:600;
                               font-size:11px;
                               letter-spacing:0.3px;
                               text-transform:uppercase;
                               box-shadow:0 2px 8px {MODERN['glow_blue']};">
                    Stats
                  </span>
                </td>
                <td style="width:33%;text-align:center;padding:8px;">
                  <span style="display:inline-block;
                               background:{MODERN['bg_elevated']};
                               border:1px solid {MODERN['border']};
                               border-radius:8px;
                               padding:6px 12px;
                               color:{MODERN['text_secondary']};
                               font-weight:600;
                               font-size:11px;
                               letter-spacing:0.3px;
                               text-transform:uppercase;">
                    ✈️ {_e(away)}
                  </span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        {rows_html}
      </table>
    </td>
  </tr>
</table>
""".strip()


def render_cards_boxes_side_by_side(cards):
    """Cartons avec design moderne épuré."""

    def box_container(title_text, content_html, color_hex):
        return f"""
        <table border="0" cellpadding="0" cellspacing="0" width="100%"
               style="background:{MODERN['bg_surface']};
                      border-left:3px solid {color_hex};
                      border-radius:12px;
                      border:1px solid {MODERN['border']};
                      box-shadow:0 4px 16px rgba(0,0,0,0.25);">
          <tr>
            <td style="padding:16px 18px;">
              <div style="color:{color_hex};
                          font-size:12px;
                          font-weight:600;
                          text-transform:uppercase;
                          letter-spacing:0.5px;
                          margin-bottom:12px;">
                {title_text}
              </div>
              {content_html}
            </td>
          </tr>
        </table>
        """

    def render_list(items_html):
        return f"""
        <ul style='margin:0;padding:0;list-style:none;'>
          {items_html}
        </ul>
        """

    def render_empty_state(message):
        return f"<div style='color:{MODERN['text_muted']};font-size:13px;font-style:italic;text-align:center;padding:12px 0;'>{message}</div>"

    # Cartons ROUGES
    reds = cards.get("red") or []
    if reds:
        lis = []
        for c in reds:
            who  = html_escape(c.get("player", "Joueur inconnu"))
            team = html_escape(c.get("team", ""))
            note = html_escape(c.get("note", ""))

            line = f"<div style='color:{MODERN['text_primary']};font-weight:600;font-size:14px;margin-bottom:2px;'>{who}</div>"
            if team:
                line += f"<div style='color:{MODERN['text_muted']};font-size:12px;'>{team}</div>"
            if note:
                line += f"<div style='color:{MODERN['text_secondary']};font-size:12px;margin-top:4px;'>{note}</div>"

            lis.append(f"<li style='margin:0 0 12px 0;padding:10px;background:{MODERN['bg_elevated']};border-radius:8px;border:1px solid {MODERN['border_light']};'>{line}</li>")

        red_inner = render_list("".join(lis))
    else:
        red_inner = render_empty_state("Aucun carton rouge")

    red_box = box_container("🟥 Cartons rouges", red_inner, MODERN["danger"])

    # Cartons JAUNES
    yellows = cards.get("yellow") or []
    if yellows:
        lis = []
        for c in yellows:
            who  = html_escape(c.get("player", "Joueur inconnu"))
            team = html_escape(c.get("team", ""))
            note = html_escape(c.get("note", ""))

            line = f"<div style='color:{MODERN['text_primary']};font-weight:600;font-size:14px;margin-bottom:2px;'>{who}</div>"
            if team:
                line += f"<div style='color:{MODERN['text_muted']};font-size:12px;'>{team}</div>"
            if note:
                line += f"<div style='color:{MODERN['text_secondary']};font-size:12px;margin-top:4px;'>{note}</div>"

            lis.append(f"<li style='margin:0 0 12px 0;padding:10px;background:{MODERN['bg_elevated']};border-radius:8px;border:1px solid {MODERN['border_light']};'>{line}</li>")

        yel_inner = render_list("".join(lis))
    else:
        yc = cards.get("_yellow_counts") or {}
        home_name = html_escape(yc.get('home_name', 'Équipe A'))
        away_name = html_escape(yc.get('away_name', 'Équipe B'))
        home_cnt  = yc.get('home', 0)
        away_cnt  = yc.get('away', 0)
        total_cnt = yc.get('total', 0)

        if total_cnt > 0:
            lis = [
                f"<li style='margin:0 0 8px 0;padding:10px;background:{MODERN['bg_elevated']};border-radius:8px;border:1px solid {MODERN['border_light']};display:flex;justify-content:space-between;align-items:center;'><span style='color:{MODERN['text_secondary']};font-weight:600;'>{home_name}</span><span style='color:{MODERN['warning']};font-weight:700;font-size:16px;'>{home_cnt}</span></li>",
                f"<li style='margin:0 0 8px 0;padding:10px;background:{MODERN['bg_elevated']};border-radius:8px;border:1px solid {MODERN['border_light']};display:flex;justify-content:space-between;align-items:center;'><span style='color:{MODERN['text_secondary']};font-weight:600;'>{away_name}</span><span style='color:{MODERN['warning']};font-weight:700;font-size:16px;'>{away_cnt}</span></li>",
                f"<li style='margin:12px 0 0 0;padding:10px;background:{MODERN['bg_elevated']};border-radius:8px;border:1px solid {MODERN['border']};border-top:2px solid {MODERN['warning']};display:flex;justify-content:space-between;align-items:center;'><span style='color:{MODERN['text_primary']};font-weight:700;'>Total</span><span style='color:{MODERN['warning']};font-weight:700;font-size:18px;'>{total_cnt}</span></li>",
            ]
            yel_inner = render_list("".join(lis))
        else:
            yel_inner = render_empty_state("Aucun carton jaune")

    yellow_box = box_container("🟨 Cartons jaunes", yel_inner, MODERN["warning"])

    return f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
  <tr>
    <td style="width:50%;vertical-align:top;padding:0 8px 0 0;">{red_box}</td>
    <td style="width:50%;vertical-align:top;padding:0 0 0 8px;">{yellow_box}</td>
  </tr>
</table>
""".strip()


def render_yc_comment(yc_md):
    """Commentaire YC moderne."""
    if not yc_md:
        return ""

    yc_html = md_to_email_html(yc_md, font_barlow=False)

    # Mise en gras des nombres
    import re
    parts = re.split(r'(<[^>]+>)', yc_html)
    num_pat = re.compile(r'(?<!\w)(\d+(?:[.,]\d+)?(?:\s*\+\s*\d+)?%?)(?!\w)')
    for i in range(0, len(parts), 2):
        parts[i] = num_pat.sub(
            rf"<strong style='font-weight:700;color:{MODERN['primary_light']};'>\1</strong>",
            parts[i]
        )
    yc_html_bold = "".join(parts)

    return f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
  <tr>
    <td style="background:{MODERN['bg_surface']};
               padding:20px;
               border-radius:12px;
               border-left:3px solid {MODERN['accent']};
               border:1px solid {MODERN['border']};
               box-shadow:0 4px 16px rgba(6,182,212,0.15);">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
        <div style="font-size:18px;">💬</div>
        <div style="color:{MODERN['accent_light']};
                    font-size:12px;
                    font-weight:600;
                    letter-spacing:0.5px;
                    text-transform:uppercase;">
          Décryptage express
        </div>
      </div>
      <div style="color:{MODERN['text_secondary']};
                  font-size:15px;
                  line-height:1.7;">
        {yc_html_bold}
      </div>
    </td>
  </tr>
</table>
""".strip()


def render_match_images_modern(title_txt: str, intro_md: str, yc_md: str) -> str:
    """Section I moderne épurée."""

    title_html = f"""
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
      <tr>
        <td style="background:{MODERN['bg_surface']};
                   padding:24px;
                   border-radius:16px;
                   border:1px solid {MODERN['border']};
                   box-shadow:0 4px 24px rgba(0,0,0,0.3);">
          <div style="text-align:center;">
            <div style="display:inline-block;
                        background:{MODERN['primary']};
                        color:#ffffff;
                        padding:6px 12px;
                        border-radius:6px;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:0.5px;
                        margin-bottom:14px;
                        box-shadow:0 2px 8px {MODERN['glow_blue']};">
              I
            </div>
            <div style="color:{MODERN['text_primary']};
                        font-size:24px;
                        font-weight:700;
                        letter-spacing:0.3px;
                        text-transform:uppercase;
                        margin-bottom:8px;">
              {html_escape(title_txt)}
            </div>
            <div style="width:64px;
                        height:3px;
                        margin:0 auto;
                        background:{MODERN['primary']};
                        border-radius:2px;
                        box-shadow:0 0 12px {MODERN['glow_blue']};"></div>
          </div>
        </td>
      </tr>
    </table>
    """.strip()

    intro_text = re.sub(r'[*_]', '', (intro_md or '').strip())
    intro_html = ""
    if intro_text:
        intro_html = f"""
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:18px;">
      <tr>
        <td style="text-align:center;padding:0;">
          <span style="display:inline-block;
                       background:{MODERN['bg_elevated']};
                       color:{MODERN['text_secondary']};
                       border:1px solid {MODERN['border']};
                       padding:8px 16px;
                       border-radius:8px;
                       font-size:12px;
                       font-weight:600;
                       letter-spacing:0.3px;">
            {html_escape(intro_text)}
          </span>
        </td>
      </tr>
    </table>
    """.strip()

    yc_html = ""
    if yc_md:
        yc_body = md_to_email_html(yc_md)
        yc_html = f"""
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
      <tr>
        <td style="padding:18px;
                   background:{MODERN['bg_surface']};
                   border-radius:12px;
                   border-left:3px solid {MODERN['accent']};
                   border:1px solid {MODERN['border']};
                   box-shadow:0 4px 16px rgba(6,182,212,0.15);">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <div style="font-size:16px;">💬</div>
            <div style="color:{MODERN['accent_light']};
                        font-size:12px;
                        font-weight:600;
                        letter-spacing:0.5px;
                        text-transform:uppercase;">
              Décryptage express
            </div>
          </div>
          {yc_body}
        </td>
      </tr>
    </table>
    """.strip()

    return f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:28px;">
  <tr>
    <td style="padding:0;">
      {title_html}
      {intro_html}
      {yc_html}
    </td>
  </tr>
</table>
""".strip()


def render_section_ii_modern(sections, meta=None):
    """Section II - Hommes du match moderne."""
    sec = get_section(sections, "ii-hommes")
    if not sec:
        return ""

    title_txt = sec.get("title") or "II. LES HOMMES DU MATCH"
    intro_md = ""
    hist_title = ""
    hist_md = ""
    yc_md = ""

    for b in sec.get("blocks") or []:
        typ = (b.get("type") or "").lower()
        if typ == "paragraph" and not intro_md:
            intro_md = (b.get("text") or "").strip()
        elif typ in ("subheading", "heading") and "performances" in (b.get("title") or "").lower():
            hist_title = b.get("title") or ""
        elif typ == "paragraph" and "top 50" in (b.get("text") or "").lower():
            hist_md = (b.get("text") or "").strip()
        elif typ == "note":
            yc_md = (b.get("text") or "").strip()

    def _club_names():
        hn = norm_display(((meta or {}).get("home") or {}).get("team") or "ÉQUIPE A")
        an = norm_display(((meta or {}).get("away") or {}).get("team") or "ÉQUIPE B")
        return hn, an

    tp = None
    for b in sec.get("blocks") or []:
        if (b.get("type") or "").lower() == "top_performers":
            tp = b.get("data") or {}
            break

    if not tp:
        home3 = away3 = []
    else:
        home3 = sorted(tp.get("home") or [], key=lambda x: x.get("rank", 99))[:3]
        away3 = sorted(tp.get("away") or [], key=lambda x: x.get("rank", 99))[:3]

    home_name, away_name = _club_names()

    def _player_card(player, rank):
        name = (player or {}).get("player") or "—"
        rating = (player or {}).get("rating")
        rating_str = f"{float(rating):.1f}" if rating not in (None, "") else "—"

        rank_emoji = "🥇" if rank == 1 else ("🥈" if rank == 2 else "🥉")

        metrics = []
        for i in range(1, 4):
            m = (player or {}).get(f"metric_{i}")
            if m:
                metrics.append(f"<div style='color:{MODERN['text_muted']};font-size:11px;margin-top:4px;'>{html_escape(m)}</div>")
        metrics_html = "".join(metrics)

        return f"""
        <table border="0" cellpadding="0" cellspacing="0" width="100%"
               style="background:{MODERN['bg_elevated']};
                      border:1px solid {MODERN['border']};
                      border-radius:12px;
                      margin-bottom:12px;
                      box-shadow:0 2px 12px rgba(0,0,0,0.2);">
          <tr>
            <td style="padding:14px 16px;">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
                <div style="display:flex;align-items:center;gap:8px;">
                  <div style="font-size:20px;">{rank_emoji}</div>
                  <div style="color:{MODERN['text_primary']};font-weight:600;font-size:14px;">
                    {html_escape(name)}
                  </div>
                </div>
                <div style="background:{MODERN['primary']};
                            color:#ffffff;
                            padding:4px 10px;
                            border-radius:6px;
                            font-weight:700;
                            font-size:13px;
                            box-shadow:0 2px 6px {MODERN['glow_blue']};">
                  {rating_str}
                </div>
              </div>
              {metrics_html}
            </td>
          </tr>
        </table>
        """

    def _team_block(emoji, team_name, players):
        if not players:
            return ""

        cards_html = "".join(_player_card(p, p.get("rank", i+1)) for i, p in enumerate(players))

        return f"""
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
          <tr>
            <td style="background:{MODERN['bg_surface']};
                       padding:18px;
                       border-radius:12px;
                       border:1px solid {MODERN['border']};
                       box-shadow:0 4px 20px rgba(0,0,0,0.3);">
              <div style="text-align:center;margin-bottom:16px;">
                <span style="display:inline-block;
                             background:{MODERN['primary']};
                             color:#ffffff;
                             padding:8px 16px;
                             border-radius:8px;
                             font-weight:600;
                             font-size:13px;
                             letter-spacing:0.3px;
                             box-shadow:0 2px 8px {MODERN['glow_blue']};">
                  {html_escape(emoji)} {html_escape(team_name)}
                </span>
              </div>
              {cards_html}
            </td>
          </tr>
        </table>
        """

    title_html = f"""
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
      <tr>
        <td style="background:{MODERN['bg_surface']};
                   padding:24px;
                   border-radius:16px;
                   border:1px solid {MODERN['border']};
                   box-shadow:0 4px 24px rgba(0,0,0,0.3);">
          <div style="text-align:center;">
            <div style="display:inline-block;
                        background:{MODERN['accent']};
                        color:#ffffff;
                        padding:6px 12px;
                        border-radius:6px;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:0.5px;
                        margin-bottom:14px;
                        box-shadow:0 2px 8px {MODERN['glow_cyan']};">
              II
            </div>
            <div style="color:{MODERN['text_primary']};
                        font-size:24px;
                        font-weight:700;
                        letter-spacing:0.3px;
                        text-transform:uppercase;
                        margin-bottom:8px;">
              {html_escape(title_txt)}
            </div>
            <div style="width:64px;
                        height:3px;
                        margin:0 auto;
                        background:{MODERN['accent']};
                        border-radius:2px;
                        box-shadow:0 0 12px {MODERN['glow_cyan']};"></div>
          </div>
        </td>
      </tr>
    </table>
    """.strip()

    intro_text = re.sub(r"[*_]", "", (intro_md or "").strip())
    intro_html = ""
    if intro_text:
        intro_html = f"""
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:18px;">
      <tr>
        <td style="text-align:center;padding:0;">
          <span style="display:inline-block;
                       background:{MODERN['bg_elevated']};
                       color:{MODERN['text_secondary']};
                       border:1px solid {MODERN['border']};
                       padding:8px 16px;
                       border-radius:8px;
                       font-size:12px;
                       font-weight:600;
                       letter-spacing:0.3px;">
            {html_escape(intro_text)}
          </span>
        </td>
      </tr>
    </table>
    """.strip()

    podium_html = ""
    if home3 or away3:
        podium_html = f"""
{_team_block("🏠", home_name, home3)}
{_team_block("✈️", away_name, away3)}
""".strip()

    hist_html = ""
    if hist_title or hist_md:
        tag = f"<div style='color:{MODERN['accent_light']};font-size:13px;font-weight:600;letter-spacing:0.3px;text-transform:uppercase;margin-bottom:10px;'>{html_escape(hist_title)}</div>" if hist_title else ""
        body = md_to_email_html(hist_md) if hist_md else ""
        hist_html = f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
  <tr>
    <td style="padding:16px;
               background:{MODERN['bg_surface']};
               border-radius:12px;
               border-left:3px solid {MODERN['accent']};
               border:1px solid {MODERN['border']};
               box-shadow:0 4px 16px rgba(6,182,212,0.15);">
      {tag}
      {body}
    </td>
  </tr>
</table>""".strip()

    yc_html = ""
    if yc_md:
        yc_body = md_to_email_html(yc_md)
        yc_html = f"""
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
      <tr>
        <td style="background:{MODERN['bg_surface']};
                   padding:18px;
                   border-radius:12px;
                   border-left:3px solid {MODERN['accent']};
                   border:1px solid {MODERN['border']};
                   box-shadow:0 4px 16px rgba(6,182,212,0.15);">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <div style="font-size:16px;">💬</div>
            <div style="color:{MODERN['accent_light']};
                        font-size:12px;
                        font-weight:600;
                        letter-spacing:0.5px;
                        text-transform:uppercase;">
              Décryptage express
            </div>
          </div>
          {yc_body}
        </td>
      </tr>
    </table>""".strip()

    return "\n".join([title_html, intro_html, podium_html, hist_html, yc_html])


def render_section_iii_modern(sections, meta=None):
    """Section III - Chiffres moderne."""
    data = parse_section_iii(sections)
    has_any = any([data.get("intro_md"), data.get("yc_md"), data.get("tables")])
    if not has_any:
        return ""

    title_txt = data.get("title") or "III. CE QUE RACONTENT LES CHIFFRES"

    title_html = f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
  <tr>
    <td style="background:{MODERN['bg_surface']};
               padding:24px;
               border-radius:16px;
               border:1px solid {MODERN['border']};
               box-shadow:0 4px 24px rgba(0,0,0,0.3);">
      <div style="text-align:center;">
        <div style="display:inline-block;
                    background:{MODERN['success']};
                    color:#ffffff;
                    padding:6px 12px;
                    border-radius:6px;
                    font-size:11px;
                    font-weight:700;
                    letter-spacing:0.5px;
                    margin-bottom:14px;
                    box-shadow:0 2px 8px rgba(16,185,129,0.3);">
          III
        </div>
        <div style="color:{MODERN['text_primary']};
                    font-size:24px;
                    font-weight:700;
                    letter-spacing:0.3px;
                    text-transform:uppercase;
                    margin-bottom:8px;">
          {html_escape(title_txt)}
        </div>
        <div style="width:64px;
                    height:3px;
                    margin:0 auto;
                    background:{MODERN['success']};
                    border-radius:2px;
                    box-shadow:0 0 12px rgba(16,185,129,0.3);"></div>
      </div>
    </td>
  </tr>
</table>
""".strip()

    intro_html = ""
    intro_md = (data.get("intro_md") or "").strip()
    if intro_md:
        intro_html = f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
  <tr>
    <td style="padding:16px;
               background:{MODERN['bg_surface']};
               border:1px solid {MODERN['border']};
               border-radius:12px;">
      {md_to_email_html(intro_md)}
    </td>
  </tr>
</table>
""".strip()

    def _best_wrapped(metric_name: str, disp_text: str, value_num: float, opponent_val: float) -> str:
        if value_num is None or opponent_val is None:
            return html_escape(disp_text)

        best_is_lower = lower_is_better(metric_name)
        is_better = (value_num < opponent_val) if best_is_lower else (value_num > opponent_val)
        if is_better:
            return f"<strong style='color:{MODERN['text_primary']};font-weight:700;'>{html_escape(disp_text)}</strong>"
        return f"<span style='color:{MODERN['text_secondary']};'>{html_escape(disp_text)}</span>"

    def _row(metric, h_val, a_val):
        disp_h, num_h = format_metric_value(metric, h_val)
        disp_a, num_a = format_metric_value(metric, a_val)
        sh = _best_wrapped(metric, disp_h, num_h, num_a)
        sa = _best_wrapped(metric, disp_a, num_a, num_h)
        return f"""
        <tr>
          <td style="padding:12px 14px;color:{MODERN['text_secondary']};font-size:13px;border-bottom:1px solid {MODERN['border_light']};">{html_escape(metric)}</td>
          <td style="padding:12px 14px;text-align:center;font-size:14px;border-bottom:1px solid {MODERN['border_light']};">{sh}</td>
          <td style="padding:12px 14px;text-align:center;font-size:14px;border-bottom:1px solid {MODERN['border_light']};">{sa}</td>
        </tr>
        """.strip()

    def _team_pills(home_label, away_label):
        return f"""
        <tr>
          <td style="padding:12px 14px;"></td>
          <td style="padding:12px 14px;text-align:center;">
            <span style="display:inline-block;
                         background:{MODERN['bg_elevated']};
                         border:1px solid {MODERN['border']};
                         border-radius:8px;
                         padding:6px 12px;
                         color:{MODERN['text_secondary']};
                         font-weight:600;
                         font-size:11px;
                         letter-spacing:0.3px;
                         text-transform:uppercase;">
              {html_escape(home_label)}
            </span>
          </td>
          <td style="padding:12px 14px;text-align:center;">
            <span style="display:inline-block;
                         background:{MODERN['primary']};
                         color:#ffffff;
                         border-radius:8px;
                         padding:6px 12px;
                         font-weight:600;
                         font-size:11px;
                         letter-spacing:0.3px;
                         text-transform:uppercase;
                         box-shadow:0 2px 8px {MODERN['glow_blue']};">
              {html_escape(away_label)}
            </span>
          </td>
        </tr>
        """.strip()

    def _table_block(t):
        title = t.get("title") or ""
        rows  = t.get("rows")  or []
        teams = t.get("teams") or {}
        home_label = teams.get("home") or "Équipe A"
        away_label = teams.get("away") or "Équipe B"

        body_rows = []
        for r in rows:
            if len(r) >= 3:
                body_rows.append(_row(r[0], r[1], r[2]))
        body_html = "\n".join(body_rows)

        return f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:18px;">
  <tr>
    <td style="background:{MODERN['bg_surface']};
               border:1px solid {MODERN['border']};
               border-radius:12px;
               box-shadow:0 4px 20px rgba(0,0,0,0.3);">
      <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
          <td colspan="3" style="padding:14px 16px;
                                  border-bottom:1px solid {MODERN['border']};
                                  background:{MODERN['bg_elevated']};
                                  border-radius:12px 12px 0 0;">
            <div style="color:{MODERN['text_primary']};
                        font-size:13px;
                        font-weight:600;
                        letter-spacing:0.3px;
                        text-transform:uppercase;">
              {html_escape(title)}
            </div>
          </td>
        </tr>
        {_team_pills(home_label, away_label)}
        {body_html}
      </table>
    </td>
  </tr>
</table>
""".strip()

    tables_html = "\n".join(_table_block(t) for t in (data.get("tables") or []))

    yc_html = ""
    yc_md = (data.get("yc_md") or "").strip()
    if yc_md:
        yc_body = md_to_email_html(yc_md)
        yc_html = f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
  <tr>
    <td style="background:{MODERN['bg_surface']};
               padding:18px;
               border-radius:12px;
               border-left:3px solid {MODERN['accent']};
               border:1px solid {MODERN['border']};
               box-shadow:0 4px 16px rgba(6,182,212,0.15);">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div style="font-size:16px;">💬</div>
        <div style="color:{MODERN['accent_light']};
                    font-size:12px;
                    font-weight:600;
                    letter-spacing:0.5px;
                    text-transform:uppercase;">
          Décryptage express
        </div>
      </div>
      {yc_body}
    </td>
  </tr>
</table>
""".strip()

    return "\n".join([title_html, intro_html, tables_html, yc_html])


def wrap_email(body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Analyse Data Ligue 1 — Newsletter Moderne</title>
</head>
<body style="margin:0;padding:0;background-color:{MODERN['bg_deep']};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background:{MODERN['bg_deep']};">
    <tr>
      <td align="center" style="padding:20px 12px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%"
               style="max-width:600px;
                      background:{MODERN['bg_deep']};
                      border-radius:20px;
                      box-shadow:0 20px 60px rgba(0,0,0,0.5);">
          <tr>
            <td style="padding:24px 20px;">
              {body_html}
            </td>
          </tr>
        </table>
        <div style="height:20px;line-height:0;font-size:0;">&nbsp;</div>
      </td>
    </tr>
  </table>
</body>
</html>"""


# ====== MAIN ======
def main():
    in_path = Path(IN_JSON)
    if not in_path.exists():
        print(f"❌ JSON introuvable : {in_path}")
        return

    try:
        data = json.loads(in_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Lecture JSON échouée : {e}")
        return
    print(f"📥 JSON chargé: {in_path}")

    meta     = (data.get("meta")     or {})
    facts    = (data.get("facts")    or {})
    sections = (data.get("sections") or [])

    home, score, away = parse_teams_score_from_meta(meta)
    league = _coerce_str(meta.get("competition")) or "Ligue 1"

    scorers = extract_scorers(facts, meta)
    cards   = extract_cards(data)
    _, yc_md_intro = find_intro_and_yc(sections)

    mi_title, mi_intro_md, mi_yc_md = find_match_images_section(sections)
    if not mi_title:
        mi_title = "LE MATCH EN IMAGES"
    match_images_block = render_match_images_modern(
        mi_title, mi_intro_md or "", mi_yc_md or ""
    )

    section_ii_block = render_section_ii_modern(sections=sections, meta=meta)
    section_iii_block = render_section_iii_modern(sections=sections, meta=meta)

    parts = [
        render_header(),
        render_scoreline(home or "Équipe A", score or "—", away or "Équipe B", league),
        render_timeline(scorers),
        render_key_stats_panel(meta, facts),
        render_cards_boxes_side_by_side(cards),
        render_yc_comment(yc_md_intro),
        match_images_block,
        section_ii_block,
        section_iii_block,
    ]

    html = wrap_email("\n".join(p for p in parts if p))
    out_path = in_path.with_name(in_path.stem + ".brevo_modern.html")
    try:
        out_path.write_text(html, encoding="utf-8")
    except Exception as e:
        print(f"❌ Écriture HTML échouée : {e}")
        return

    print(f"✅ HTML moderne généré : {out_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("❌ Erreur inattendue :")
        traceback.print_exc()
