#!/usr/bin/env python3
"""Generate the dependency-free GitHub Pages website from verified product facts."""
from pathlib import Path
from html import escape
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / 'site.json').read_text())
BASE = CONFIG['url'].rstrip('/')
OWNER = CONFIG['provider']
APP = CONFIG['schafkopf']
FORM = CONFIG['form']
DATE = '25. Oktober 2026'
MAIL = escape(OWNER['email'])
NAME = escape(OWNER['name'])
ADDRESS = f"{NAME}<br>{escape(OWNER['street'])}<br>{escape(OWNER['postcode'])} {escape(OWNER['city'])}<br>{escape(OWNER['country'])}"
PAGES = []


def picture(name, alt, eager=False, sizes='(max-width: 760px) 94vw, 600px'):
    source = ', '.join(f'/assets/images/{name}-{w}.webp {w}w' for w in (640, 1280, 1920))
    fallback = ', '.join(f'/assets/images/{name}-{w}.jpg {w}w' for w in (640, 1280, 1920))
    loading = 'eager' if eager else 'lazy'
    priority = ' fetchpriority="high"' if eager else ''
    return f'''<picture><source type="image/webp" srcset="{source}" sizes="{sizes}">
      <img src="/assets/images/{name}-1280.jpg" srcset="{fallback}" sizes="{sizes}"
      width="1280" height="800" loading="{loading}" decoding="async"{priority} alt="{escape(alt)}"></picture>'''


def screenshot(name, alt, eager=False):
    return f'<a href="/assets/images/{name}-1920.jpg" aria-label="{escape(alt)} – große Aufnahme öffnen">{picture(name, alt, eager)}</a>'


def button(label, href, secondary=False):
    kind = ' secondary' if secondary else ''
    return f'<a class="button{kind}" href="{escape(href, quote=True)}">{label}<span aria-hidden="true">↗</span></a>'


def header(active):
    current = lambda key: ' aria-current="page"' if active == key else ''
    return f'''<a class="skip" href="#inhalt">Zum Inhalt</a>
    <header class="site-header"><div class="wrap header-row">
      <a class="brand" href="/" aria-label="Andreas Distel – Startseite"><span class="brand-mark" aria-hidden="true">ad</span>Andreas Distel</a>
      <nav aria-label="Hauptnavigation"><a href="/schafkopf/"{current('schafkopf')}>Schafkopf</a><a href="/schafkopf/support/"{current('support')}>Support</a><a class="nav-download" href="/schafkopf/#download">Herunterladen <span aria-hidden="true">↗</span></a></nav>
    </div></header>'''


def footer():
    return f'''<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><a class="brand" href="/">Andreas Distel</a><p>Spiele für deinen Computer.</p></div>
      <div class="footer-links" aria-label="Kontakt und Rechtliches"><a href="/schafkopf/support/">Support &amp; Kontakt</a><a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz Webseite</a><a href="/schafkopf/datenschutz/">Datenschutz Schafkopf</a></div></div>
      <p class="copyright">© 2026 {NAME}. Alle Rechte vorbehalten.</p></div></footer>'''


def page(route, title, description, content, active='', noindex=False, form_action=False):
    canonical = BASE + route
    robots = '<meta name="robots" content="noindex">' if noindex else ''
    form_policy = "'self' https://form.taxi" if form_action else "'none'"
    html = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer"><meta name="color-scheme" content="light">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'self'; font-src 'self'; script-src 'none'; object-src 'none'; base-uri 'none'; form-action {form_policy}">
