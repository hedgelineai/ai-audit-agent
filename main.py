from flask import Flask, request, render_template_string, send_file
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>AI Website Audit</title></head>
<body>
    <h1>AI Website Audit Tool</h1>
    <form method="post">
        <label>Website URL:</label>
        <input type="text" name="url" required>
        <input type="submit" value="Generate Audit">
    </form>

    {% if pdf_path %}
        <p>✅ Audit ready: <a href="{{ pdf_path }}">Download PDF</a></p>
        <p>📅 Ready to improve your site?</p>
        <a href="https://calendly.com/hedgelineai/free-ai-website-audit-call" target="_blank">
            <button style="padding: 10px 20px; font-size: 16px;">Book Free Call</button>
        </a>
    {% endif %}
</body>
</html>
"""


def run_audit(url):
    return f"""
📄 AI Website Audit Report for: {url}

Design Issues:
- Website may lack mobile optimization.
- No clear call-to-action buttons.

SEO Issues:
- Meta tags missing or not optimized.
- No sitemap.xml or robots.txt found.

AI Gaps:
- No chatbot, calendar, or email automation.
- No personalized landing experience.

Recommendations:
Upgrade your website with modern AI tools.
Book a free call here: https://calendly.com/YOURNAME/free-ai-audit

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    pdf_path = None
    if request.method == "POST":
        url = request.form["url"]
        content = run_audit(url)

        filename = f"audit_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        filepath = os.path.join("static", filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in content.split("\n"):
            pdf.multi_cell(0, 10, line)

        pdf.output(filepath)
        pdf_path = f"/static/{filename}"
    
    return render_template_string(HTML, pdf_path=pdf_path)

@app.route("/static/<filename>")
def download(filename):
    return send_file(os.path.join("static", filename), as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.mkdir("static")
    app.run(host="0.0.0.0", port=3000)
