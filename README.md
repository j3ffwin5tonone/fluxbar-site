# Produkt- und Supportseite von Andreas Distel

Statische Website unter **https://fluxbar.app/**, veröffentlicht über das
bestehende GitHub-Pages-Setup aus `main` (Repository-Wurzel). Die Domain bleibt
erhalten. Die frühere FluxBar-Produktdarstellung wurde vollständig ersetzt;
ältere Impressums- und Datenschutz-URLs leiten auf die aktuellen Seiten weiter.

## Seiten und App-Store-Adressen

- Startseite: https://fluxbar.app/
- Schafkopf-Produktseite / Marketing URL: https://fluxbar.app/schafkopf/
- Support URL: https://fluxbar.app/schafkopf/support/
- Privacy Policy URL für Schafkopf: https://fluxbar.app/schafkopf/datenschutz/
- Datenschutz der Website: https://fluxbar.app/datenschutz/
- Impressum: https://fluxbar.app/impressum/
- Kontaktformular: https://fluxbar.app/kontakt/

Die zweite Produktseite für **CRT Chess** (früher ZUGZWANG) wird später unter
`/crt-chess/` ergänzt. Aktuell werden weder eine unfertige Produktseite noch
Download-Links für CRT Chess beworben. Gemeinsame Navigation, Kontakt und
Website-Datenschutz können dann weiterverwendet werden. App-Datenschutz bekommt
eine eigene Adresse und muss am tatsächlichen CRT-Chess-Build geprüft werden.

## Kontaktformular aktivieren

Das Formular ist für **Form.taxi** vorbereitet. Die Verarbeitung erfolgt nach
Anbieterangaben innerhalb der EU; ein AV-Vertrag ist im Kundenkonto verfügbar.
Die Nutzungs- und Datenschutzverträge muss der Betreiber selbst abschließen.

1. Bei https://form.taxi/de/ ein eigenes Konto im Free-Tarif anlegen. Der Tarif
   bietet laut Preisübersicht vom 25.10.2026 40 Sendungen pro Monat.
2. Formular „Support Andreas Distel“ für `https://fluxbar.app/kontakt/` erstellen.
3. Empfänger `support@fluxbar.app` einrichten und die E-Mail-Adresse bestätigen,
   falls der Dienst eine Bestätigung anfordert. Benachrichtigungen aktivieren.
4. Den AV-Vertrag im Bereich Datenschutz erstellen und aufbewahren.
5. Sprache Deutsch, Honeypot-Feld `_gotcha`, keine externen Automatisierungen
   oder zusätzlichen Captcha-Skripte aktivieren. Beim Spamfilter auch den
   Spam-Ordner regelmäßig prüfen. Domainfreigabe: `fluxbar.app`.
6. Erfolgsseite: `https://fluxbar.app/kontakt/danke/`. Diese wird zusätzlich
   über das dokumentierte Feld `_next` mitgeschickt.
7. Die öffentliche Sendeadresse `https://form.taxi/s/…` in `site.json` bei
   `form.endpoint` eintragen. Nach Abschluss des AV-Vertrags
   `form.avv_confirmed` auf `true` setzen. Ein API-Schlüssel wird nicht benötigt.
8. Produktions-Build und Prüfung ausführen. Eine eigene Testnachricht absenden
   und Empfang im Postfach sowie im Formularpanel prüfen. Das reale Postfach
   wurde durch die lokale Webseitenprüfung nicht getestet.

Solange die Sendeadresse fehlt, ist das Formular als Vorschau deaktiviert.
`--production` verweigert in diesem Zustand die Freigabe. Ein nur per `mailto:`
vorbefüllter Entwurf wird nicht als zweiter Kontaktweg ausgegeben.
Anfragen über das Formular müssen tatsächlich zeitnah bearbeitet werden; die
technische Einrichtung allein ersetzt diese organisatorische Pflicht nicht.
Den Eingang und das aktuelle Sendungslimit im Betreiberkonto im Blick behalten.

## Bauen, prüfen und lokal ansehen