<title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}">{robots}
<link rel="canonical" href="{canonical}"><link rel="icon" type="image/png" sizes="128x128" href="/assets/images/icon-128.png">
<link rel="stylesheet" href="/assets/site.css"><link rel="preload" href="/assets/fonts/figtree-400.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:locale" content="de_DE"><meta property="og:type" content="website"><meta property="og:site_name" content="Andreas Distel · Spiele">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/images/og-schafkopf-1200x630.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Schafkopf Classic – echte Spielansicht am dunklen Stammtisch.">
<meta name="twitter:card" content="summary_large_image"></head><body>{header(active)}<main id="inhalt">{content}</main>{footer()}</body></html>'''
    filename = ROOT / ('index.html' if route == '/' else route.strip('/') + '/index.html')
    if route == '/404.html':
        filename = ROOT / '404.html'
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.write_text(html + '\n')
    if not noindex:
        PAGES.append(canonical)


def heading(title, lede='', breadcrumb=''):
    crumbs = f'<p class="breadcrumbs"><a href="/">Start</a><span aria-hidden="true">/</span>{breadcrumb or title}</p>'
    return f'<div class="page-heading"><div class="wrap">{crumbs}<h1>{title}</h1>{f"<p class=lede>{lede}</p>" if lede else ""}</div></div>'


def contact():
    return f'<address>{ADDRESS}</address><p>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a><br>Kontaktformular: <a href="/kontakt/">Nachricht schreiben</a></p>'


def home():
    content = f'''<section class="hero"><div class="wrap hero-grid"><div class="hero-copy">
      <p class="eyebrow"><img class="app-mini" src="/assets/images/icon-128.png" alt="" width="38" height="38">Schafkopf Classic</p>
      <h1>Dein Stammtisch.<br><em>Jederzeit.</em></h1>
      <p class="lede">Ein Platz ist noch frei. Spiel bayerischen Schafkopf gegen drei Computerspieler – ganz in deinem Tempo.</p>
      <div class="actions">{button('Schafkopf entdecken', '/schafkopf/')}<a class="text-link" href="/schafkopf/#download">Direkt zum Download</a></div>
      <p class="note">Für Windows und macOS. Kostenlos spielen, ohne Konto und ohne Werbung.</p>
    </div><figure class="screen-stage">{screenshot('stammtisch', 'Schafkopf Classic am dunklen Stammtisch mit klassischem Kartensatz.', True)}<figcaption>Drei Computerspieler, ein bayerischer Klassiker.</figcaption></figure></div></section>
    <div class="wrap reassurance"><span>Offline spielen</span><span>Drei KI-Stufen</span><span>Lernmodus inklusive</span><span>Spielstand bleibt auf deinem Gerät</span></div>
    <section class="section"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Vertrautes Spiel. Eigener Stil.</p><h2>Eine gute Runde<br>geht immer.</h2></div><p>Ob erste Partie oder fester Stammtisch: Stell dein Gegenüber, die Bedenkzeit und deinen Spieltisch so ein, wie es dir gefällt.</p></div>
    <div class="feature-list"><article><h3>Entspannt anfangen.</h3><p>Einführung, Lernmodus und Zugvorschläge helfen dir, Karten, Trumpf und Stiche besser zu verstehen.</p></article><article><h3>In Ruhe besser werden.</h3><p>Wähle zwischen drei KI-Stufen. Deine Statistik und dein Spielstand bleiben auf deinem Computer.</p></article><article><h3>Den eigenen Tisch finden.</h3><p>Dunkler Stammtisch oder heller Biergarten. Klassische Karten oder Dirndl-Kartensatz. Du entscheidest.</p></article></div></div></section>
    <section class="section section-dark"><div class="wrap split"><figure>{screenshot('biergarten','Schafkopf Classic am hellen Biergartentisch mit Dirndl-Kartensatz.')}</figure><div><p class="eyebrow">Schafkopf Classic</p><h2>Bayerisch.<br>Bis ins Blatt.</h2><p class="lede">Sauspiel, Wenz oder Solo: die lange Karte mit 32 Karten, drei Computerspieler und die nächste Runde direkt vor dir.</p><a class="text-link" href="/schafkopf/">Mehr über das Spiel <span aria-hidden="true">→</span></a></div></div></section>
    <section class="section"><div class="wrap support-strip"><div><p class="eyebrow">Direkt zum Entwickler</p><h2>Eine Frage zum Spiel?</h2><p>Hier findest du Hilfe, Antworten auf häufige Fragen und die Kontaktadresse für Schafkopf Classic.</p></div>{button('Zum Support','/schafkopf/support/')}</div></section>'''
    page('/', 'Schafkopf Classic · Spiele von Andreas Distel', 'Bayerischer Schafkopf gegen drei Computerspieler. Offline, mit Lernmodus, drei KI-Stufen und zwei Tischgestaltungen. Für Windows und macOS.', content)


def product():
    store_url = APP.get('app_store_url')
    store = button('Im Mac App Store ansehen', store_url) if store_url else '<p><strong>Mac App Store</strong><br><span class="note">Die Veröffentlichung im Mac App Store wird vorbereitet.</span></p>'
    content = f'''<section class="product-intro"><div class="wrap product-hero"><div><p class="breadcrumbs"><a href="/">Start</a><span aria-hidden="true">/</span>Schafkopf Classic</p><p class="eyebrow"><img class="app-mini" src="/assets/images/icon-128.png" alt="" width="38" height="38">Schafkopf Classic</p><h1>Ein Platz ist<br><em>noch frei.</em></h1><p class="lede">Bayerischer Schafkopf für deinen Computer. Du spielst gegen Sepp, Resi und Wastl – ohne Internetverbindung und mit allem, was eine gute Runde braucht.</p><div class="actions">{button('Jetzt herunterladen','#download')}<a class="text-link" href="#einblicke">Spiel ansehen</a></div></div><figure class="screen-stage">{screenshot('stammtisch','Echte Spielansicht am dunklen Stammtisch.',True)}<figcaption>Die lange Karte. Ein Mensch. Drei Computerspieler.</figcaption></figure></div></section>
    <div class="wrap reassurance"><span>Alle Spielfunktionen kostenlos</span><span>Ohne Anmeldung</span><span>Keine Werbung</span></div>
    <section class="section"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Eine Runde nach deinen Regeln</p><h2>Vertraut am Tisch.<br>Flexibel im Alltag.</h2></div><p>Gespielt wird mit 32 Karten: Sauspiel, Wenz, Farbwenz und Farbsolo sowie Tout und Sie. Stoß, Retour, Schneider, Schwarz und Laufende gehören dazu.</p></div>
    <div class="feature-list"><article><h3>Dein Gegenüber.</h3><p>Leicht, Mittel oder Stark: Drei KI-Stufen machen Platz für den entspannten Einstieg und anspruchsvollere Partien.</p></article><article><h3>Dein Tempo.</h3><p>Die Bedenkzeit der Computer lässt sich einstellen. Nach jeder Aktion wird gespeichert, damit du später weiterspielen kannst.</p></article><article><h3>Dein Spielstand.</h3><p>Konten, Statistik und Einstellungen bleiben lokal. Die Beträge im Spiel sind fiktiv. Es gibt keine Geldeinsätze oder Auszahlungen.</p></article></div></div></section>
    <section class="section section-dark"><div class="wrap split"><figure>{screenshot('lernmodus','Lernmodus mit Erklärungen, Augenübersicht und Zugvorschlag.')}</figure><div><p class="eyebrow">Zug für Zug verstehen</p><h2>Du musst kein<br>Profi sein.</h2><p class="lede">Der Lernmodus erklärt die Situation am Tisch, zeigt Augen und Trümpfe und bietet einen Zugvorschlag. So lernst du direkt beim Spielen.</p><p>Lernpartien verändern deine Spielkonten und Statistik nicht. Du kannst also ganz in Ruhe ausprobieren.</p></div></div></section>
    <section class="section" id="einblicke"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Zwei Tische. Dein Stil.</p><h2>Drinnen gemütlich.<br>Draußen gesellig.</h2></div><p>Stammtisch mit bayerischen Texten oder heller Biergarten mit Hochdeutsch: Beide Gestaltungen stehen dir zur Verfügung, ebenso zwei Kartensätze.</p></div><div class="gallery"><figure>{screenshot('stammtisch','Dunkler Stammtisch mit klassischem Kartensatz.')}<figcaption>Der Stammtisch</figcaption><p class="note">Dunkles Holz, bayerische Texte und klassische Karten.</p></figure><figure>{screenshot('biergarten','Heller Biergarten mit Dirndl-Kartensatz.')}<figcaption>Der Biergarten</figcaption><p class="note">Helle Gestaltung, hochdeutsche Texte und ein zweiter Kartensatz.</p></figure></div></div></section>
    <section class="section download-section" id="download"><div class="wrap"><p class="eyebrow">Die nächste Runde wartet</p><h2>Schafkopf für<br>deinen Computer.</h2><p class="lede">Die Direktdownloads für Windows und macOS sind verfügbar. Alle Spielfunktionen sind kostenlos.</p><div class="download-grid"><article class="download"><h3>Windows</h3><p class="platform">Windows 10/11 · 64 Bit · Version {APP['version']}</p>{button('Windows-Installer (.exe)',APP['windows_url'])}<p class="note">Der Installer ist nicht Authenticode-signiert. Windows kann deshalb einen Sicherheitshinweis anzeigen. Alternativ steht auf der Downloadseite eine MSI-Datei bereit.</p></article><article class="download"><h3>macOS</h3><p class="platform">Apple Silicon &amp; Intel · Universal-DMG · Version {APP['version']}</p>{button('macOS-Disk-Image (.dmg)',APP['macos_url'])}<p class="note">Der Direktdownload ist ad-hoc signiert und nicht notarisiert. macOS kann einen Sicherheitshinweis anzeigen. Die App aus dem Disk-Image in „Programme“ ziehen.</p></article></div><p class="note"><a href="{APP['release_url']}">Alle Downloads, Lizenztexte und SHA-256-Prüfsummen auf GitHub</a>. Beim Öffnen oder Herunterladen verlässt du diese Website.</p><div class="store-status">{store}<p class="note">Freiwilliges Trinkgeld unterstützt die Entwicklung.<br>Es schaltet keine Funktionen frei und ist kein Abo.</p></div></div></section>
    <section class="section"><div class="wrap support-strip"><div><h2>Wir bleiben in Kontakt.</h2><p>Hilfe bei Installation und Spiel, ein Fehler oder eine Idee für die nächste Version: Schreib mir.</p></div>{button('Hilfe &amp; Kontakt','/schafkopf/support/')}</div></section>'''
    page('/schafkopf/', 'Schafkopf Classic für Windows und macOS · Andreas Distel', 'Bayerischer Schafkopf mit 32 Karten gegen drei Computerspieler. Drei KI-Stufen, Lernmodus, zwei Gestaltungen und lokaler Spielstand. Kostenlos herunterladen.', content, 'schafkopf')


def support():
    content = heading('Hilfe für deine Runde.', 'Support, Fragen und Feedback zu Schafkopf Classic.', 'Schafkopf · Support')
    content += f'''<div class="wrap"><article class="article"><div class="contact-box"><p class="eyebrow">Direkt zum Entwickler</p><h2>Schreib mir.</h2><p>Bei technischen Fragen, Problemen mit dem Spiel oder Ideen für eine Verbesserung erreichst du mich unter:</p><p class="email"><a href="mailto:{MAIL}?subject=Schafkopf%20Classic%20%E2%80%93%20Support">{MAIL}</a></p><p>Hilfreich sind deine App-Version, dein Betriebssystem, eine kurze Beschreibung und der genaue Wortlaut einer Fehlermeldung. Bitte schicke keine Passwörter, Zahlungsdaten oder vertraulichen Dateien.</p><p class="note">Deine Nachricht wird zur Bearbeitung der Anfrage verwendet. Einzelheiten findest du im <a href="/datenschutz/#kontakt">Datenschutz zur Kontaktaufnahme</a>.</p></div>
    <p>{button('Kontaktformular öffnen','/kontakt/')}</p><h2>Häufige Fragen</h2><div class="faq">
    <details><summary>Brauche ich Internet oder ein Benutzerkonto?</summary><p>Für das Spiel nicht. Die Computerspieler werden auf deinem Gerät berechnet. Eine Verbindung zu Apple wird für StoreKit-Produktinformationen und freiwillige In-App-Käufe in der Mac-App-Store-Version verwendet.</p></details>
    <details><summary>Wird mit echtem Geld gespielt?</summary><p>Nein. Alle Beträge am Spieltisch sind fiktive Spielbeträge. Es gibt keine Einzahlungen, Einsätze oder Auszahlungen. Freiwilliges Trinkgeld an den Entwickler ist davon unabhängig und verändert das Spiel nicht.</p></details>
    <details><summary>Wie kann ich eine Partie fortsetzen?</summary><p>Schafkopf speichert nach jeder Spielaktion. Beim nächsten Start wählst du „Weiterspielen“. Die Spielstände liegen als <code>spielstand.json</code> im lokalen App-Datenverzeichnis. Eine Sicherung oder Synchronisierung in einer Cloud ist nicht eingebaut.</p></details>
    <details><summary>Warum zeigt mein System beim Direktdownload eine Warnung?</summary><p>Die Windows-Dateien sind nicht Authenticode-signiert. Der macOS-Direktdownload ist ad-hoc signiert und nicht notarisiert. Die auf dieser Seite verlinkte Downloadseite enthält die Dateien und zugehörigen SHA-256-Prüfsummen. Wenn du unsicher bist, öffne die Datei nicht und kontaktiere mich mit dem genauen Hinweis.</p></details>
    <details><summary>Was passiert im Lernmodus mit Konten und Statistik?</summary><p>Eine Partie, in der der Lernmodus benutzt wurde, zählt nicht für die Spielkonten und Statistik. Das gilt auch, wenn du ihn während derselben Partie wieder ausschaltest. Die Abrechnung bleibt zur Erklärung sichtbar.</p></details>
    <details><summary>Kann ich Spielstände zwischen Versionen übernehmen?</summary><p>Die App speichert lokal. Die Mac-App-Store-Version nutzt einen eigenen App-Container; ein automatischer Import aus der Direktdownload-Version ist nicht eingerichtet. Bitte sichere vorhandene Daten vor einem Wechsel und frage bei Bedarf nach.</p></details>
    <details><summary>Wie funktionieren freiwilliges Trinkgeld und Erstattungen?</summary><p>Alle Spielfunktionen sind ohne Trinkgeld nutzbar. Die Mac-App-Store-Version verwendet für Trinkgeld einen wiederholt kaufbaren Verbrauchsartikel über Apple. Der Preis wird von Apple geladen. Für Kaufprobleme oder mögliche Erstattungen über Apple nutze <a href="https://reportaproblem.apple.com/">Apples Seite „Problem melden“</a>. Im Direktdownload öffnet der Trinkgeld-Knopf auf Wunsch PayPal im Browser.</p></details>
    </div><div class="subtle-panel"><h2>Kontakt und Anbieter</h2>{contact()}<p>Vollständige Anbieterangaben einschließlich USt-IdNr. stehen im <a href="/impressum/">Impressum</a>.</p></div></article></div>'''
    page('/schafkopf/support/', 'Support & Kontakt · Schafkopf Classic', 'Hilfe zu Installation, Spielständen und Lernmodus. Kontakt zum Entwickler von Schafkopf Classic, häufige Fragen und Informationen zu freiwilligem Trinkgeld.', content, 'support')


def imprint():
    if not re.fullmatch(r'DE\d{9}', OWNER['vat_id']):
        raise SystemExit('A valid-format, owner-provided VAT identifier is required before publishing.')
    content = heading('Impressum', 'Anbieter dieser Website und von Schafkopf Classic.')
    content += f'''<div class="wrap"><article class="article"><h2>Angaben nach § 5 DDG</h2>{contact()}
    <h2>Umsatzsteuer-Identifikationsnummer</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz:<br><strong>{escape(OWNER['vat_id'])}</strong></p>
    <h2>Inhalte und Rechte</h2><p>Verantwortlich für die hier bereitgestellten Inhalte ist {NAME}. Die Rechte an eigenen Texten, Bildern und Programmen bleiben vorbehalten. In den Apps und auf dieser Website verwendete Software Dritter unterliegt ihren jeweiligen Lizenzen.</p><p>Die lokal eingebundene Schrift Figtree steht unter der SIL Open Font License. Der <a href="/assets/fonts/FIGTREE-LICENSE.txt">Lizenztext</a> ist hier abrufbar. Lizenzinformationen zu Schafkopf findest du in der App unter „Über“ und bei den <a href="{APP['release_url']}">öffentlichen Downloads</a>.</p>
    <h2>Support und Datenschutz</h2><p>Für Fragen zur App nutze die <a href="/schafkopf/support/">Supportseite</a>. Informationen zur Datenverarbeitung stehen im <a href="/datenschutz/">Datenschutz der Website</a> und im <a href="/schafkopf/datenschutz/">Datenschutz für Schafkopf Classic</a>.</p><p class="date">Stand: {DATE}</p></article></div>'''
    page('/impressum/', 'Impressum · Andreas Distel', 'Anbieterkennzeichnung nach § 5 DDG: Andreas Distel, Kontakt, Anschrift und Umsatzsteuer-Identifikationsnummer.', content)


def rights():
    return '''<h2 id="rechte">Deine Datenschutzrechte</h2><p>Soweit personenbezogene Daten von mir verarbeitet werden, stehen dir nach Maßgabe der DSGVO insbesondere Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung und Datenübertragbarkeit zu. Eine erteilte Einwilligung kannst du mit Wirkung für die Zukunft widerrufen.</p><p><strong>Widerspruch:</strong> Erfolgt eine Verarbeitung auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO, kannst du aus Gründen deiner besonderen Situation widersprechen. Die Kontaktadresse des Verantwortlichen findest du oben.</p><p>Außerdem kannst du dich bei einer Datenschutzaufsichtsbehörde beschweren, etwa an deinem Aufenthaltsort. Für den Anbieter zuständig ist der <a href="https://www.baden-wuerttemberg.datenschutz.de/kontakt-aufnehmen/">Landesbeauftragte für den Datenschutz und die Informationsfreiheit Baden-Württemberg</a>, Heilbronner Straße 35, 70191 Stuttgart, E-Mail <a href="mailto:poststelle@lfdi.bwl.de">poststelle@lfdi.bwl.de</a>.</p><p>Eine automatisierte Entscheidungsfindung mit rechtlicher oder vergleichbar erheblicher Wirkung und ein entsprechendes Profiling finden durch mich nicht statt.</p>'''


def contact_page():
    endpoint = FORM.get('endpoint')
    enabled = bool(endpoint and FORM.get('avv_confirmed'))
    disabled = '' if enabled else ' disabled'
    action = escape(endpoint or '/kontakt/', quote=True)
    status = '' if enabled else '<p class="form-status" role="status">Das Kontaktformular ist noch nicht freigeschaltet. Du erreichst mich bereits per E-Mail.</p>'
    content = heading('Schreib mir.', 'Eine Frage zu Schafkopf, ein Fehler oder eine Idee? Hier ist Platz für deine Nachricht.', 'Kontakt')
    content += f'''<div class="wrap"><article class="article"><p>Empfänger: {NAME}. Die Angaben mit * werden benötigt, um deine Anfrage zu bearbeiten und dir zu antworten.</p>{status}
    <form class="contact-form" action="{action}" method="post" accept-charset="UTF-8" aria-label="Kontakt zu Andreas Distel">
      <input type="hidden" name="_subject" value="Kontakt über fluxbar.app"><input type="hidden" name="_lang" value="de"><input type="hidden" name="_next" value="{BASE}/kontakt/danke/">
      <div class="form-trap" aria-hidden="true"><label for="website-field">Dieses Feld bitte leer lassen</label><input id="website-field" type="text" name="_gotcha" tabindex="-1" autocomplete="off"></div>
      <fieldset{disabled}><legend>Deine Nachricht</legend>
      <div class="form-columns"><div class="form-field"><label for="sender-name">Dein Name *</label><input id="sender-name" name="Name" type="text" autocomplete="name" maxlength="100" required></div>
      <div class="form-field"><label for="sender-email">Deine E-Mail-Adresse *</label><input id="sender-email" name="E-Mail" type="email" autocomplete="email" inputmode="email" required maxlength="254"></div></div>
      <div class="form-field"><label for="topic">Worum geht es? *</label><select id="topic" name="Thema" required><option value="Schafkopf Classic">Schafkopf Classic</option><option value="Website oder allgemeine Anfrage">Website oder allgemeine Anfrage</option><option value="Datenschutzanfrage">Datenschutzanfrage</option></select></div>
      <div class="form-field"><label for="message">Deine Nachricht *</label><textarea id="message" name="Nachricht" rows="7" required minlength="10" maxlength="5000" aria-describedby="message-help"></textarea><p id="message-help" class="note">Bitte keine Passwörter, Zahlungsdaten oder vertraulichen Dateien senden. Bei Fehlern helfen App-Version, Betriebssystem und die genaue Fehlermeldung.</p></div>
      <p class="note">Mit „Nachricht senden“ werden deine Angaben zur Bearbeitung der Anfrage über Form.taxi zugestellt. Mehr dazu im <a href="/datenschutz/#formular">Datenschutz zum Kontaktformular</a>.</p>
      <label class="form-confirm"><input type="checkbox" name="Datenverarbeitung bestätigt" value="Ja" required><span>Ich habe die <a href="/datenschutz/#formular">Datenschutzhinweise zur Anfragebearbeitung</a> zur Kenntnis genommen. *</span></label>
      <button class="button" type="submit">Nachricht senden <span aria-hidden="true">→</span></button>
      </fieldset></form><div class="subtle-panel"><h2>Lieber per E-Mail?</h2><p>Du erreichst mich auch unter <a href="mailto:{MAIL}">{MAIL}</a>. Weitere Kontaktdaten stehen im <a href="/impressum/">Impressum</a>.</p></div></article></div>'''
    page('/kontakt/', 'Kontakt · Andreas Distel', 'Kontaktformular für Fragen zu Schafkopf Classic, Support und Datenschutz. Direkter Kontakt zum Entwickler Andreas Distel.', content, form_action=True)
    content = heading('Danke für deine Nachricht.', 'Die Formularübermittlung wurde abgeschlossen.')
    content += '<div class="wrap"><article class="article"><p>Ich melde mich über die angegebene E-Mail-Adresse bei dir. Bitte prüfe auch deinen Spam-Ordner. Wenn du einen Fehler bei der Übermittlung gesehen hast, schreibe direkt an <a href="mailto:'+MAIL+'">'+MAIL+'</a>.</p><div class="actions">'+button('Zurück zu Schafkopf','/schafkopf/')+'</div></article></div>'
    page('/kontakt/danke/', 'Nachricht übermittelt · Andreas Distel', 'Bestätigung nach dem Versand einer Kontaktanfrage.', content, noindex=True)


def website_privacy():
    content = heading('Datenschutz der Website', 'Was beim Besuch dieser Seiten und bei einer Kontaktaufnahme mit deinen Daten geschieht.')
    content += f'''<div class="wrap"><article class="article"><p class="date">Stand: {DATE}</p><p>Diese Erklärung gilt für die Website unter <strong>fluxbar.app</strong>. Die App hat eine eigene <a href="/schafkopf/datenschutz/">Datenschutzerklärung für Schafkopf Classic</a>.</p>
    <div class="toc"><p>Auf dieser Seite</p><ul><li><a href="#verantwortlich">Verantwortlicher</a></li><li><a href="#hosting">Hosting und technische Daten</a></li><li><a href="#cookies">Cookies und eingebundene Inhalte</a></li><li><a href="#kontakt">Kontakt per E-Mail</a></li><li><a href="#formular">Kontaktformular</a></li><li><a href="#links">Externe Links</a></li><li><a href="#rechte">Deine Rechte</a></li></ul></div>
    <h2 id="verantwortlich">Verantwortlicher</h2>{contact()}
    <h2 id="hosting">Hosting und technische Daten</h2><p>Diese Website wird über GitHub Pages ausgeliefert. Anbieter ist GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. GitHub verarbeitet beim Abruf technische Verbindungsdaten und protokolliert nach eigener Angabe IP-Adressen zu Sicherheitszwecken, auch ohne GitHub-Anmeldung.</p><p>Die technische Verarbeitung dient dazu, die angeforderten Seiten auszuliefern und den Betrieb gegen Missbrauch abzusichern. Grundlage für die Bereitstellung durch mich ist Art. 6 Abs. 1 lit. f DSGVO; das berechtigte Interesse liegt im sicheren und verlässlichen Betrieb dieser Produkt- und Supportseite.</p><p>GitHub kann Daten in den USA und weiteren Ländern verarbeiten. GitHub beschreibt hierfür unter anderem Standardvertragsklauseln und seine Teilnahme am EU-US Data Privacy Framework. Umfang, Zwecke und Aufbewahrung durch GitHub erläutert die <a href="https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement">GitHub-Datenschutzerklärung</a>. Weitere Informationen stehen in <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection">GitHubs Hinweisen zu Pages</a>. Ich habe keinen Zugriff auf die von GitHub geführten IP-Protokolle und kann deren Löschfristen nicht selbst bestimmen.</p>
    <h2 id="cookies">Cookies, Schriften und eingebundene Inhalte</h2><p>Diese Website setzt selbst keine Cookies und verwendet kein Local Storage, keine Webanalyse, keine Werbetracker und kein Fingerprinting. Schriften, Bilder und Styles werden von derselben Website geladen. Es gibt keine eingebetteten Videos, Karten, Social-Media-Widgets oder externen Schriftendienste.</p><p>Für diese Funktionen wird daher keine Einwilligung in Analyse- oder Marketing-Speicherungen abgefragt. Die technische Verarbeitung beim Hosting wird oben gesondert beschrieben.</p>
    <h2 id="kontakt">Kontakt per E-Mail</h2><p>Wenn du mir schreibst, werden deine E-Mail-Adresse, der Inhalt deiner Nachricht und freiwillig mitgeteilte Angaben zur Bearbeitung der Anfrage verarbeitet. Ein Klick auf einen E-Mail-Link öffnet dein eigenes E-Mail-Programm; die Website sendet nicht automatisch eine Nachricht.</p><p>Die Verarbeitung beruht bei vertragsbezogenen Anfragen auf Art. 6 Abs. 1 lit. b DSGVO, bei sonstigen Anfragen auf Art. 6 Abs. 1 lit. f DSGVO. Mein berechtigtes Interesse besteht darin, Anfragen zu beantworten und Support anzubieten. Zur Übermittlung und Verwaltung werden die an der E-Mail-Kommunikation beteiligten E-Mail-Dienstleister eingesetzt.</p><p>Die Angaben werden gelöscht, wenn die Anfrage abschließend bearbeitet ist und weder gesetzliche Aufbewahrungspflichten noch erforderliche Nachweise oder berechtigte Sicherungsinteressen eine weitere Speicherung erfordern. Die Kontaktaufnahme ist freiwillig; ohne Rücksendeadresse und Beschreibung des Anliegens kann ich die Anfrage gegebenenfalls nicht beantworten.</p>
    <h2 id="formular">Kontaktformular über Form.taxi</h2><p>Das <a href="/kontakt/">Kontaktformular</a> verwendet Form.taxi, betrieben von wrkt*biz Reinhard Söllradl in Österreich, als Auftragsverarbeiter. Name, E-Mail-Adresse, Nachricht, Thema und technische Verbindungsdaten werden zur Zustellung und Spam-Abwehr verarbeitet. Der Anbieter beschreibt eine Verarbeitung innerhalb der EU und eine maximale Archivdauer von einem Jahr. Frühere Löschung bleibt möglich.</p><p>Rechtsgrundlagen und Löschkriterien entsprechen der oben beschriebenen Kontaktbearbeitung. Grundlage der Beauftragung ist ein AV-Vertrag nach Art. 28 DSGVO. Hinweise des Anbieters: <a href="https://docs.form.taxi/de/privacy">Form.taxi-Datenschutz</a>. Auf der Website werden dafür keine externen Skripte geladen; die Übertragung startet mit dem Absenden.</p>
    <h2 id="links">Externe Links und Downloads</h2><p>Links führen unter anderem zu GitHub-Downloads, Apple und den dort verlinkten Datenschutzhinweisen. Erst wenn du einen solchen Link öffnest, rufst du das jeweilige Angebot auf. Dort gilt die Datenverarbeitung des jeweiligen Anbieters. Diese Website übermittelt beim Weiterklicken aufgrund ihrer Referrer-Einstellung keine Herkunftsadresse.</p>
    {rights()}<h2>Änderungen</h2><p>Bei Änderungen an den eingesetzten Diensten oder an der Verarbeitung wird diese Erklärung aktualisiert. Das oben angegebene Datum zeigt den letzten Stand.</p></article></div>'''
    page('/datenschutz/', 'Datenschutz der Website · Andreas Distel', 'Datenschutz für fluxbar.app: GitHub Pages, technische Zugriffsdaten, lokale Schriften, E-Mail-Kontakt und deine Datenschutzrechte.', content)


def app_privacy():
    content = heading('Datenschutz für Schafkopf Classic', 'Dein Spiel bleibt auf deinem Computer. Hier stehen die Einzelheiten – auch zu optionalem Trinkgeld.', 'Schafkopf · Datenschutz')
    content += f'''<div class="wrap"><article class="article"><p class="date">Stand: {DATE}</p><div class="privacy-summary"><p><strong>Lokal spielen</strong>Spielstände und Statistik bleiben auf deinem Gerät.</p><p><strong>Ohne Tracking</strong>Keine Werbung, keine Analyse- oder Trackingdienste.</p><p><strong>Trinkgeld freiwillig</strong>Zahlungen über Apple oder PayPal sind von der Partie getrennt.</p></div>
    <div class="toc"><p>Auf dieser Seite</p><ul><li><a href="#verantwortlich">Verantwortlicher</a></li><li><a href="#lokal">Spiel und lokale Daten</a></li><li><a href="#apple">Apple und In-App-Käufe</a></li><li><a href="#paypal">Direktdownload und PayPal</a></li><li><a href="#deine-daten">Speicherung und Löschung</a></li><li><a href="#rechte">Deine Rechte</a></li></ul></div>
    <h2 id="verantwortlich">Verantwortlicher</h2>{contact()}
    <h2 id="lokal">Spiel und lokale Daten</h2><p>Schafkopf Classic funktioniert ohne Spielkonto und ohne Online-Spielserver. Die Entscheidungen der Computerspieler werden auf deinem Gerät berechnet. Spielstände, Einstellungen, Spielkonten und Statistik werden lokal gespeichert. Die Spielkonten enthalten ausschließlich fiktive Spielbeträge; es gibt keine Einzahlungen oder Auszahlungen für das Kartenspiel.</p><p>Die App übermittelt diese Spielinformationen nicht an mich und enthält keine Werbe-, Analyse- oder Trackingdienste. Standort, Kamera, Mikrofon und Kontakte werden nicht angefordert. Soweit lokale Daten einen Personenbezug haben, dient ihre Verarbeitung der Bereitstellung und Fortsetzung des gewünschten Spiels, Art. 6 Abs. 1 lit. b DSGVO.</p>
    <h2 id="apple">Mac App Store und freiwilliges Trinkgeld</h2><p>Die für den Mac App Store vorbereitete App-Version verwendet StoreKit für Produktinformationen und freiwilliges Trinkgeld. Dabei kommuniziert sie mit Apple und verarbeitet die von Apple gelieferten Produktinformationen sowie bestätigte Kauftransaktionen. Zahlungsabwicklung und Zahlungsmittel verwaltet Apple. Die App erhält keine Kreditkarten- oder Bankdaten und sendet keine Kauftransaktionen an einen Server des Entwicklers.</p><p>Die Verarbeitung in der App dient der Anzeige des Angebots und der Abwicklung eines von dir gewünschten Kaufs, Art. 6 Abs. 1 lit. b DSGVO. Apple verarbeitet Daten nach den für seine Dienste geltenden Bedingungen und Datenschutzhinweisen, auch in eigener datenschutzrechtlicher Verantwortung. Einzelheiten findest du in <a href="https://www.apple.com/legal/privacy/">Apples Datenschutzhinweisen</a>.</p><p>Trinkgeld ist freiwillig, verändert keine Spielfunktionen und ist kein Abonnement. Alle Spielfunktionen bleiben ohne Kauf verfügbar. In der Mac-App-Store-Version gibt es keinen externen PayPal-Knopf.</p>
    <h2 id="paypal">Direktdownload-Version und PayPal</h2><p>In der Direktdownload-Version kann ein freiwilliger Trinkgeld-Link die PayPal-Seite im Standardbrowser öffnen. Die App erhält keine Zahlungsdaten von PayPal. Erst beim Aufruf des Angebots verarbeitet PayPal die dort anfallenden Daten nach den <a href="https://www.paypal.com/privacy-full">PayPal-Datenschutzhinweisen</a>. Das Trinkgeld schaltet auch hier keine Spielfunktionen frei.</p>
    <h2 id="deine-daten">Speicherung, Löschung und Kontakt</h2><p>Lokale Spielstände bleiben gespeichert, bis du sie selbst entfernst oder durch neue Daten ersetzt. Das Deinstallieren der App kann je nach Betriebssystem Daten zurücklassen. Die App-Store-Version auf dem Mac speichert im eigenen App-Container. Du kannst lokale App-Daten über die Dateiverwaltung deines Betriebssystems entfernen. Eine Sicherung und Wiederherstellung durch den Entwickler ist nicht möglich, da keine Kopie auf einem Entwickler-Server liegt.</p><p>Apple und PayPal speichern Zahlungs- und Abrechnungsdaten nach ihren eigenen Bedingungen und gesetzlichen Pflichten. Fragen hierzu und entsprechende Löschanliegen richte bitte an den jeweiligen Zahlungsanbieter.</p><p>Bei einer <a href="/schafkopf/support/">Supportanfrage</a> per E-Mail oder Kontaktformular verarbeite ich die von dir mitgeteilten Angaben. Einzelheiten zur Rechtsgrundlage und Speicherdauer stehen im <a href="/datenschutz/#kontakt">Abschnitt zur Kontaktaufnahme</a>. Bitte sende keine unnötigen vertraulichen Daten.</p><p>Wenn du diese Datenschutzerklärung im Browser öffnest, fallen zusätzlich die im <a href="/datenschutz/">Datenschutz der Website</a> beschriebenen technischen Zugriffsdaten an.</p>
    {rights()}<h2>Änderungen</h2><p>Diese Erklärung wird angepasst, wenn sich Funktionen oder Datenverarbeitung ändern. Für die App-Store-Angaben ist stets die Datenverarbeitung des tatsächlich eingereichten Builds maßgeblich.</p></article></div>'''
    page('/schafkopf/datenschutz/', 'Datenschutz · Schafkopf Classic', 'Datenschutzerklärung für Schafkopf Classic: lokale Spielstände, kein Tracking, optionale In-App-Käufe über Apple und freiwilliges Trinkgeld über PayPal im Direktdownload.', content, 'schafkopf')


def redirect(filename, destination, title):
    canonical = BASE + destination
    (ROOT / filename).write_text(f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={destination}"><meta name="robots" content="noindex"><meta name="referrer" content="no-referrer"><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="/assets/site.css"><title>{title} · Andreas Distel</title></head><body><main class="wrap not-found"><h1>{title}</h1><p>Die Seite ist unter einer neuen Adresse erreichbar.</p><a class="button" href="{destination}">Zur aktuellen Seite</a></main></body></html>\n''')


