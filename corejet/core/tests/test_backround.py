import os.path
import shutil
import tempfile
import datetime
import unittest2 as unittest
import lxml.etree

from corejet.core import Scenario, story, scenario, given, when, then
from corejet.core.parser import appendScenarios


@story(id="bg-1",
       title=u"As a developer, I can serialize my story background to XML")
class Story1(unittest.TestCase):

    @scenario(u"Requirements extract")
    class ScenarioA(Scenario):

        @given(u"A requirements catalogue containing user requirements")
        def given(self):
            from corejet.core.model import\
               RequirementsCatalogue,  Epic, Story, Scenario, Step

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

            story1.givens = [Step("some background", 'given'),
                             Step("more background", 'given')]

            scenario1 = Scenario("First scenario", story=story1,
                givens=[Step("something", 'given')],
                whens=[Step("something happens", 'when')],
                thens=[Step("do something", 'then'),
                       Step("and something else", 'then')],
                )
            story1.scenarios.append(scenario1)

            scenario2 = Scenario("Second scenario", story=story2,
                givens=[Step("something", 'given')],
                whens=[Step("something happens", 'when')],
                thens=[Step("do something", 'then'),
                       Step("and something else", 'then')],
                )
            story1.scenarios.append(scenario2)

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
        <then>and something else</then>
      </scenario>
      <scenario name="Second scenario">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>and something else</then>
      </scenario>
    </story>
    <story id="S2" title="Second story" points="3" requirementStatus="closed" requirementResolution="fixed" priority="high"/>
  </epic>
  <epic id="E2" title="Second epic"/>
</requirementscatalogue>""".strip())

    @scenario(u"Test run extract")
    class ScenarioB(Scenario):

        @given(u"A requirements catalogue containing test results")
        def given(self):
            from corejet.core.model import\
               RequirementsCatalogue,  Epic, Story, Scenario, Step

            self.catalogue = RequirementsCatalogue(project="Test project",
                extractTime=datetime.datetime(2011, 1, 2, 12, 1, 0),
                testTime=datetime.datetime(2011, 1, 2, 12, 5, 0))

            epic1 = Epic("E1", "First epic")
            self.catalogue.epics.append(epic1)

            epic2 = Epic("E2", "Second epic")
            self.catalogue.epics.append(epic2)

            story1 = Story("S1", "First story", points=3, status="open",
                priority="high", epic=epic1)
            epic1.stories.append(story1)

            story1.givens = [Step("some background", 'given'),
                             Step("more background", 'given')]

            story2 = Story("S2", "Second story", points=3, status="closed",
                resolution="fixed", priority="high", epic=epic1)
            epic1.stories.append(story2)

            scenario1 = Scenario("First scenario", story=story1,
                givens=[Step("something", 'given')],
                whens=[Step("something happens", 'when')],
                thens=[Step("do something", 'then'),
                       Step("and something else", 'then')],
                status="pass",
                )
            story1.scenarios.append(scenario1)

            scenario2 = Scenario("Second scenario", story=story2,
                givens=[Step("something", 'given')],
                whens=[Step("something happens", 'when')],
                thens=[Step("do something", 'then'),
                       Step("and something else", 'then')],
                status="mismatch",
                )
            story1.scenarios.append(scenario2)

        @when(u"The serialize() method is called")
        def when(self):
            self.tree = self.catalogue.serialize()

        @then(u"An XML tree is output containing all epics, stories with "
              u"backround and scenarios and their status")
        def then(self):
            self.assertEqual(
                lxml.etree.tostring(self.tree, pretty_print=True).strip(), """\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00" testTime="2011-01-02T12:05:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
      <given>some background</given>
      <given>more background</given>
      <scenario name="First scenario" testStatus="pass">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>and something else</then>
      </scenario>
      <scenario name="Second scenario" testStatus="mismatch">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>and something else</then>
      </scenario>
    </story>
    <story id="S2" title="Second story" points="3" requirementStatus="closed" requirementResolution="fixed" priority="high"/>
  </epic>
  <epic id="E2" title="Second epic"/>