Python 3 aus der Standardbibliothek genügt. Kein npm, Framework oder externer
Build-Dienst ist erforderlich.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8768 --bind 127.0.0.1
```

Vor einer Veröffentlichung:

```sh
python3 scripts/build.py --production
python3 scripts/check.py --production
git diff --check
```

Die generierten HTML-Dateien werden eingecheckt und direkt von GitHub Pages
ausgeliefert. `.nojekyll` deaktiviert eine unnötige Jekyll-Verarbeitung. `CNAME`
und HTTPS-Konfiguration bleiben erhalten. Für eine Rückkehr zu einer früheren
Fassung die Git-Historie verwenden; die Historie wurde nicht umgeschrieben.

`site.json` enthält die öffentlichen Anbieterangaben, die verifizierten
Download-URLs und die öffentliche Formularadresse. Dort gehören **keine**
Passwörter, SMTP-Zugangsdaten oder API-Schlüssel hinein. Beim späteren App-Store-
Release die echte Store-URL unter `schafkopf.app_store_url` ergänzen und neu bauen.

## Datenschutz und rechtliche Umsetzung

Der eigene Seitencode nutzt keine Besucheranalyse oder Werbedienste, keine
eingebetteten Drittanbieter-Widgets, keine eigenen Cookies und keinen
Browser-Speicher. Cloudflares bestehende Sicherheitsverarbeitung und mögliche
technisch erforderliche Cookies werden gesondert erläutert. Schriften und
Bilder werden lokal ausgeliefert. Das Kontaktformular lädt keine Fremdskripte;
erst beim Absenden wird an den konfigurierten Dienst übertragen. Die
Content-Security-Policy erlaubt auf der Formularseite nur den vorgesehenen
Formularanbieter und die eigene Erfolgsseite als Formularziele.

Website-Hosting über GitHub Pages mit vorgeschaltetem Cloudflare, Kontaktbearbeitung, der Formulardienst und die
App-Verarbeitung sind in den Datenschutzhinweisen getrennt beschrieben. GitHub
protokolliert nach eigener Angabe Besucher-IP-Adressen; es wird daher keine
pauschale Behauptung aufgestellt, die Website verarbeite keinerlei Daten.

Name, Anschrift und E-Mail stammen aus den bisherigen öffentlichen Angaben und
wurden für diesen Neuaufbau beibehalten. Die USt-IdNr. wurde vom Betreiber für
die Veröffentlichung mitgeteilt; eine amtliche Gültigkeitsprüfung wurde nicht
durchgeführt. Es wurden keine Registereinträge oder Berufs-/Kammerangaben erfunden.
Geänderte Anbieter- oder Verarbeitungstatsachen müssen entsprechend nachgepflegt
werden. Die Texte bilden die bekannten Funktionen ab; sie sind keine Bestätigung
einer abgeschlossenen anwaltlichen Prüfung oder einer Apple-Freigabe.

Geprüfte Grundlagen (25.10.2026):

- [§ 5 DDG](https://www.gesetze-im-internet.de/ddg/__5.html)
- [EuGH C-298/07: weiterer schneller Kontaktweg](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A62007CJ0298)
- [DSGVO, insbesondere Art. 6 und 13](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32016R0679)
- [§ 25 TDDDG](https://www.gesetze-im-internet.de/ttdsg/__25.html)
- [Apple: Privacy Policy URL](https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy/)
- [Apple: Support URL](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information)
- [GitHub Pages: technische Zugriffsdaten](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection)
- [Form.taxi: Einrichtung](https://docs.form.taxi/de/form-setup), [Datenschutz](https://docs.form.taxi/de/privacy)

## Bilder und Schrift

Die Produktaufnahmen stammen aus der echten Schafkopf-App. WebP und JPG sind als
responsive Varianten eingebunden. Die Schrift Figtree ist lokal gehostet; ihr
SIL-OFL-Lizenztext liegt unter `assets/fonts/FIGTREE-LICENSE.txt`. Eigene Bilder
und Texte bleiben urheberrechtlich geschützt. Lizenztexte der App sind über die
verlinkte Downloadseite und innerhalb der App erreichbar.

Der Live-Abruf bestätigt einen vorgeschalteten Cloudflare-Proxy. E-Mail-Adressen
werden mit den dokumentierten `email_off`-Markierungen vor der automatischen
Verschleierung geschützt, damit die Kontaktangaben ohne JavaScript lesbar und
anklickbar bleiben. Sonstige Cloudflare-Einstellungen wurden nicht verändert.
