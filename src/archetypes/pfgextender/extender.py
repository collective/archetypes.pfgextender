from zope.component import queryUtility

from Products.PloneFormGen.content.fieldsBase import BaseFormField

from archetypes.pfgextender.interfaces import IPFGExtenderForm
from archetypes.pfgextender.fields import makeATFieldFromPFGField


class Extender(object):
    """Extend archetypes schema with fields constructed from the fields found
    in a PloneFormGen form. That form is queried by name.
    """

    def __init__(self, context):
        self.context = context

    def getFields(self):
        pfgForm = queryUtility(IPFGExtenderForm, name=self.context.portal_type)
        if pfgForm is None:
            return []
        pfgFields = [item for item in pfgForm.objectValues()
            if isinstance(item, BaseFormField)]
        atFields = [
            makeATFieldFromPFGField(pfgField) for pfgField in pfgFields]
        return [atField for atField in atFields if atField is not None]
