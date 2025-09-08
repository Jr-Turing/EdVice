This folder holds site images such as the navbar logo, favicons, and other static assets.

Recommended names:
- logo.png (32–48px height for navbar)
- favicon.ico (16x16/32x32 multi-size icon)
- social-preview.png (Open Graph/Twitter card)

How to reference in templates (Flask/Jinja):
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" class="navbar-logo">
