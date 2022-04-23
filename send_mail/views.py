
from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


def send_new_order_email(email):
    send_mail(
        'Votre commande sur Jaba',
        'Nous avons bien reçu votre commande',
        'contact@jaba.com',
        [email],
        fail_silently=False,
    )


def send_new_order_email_with_template(email):
    template = get_template("email/new-order.html")
    context = {"email": email}
    subject, from_email = ("Nouvelle commande sur Java", "contact@jaba.com")
    body = template.render(context)
    message = EmailMultiAlternatives(subject, body, from_email, [email])
    message.attach_alternative(body, "text/html")
    message.send(fail_silently=False)


def payment_successful_email(email):
    send_mail(
        'Votre commande sur Jaba',
        'Nous avons bien reçu votre paiement',
        'contact@jaba.com',
        [email],
        fail_silently=False,
    )
