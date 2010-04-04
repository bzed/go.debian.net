{% extends "base" %}

{% block extra_heads %}
	{% if google_site_verification is string %}
		<meta name="google-site-verification" content="{{ google_site_verification }}" />
	{% endif %}
{% endblock %}

{% block body %}
<p>Welcome to <a href="http://deb.li">deb.li</a>, the <a href="http://www.debian.org">Debian</a> ShortURL Service.</p>
{% endblock %}
