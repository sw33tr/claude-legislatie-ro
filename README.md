# legislatie-ro: legislația românească pentru Claude

[Română](#română) · [English](#english)

---

## Română

Skill pentru Claude care caută acte normative pe [legislatie.just.ro](https://legislatie.just.ro)
și citește textul **în forma consolidată în vigoare**, nu în forma publicată inițial.

```
ACT:    id 215925 — https://legislatie.just.ro/Public/DetaliiDocument/215925
FORMA:  consolidată — Consolidarea din 12.09.2026

--- Articolul 485^1 (3,438 caractere) ---
Articolul 485^1 Evaluarea performanțelor profesionale individuale ale funcționarilor publici ...
```

### De ce

Portalul servește, pentru același act, două forme: cea publicată inițial și ultima consolidare.
Diferența nu se vede din text. Codul administrativ „arată complet” și în forma din 2019, doar că
îi lipsesc articolele adăugate ulterior. Skill-ul ia întotdeauna ultima consolidare și spune
din ce dată e.

### Ce face

- caută actul după referință (`OUG 57/2019`, `Legea nr. 53/2003`, `HG 1336/2022`) sau după text liber;
- descarcă textul în vigoare și indică data consolidării;
- extrage un articol (`56`, `485^1`, `XLIX`, `unic`) cu notele de modificare și deciziile ÎCCJ/CCR de sub el;
- urmează automat actele care sunt doar „ambalaj” (Legea 53/2003 → Codul muncii);
- semnalează actele posibil abrogate;
- oferă forme istorice (`--id <id consolidare> --exact`).

### Instalare

**claude.ai / aplicația Claude:** descarcă [`dist/legislatie-ro.zip`](dist/legislatie-ro.zip), apoi în
Claude mergi la **Customize → Skills → + → Create skill → Upload a skill**.

**Claude Code / Cowork (plugin):**

```
/plugin marketplace add sw33tr/claude-legislatie-ro
/plugin install legislatie-ro@legislatie-ro
```

### Rețea

Portalul blochează unele rețele, mai ales IP-urile de datacenter. Tipic, din sandbox-ul cloud al
Claude căutarea merge, dar textul nu. Skill-ul detectează asta și trece singur la altă rută:
calculatorul utilizatorului (Cowork), browserul (Claude in Chrome) sau, ca ultim resort, textul
din API, marcat explicit ca formă publicată inițial. De pe o conexiune obișnuită din România
totul merge direct.

### Folosire fără Claude

Scripturile folosesc doar biblioteca standard Python 3.6+:

```bash
python3 skills/legislatie-ro/scripts/legislatie_search.py "OUG 57/2019" --articol 485^1
python3 skills/legislatie-ro/scripts/legislatie_search.py "Lege 53/2003" --grep "concediu de odihn"
python3 skills/legislatie-ro/scripts/legislatie_search.py --diagnostic
```

Pe Windows folosește `py -3` în loc de `python3`.

### Limitări

- Consolidările apar pe portal cu întârziere față de Monitorul Oficial. Pentru modificări foarte
  recente, verifică actele modificatoare.
- Nu este consultanță juridică. Textul oficial rămâne cel din Monitorul Oficial.
- Proiect independent, fără legătură cu Ministerul Justiției sau cu administratorii portalului.

---

## English

A Claude skill that looks up Romanian legislation on the official portal
[legislatie.just.ro](https://legislatie.just.ro) and reads the text **in its current consolidated
(in-force) form**, not the originally published version. Each result states the consolidation date.

**Why:** the portal serves both the originally published text and the latest consolidation
for the same act. They look alike, but the published form silently lacks every later amendment.

**Features:** search by reference or free text; in-force text with its consolidation date;
article extraction (`56`, `485^1`, `XLIX`) including the amendment notes and High Court /
Constitutional Court decisions attached to it; wrapper-act resolution (Law 53/2003 → Labour Code);
repeal warnings; historical versions.

**Install:**

- **claude.ai / Claude apps:** download [`dist/legislatie-ro.zip`](dist/legislatie-ro.zip), then go to
  **Customize → Skills → + → Create skill → Upload a skill**.
- **Claude Code / Cowork:** run `/plugin marketplace add sw33tr/claude-legislatie-ro`, then
  `/plugin install legislatie-ro@legislatie-ro`.

**Network:** the portal blocks some networks, notably datacenter IPs, so Claude's cloud sandbox
can usually search but not fetch text. The skill detects this and falls back, in order, to the
user's computer (Cowork), the browser (Claude in Chrome), and finally the API text, clearly
labelled as the published form.

**Standalone:** Python 3.6+, standard library only. See the commands above.

**Disclaimer:** not legal advice. This is an independent project, not affiliated with the
Romanian Ministry of Justice. Official legislative texts are not protected by copyright in Romania
(Law 8/1996, art. 9 lit. b).

## License

[Apache-2.0](LICENSE) © Mihai Dobre
