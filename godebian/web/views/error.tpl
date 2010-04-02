{% extends "base" %}
{% block title %}Error {{ status }}: {{ error_name }}{% endblock %}
{% block header_subtitle %}Error {{ status }}: {{ error_name }}{% endblock %}
{% block body %}
<p>Sorry, the requested URL <tt>{{ url }}</tt> caused an error:</p>
<pre>
	{{ error_message }}
</pre>
{% endblock %}
