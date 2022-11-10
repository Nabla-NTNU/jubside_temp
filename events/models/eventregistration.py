from struct import *
from io import BytesIO
import uuid
import base64
from email.mime.image import MIMEImage
from django.db import models
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from qrcode import make

from .managers import RelatedEventRegistrationManager, EventRegistrationManager

class EventRegistration(models.Model):
    """Modell for påmelding på arrangementer.

    Inneholder både påmeldinger og venteliste.
    For ventelistepåmelding er attending satt til False og førstmann på ventelista har number=1.
    """

    event = models.ForeignKey(
        'Event',
        blank=False,
        null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='bruker',
        blank=False,
        null=True)
    date = models.DateTimeField(
        verbose_name="Påmeldingsdato",
        auto_now_add=True,
        null=True)
    number = models.PositiveIntegerField(
        verbose_name='kønummer',
        blank=True,
        null=True,
        help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.')
    attending = models.BooleanField(
        verbose_name='har plass',
        default=True,
        blank=False,
        null=False,
        help_text="Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.")
    has_paid = models.BooleanField(
        verbose_name='Har betalt',
        default=False,
        blank=False,
        null=False,
        help_text="Hvis sann har den påmeldte betalt for billett."
    )
    ticket_id = models.UUIDField(
        verbose_name="unik billett id",
        unique=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unik id som ingen kan gjette seg til.."
    )
    has_received_ticket = models.BooleanField(
        verbose_name="Har mottatt billett",
        default=False,
        help_text="Om billetten har blitt tilsendt brukeren på epost",
        blank=False,
        null=False,
    )
    checked_in = models.BooleanField(
        verbose_name="Sjekket inn",
        default=False,
        help_text="Om personen har sjekket inn på arrangementet.",
        blank=False,
        null=False
    )
    check_in_time = models.DateTimeField(
        verbose_name="Innsjekkstidspunkt",
        blank=True,
        null=True,
        help_text="Hvis sjekket inn: tidspunkt for innsjekk."
    )

    class Meta:
        verbose_name = 'påmelding'
        verbose_name_plural = 'påmeldte'
        db_table = "content_eventregistration"

    objects = EventRegistrationManager()

    def __str__(self):
        return '%s, %s is %s, place: %s' % (self.event,
                                             self.user,
                                             "Attending" if self.attending else "Waiting",
                                             self.number)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        EventRegistration.objects.update_lists(self.event)

    @classmethod
    def get_manager_for(cls, event):
        """Henter en manager for en gitt event."""
        return RelatedEventRegistrationManager(event)

    @property
    def waiting(self):
        """Indikerer om det er en ventelisteplass."""
        return not self.attending

    def waiting_list_place(self):
        """Returnerer hvilken plass man har på ventelisten gitt at man er på ventelisten."""
        return self.number if self.waiting else None

    def set_attending_if_waiting(self):
        """Flytter en bruker fra ventelisten til påmeldte hvis ikke allerede påmeldt."""
        if not self.attending:
            self.number = self.event.users_attending()+1
            self.attending = True
            self.save()

    def set_attending_and_send_email(self):
        self.set_attending_if_waiting()
        self._send_moved_to_attending_email()

    def _send_moved_to_attending_email(self):
        if self.user.email:
            subject = 'Påmeldt %s' % self.event.headline
            template = loader.get_template("events/moved_to_attending_email.txt")
            message = template.render({'event': self.event, 'name': self.user.get_full_name()})
            self.user.email_user(subject, message)

    def set_has_paid(self):
        self.has_paid = True
        self.save()

    def send_ticket(self):
        if self.user.email:
            subject = 'Billett til %s - Nablas 75-årsjubileum' % self.event.headline
            template = loader.get_template("events/event_ticket_email.txt")
            c = {'event': self.event, 'name': self.user.get_full_name(),
                 'ticket_id': EventRegistration.objects.get(event=self.event, user=self.user).ticket_id}
            message = template.render(c)
            email = EmailMultiAlternatives(subject,
                      message,
                      'noreply@nabla.no',
                      [self.user.email])
            img = make(self.ticket_id)
            stream = BytesIO()
            img.save(stream, format='png')
            email.attach(filename=(str(self.event.headline.replace(' ', '-')) + "-billett-Nablas-75aarsjubileum.png"),
                         content=stream.getbuffer(), mimetype='image/png')
            email.send(fail_silently=False)
