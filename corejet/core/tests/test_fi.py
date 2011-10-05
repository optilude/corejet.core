# -*- coding: utf-8 -*-
import datetime
import unittest2 as unittest
import lxml.etree

from corejet.core import Scenario, story, scenario, given, when, then
from corejet.core.parser import appendScenarios


@story(id="fi-1",
       title=u"As a developer, I can describe my scenarios in Finnish")
class Story(unittest.TestCase):

    @scenario(u"Requirements extract")
    class Scenario(Scenario):

        @given(u"A requirements catalogue containing user requirements")
        def given(self):
            from corejet.core.model import RequirementsCatalogue, Epic, Story

            self.catalogue = RequirementsCatalogue(project="Test project",
                    extractTime=datetime.datetime(2011, 1, 2, 12, 1, 0))

            epic1 = Epic("E1", "First epic")
            self.catalogue.epics.append(epic1)

            epic2 = Epic("E2", "Second epic")
            self.catalogue.epics.append(epic2)

            story1 = Story("S1", "First story", points=3, status="open",
                priority="high", epic=epic1)
            epic1.stories.append(story1)

            story2 = Story("S2", "Second story", points=3, status="closed",
                resolution="fixed", priority="high", epic=epic1)
            epic1.stories.append(story2)

            text = u"""\
# language: fi

Tapaus: Ensimmäinen tapaus
Oletetaan, että ajan polkupyörällä,
  mutta minulla ei ole pyöräilykypärää.
Kun törmään liikenteessä autoon,
niin minulle käy tosi huonosti,
  mutta auton kuljettaja voi selvitä vammoitta.

Tapaus: Toinen tapaus
Oletetaan, että olen 1. ja 2. korttelin välissä.
Kun katson suoraan oikealle
niin näen uuden kirjakaupan
  ja kauniin näyteikkunan.

Tapaus: RTFM suomeksi
Oletetaan, että olen pulassa.
Kun klikkaan "Ohjeet"-linkkiä,
niin löydän apua.
"""
            appendScenarios(story1, text)

        @when(u"The serialize() method is called")
        def when(self):
            self.tree = self.catalogue.serialize()

        @then(u"An XML tree is output containing all epics, stories "
              u"and scenarios")
        def then(self):
            self.assertEqual(
                unicode(lxml.etree.tostring(self.tree, pretty_print=True,
                                            encoding="utf-8"),
                        "utf-8").strip(), u"""\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
      <scenario name="Ensimmäinen tapaus">
        <given>ajan polkupyörällä</given>
        <given>minulla ei ole pyöräilykypärää</given>
        <when>törmään liikenteessä autoon</when>
        <then>minulle käy tosi huonosti</then>
        <then>auton kuljettaja voi selvitä vammoitta</then>
      </scenario>
      <scenario name="Toinen tapaus">
        <given>olen 1. ja 2. korttelin välissä</given>
        <when>katson suoraan oikealle</when>
        <then>näen uuden kirjakaupan</then>
        <then>kauniin näyteikkunan</then>
      </scenario>
      <scenario name="RTFM suomeksi">
        <given>olen pulassa</given>
        <when>klikkaan 'Ohjeet'-linkkiä</when>
        <then>löydän apua</then>
      </scenario>
    </story>
    <story id="S2" title="Second story" points="3" requirementStatus="closed" requirementResolution="fixed" priority="high"/>
  </epic>
  <epic id="E2" title="Second epic"/>
</requirementscatalogue>""".strip())
