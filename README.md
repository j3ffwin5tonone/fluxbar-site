# Former FluxBar / Schafkopf website

The product website moved to https://schafkopf-classic.de/ on 2026-10-27.

This repository now serves only static redirect pages for the former public
addresses. Product pages, screenshots, fonts, styles, the contact form and
the former site generator were removed from the published tree.

Known old pages redirect to their matching pages on the new website.
The custom 404 page sends unknown old addresses to the new homepage.
These are HTML meta-refresh redirects because GitHub Pages does not apply
Apache .htaccess rules.

Keep GitHub Pages and the existing fluxbar.app custom-domain configuration
enabled while old links are being used. DNS and email services were not changed.
The earlier site remains recoverable in Git history at commit
d8f08c8327086708914b3879c01a5de9f2ae9640.
