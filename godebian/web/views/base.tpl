<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
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
						<div class="header-title"><h1><img src="/static/openlogo-nd-50.png" />deb.li: Debian ShortURL Service</h1></div>
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
						</div>
						<div class="footer-banner">
                                                        {% block footer_banner %}
								<ul>
									<li><a href="http://www.debian.org/"><img src="/static/button-debian.png" alt="debian.org"/></a></li>
									<li><a href="http://jigsaw.w3.org/css-validator/check/referer"><img src="/static/button-css.png"/></a></li>
									<li><a href="http://validator.w3.org/check/referer"><img src="/static/button-xhtml.png"/></a></li>
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
