import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ccl-secret-key-change-in-production")

# ── Mail Configuration (Gmail SMTP) ──────────────────────────────────────
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "ChukselConstructionltd@gmail.com")

app.config["MAIL_SERVER"] = "mail.chukselconstructionltd.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = ADMIN_EMAIL
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
app.config["MAIL_DEFAULT_SENDER"] = ("Chuksel Construction Ltd", ADMIN_EMAIL)

mail = Mail(app)

# ── Service label mapping ────────────────────────────────────────────────
SERVICE_LABELS = {
    "civil-engineering": "Civil Engineering",
    "project-management": "Project Management",
    "general-contracting": "General Contracting",
    "renovation": "Renovation & Remodeling",
    "sustainable-building": "Sustainable Building",
}


# ── Page Routes ──────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/projects")
def projects():
    return render_template("portfolio.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Collect form data
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()

        # Basic validation
        if not name or not email or not message:
            flash("Please fill in all required fields (Name, Email, and Project Details).", "error")
            return redirect(url_for("contact"))

        service_label = SERVICE_LABELS.get(service, service or "Not specified")

        try:
            # ── Email to Admin ───────────────────────────────────────
            admin_msg = Message(
                subject=f"New Quote Request from {name}",
                recipients=[ADMIN_EMAIL],
            )
            admin_msg.html = f"""
            <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0B0C10; border-radius: 8px; overflow: hidden;">
                <div style="background: linear-gradient(135deg, #EBB12F, #C99522); padding: 30px 32px;">
                    <h1 style="color: #0B0C10; margin: 0; font-size: 22px; font-weight: 700;">New Quote Request</h1>
                    <p style="color: #0B0C10; margin: 6px 0 0; font-size: 14px; opacity: 0.8;">A potential client has submitted a project inquiry.</p>
                </div>
                <div style="padding: 32px;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #1f2937; color: #9CA3AF; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; width: 140px;">Name</td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #1f2937; color: #ffffff; font-size: 15px;">{name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #1f2937; color: #9CA3AF; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Email</td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #1f2937; color: #EBB12F; font-size: 15px;"><a href="mailto:{email}" style="color: #EBB12F; text-decoration: none;">{email}</a></td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #1f2937; color: #9CA3AF; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Phone</td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #1f2937; color: #ffffff; font-size: 15px;">{phone or 'Not provided'}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #1f2937; color: #9CA3AF; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Service</td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #1f2937; color: #ffffff; font-size: 15px;">{service_label}</td>
                        </tr>
                    </table>
                    <div style="margin-top: 24px;">
                        <p style="color: #9CA3AF; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 8px;">Project Details</p>
                        <div style="background: #15171E; border: 1px solid #1f2937; border-radius: 6px; padding: 16px;">
                            <p style="color: #d1d5db; font-size: 14px; line-height: 1.6; margin: 0; white-space: pre-wrap;">{message}</p>
                        </div>
                    </div>
                </div>
                <div style="padding: 20px 32px; border-top: 1px solid #1f2937; text-align: center;">
                    <p style="color: #6b7280; font-size: 12px; margin: 0;">Chuksel Construction Limited &bull; Quote Request System</p>
                </div>
            </div>
            """

            # ── Confirmation Email to User ───────────────────────────
            user_msg = Message(
                subject="Your Quote Request Has Been Received – Chuksel Construction",
                recipients=[email],
            )
            user_msg.html = f"""
            <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0B0C10; border-radius: 8px; overflow: hidden;">
                <div style="background: linear-gradient(135deg, #EBB12F, #C99522); padding: 30px 32px;">
                    <h1 style="color: #0B0C10; margin: 0; font-size: 22px; font-weight: 700;">Thank You, {name}!</h1>
                    <p style="color: #0B0C10; margin: 6px 0 0; font-size: 14px; opacity: 0.8;">We've received your project inquiry.</p>
                </div>
                <div style="padding: 32px;">
                    <p style="color: #d1d5db; font-size: 15px; line-height: 1.7; margin: 0 0 20px;">
                        Thank you for reaching out to <strong style="color: #EBB12F;">Chuksel Construction Limited</strong>. 
                        We have received your quote request and our team will review your project details carefully.
                    </p>
                    <p style="color: #d1d5db; font-size: 15px; line-height: 1.7; margin: 0 0 20px;">
                        You can expect to hear back from us within <strong style="color: #ffffff;">24 hours</strong>.
                    </p>
                    <div style="background: #15171E; border: 1px solid #1f2937; border-radius: 6px; padding: 20px; margin: 24px 0;">
                        <p style="color: #9CA3AF; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 12px;">Your Submission Summary</p>
                        <p style="color: #ffffff; font-size: 14px; margin: 0 0 6px;"><strong>Service:</strong> {service_label}</p>
                        <p style="color: #ffffff; font-size: 14px; margin: 0;"><strong>Message:</strong></p>
                        <p style="color: #d1d5db; font-size: 13px; line-height: 1.5; margin: 6px 0 0; white-space: pre-wrap;">{message}</p>
                    </div>
                    <p style="color: #9CA3AF; font-size: 13px; line-height: 1.6; margin: 0;">
                        If you have any urgent questions, feel free to contact us directly at 
                        <a href="mailto:{ADMIN_EMAIL}" style="color: #EBB12F; text-decoration: none;">{ADMIN_EMAIL}</a> 
                        or via WhatsApp.
                    </p>
                </div>
                <div style="padding: 20px 32px; border-top: 1px solid #1f2937; text-align: center;">
                    <p style="color: #6b7280; font-size: 12px; margin: 0;">Chuksel Construction Limited &bull; Building Tomorrow's Landmarks</p>
                </div>
            </div>
            """

            mail.send(admin_msg)
            mail.send(user_msg)

            flash("Your quote request has been sent successfully! We'll get back to you within 24 hours.", "success")

        except Exception as e:
            print(f"[MAIL ERROR] {e}")
            flash("Something went wrong while sending your request. Please try again or contact us directly.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5500)
