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
- când același număr și an vin de la emitenți diferiți (Decizia 60/2020: Prim-Ministrul și CCR; Ordinul 1/2026:
  șase instituții), listează emitenții și cere `--emitent` în loc să aleagă singur;
- semnalează abrogarea când se vede în textul consolidat (notă în antet sau toate articolele marcate „Abrogat.”);
  un act abrogat după ultima lui consolidare nu poate fi detectat așa;
- oferă forme istorice (`--id <id consolidare> --exact`).

### Instalare

**claude.ai / aplicația Claude:** descarcă [`legislatie-ro.zip`](https://github.com/sw33tr/claude-legislatie-ro/releases/latest/download/legislatie-ro.zip) din ultima versiune publicată, apoi în
Claude mergi la **Customize → Skills → + → Create skill → Upload a skill**.

**Claude Code / Cowork (plugin):**

```
/plugin marketplace add sw33tr/claude-legislatie-ro
/plugin install legislatie-ro@legislatie-ro
```

### Ce rulează și ce trimite

- Singurul server contactat este portalul oficial `legislatie.just.ro`: API-ul public SOAP
  (`/apiws/FreeWebService.svc/SOAP`, prin http, cu revenire la https) pentru căutare și paginile
  `Public/DetaliiDocument/<id>` (https) pentru text. Se trimite doar ce cauți (ex. `OUG 57/2019`).
- Fără telemetrie, conturi sau chei API. Nu citește și nu trimite date personale.
- `http://tempuri.org/` și `schemas.xmlsoap.org` apar în cod doar ca namespace-uri XML cerute de protocolul SOAP;
  nicio cerere nu pleacă spre ele.
- Textul descărcat se păstrează local, în `legislatie_cache` din directorul temporar al sistemului
  (sau în `$LEGISLATIE_CACHE`).
- În Cowork, dacă portalul nu răspunde din cloud, skill-ul își copiază cele două scripturi într-un
  folder ascuns `.legislatie-ro` dintr-un folder conectat de pe calculatorul tău, le rulează acolo
  și îți spune că a creat folderul. Îl poți șterge oricând.
- Ruta de browser rulează un fragment JavaScript (în `references/browser.md`) doar pe pagina
  actului de pe portal, ca să extragă textul.

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
Constitutional Court decisions attached to it; wrapper-act resolution (Law 53/2003 → Labour Code); when the same number and year come from several
issuers (decisions, ministerial orders) it lists them and asks for `--emitent` instead of guessing;
repeal warnings when the consolidated text shows them (an act repealed after its last consolidation
cannot be detected this way); historical versions.

**Install:**

- **claude.ai / Claude apps:** download [`legislatie-ro.zip`](https://github.com/sw33tr/claude-legislatie-ro/releases/latest/download/legislatie-ro.zip) from the latest release, then go to
  **Customize → Skills → + → Create skill → Upload a skill**.
- **Claude Code / Cowork:** run `/plugin marketplace add sw33tr/claude-legislatie-ro`, then
  `/plugin install legislatie-ro@legislatie-ro`.

**Network:** the portal blocks some networks, notably datacenter IPs, so Claude's cloud sandbox
can usually search but not fetch text. The skill detects this and falls back, in order, to the
user's computer (Cowork), the browser (Claude in Chrome), and finally the API text, clearly
labelled as the published form.

**What it runs and sends:** the only server contacted is the official portal
`legislatie.just.ro`: its public SOAP API (`/apiws/FreeWebService.svc/SOAP`, over http with an
https fallback) for search, and `Public/DetaliiDocument/<id>` pages (https) for text. Only your
query (e.g. `OUG 57/2019`) is sent. No telemetry, accounts or API keys; no personal data is read or
sent. `http://tempuri.org/` and `schemas.xmlsoap.org` appear in the code only as XML namespaces required by
SOAP; no request is ever sent to them. Downloaded text is cached locally in `legislatie_cache` under the system temp directory (or
`$LEGISLATIE_CACHE`). In Cowork, when the portal is unreachable from the cloud, the skill copies its
two scripts into a hidden `.legislatie-ro` folder inside one of your connected folders, runs them
there and tells you it did; you can delete the folder at any time. The browser route runs one
JavaScript snippet (in `references/browser.md`) on the act's page on the portal to extract the text.

**Standalone:** Python 3.6+, standard library only. See the commands above.

**Disclaimer:** not legal advice. This is an independent project, not affiliated with the
Romanian Ministry of Justice. Official legislative texts are not protected by copyright in Romania
(Law 8/1996, art. 9 lit. b).

## License

[Apache-2.0](LICENSE) © Mihai Dobre
