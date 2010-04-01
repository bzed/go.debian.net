<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" >
	<head>
		<title>deb.li: Debian ShortURL Service - {% block title %}{{ title }}{% endblock %}</title>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<link rel="stylesheet" type="text/css" href="/static/style.css" />
		{% block extra_heads %}
		{% endblock %}
	</head>
	<body>
		<div class="container-outer">
			<div class="container-inner">
				<div class="header-outer">
					<div class="header-inner">
						<div class="header-title"><h1><img src="/static/openlogo-nd-50.png" alt="debian.org"/>deb.li: Debian ShortURL Service</h1></div>
						<div class="header-subtitle"><h2>{% block header_subtitle %}{{ title }}{% endblock %}</h2></div>
					</div> <!-- header-inner -->
				</div> <!-- header-outer -->
				<div class="body-outer">
					<div class="body-content">
						{% block body %}
						{% endblock %}
					</div> <!-- body-content -->
				</div> <!-- body-outer -->
				<div class="footer-outer">
					<div class="footer-inner">
						<div class="footer-content">
	                                                {% block footer_content %}
        	                                        {% endblock %}
							<ul>
								<li><a href="http://wiki.debian.org/deb.li">Documentation</a></li>
								<li><a href="/imprint">Imprint/Impressum</a></li>
								<li><a href="mailto:bzed@debian.org?subject=deb.li">Contact</a></li>
							</ul>
							<p>Powered by <a href="http://bzed.de">Bernd Zeimetz'</a> <a href="http://git.recluse.de/?p=debian/go.debian.net.git">godebian</a> software, using <a href="http://www.python.org/">Python</a>, <a href="http://bottle.paws.de/">Bottle</a>, <a href="http://www.sqlalchemy.org/">SQLAlchemy</a> and <a href="http://www.postgresql.org/">PostgreSQL</a></p>
						</div>
						<div class="footer-banner">
                                                        {% block footer_banner %}
								<ul>
									<li><a href="http://www.debian.org/"><img src="/static/button-debian.png" alt="debian.org"/></a></li>
									<li><a href="http://jigsaw.w3.org/css-validator/check/referer"><img src="/static/button-css.png" alt="valid CSS"/></a></li>
									<li><a href="http://validator.w3.org/check/referer"><img src="/static/button-xhtml.png" alt="valid XHTML"/></a></li>
									<li><a href="http://www.credativ.de"><img src="/static/button-credativ.png" alt="credativ GmbH" /></a></li>
								</ul>
                                                        {% endblock %}
						</div>
					</div> <!-- footer-inner -->
				</div> <!-- footer-outer -->
			</div> <!-- container-inner -->
		</div> <!-- container-outer -->
	</body>
</html>
