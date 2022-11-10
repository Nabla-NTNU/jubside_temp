from content.models import (
    PublicationManagerMixin,
    ViewCounterMixin,
    TimeStamped,
)
from .mixins import RegistrationInfoMixin, EventInfoMixin
from .news.models import TextContent

class AbstractEvent(
    RegistrationInfoMixin,
    EventInfoMixin,
    PublicationManagerMixin,
    ViewCounterMixin,
    TextContent,
    TimeStamped,
):
    """
    Abstract model with the things that are common between Event and Bedpres.
    """

    class Meta:
        abstract = True

    def __str__(self):
        return '%s, %s' % (self.headline, self.event_start.strftime('%d.%m.%y'))

    def get_short_name(self):
        """Henter short_name hvis den finnes, og kutter av enden av headline hvis ikke."""
        return self.short_name if self.short_name else (self.headline[0:18].capitalize() + '...')