</requirementscatalogue>""".strip())

    @scenario(u"Writing to disk")
    class ScenarioC(Scenario):

        @given(u"A temporary directory")
        def givenA(self):
            self.tmpdir = tempfile.mkdtemp()

        @given(u"A requirements catalogue containing user requirements")
        def givenB(self):
            from corejet.core.model import\
               RequirementsCatalogue,  Epic, Story, Scenario, Step

            self.catalogue = RequirementsCatalogue(project="Test project",
                extractTime=datetime.datetime(2011, 1, 2, 12, 1, 0),
                testTime=datetime.datetime(2011, 1, 2, 12, 5, 0))

            epic1 = Epic("E1", "First epic")
            self.catalogue.epics.append(epic1)

            epic2 = Epic("E2", "Second epic")
            self.catalogue.epics.append(epic2)

            story1 = Story("S1", "First story", points=3, status="open",
                priority="high", epic=epic1)
            epic1.stories.append(story1)

            story1.givens = [Step("some background", 'given'),
                             Step("more background", 'given')]

            story2 = Story("S2", "Second story", points=3, status="closed",
                resolution="fixed", priority="high", epic=epic1)
            epic1.stories.append(story2)

            scenario1 = Scenario("First scenario", story=story1,
                givens=[Step("something", 'given')],
                whens=[Step("something happens", 'when')],
                thens=[Step("do something", 'then'),
                       Step("and something else", 'then')],
                status="pass",
                )
            story1.scenarios.append(scenario1)

            scenario2 = Scenario("Second scenario", story=story2,
                givens=[Step("something", 'given')],
                whens=[Step("something happens", 'when')],
                thens=[Step("do something", 'then'),
                       Step("and something else", 'then')],
                status="mismatch",
                )
            story1.scenarios.append(scenario2)

        @when(u"The write() method is called with a file in the temporary "
              u"directory")
        def when(self):
            with open(os.path.join(self.tmpdir, 'output.xml'), 'w') as f:
                self.catalogue.write(f)

        @then(u"An XML tree is output containing all epics, stories with "
              u"background and scenario")
        def thenA(self):
            self.assertEqual(open(os.path.join(self.tmpdir,
                             'output.xml'), 'r').read().strip(), """\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00" testTime="2011-01-02T12:05:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
      <given>some background</given>
      <given>more background</given>
      <scenario name="First scenario" testStatus="pass">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>and something else</then>
      </scenario>
      <scenario name="Second scenario" testStatus="mismatch">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>and something else</then>
      </scenario>
    </story>
    <story id="S2" title="Second story" points="3" requirementStatus="closed" requirementResolution="fixed" priority="high"/>
  </epic>
  <epic id="E2" title="Second epic"/>
</requirementscatalogue>""".strip())

        @then(u"Clean up")
        def thenB(self):
            shutil.rmtree(self.tmpdir)


@story(id="bg-2",
       title=u"As a developer, I can parse tests with background from XML")
class Story2(unittest.TestCase):

    @given(u"A working directory")
    def given(self):
        self.tmpdir = tempfile.mkdtemp()

    @then(u"Clean up")
    def then(self):
        shutil.rmtree(self.tmpdir)

    @scenario(u"Requirements extract")
    class Scenario(Scenario):

        @given(u"A requirements catalogue file extracted with requirements")
        def given(self):
            with open(os.path.join(self.tmpdir, 'input.xml'), 'w') as f:
                f.write("""\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
      <given>some background</given>
      <given>more background</given>
      <scenario name="First scenario">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>and something else</then>
      </scenario>
      <scenario name="Second scenario">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>and something else</then>
      </scenario>
    </story>
    <story id="S2" title="Second story" points="3" requirementStatus="closed" requirementResolution="fixed" priority="high"/>
  </epic>
  <epic id="E2" title="Second epic"/>
</requirementscatalogue>
""")

        @when(u"The populate() method is called")
        def when(self):
            from corejet.core.model import RequirementsCatalogue
            self.catalogue = RequirementsCatalogue()
            with open(os.path.join(self.tmpdir, 'input.xml'), 'r') as f:
                self.catalogue.populate(f)

        @then(u"A minimal requirements catalogue is built")
        def then(self):
            self.assertEqual(len(self.catalogue.epics), 2)
            self.assertEqual(len(self.catalogue.epics[0].stories), 2)
            self.assertEqual(len(self.catalogue.epics[1].stories), 0)

            self.assertEqual(len(self.catalogue.epics[0].stories[0].givens), 2)
            self.assertEqual(self.catalogue.epics[0].stories[0].givens[0].text, "some background")
            self.assertEqual(self.catalogue.epics[0].stories[0].givens[1].text, "more background")

            self.assertEqual(len(self.catalogue.epics[0].stories[1].givens), 0)


@story(id="bg-3",
       title=u"As a developer, I can parse my scenarios with background from text")
class Story3(unittest.TestCase):

    @scenario(u"Without background")
    class ScenarioA(Scenario):

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
Scenario: First scenario
Given something
When something happens
Then do something
  And something else

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
      <scenario name="First scenario">
        <given>something</given>
        <when>something happens</when>
        <then>do something</then>
        <then>something else</then>
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

    @scenario(u"Requirements extract")
    class ScenarioB(Scenario):

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
