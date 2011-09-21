import os.path
import shutil
import tempfile
import datetime
import unittest2 as unittest
import lxml.etree

from corejet.core import Scenario, story, scenario, given, when, then

@story(id="CC-1", title="As a developer, I can serialize my tests to XML")
class XMLSerialization(unittest.TestCase):

    @scenario("Empty catalogue")
    class MinimalOutput(Scenario):

        @given("An empty requirements catalogue")
        def create(self):
            from corejet.core.model import RequirementsCatalogue
            self.catalogue = RequirementsCatalogue()

        @when("The serialize() method is called")
        def serialize(self):
            self.tree = self.catalogue.serialize()

        @then("A minimal XML tree is output")
        def checkOutput(self):
            output = lxml.etree.tostring(self.tree)
            self.assertEqual(output, '<requirementscatalogue/>')

    @scenario("Requirements extract")
    class RequirementsExtract(Scenario):

        @given("A requirements catalogue containing user requirements")
        def create(self):
            from corejet.core.model import RequirementsCatalogue
            from corejet.core.model import Epic, Story, Scenario, Step

            self.catalogue = RequirementsCatalogue(project="Test project",
                    extractTime=datetime.datetime(2011,1,2,12,1,0))

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

            scenario1 = Scenario("First scenario", story=story1,
                    givens=[Step("something", 'given')],
                    whens=[Step("something happens", 'when')],
                    thens=[Step("do something", 'then'), Step("and something else", 'then')],
                )
            story1.scenarios.append(scenario1)

            scenario2 = Scenario("Second scenario", story=story2,
                    givens=[Step("something", 'given')],
                    whens=[Step("something happens", 'when')],
                    thens=[Step("do something", 'then'), Step("and something else", 'then')],
                )
            story1.scenarios.append(scenario2)

        @when("The serialize() method is called")
        def serialize(self):
            self.tree = self.catalogue.serialize()

        @then("An XML tree is output containing all epics, stories and scenarios")
        def checkOutput(self):
            self.assertEqual(lxml.etree.tostring(self.tree, pretty_print=True).strip(), """\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
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

    @scenario("Test run extract")
    class TestRunExtract(Scenario):

        @given("A requirements catalogue containing test results")
        def create(self):
            from corejet.core.model import RequirementsCatalogue
            from corejet.core.model import Epic, Story, Scenario, Step

            self.catalogue = RequirementsCatalogue(project="Test project",
                extractTime=datetime.datetime(2011,1,2,12,1,0),
                testTime=datetime.datetime(2011,1,2,12,5,0))

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

            scenario1 = Scenario("First scenario", story=story1,
                    givens=[Step("something", 'given')],
                    whens=[Step("something happens", 'when')],
                    thens=[Step("do something", 'then'), Step("and something else", 'then')],
                    status="pass",
                )
            story1.scenarios.append(scenario1)

            scenario2 = Scenario("Second scenario", story=story2,
                    givens=[Step("something", 'given')],
                    whens=[Step("something happens", 'when')],
                    thens=[Step("do something", 'then'), Step("and something else", 'then')],
                    status="mismatch",
                )
            story1.scenarios.append(scenario2)

        @when("The serialize() method is called")
        def serialize(self):
            self.tree = self.catalogue.serialize()

        @then("An XML tree is output containing all epics, stories and scenarios and their status")
        def checkOutput(self):
            self.assertEqual(lxml.etree.tostring(self.tree, pretty_print=True).strip(), """\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00" testTime="2011-01-02T12:05:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
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

    @scenario("Writing to disk")
    class Writing(Scenario):

        @given("A temporary directory")
        def tempDir(self):
            self.tmpdir = tempfile.mkdtemp()

        @given("A requirements catalogue containing user requirements")
        def create(self):
            from corejet.core.model import RequirementsCatalogue
            from corejet.core.model import Epic, Story, Scenario, Step

            self.catalogue = RequirementsCatalogue(project="Test project",
                extractTime=datetime.datetime(2011,1,2,12,1,0),
                testTime=datetime.datetime(2011,1,2,12,5,0))

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

            scenario1 = Scenario("First scenario", story=story1,
                    givens=[Step("something", 'given')],
                    whens=[Step("something happens", 'when')],
                    thens=[Step("do something", 'then'), Step("and something else", 'then')],
                    status="pass",
                )
            story1.scenarios.append(scenario1)

            scenario2 = Scenario("Second scenario", story=story2,
                    givens=[Step("something", 'given')],
                    whens=[Step("something happens", 'when')],
                    thens=[Step("do something", 'then'), Step("and something else", 'then')],
                    status="mismatch",
                )
            story1.scenarios.append(scenario2)

        @when("The write() method is called with a file in the temporary directory")
        def serialize(self):
            with open(os.path.join(self.tmpdir, 'output.xml'), 'w') as f:
                self.catalogue.write(f)

        @then("An XML tree is output containing all epics, stories and scenarios")
        def checkOutput(self):
            self.assertEqual(open(os.path.join(self.tmpdir, 'output.xml'), 'r').read().strip(), """\
<requirementscatalogue project="Test project" extractTime="2011-01-02T12:01:00" testTime="2011-01-02T12:05:00">
  <epic id="E1" title="First epic">
    <story id="S1" title="First story" points="3" requirementStatus="open" priority="high">
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

        @then("Clean up")
        def cleanUp(self):
            shutil.rmtree(self.tmpdir)
