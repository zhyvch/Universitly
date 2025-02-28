from django.db import models
from django.utils.translation import gettext as _

from core.apps.common.models import TimestampedBaseModel


class Email(TimestampedBaseModel):
    class EmailType(models.TextChoices):
        CREATING = 'C', _('Creating')
        UPDATING = 'U', _('Updating')
        DELETING = 'D', _('Deleting')
        MARKETING = 'M', _('Marketing')

    type = models.CharField(
        verbose_name=_('Type'),
        choices=EmailType,
        default=EmailType.CREATING,
        unique=True,
    )
    subject = models.CharField(
        verbose_name=_('Subject'),
        max_length=255,
    )
    plain_text = models.TextField(
        verbose_name=_('Plain text'),
    )
    html = models.TextField(
        verbose_name=_('HTML'),
    )

