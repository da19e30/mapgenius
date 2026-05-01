import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional


def _get_smtp_config():
    """Obtiene la configuración SMTP desde variables de entorno."""
    return {
        "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "sender": os.getenv("SMTP_SENDER", "noreply@mapgenius.com"),
        "admin_email": os.getenv("ADMIN_EMAIL", "admin@mapgenius.com"),
        "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true",
    }


def _send_email(to: str, subject: str, html_body: str, text_body: str = "", attachments: Optional[list] = None) -> bool:
    """Envía un correo electrónico con opcionales adjuntos.

    Si la configuración SMTP no está completa, se simula el envío y se escribe en stdout.
    """
    config = _get_smtp_config()

    if not config["user"] or not config["password"]:
        print(f"[EMAIL SIMULATION] To: {to}, Subject: {subject}")
        print(f"[EMAIL SIMULATION] Attachments: {[os.path.basename(a) for a in attachments or []]}")
        print(f"[EMAIL SIMULATION] Body: {text_body or html_body[:200]}")
        return True

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = config["sender"]
    msg["To"] = to

    # Cuerpo alternativo (texto plano y HTML)
    if text_body:
        msg.attach(MIMEText(text_body, "plain"))
    if html_body:
        msg.attach(MIMEText(html_body, "html"))

    # Adjuntos
    for path in attachments or []:
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(path)}"'
        msg.attach(part)

    try:
        with smtplib.SMTP(config["host"], config["port"]) as server:
            if config["use_tls"]:
                server.starttls()
            server.login(config["user"], config["password"])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email to {to}: {e}")
        return False


def send_welcome_email(user_email: str, username: str) -> bool:
    """Envía un correo de bienvenida al nuevo usuario."""
    subject = "¡Bienvenido a Mapgenius Solutions!"
    html = f"""
    <html>
      <body style='font-family: Arial, sans-serif; padding: 20px;'>
        <div style='max-width: 600px; margin: 0 auto; background: #f9fafb; padding: 20px; border-radius: 8px;'>
          <h1 style='color: #4f46e5;'>¡Bienvenido a Mapgenius Solutions, {username}!</h1>
          <p>Tu cuenta ha sido creada exitosamente.</p>
          <p>Con Mapgenius podrás:</p>
          <ul>
            <li>📄 Procesar facturas con OCR inteligente</li>
            <li>🤖 Clasificar gastos e ingresos automáticamente</li>
            <li>📊 Visualizar análisis financieros y tendencias</li>
          </ul>
          <p style='margin-top: 20px;'>
            <a href='http://localhost:5173/login' style='background: #4f46e5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>
              Iniciar sesión
            </a>
          </p>
          <hr style='margin: 20px 0;' />
          <p style='font-size: 12px; color: #6b7280;'>© 2026 Mapgenius Solutions. Todos los derechos reservados.</p>
        </div>
      </body>
    </html>
    """
    text = f"¡Bienvenido a Mapgenius Solutions, {username}!\nTu cuenta ha sido creada exitosamente.\nInicia sesión en: http://localhost:5173/login"
    return _send_email(to=user_email, subject=subject, html_body=html, text_body=text)


def send_admin_notification(user_email: str, username: str, user_id: int) -> bool:
    """Notifica al administrador sobre un nuevo registro de usuario."""
    config = _get_smtp_config()
    admin_email = config["admin_email"]
    subject = f"Nuevo registro: {username}"
    html = f"""
    <html>
      <body style='font-family: Arial, sans-serif; padding: 20px;'>
        <h2>Nuevo usuario registrado</h2>
        <table style='border-collapse: collapse; width: 100%;'>
          <tr><td style='padding: 8px; border: 1px solid #ddd;'><strong>ID:</strong></td><td style='padding: 8px; border: 1px solid #ddd;'>{user_id}</td></tr>
          <tr><td style='padding: 8px; border: 1px solid #ddd;'><strong>Usuario:</strong></td><td style='padding: 8px; border: 1px solid #ddd;'>{username}</td></tr>
          <tr><td style='padding: 8px; border: 1px solid #ddd;'><strong>Email:</strong></td><td style='padding: 8px; border: 1px solid #ddd;'>{user_email}</td></tr>
        </table>
        <p style='margin-top: 10px; font-size: 12px; color: #6b7280;'>Fecha: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
      </body>
    </html>
    """
    return _send_email(to=admin_email, subject=subject, html_body=html)


def send_invoice_email(to: str, xml_path: str, pdf_path: str, custom_message: str = "Adjuntamos su factura electrónica.") -> bool:
    """Envía la factura electrónica al cliente con XML y PDF adjuntos.

    Parameters
    ----------
    to: str
        Destinatario (email del cliente).
    xml_path: str
        Ruta absoluta al archivo XML firmado.
    pdf_path: str
        Ruta absoluta al PDF generado.
    custom_message: str, optional
        Mensaje adicional que aparecerá en el cuerpo del correo.
    """
    subject = "Factura electrónica Mapgenius - Documento adjunto"
    html = f"""
    <html>
      <body style='font-family: Arial, sans-serif; padding: 20px;'>
        <p>{custom_message}</p>
        <p>Puede revisar su factura en los documentos adjuntos.</p>
        <p>Saludos cordiales,<br/>Equipo Mapgenius Solutions</p>
      </body>
    </html>
    """
    text = f"{custom_message}\nPuede revisar su factura en los documentos adjuntos.\nSaludos,\nEquipo Mapgenius Solutions"
    return _send_email(to=to, subject=subject, html_body=html, text_body=text, attachments=[xml_path, pdf_path])
