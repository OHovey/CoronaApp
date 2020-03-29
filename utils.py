from itertools import islice
from models import db_session
 
class BulkManager(object):
    def __init__(self, model, items=[], update_dict={}, removed_items=[], batch_size=100):
        
        self.session = db_session
        self.model = model
        self.update_dict = update_dict
        self.batch_size = batch_size
        self.removed_items = removed_items
 
        self.new_items = list(filter(lambda item: not item.get("id"), items))
        self.existing_items = list(
            filter(lambda item: item.get("id") is not None, items)
        )
 
        if self.new_items:
            self.bulk_create()
        if self.existing_items:
            self.bulk_update()
        if self.removed_items:
            self.bulk_delete()
 
    def _prepare_bulk_create_data(self):
        for item in self.new_items:
            item.update(self.update_dict)
            yield self.model(**item)
 
    def _prepare_bulk_update_data(self):
        for item in self.existing_items:
            item.update(self.update_dict)
            yield self.model(**item)
 
    def bulk_create(self):
        data = self._prepare_bulk_create_data()
        while True:
            items = list(islice(data, self.batch_size))
            if not items:
                break
            self.model.objects.bulk_create(items, self.batch_size)
 
    def bulk_update(self):
        field_item = self.existing_items[0]
        fields = list(filter(lambda key: key is not "id", field_item.keys()))
        data = self._prepare_bulk_update_data() 
 
        while True:
            items = list(islice(data, self.batch_size))
            if not items:
                break
            self.model.objects.bulk_update(items, fields)
 
    def bulk_delete(self):
        ids = [item.get("id") for item in self.removed_items if item.get("id")]
        del_objs = self.model.objects.filter(pk__in=ids)
        if del_objs.exists():
            del_objs._raw_delete("default")