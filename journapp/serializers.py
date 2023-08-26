from rest_framework import serializers
# from rest_framework.validators import UniqueValidator

from .models import *


class JournalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Journal
        fields = ('id', 'content', 'cre_date', 'subject')