def main():
    if '--production' in sys.argv:
        if not re.fullmatch(r'https://form\.taxi/s/[A-Za-z0-9_-]+', FORM.get('endpoint') or ''):
            raise SystemExit('Publication blocked: configure the real Form.taxi endpoint in site.json.')
        if not FORM.get('avv_confirmed'):
            raise SystemExit('Publication blocked: owner must confirm the Form.taxi processing agreement.')
    home(); product(); support(); imprint(); website_privacy(); app_privacy(); contact_page()
    page('/404.html', 'Seite nicht gefunden · Andreas Distel', 'Diese Seite wurde nicht gefunden.', '<div class="wrap not-found"><p class="eyebrow">404 · Hier liegt keine Karte.</p><h1>Zurück an den Tisch.</h1><p>Die gesuchte Seite gibt es unter dieser Adresse nicht.</p><div class="actions">'+button('Zur Startseite','/')+button('Zum Support','/schafkopf/support/',True)+'</div></div>', noindex=True)
    redirect('Impressum.html', '/impressum/', 'Impressum')
    redirect('impressum.html', '/impressum/', 'Impressum')
    redirect('privacy.html', '/datenschutz/', 'Datenschutz')
    (ROOT / 'support').mkdir(exist_ok=True)
    redirect('support/index.html', '/schafkopf/support/', 'Support')
    entries = ''.join(f'<url><loc>{url}</loc><lastmod>2026-10-25</lastmod></url>' for url in PAGES)
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+entries+'</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /scripts/\nDisallow: /site.json\nSitemap: {BASE}/sitemap.xml\n')
    print(f'Generated {len(PAGES)} public pages, legacy redirects and custom 404. Domain: {BASE}')


if __name__ == '__main__':
    main()
