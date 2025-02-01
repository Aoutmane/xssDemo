from flask import Flask, request, render_template
from markupsafe import Markup  # Import Markup from markupsafe

app = Flask(__name__)

# Global list to store comments (for Stored XSS demonstration)
comments = []

# Home page with navigation
@app.route('/')
def home():
    return render_template('home.html')

# Reflected XSS vulnerability
@app.route('/reflected')
def reflected_xss():
    user_input = request.args.get('input', '')
    # Demonstrate escaping (for educational purposes)
    escaped_input = Markup.escape(user_input) if user_input else ''
    return render_template('reflected.html', user_input=user_input, escaped_input=escaped_input)

# Stored XSS vulnerability
@app.route('/stored', methods=['GET', 'POST'])
def stored_xss():
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        comments.append(comment)
    return render_template('stored.html', comments=comments)

# DOM-based XSS vulnerability
@app.route('/dom')
def dom_xss():
    return render_template('dom.html')

# Add a CSP header to mitigate some XSS risks
@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = "script-src 'self'style-src 'self' 'unsafe-inline';"
    return response

if __name__ == '__main__':
    app.run(debug=True)