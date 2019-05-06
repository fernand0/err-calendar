{% if updates %} 
Cal
{% for dd, day, date, hour, dur, title in updates %}     {{ loop.index0 }}) {{"%2d" % day}}, {{"%2d" % date}}:{{"%02d" % hour}} ({{dur}}) {{title}}
{% endfor %} 
{% endif %}
