import unittest

from hos_engine.human_model import *


class T(unittest.TestCase):
 def test_contest(self):
  m=HumanModel(); r=m.add(subject_id='H',domain='identity',key='role',value='x',evidence_type=EvidenceType.OBSERVATION,confidence=.7,source_id='S'); m.contest(r.record_id,subject_id='H'); self.assertEqual(m.get(r.record_id).status,RecordStatus.CONTESTED)
 def test_supersede(self):
  m=HumanModel(); a=m.add(subject_id='H',domain='goals',key='g',value='A',evidence_type=EvidenceType.USER_DECLARATION,confidence=1,source_id='H'); m.add(subject_id='H',domain='goals',key='g',value='B',evidence_type=EvidenceType.USER_DECLARATION,confidence=1,source_id='H',supersedes=a.record_id); self.assertEqual(m.get(a.record_id).status,RecordStatus.SUPERSEDED)
 def test_layer2_metadata_fields(self):
  m=HumanModel(); r=m.add(subject_id='H',domain='biology',key='sleep_h',value=5.6,evidence_type=EvidenceType.OBSERVATION,confidence=.9,source_id='DEV-1',context='workweek, device-tracked',unit='hours',quality='device-grade',consent_scope='personal-analysis'); self.assertEqual(r.unit,'hours'); self.assertEqual(r.consent_scope,'personal-analysis'); self.assertEqual(r.context,'workweek, device-tracked'); self.assertEqual(r.quality,'device-grade')
 def test_layer2_metadata_defaults_to_none(self):
  m=HumanModel(); r=m.add(subject_id='H',domain='identity',key='k',value='v',evidence_type=EvidenceType.HYPOTHESIS,confidence=.5,source_id='S'); self.assertIsNone(r.context); self.assertIsNone(r.unit); self.assertIsNone(r.quality); self.assertIsNone(r.consent_scope)
