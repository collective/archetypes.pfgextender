import unittest

from zope.component import provideUtility

from Products.PloneTestCase import PloneTestCase
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from Products.CMFCore.utils import getToolByName

from archetypes.pfgextender.testing import layer
from archetypes.pfgextender.testing import populate
from archetypes.pfgextender.testing import FORM_ID
from archetypes.pfgextender.testing import TEXT_ID
from archetypes.pfgextender.tests import IBirth

PloneTestCase.setupPloneSite()

DOCUMENT_ID = 'document'


class BaseTests(PloneTestCase.PloneTestCase):
    layer = layer

    def testInstalled(self):
        self.failUnless(
            hasattr(self.portal, 'formgen_tool'))
        self.failUnless(
            hasattr(self.portal, 'pfgextender_tool'))

    def testFactory(self):
        id = self.folder.invokeFactory('Birth', 'birth')
        birth = getattr(self.folder, id)
        self.failUnless(IBirth.providedBy(birth))

    def testPopulated(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getToolByName(self.portal, 'pfgextender_tool')
        self.failUnless(FORM_ID in tool)

    def testTypeIsExtended(self):
        self.loginAsPortalOwner()
        populate(self.portal)
        tool = getToolByName(self.portal, 'pfgextender_tool')
        pfgForm = getattr(tool, FORM_ID)
        provideUtility(pfgForm, provides=IPloneFormGenForm)
        self.folder.invokeFactory('Document', DOCUMENT_ID)
        document = getattr(self.folder, DOCUMENT_ID)
        schema = document.Schema()
        self.failUnless(TEXT_ID in schema.keys())
        field = schema.getField(TEXT_ID)
        self.assertEquals(field.getName(), TEXT_ID)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTests))
    return suite
