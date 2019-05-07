{% if updates %} 
List
{% for num, name in updates %}     {{ num }}) {{"%s" % name}} 
{% endfor %} 
{% endif %}
