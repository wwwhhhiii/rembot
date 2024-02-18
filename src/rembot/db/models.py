from tortoise.models import Model
from tortoise import fields


class RemUser(Model):
    """"""

    id = fields.UUIDField(pk=True)
    tg_id = fields.IntField()
    username = fields.CharField(max_length=50)
    reminders: fields.ManyToManyRelation["Reminder"]

    def __str__(self) -> str:
        return self.username


class Reminder(Model):
    """"""

    id = fields.UUIDField(pk=True)
    time = fields.DatetimeField()
    text = fields.TextField()
    user: fields.ManyToManyRelation[RemUser] = fields.ManyToManyField(
        'models.RemUser', related_name='reminders', on_delete=fields.CASCADE)

    def __str__(self) -> str:
        return str(self.time)
