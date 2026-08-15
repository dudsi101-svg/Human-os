import unittest

from hos_engine.consent import ConsentRegistry
from hos_engine.human_model import *
from hos_engine.personalization import ConsentAwarePersonalizer


class T(unittest.TestCase):
 def test_projection(self):
  m=HumanModel(); m.add(subject_id='H',domain='goals',key='goal',value='ship',evidence_type=EvidenceType.USER_DECLARATION,confidence=1,source_id='H'); c=ConsentRegistry(); c.grant(subject_id='H',grantee_id='A',purposes={'planning'},domains={'goals'},actions={'read'}); x=ConsentAwarePersonalizer(m,c).build_context(subject_id='H',grantee_id='A',purpose='planning',domain='goals'); self.assertIn('goal',x.projection)
