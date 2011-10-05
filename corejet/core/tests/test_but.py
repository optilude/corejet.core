import datetime
import unittest2 as unittest
import lxml.etree

from corejet.core import Scenario, story, scenario, given, when, then
from corejet.core.parser import appendScenarios


@story(id="but-1",
       title=u"As a developer, I can use 'But' like 'And' in scenarios.")
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

            text = """\
Background:
Given some background
  And more background

Scenario: First scenario
Given something
When something happens
Then do something
  And something else
  But not this

Scenario: Second scenario
Given something
When something happens
Then do something
  And something else
"""
            appendScenarios(story1, text)

        @when(u"The serialize() method is called")
        def when(self):
            self.tree = self.catalogue.serialize()

        @then(u"An XML tree is output containing all epics, stories "
              u"with background and scenarios")
        def then(self):
            self.assertEqual(
                lxml.etree.tostring(self.tree, pretty_print=True).strip(), """\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
      <given>some background</given>
      <given>more background</given>
      <scenario name="First scenario">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>something else</then>
        <then>not this</then>
      </scenario>
      <scenario name="Second scenario">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>something else</then>
      </scenario>
    </story>
    <story id="S2" title="Second story" points="3" requirementStatus="closed" requirementResolution="fixed" priority="high"/>
  </epic>
  <epic id="E2" title="Second epic"/>
</requirementscatalogue>""".strip())
