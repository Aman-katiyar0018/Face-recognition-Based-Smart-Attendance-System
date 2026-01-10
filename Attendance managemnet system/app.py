from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Attendance</title>
<h1>Attendance Log</h1>

{% if rows|length == 0 %}
<p>No attendance yet.</p>
{% else %}
<table border="1" cellpadding="5">
<tr>
<th>Timestamp</th>
<th>Name</th>
<th>Distance</th>
</tr>
{% for row in rows %}
<tr>
<td>{{ row[0] }}</td>
<td>{{ row[1] }}</td>
<td>{{ row[2] }}</td>
</tr>
{% endfor %}
</table>
{% endif %}
"""

@app.route("/")
def index():
    try:
        df = pd.read_csv("attendance.csv", header=None)
        rows = df.values.tolist()
    except Exception:
        rows = []

    return render_template_string(TEMPLATE, rows=rows)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)

