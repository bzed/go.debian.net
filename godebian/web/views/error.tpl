{% extends "base" %}
{% block title %}Error {{ status }}: {{ error_name }}{% endblock %}
{% block header_subtitle %}Error {{ status }}: {{ error_name }}{% endblock %}
{% block body %}
<p>Sorry, the requested URL <tt>{{ url }}</tt> caused an error:</p>
<pre>
	{{ error_message }}
</pre>
{% if debug %}
<pre>
{% if traceback is defined %}
{{ traceback }}
{% endif %}

{% if exception is defined %}
{{ exception }}
{% endif %}
</pre>
{% endif %}
{% endblock %}
