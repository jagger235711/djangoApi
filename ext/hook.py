from collections import OrderedDict
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject


class HookSerializer(object):
    def to_representation(self, instance):
        super().to_representation(instance)
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            # 自定义字段映射
            if hasattr(self, "sb_%s" % field.field_name):
                value = getattr(self, "sb_%s" % field.field_name)(instance)
                ret[field.field_name] = value
            else:
                try:
                    attribute = field.get_attribute(instance)
                except SkipField:
                    continue

                check_for_none = (
                    attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
                )
                if check_for_none is None:
                    ret[field.field_name] = None
                else:
                    ret[field.field_name] = field.to_representation(attribute)

        return ret
