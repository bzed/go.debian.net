{% extends "base" %}
{% block title %}Preview of {{ domain }}/{{ key }}{% endblock %}

{% block header_subtitle %}Preview of {{ domain }}/{{ key }}{% endblock %}

{% block body %}
<p>This {{ domain }} URL redirects to</p>
<p class="url-preview"><a href="{{ url }}">{{ url }}</a></p>
<p><a href="{{ url }}">here</a> Proceed to this site.</p>
<p>In case you want to abort, 
{% endblock %}

