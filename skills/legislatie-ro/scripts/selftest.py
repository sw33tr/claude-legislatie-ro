#!/usr/bin/env python3
"""selftest — verifică euristicile pe care se sprijină skill-ul, offline (parsere) și live (portal).

Fiecare verificare numește ce s-a rupt, ca să știi unde să te uiți când portalul își schimbă marcajul.

  python3 selftest.py            # tot
  python3 selftest.py --offline  # doar parserele, fără rețea

Coduri de ieșire: 0 totul trece | 1 cel puțin un eșec | 3 portalul e inaccesibil de aici (neconcludent)
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lj_core  # noqa: E402
import legislatie_search as ls  # noqa: E402

RESULTS = []


def check(name, cond, hint=""):
    RESULTS.append((name, bool(cond), hint))
    print("  %s  %s%s" % ("ok " if cond else "EȘEC", name, ("  -> " + hint) if (hint and not cond) else ""))
    return bool(cond)


# ── Offline: parsere și regex-uri ───────────────────────────────────────────

def offline():
    print("OFFLINE")
    p = ls.parse_act_reference
    check("referință simplă", (p("OUG 57/2019") or {}).get("SearchNumar") == "57", "parse_act_reference")
    check("formă articulată", (p("Hotărârea 1336/2022") or {}).get("SearchTitlu") == "HOTARARE", "ACT_TYPE_MAP / _tip_key")
    check("alias de cod", (p("Codul muncii art. 39") or {}).get("SearchNumar") == "53", "CODE_ALIASES / resolve_code_alias")
    check("articol din referință", (p("art. 485^1 din OUG 57/2019") or {}).get("_articol") == "485^1", "_ART_IN_TEXT / _article_in")
    check("articol cu punct de mii", (p("Codul civil art. 1.357") or {}).get("_articol") == "1.357", "_ART_IN_TEXT")
    check("emitent din referință", (p("Decizia CCR 60/2020") or {}).get("_emitent") == "Curtea Constituțională", "ISSUER_ALIASES")
    check("emitent cu cratimă", (p("Decizia Prim-ministrului 60/2020") or {}).get("_emitent") == "Prim-Ministrul", "_tip_key (cratimă)")
    check("emitent tolerant la ș/ț pierdute",
          ls._matches_emitent({"Emitent": "Curtea Constitu?ională"}, "Curtea Constituțională"), "_matches_emitent")
    check("an din titlu", ls._act_year({"Titlu": "DECIZIA nr. 60 din 25 februarie 2025 referitoare"}) == "2025", "_act_year")
    n = lj_core._norm_ref
    check("normalizare referință articol", (n("Art. 5"), n("485¹"), n("1.357")) == ("5", "485^1", "1357"), "_norm_ref")
    check("tipar numeric cu mii", lj_core._num_pattern("1357") == r"1\.?357", "_num_pattern")
    text = ("Forma printabilă\nLEGE nr. 1\nArticolul 1\nArticolul 2\nArticolul 1 Primul text.\n(la 01-01-2020,\n"
            "Articolul 1 din Capitolul I a fost modificat de Legea 2)\nArticolul 2 Abrogat.\nArticolul 1.357 Mii.\n"
            "Articolul 485^1 Sup.\nArticolul 486 Final.\n")
    e = lj_core.extract_articol
    check("extragere articol (corpul, nu cuprinsul)", (e(text, "1") or "").startswith("Articolul 1 Primul"), "extract_articol")
    check("extragere 1.357 / 485^1", (e(text, "1357") or "").startswith("Articolul 1.357") and
          (e(text, "485^1") or "").startswith("Articolul 485^1"), "extract_articol / _num_pattern")
    check("extragere ARTICOL UNIC", (e("Forma printabilă\nARTICOL UNIC Se promulgă.\nx\n", "unic") or "").startswith("ARTICOL UNIC"),
          "extract_articol (lead ARTICOL)")
    check("_has_body pe decret scurt", lj_core._has_body("Forma printabilă\nDECRET nr. 1\nARTICOL UNIC Se promulgă legea.\n" + "x" * 200),
          "_has_body / _ART_HEAD")
    check("_has_body fals pe ambalaj", not lj_core._has_body("Forma printabilă\nLEGE nr. 53 (republicată) Codul muncii\nEMITENT\n"),
          "_has_body")
    rep = "Forma printabilă\n" + "".join("Articolul %d Abrogat.\n" % i for i in range(1, 12)) + "Articolul 12 Text.\n"
    check("avertisment abrogare (raport)", "Posibil abrogat integral" in (lj_core.repeal_warning(rep) or ""), "repeal_warning")
    fisa = [{"sectiune": "Actul", "op": "ABROGAT DE", "act": "LEGE 1", "data": "2020-01-01", "id": "1"}]
    check("abrogare din fișă", "ABROGAT de LEGE 1" in (lj_core.fisa_repeal(fisa) or ""), "fisa_repeal")
    check("format fișă cu filtru de dată", "0 de la 01.01.2021" in lj_core.format_fisa(fisa, "2021-01-01"), "format_fisa / _iso_date")
    hist = lj_core.parse_istoric("<div id='istoric_fa'><a title='x'>12.09.2026</a><a href='DetaliiDocument/5'>01.01.2020</a></div>")
    check("parse_istoric", [h["id"] for h in hist] == [None, "5"], "parse_istoric")
    check("parse_forme", lj_core.parse_forme("incarcaFormaDeBaza(41627); href='DetaliiDocument/128647?isFormaDeBaza=True'") == ["41627", "128647"],
          "parse_forme")


# ── Live: portalul ───────────────────────────────────────────────────────────

def live():
    print("LIVE (legislatie.just.ro)")
    try:
        tok = ls.get_token()
    except Exception as e:  # noqa: BLE001
        print("  API SOAP inaccesibil: %s" % e)
        return 3
    res = ls.search_paged(tok, search_titlu="ORDONANTA DE URGENTA", search_numar="57", search_an="2019", emitent="guvern")
    res = [r for r in res if ls._matches_year(r, "2019")]
    check("căutare OUG 57/2019 -> 215925", any(lj_core.doc_id_of(r["LinkHtml"]) == "215925" for r in res), "API SOAP / search_paged")
    dec = ls.search_paged(tok, search_titlu="DECIZIE", search_numar="60", search_an="2020", exhaustive=True)
    dec = [r for r in dec if ls._matches_year(r, "2020")]
    check("Decizia 60/2020 are ≥2 emitenți", len({ls._norm(r.get("Emitent", "")) for r in dec}) >= 2, "search_paged exhaustive")
    try:
        ca = lj_core.get_in_force("215925", no_cache=True)
    except lj_core.RouteBlocked as e:
        print("  HTTPS către portal blocat de aici (%s): verificările de text sunt neconcludente." % e)
        return 3
    raw = lj_core.fetch_html("/Public/DetaliiDocument/215925")
    check("marcaj istoric_fa prezent", "istoric_fa" in raw, "parse_istoric (blocul de consolidări a dispărut)")
    check("marcaj Forme act prezent", "incarcaFormaDeBaza(" in raw, "parse_forme")
    check("marcaj «Forma printabilă» prezent", "Forma printabilă" in ca["text"], "_body_text / _has_body / repeal_warning")
    check("Codul administrativ: consolidare cu dată", (ca.get("forma") or "").startswith("consolidată — Consolidarea din"), "parse_istoric / get_in_force")
    check("Codul administrativ: ≥50 consolidări în istoric", len(lj_core.parse_istoric(raw)) >= 50, "parse_istoric")
    art = lj_core.extract_articol(ca["text"], "485^1") or ""
    check("art. 485^1 extras", art.startswith("Articolul 485^1") and "Evaluarea" in art[:200], "extract_articol / html_to_text")
    check("fișa Codului administrativ ≥200 acțiuni", len(ca.get("fisa") or []) >= 200, "fisa_act (POST actiuniSuferite)")
    cm = lj_core.get_in_force("41625", no_cache=True)
    check("Legea 53/2003 urmată la Codul muncii", bool(cm.get("id_consolidare")), "_load (ambalaj -> div_Formaconsolidata)")
    check("Codul muncii art. 39", "Salariatul" in (lj_core.extract_articol(cm["text"], "39") or "")[:120], "extract_articol")
    check("fișa Codului muncii include republicarea", len(cm.get("fisa") or []) >= 300, "parse_forme + fisa_act")
    de = lj_core.get_in_force("306260", no_cache=True)
    check("Decretul 1/2026 nu sare la lege", de.get("id_consolidare") in (None, "", "306260") and
          (lj_core.extract_articol(de["text"], "unic") or "").startswith("ARTICOL UNIC"), "_has_body / extract_articol (ARTICOL UNIC)")
    l188 = lj_core.get_in_force("20173", no_cache=True)
    check("Legea 188/1999: abrogat în mare parte", "Abrogat în mare parte" in (l188.get("avertisment") or ""), "repeal_warning")
    cf = lj_core.get_in_force("48697", no_cache=True)
    check("Legea 571/2003: abrogat din fișă", "ABROGAT de" in (cf.get("avertisment") or ""), "fisa_repeal")
    cc = lj_core.get_in_force("109883", no_cache=True)
    check("Codul civil art. 1357 (punct de mii)", (lj_core.extract_articol(cc["text"], "1357") or "").startswith("Articolul 1.357"),
          "_num_pattern / extract_articol")
    return 0


def main(argv=None):
    lj_core.utf8_console()
    ap = argparse.ArgumentParser(description="Autotest legislatie-ro")
    ap.add_argument("--offline", action="store_true", help="doar verificările fără rețea")
    a = ap.parse_args(argv)
    t0 = time.time()
    offline()
    rc = 0 if a.offline else live()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("\n%d verificări, %d eșecuri, %.0f s%s" % (len(RESULTS), len(failed), time.time() - t0,
                                                   "" if rc != 3 else " — LIVE NECONCLUDENT (portal inaccesibil de aici)"))
    for n in failed:
        print("  EȘEC: " + n)
    return 1 if failed else rc


if __name__ == "__main__":
    sys.exit(main())
