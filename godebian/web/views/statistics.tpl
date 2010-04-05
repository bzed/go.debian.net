{% extends "base" %}
{% block title %}Statistics{% endblock %}
{% block header_subtitle %}Statistics{% endblock %}
{% block body %}
<h2>Some statistics</h2>
<ul>
	<li>
		ShortURLs with dynamically generated keys: {{ non_static_urls }}
	</li>
	<li>
		ShortURLs selected keys: {{ static_urls }}
	</li>
</ul>
{% endblock %}

