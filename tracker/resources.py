from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Category, Transaction


class TransactionResource(resources.ModelResource):
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="name"),
    )

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.user = kwargs.get('user')

    class Meta:
        model = Transaction
        fields = ("date", "type", "category", "amount")
        import_id_fields = ("date", "type", "category", "amount")
