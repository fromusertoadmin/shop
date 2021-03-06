from django.db import models


class EmailType(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=False)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Тип имейла'
        verbose_name_plural = 'Типы имейлов'


class EmailSendingFact(models.Model):
    type = models.ForeignKey(EmailType)
    order = models.ForeignKey("orders.Order", blank=True, null=True, default=None)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name = 'Отправленый имейл'
        verbose_name_plural = 'Отправленые имейлы'

