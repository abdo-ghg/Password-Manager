import string as _string
import streamlit as st
from authentication import register_user, login_user
from password_checker import check_password_strength
from password_generator import generate_password
from file_management import (
    save_password,
    get_passwords,
    delete_password,
    update_password
)

st.set_page_config(page_title="Password Manager", page_icon="🔐", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    [data-testid="stSidebar"] { background-color: #1a1d27; }

    .password-card {
        background: #1e2130;
        border: 1px solid #2d3250;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .password-card h4 { color: #7c83fd; margin: 0 0 10px 0; font-size: 1.05rem; }
    .card-row { display: flex; justify-content: space-between; margin: 5px 0; color: #cdd6f4; font-size: 0.9rem; }
    .card-label { color: #888da7; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; }

    .badge-weak     { background:#f38ba8; color:#11111b; border-radius:4px; padding:2px 8px; font-size:0.8rem; font-weight:600; }
    .badge-moderate { background:#fab387; color:#11111b; border-radius:4px; padding:2px 8px; font-size:0.8rem; font-weight:600; }
    .badge-strong   { background:#a6e3a1; color:#11111b; border-radius:4px; padding:2px 8px; font-size:0.8rem; font-weight:600; }

    .gen-password-box {
        background: #1e2130;
        border: 1px solid #7c83fd;
        border-radius: 8px;
        padding: 14px 18px;
        font-family: monospace;
        font-size: 1.25rem;
        color: #cdd6f4;
        letter-spacing: 2px;
        text-align: center;
        margin: 12px 0;
        word-break: break-all;
    }

    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def strength_bar(strength: str):
    """Render a colored progress bar + badge for password strength."""
    levels = {"Weak": 1, "Moderate": 2, "Strong": 3}
    colors = {"Weak": "#f38ba8", "Moderate": "#fab387", "Strong": "#a6e3a1"}
    pct = levels.get(strength, 1) / 3 * 100
    color = colors.get(strength, "#888")
    st.markdown(f"""
    <div style="background:#2d3250;border-radius:6px;height:10px;margin:6px 0 4px 0;">
        <div style="background:{color};width:{pct:.0f}%;height:10px;border-radius:6px;"></div>
    </div>
    <span class="badge-{strength.lower()}">{strength}</span>
    """, unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "gen_password" not in st.session_state:
    st.session_state.gen_password = ""


# ══════════════════════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:

    st.title("🔐 Password Manager")
    st.markdown("---")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    # ── Register ──────────────────────────────────────────────────────────────
    with tab_register:
        st.subheader("Create Account")
        email    = st.text_input("Email",    key="reg_email")
        username = st.text_input("Username", key="reg_username")
        password = st.text_input("Password", type="password", key="reg_password")

        if password:
            strength_bar(check_password_strength(password))

        if st.button("Register", use_container_width=True):
            if not email or not username or not password:
                st.error("All fields are required.")
            elif register_user(email, username, password):
                st.success("Account created! You can now log in.")
            else:
                st.error("Email or username already exists.")

    # ── Login ─────────────────────────────────────────────────────────────────
    with tab_login:
        st.subheader("Welcome back")
        identifier = st.text_input("Email or Username", key="login_id")
        password   = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", use_container_width=True):
            if not identifier or not password:
                st.error("Please fill in all fields.")
            else:
                user = login_user(identifier, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials.")


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
else:
    user_email = st.session_state.user["email"]
    username   = st.session_state.user["username"]

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"### 👤 {username}")
        st.caption(user_email)
        st.markdown("---")
        menu = st.radio(
            "Navigation",
            [
                "🔑 Password Generator",
                "🛡️ Check Strength",
                "💾 Save Password",
                "📋 View Passwords",
                "✏️ Update Password",
                "🗑️ Delete Password",
                "🚪 Logout",
            ],
            label_visibility="collapsed"
        )

    st.title("🔐 Password Manager")
    st.markdown("---")

    # ── Password Generator ────────────────────────────────────────────────────
    if menu == "🔑 Password Generator":
        st.header("Generate a Secure Password")

        length = st.slider("Length", 6, 64, 16)

        c1, c2, c3 = st.columns(3)
        numbers   = c1.checkbox("Numbers",   value=True)
        symbols   = c2.checkbox("Symbols",   value=True)
        uppercase = c3.checkbox("Uppercase", value=True)

        if st.button("⚙️ Generate", use_container_width=True):
            st.session_state.gen_password = generate_password(length, numbers, symbols, uppercase)

        if st.session_state.gen_password:
            st.markdown(
                f'<div class="gen-password-box">{st.session_state.gen_password}</div>',
                unsafe_allow_html=True
            )
            strength_bar(check_password_strength(st.session_state.gen_password))
            st.text_input("Copy from here:", value=st.session_state.gen_password, key="copy_box")

    # ── Check Strength ────────────────────────────────────────────────────────
    elif menu == "🛡️ Check Strength":
        st.header("Check Password Strength")
        password = st.text_input("Enter password", type="password")

        if password:
            strength = check_password_strength(password)
            strength_bar(strength)

            tips = []
            if len(password) < 8:
                tips.append("Use at least 8 characters")
            if not any(c.isupper() for c in password):
                tips.append("Add uppercase letters")
            if not any(c.isdigit() for c in password):
                tips.append("Add numbers")
            if not any(c in _string.punctuation for c in password):
                tips.append("Add symbols (e.g. !@#$)")

            if tips:
                st.markdown("**Tips to improve:**")
                for tip in tips:
                    st.markdown(f"- {tip}")

    # ── Save Password ─────────────────────────────────────────────────────────
    elif menu == "💾 Save Password":
        st.header("Save a Password")

        website       = st.text_input("Website / App name")
        website_email = st.text_input("Account Email or Username")
        password      = st.text_input("Password", type="password")

        if password:
            strength_bar(check_password_strength(password))

        if st.button("💾 Save", use_container_width=True):
            if not website or not website_email or not password:
                st.error("All fields are required.")
            else:
                strength = check_password_strength(password)
                save_password(user_email, website, website_email, password, strength)
                st.success(f"Password for **{website}** saved!")

    # ── View Passwords ────────────────────────────────────────────────────────
    elif menu == "📋 View Passwords":
        st.header("Saved Passwords")
        passwords = get_passwords(user_email)

        if not passwords:
            st.info("No passwords stored yet. Go to **Save Password** to add one.")
        else:
            st.caption(f"{len(passwords)} entr{'y' if len(passwords) == 1 else 'ies'} found")
            show_passwords = st.toggle("Show passwords", value=False)

            for p in passwords:
                badge_cls = f"badge-{p['strength'].lower()}"
                displayed = p["password"] if show_passwords else "••••••••••••"
                st.markdown(f"""
                <div class="password-card">
                    <h4>🌐 {p['website']}</h4>
                    <div class="card-row">
                        <span class="card-label">Account</span>
                        <span>{p['email']}</span>
                    </div>
                    <div class="card-row">
                        <span class="card-label">Password</span>
                        <span style="font-family:monospace">{displayed}</span>
                    </div>
                    <div class="card-row">
                        <span class="card-label">Strength</span>
                        <span class="{badge_cls}">{p['strength']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Update Password ───────────────────────────────────────────────────────
    elif menu == "✏️ Update Password":
        st.header("Update a Password")
        passwords = get_passwords(user_email)
        sites = [p["website"] for p in passwords]

        if not sites:
            st.info("No saved passwords to update.")
        else:
            website      = st.selectbox("Select website", sites)
            new_password = st.text_input("New Password", type="password")

            if new_password:
                strength_bar(check_password_strength(new_password))

            if st.button("✏️ Update", use_container_width=True):
                if not new_password:
                    st.error("Please enter a new password.")
                else:
                    strength = check_password_strength(new_password)
                    update_password(user_email, website, new_password, strength)
                    st.success(f"Password for **{website}** updated!")

    # ── Delete Password ───────────────────────────────────────────────────────
    elif menu == "🗑️ Delete Password":
        st.header("Delete a Password")
        passwords = get_passwords(user_email)
        sites = [p["website"] for p in passwords]

        if not sites:
            st.info("No saved passwords to delete.")
        else:
            website = st.selectbox("Select website to delete", sites)

            if st.button("🗑️ Delete", use_container_width=True, type="primary"):
                delete_password(user_email, website)
                st.success(f"Entry for **{website}** deleted.")
                st.rerun()

    # ── Logout ────────────────────────────────────────────────────────────────
    elif menu == "🚪 Logout":
        st.session_state.user = None
        st.session_state.gen_password = ""
        st.rerun()