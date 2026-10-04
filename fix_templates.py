register_html = """\
{% extends "base.html" %}
{% block title %}Create Account - EduSpace{% endblock %}
{% block public_content %}
<div class="auth-page" style="align-items:flex-start;padding-top:90px;">
    <div class="auth-card" style="max-width:560px;">
        <div style="text-align:center;margin-bottom:28px;">
            <div class="logo-icon" style="margin:0 auto 16px;width:52px;height:52px;font-size:22px;"><i class="fas fa-graduation-cap"></i></div>
            <h1>Create your account</h1>
            <p class="subtitle">Join EduSpace as a teacher or student</p>
        </div>
        <form method="post" enctype="multipart/form-data" novalidate>
            {% csrf_token %}
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div class="form-group">
                    <label>First Name</label>
                    <input type="text" name="first_name" placeholder="First name" value="{{ form.first_name.value|default:'' }}">
                    {% if form.first_name.errors %}<ul class="errorlist">{% for e in form.first_name.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
                </div>
                <div class="form-group">
                    <label>Last Name</label>
                    <input type="text" name="last_name" placeholder="Last name" value="{{ form.last_name.value|default:'' }}">
                    {% if form.last_name.errors %}<ul class="errorlist">{% for e in form.last_name.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
                </div>
            </div>
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Choose a username" value="{{ form.username.value|default:'' }}">
                {% if form.username.errors %}<ul class="errorlist">{% for e in form.username.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" placeholder="your@email.com" value="{{ form.email.value|default:'' }}">
                {% if form.email.errors %}<ul class="errorlist">{% for e in form.email.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password1" placeholder="Choose password">
                    {% if form.password1.errors %}<ul class="errorlist">{% for e in form.password1.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
                </div>
                <div class="form-group">
                    <label>Confirm Password</label>
                    <input type="password" name="password2" placeholder="Confirm password">
                    {% if form.password2.errors %}<ul class="errorlist">{% for e in form.password2.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
                </div>
            </div>
            <div class="form-group">
                <label>I am a...</label>
                <div class="radio-group">
                    <label><input type="radio" name="role" value="teacher" {% if form.role.value == 'teacher' %}checked{% endif %}> <i class="fas fa-chalkboard-teacher"></i> Teacher</label>
                    <label><input type="radio" name="role" value="student" {% if not form.role.value or form.role.value == 'student' %}checked{% endif %}> <i class="fas fa-user-graduate"></i> Student</label>
                </div>
                {% if form.role.errors %}<ul class="errorlist">{% for e in form.role.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
            </div>
            <div class="form-group">
                <label>Bio <small style="color:var(--text-muted)">(optional)</small></label>
                <textarea name="bio" rows="2" placeholder="Tell us a little about yourself...">{{ form.bio.value|default:'' }}</textarea>
            </div>
            <div class="form-group">
                <label>Profile Photo <small style="color:var(--text-muted)">(optional)</small></label>
                <input type="file" name="avatar" accept="image/*">
            </div>
            {% if form.non_field_errors %}
            <div class="alert alert-error" style="margin-bottom:16px;">
                <i class="fas fa-exclamation-circle"></i>
                {% for e in form.non_field_errors %}{{ e }} {% endfor %}
            </div>
            {% endif %}
            <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;padding:11px;">
                <i class="fas fa-user-plus"></i> Create Account
            </button>
        </form>
        <p class="auth-link">Already have an account? <a href="{% url 'login' %}">Sign in</a></p>
    </div>
</div>
{% endblock %}
"""

login_html = """\
{% extends "base.html" %}
{% block title %}Sign In - EduSpace{% endblock %}
{% block public_content %}
<div class="auth-page">
    <div class="auth-card">
        <div style="text-align:center;margin-bottom:24px;">
            <div class="logo-icon" style="margin:0 auto 16px;width:52px;height:52px;font-size:22px;"><i class="fas fa-graduation-cap"></i></div>
            <h1>Welcome back</h1>
            <p class="subtitle">Sign in to your EduSpace account</p>
        </div>
        <form method="post" novalidate>
            {% csrf_token %}
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter your username" value="{{ form.username.value|default:'' }}" autocomplete="username">
                {% if form.username.errors %}<ul class="errorlist">{% for e in form.username.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter your password" autocomplete="current-password">
                {% if form.password.errors %}<ul class="errorlist">{% for e in form.password.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
            </div>
            {% if form.non_field_errors %}<div class="alert alert-error" style="margin-bottom:16px;"><i class="fas fa-exclamation-circle"></i>{% for e in form.non_field_errors %}{{ e }}{% endfor %}</div>{% endif %}
            <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;padding:11px;">
                <i class="fas fa-sign-in-alt"></i> Sign In
            </button>
        </form>
        <p class="auth-link">Don't have an account? <a href="{% url 'register' %}">Create one</a></p>
    </div>
</div>
{% endblock %}
"""

with open('templates/accounts/register.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(register_html)

with open('templates/accounts/login.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(login_html)

print("Done! Files written successfully.")
