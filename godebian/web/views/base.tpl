<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
		<title>deb.li: Debian ShortURL Service - %{ block title %}{{ title }}{% endblock %}</title>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<link rel="stylesheet" type="text/css" href="style.css" />
		{% block extra_heads %}
		{% endblock %}
	</head>
	<body>
		<div class="container-outer">
			<div class="container-inner">
				<div class="header-outer">
					<div class="header-inner">
						<div class="header-title"><h1>deb.li: Debian ShortURL Service</h1></div>
						<div class="header-subtitle"><h2>{% block header_subtitle %}{{ title }}{% endblock %}</h2></div>
					</div> <!-- header-inner -->
				</div> <!-- header-outer -->
				<div class="body-outer">
					<div class="body-logo">
                                                {% block body_logo %}
                                                {% endblock %}
					</div> <!-- body-logo -->
					<div class="body-content">
						{% block body %}
						{% endblock %}
					</div> <!-- body-content -->
				</div> <!-- body-outer -->
				<div class="footer-outer">
					<div class="footer-inner">
                                                {% block footer_inner %}
                                                {% endblock %}
					</div> <!-- footer-inner -->
				</div> <!-- footer-outer -->
			</div> <!-- container-inner -->
		</div> <!-- container-outer -->
	</body>
</html>