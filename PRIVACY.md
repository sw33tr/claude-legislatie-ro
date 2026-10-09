# Confidențialitate / Privacy — legislatie-ro

[Română](#română) · [English](#english)

## Română

- **Ce trimite skill-ul**: doar textul căutării tale (de exemplu `OUG 57/2019` sau cuvintele dintr-o căutare
  liberă) către portalul oficial `legislatie.just.ro` — API-ul public SOAP (`/apiws/FreeWebService.svc/SOAP`)
  pentru căutare și paginile `Public/DetaliiDocument/<id>` pentru text. Niciun alt server nu este contactat.
  Identificatorii `http://tempuri.org/` și `schemas.xmlsoap.org` din cod sunt namespace-uri XML cerute de
  protocolul SOAP, nu destinații ale vreunei cereri.
- **Ce nu face**: nu colectează, nu stochează și nu transmite date personale; nu are telemetrie, conturi, chei API
  sau servicii proprii. Autorul nu primește nimic din ce cauți.
- **Ce rămâne pe calculatorul tău**: textul actelor descărcate, într-un cache local
  (`legislatie_cache` din directorul temporar al sistemului sau `$LEGISLATIE_CACHE`), reutilizat 6 ore. În Cowork,
  dacă portalul nu răspunde din cloud, scripturile sunt copiate într-un folder ascuns `.legislatie-ro` dintr-un
  folder conectat, iar skill-ul îți spune că l-a creat. Poți șterge oricând ambele.
- **Portalul**: cererile ajung la Ministerul Justiției, administratorul `legislatie.just.ro`, conform politicii lor
  (vezi secțiunea „Protecția datelor cu caracter personal” de pe portal). Textele oficiale nu sunt protejate de
  drept de autor în România (Legea 8/1996, art. 9 lit. b).
- **Întrebări**: https://github.com/sw33tr/claude-legislatie-ro/issues

## English

- **What the skill sends**: only your query (for example `OUG 57/2019`, or the words of a free-text search) to the
  official portal `legislatie.just.ro` — its public SOAP API (`/apiws/FreeWebService.svc/SOAP`) for search and the
  `Public/DetaliiDocument/<id>` pages for text. No other server is contacted. `http://tempuri.org/` and
  `schemas.xmlsoap.org` in the code are XML namespaces required by SOAP, not request destinations.
- **What it does not do**: it collects, stores and transmits no personal data; it has no telemetry, accounts, API
  keys or services of its own. The author receives nothing about your searches.
- **What stays on your machine**: the downloaded act texts, in a local cache (`legislatie_cache` under the system
  temp directory, or `$LEGISLATIE_CACHE`), reused for 6 hours. In Cowork, when the portal is unreachable from the
  cloud, the scripts are copied into a hidden `.legislatie-ro` folder inside a connected folder and the skill tells
  you it did so. You can delete both at any time.
- **The portal**: requests reach the Romanian Ministry of Justice, which runs `legislatie.just.ro`, under its own
  policy (see the portal's personal-data section). Official legislative texts are not copyrighted in Romania
  (Law 8/1996, art. 9 b).
- **Questions**: https://github.com/sw33tr/claude-legislatie-ro/issues
