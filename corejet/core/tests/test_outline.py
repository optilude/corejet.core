import datetime
import unittest2 as unittest
import lxml.etree

from corejet.core import Scenario, story, scenario, given, when, then
from corejet.core.parser import appendScenarios


@story(id="outline-1",
       title=u"As a developer, I can use 'Scenario Outline'.")
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
Scenario Outline: Count some apples
Given I have <Start amount> apples
When I get <Red> red and <Green> green apples more
Then I have a total of <Sum> apples

Examples:
| Start amount | Red | Green | Sum |
| 2            | 3   | 4     | 9   |
| 3            | 4   | 5     | 12  |
"""
            appendScenarios(story1, text)

        @when(u"The serialize() method is called")
        def when(self):
            self.tree = self.catalogue.serialize()

        @then(u"An XML tree is output containing all epics, stories "
              u"and scenarios")
        def then(self):
            self.assertEqual(
                lxml.etree.tostring(self.tree, pretty_print=True).strip(), """\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
      <scenario name="Count some apples #01">
        <given>I have 2 apples</given>
        <when>I get 3 red and 4 green apples more</when>
        <then>I have a total of 9 apples</then>
      </scenario>
      <scenario name="Count some apples #02">
        <given>I have 3 apples</given>
        <when>I get 4 red and 5 green apples more</when>
        <then>I have a total of 12 apples</then>
      </scenario>
    </story>
    <story id="S2" title="Second story" points="3" requirementStatus="closed" requirementResolution="fixed" priority="high"/>
  </epic>
  <epic id="E2" title="Second epic"/>
</requirementscatalogue>""".strip())
