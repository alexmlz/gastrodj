from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date

today = date.today()
today_day = today.day
today_month = today.month
today_year = today.year

# Create your models here.


class UtaInt(models.Model):
    """unique list of internal documents"""

    int_ta = models.CharField(max_length=75, blank=True, null=True)
    sub_ta = models.CharField(max_length=50, blank=True, null=True)
    version_ta = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'u_ta_int'


class Agent(models.Model):
    """An agent within the economic market(previously known as marktteilnehmer)

    A person can act as different agents (personal, tax advisor,
    self-employed). Companies, too, act as agents within the market.

    - old_id:
        The ID in the old system.
    - old_name:
        The name in the old system.
    - birthday:
        The person's birthday.
    - tax_number:
        The person's tax number.
    - social_number:
        The person's social number.
    """
    old_mt_config = models.CharField(max_length=100)
    person = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    StatusType = models.TextChoices(
        'StatusType',
        'ACTIVE DELETED PIPELINE PASSIVE'
    )
    status = models.CharField(max_length=20, choices=StatusType.choices)
    status_reason = models.TextField()
    description = models.CharField(max_length=100)
    EntityType = models.TextChoices(
        'EntityType',
        'person gesellschaft'
    )
    entity = models.CharField(max_length=20, choices=EntityType.choices)
    LawType = models.TextChoices(
        'LawType',
        'bgb gmbhg aktg hgb'
    )
    law = models.CharField(max_length=20, choices=LawType.choices)
    AgentType = models.TextChoices(
        'AgentType',
        'private unternehmen mitarbeiter'
    )
    agent_type = models.CharField(max_length=20, choices=AgentType.choices)
    SubTypeType = models.TextChoices(
        'SubTypeType',
        'freiberuf gewerbe mini-geringf sozialv sozialv-frei'
    )
    sub_type = models.CharField(max_length=20, choices=SubTypeType.choices)
    LevelType = models.TextChoices(
        'LevelType',
        'CLIENT'
    )
    level = models.CharField(max_length=20, choices=LevelType.choices)
    tax_number = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    class Meta:
        db_table = 'agent'


class Asys(models.Model):
    """a_sys"""

    sys_cp = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='sys_cp',
        null=True
    )
    sys_mt = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name='sys_mt',
        null=True
    )
    tmsp = models.DateTimeField(auto_now=True,null=True)
    day = models.PositiveSmallIntegerField(null=True, default=today_day)
    month = models.PositiveSmallIntegerField(null=True, default=today_month)
    year = models.PositiveSmallIntegerField(null=True, default=today_year)
    period = models.CharField(max_length=2, blank=True, null=True)
    navi = models.CharField(max_length=2, blank=True, null=True)
    info = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    reason = models.CharField(max_length=20, blank=True, null=True)
    mt_sender = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name='mt_sender',
        null=True
    )
    mt_receiver = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name='mt_receiver',
        null=True
    )
    mt_bevollm = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name='mt_bevollm',
        null=True
    )
    utaint = models.ForeignKey(
        UtaInt,
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        db_table = 'a_sys'


class AiSysDate(models.Model):
    """Flags define for example if its actual or not"""

    class DatumType(models.TextChoices):
        LIEFER = 'liefer', _('liefer')
        LEISTUNG = 'leistung', _('leistung')
        TERMIN = 'termin', _('termin')

    class Zeitraum(models.TextChoices):
        ZEITRAUM = 'zeitraum', _('zeitraum')
        X = 'x', _('x')

    tmsp = models.DateTimeField(auto_now=True)
    day = models.PositiveSmallIntegerField(null=True, default=today_day)
    month = models.PositiveSmallIntegerField(null=True, default=today_month)
    year = models.PositiveSmallIntegerField(null=True, default=today_year)
    period = models.CharField(max_length=2, blank=True, null=True)
    datum_type = models.CharField(max_length=10, choices=DatumType.choices, null=True)
    zeitraum = models.CharField(max_length=10, choices=Zeitraum.choices, null=True)
    d_beginn_tmsp = models.DateTimeField(auto_now=False, null=True)
    d_beginn_item_day = models.PositiveSmallIntegerField(null=True)
    d_beginn_item_month = models.PositiveSmallIntegerField(null=True)
    d_beginn_item_year = models.PositiveSmallIntegerField(null=True)
    d_beginn_item_period = models.CharField(max_length=2, blank=True, null=True)
    d_end_tmsp = models.DateTimeField(auto_now=False, null=True)
    d_end_item_day = models.PositiveSmallIntegerField(null=True)
    d_end_item_month = models.PositiveSmallIntegerField(null=True)
    d_end_item_year = models.PositiveSmallIntegerField(null=True)
    d_end_item_period = models.CharField(max_length=2, blank=True, null=True)
    # Uhrzeit
    d_beginn_minute = models.PositiveSmallIntegerField(null=True)
    d_beginn_hour = models.PositiveSmallIntegerField(null=True)
    d_end_minute = models.PositiveSmallIntegerField(null=True)
    d_end_hour = models.PositiveSmallIntegerField(null=True)
    asys = models.ForeignKey(
        Asys,
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'ai_sys_date'


class Atalk(models.Model):
    """communication"""

    thema_item = models.CharField(max_length=100, blank=True, null=True)
    sub_item = models.CharField(max_length=40, blank=True, null=True)
    asys = models.ForeignKey(
        Asys,
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        db_table = 'a_talk'


class Atermin(models.Model):
    """appointments"""

    thema_item = models.CharField(max_length=100, blank=True, null=True)
    sub_item = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    telefon = models.CharField(max_length=40, blank=True, null=True)
    asys = models.ForeignKey(
        Asys,
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        db_table = 'a_termin'


class AqAnda(models.Model):
    """q and a"""

    item_q = models.TextField(blank=True, null=True)
    item_a = models.TextField(blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    asys = models.ForeignKey(
        Asys,
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        db_table = 'a_qanda'


class Athema(models.Model):
    """thema"""

    thema_item = models.CharField(max_length=100, blank=True, null=True)
    sub_item = models.CharField(max_length=40, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    asys = models.ForeignKey(
        Asys,
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        db_table = 'a_thema'


class Akommentar(models.Model):
    """thema kommentar"""

    kommentar = models.TextField(blank=True, null=True)
    athema = models.ForeignKey(
        Athema,
        on_delete=models.PROTECT,
        null=True
    )
    asys = models.ForeignKey(
        Asys,
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        db_table = 'a_kommentar'
