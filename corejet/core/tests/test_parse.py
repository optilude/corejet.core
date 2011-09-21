import os.path
import shutil
import tempfile
import datetime
import unittest2 as unittest

from corejet.core import Scenario, story, scenario, given, when, then

@story(id="CC-2", title="As a developer, I can parse tests from XML")
class XMLParsing(unittest.TestCase):

    @given("A working directory")
    def workingDirectory(self):
        self.tmpdir = tempfile.mkdtemp()

    @then("Clean up")
    def cleanUp(self):
        shutil.rmtree(self.tmpdir)

    @scenario("Empty catalogue")
    class MinimalInput(Scenario):

        @given("A minimal requirements catalogue file")
        def create(self):
            with open(os.path.join(self.tmpdir, 'input.xml'), 'w') as f:
                f.write("""\
<requirementscatalogue />
""")

        @when("The populate() method is called")
        def serialize(self):
            from corejet.core.model import RequirementsCatalogue
            self.catalogue = RequirementsCatalogue()
            with open(os.path.join(self.tmpdir, 'input.xml'), 'r') as f:
                self.catalogue.populate(f)

        @then("A minimal requirements catalogue is built")
        def checkInput(self):
            self.assertEqual(self.catalogue.extractTime, None)
            self.assertEqual(self.catalogue.testTime, None)
            self.assertEqual(self.catalogue.project, None)
            self.assertEqual(self.catalogue.epics, [])

    @scenario("Requirements extract")
    class RequirementsExtract(Scenario):

        @given("A requirements catalogue file extracted with requirements")
        def create(self):
            with open(os.path.join(self.tmpdir, 'input.xml'), 'w') as f:
                f.write("""\
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
</requirementscatalogue>
""")

        @when("The populate() method is called")
        def serialize(self):
            from corejet.core.model import RequirementsCatalogue
            self.catalogue = RequirementsCatalogue()
            with open(os.path.join(self.tmpdir, 'input.xml'), 'r') as f:
                self.catalogue.populate(f)

        @then("A minimal requirements catalogue is built")
        def checkInput(self):
            self.assertEqual(self.catalogue.extractTime, datetime.datetime(2011, 1, 2, 12, 1, 0))
            self.assertEqual(self.catalogue.testTime, None)
            self.assertEqual(self.catalogue.project, "Test project")
            self.assertEqual(len(self.catalogue.epics), 2)

            self.assertEqual(self.catalogue.epics[0].name, "E1")
            self.assertEqual(self.catalogue.epics[0].title, "First epic")
            self.assertEqual(len(self.catalogue.epics[0].stories), 2)

            self.assertEqual(self.catalogue.epics[1].name, "E2")
            self.assertEqual(self.catalogue.epics[1].title, "Second epic")
            self.assertEqual(len(self.catalogue.epics[1].stories), 0)

            self.assertEqual(self.catalogue.epics[0].stories[0].name, "S1")
            self.assertEqual(self.catalogue.epics[0].stories[0].title, "First story")
            self.assertEqual(self.catalogue.epics[0].stories[0].points, 3)
            self.assertEqual(self.catalogue.epics[0].stories[0].status, "open")
            self.assertEqual(self.catalogue.epics[0].stories[0].resolution, None)
            self.assertEqual(self.catalogue.epics[0].stories[0].priority, "high")
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios), 2)

            self.assertEqual(self.catalogue.epics[0].stories[1].name, "S2")
            self.assertEqual(self.catalogue.epics[0].stories[1].title, "Second story")
            self.assertEqual(self.catalogue.epics[0].stories[1].points, 3)
            self.assertEqual(self.catalogue.epics[0].stories[1].status, "closed")
            self.assertEqual(self.catalogue.epics[0].stories[1].resolution, "fixed")
            self.assertEqual(self.catalogue.epics[0].stories[1].priority, "high")
            self.assertEqual(len(self.catalogue.epics[0].stories[1].scenarios), 0)

            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].name, "First scenario")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].status, None)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[0].givens), 1)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[0].whens), 1)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[0].thens), 2)

            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].name, "Second scenario")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].status, None)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[1].givens), 1)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[1].whens), 1)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[1].thens), 2)

            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].givens[0].text, "something")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].whens[0].text, "something happens")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].thens[0].text, "do something")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].thens[1].text, "and something else")

            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].givens[0].text, "something")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].whens[0].text, "something happens")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].thens[0].text, "do something")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].thens[1].text, "and something else")

    @scenario("Text extract")
    class TextExtract(Scenario):

        @given("A requirements catalogue file extracted with requirements and test results")
        def create(self):
            with open(os.path.join(self.tmpdir, 'input.xml'), 'w') as f:
                f.write("""\
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
</requirementscatalogue>
""")

        @when("The populate() method is called")
        def serialize(self):
            from corejet.core.model import RequirementsCatalogue
            self.catalogue = RequirementsCatalogue()
            with open(os.path.join(self.tmpdir, 'input.xml'), 'r') as f:
                self.catalogue.populate(f)

        @then("A minimal requirements catalogue is built")
        def checkInput(self):
            self.assertEqual(self.catalogue.extractTime, datetime.datetime(2011, 1, 2, 12, 1, 0))
            self.assertEqual(self.catalogue.testTime, datetime.datetime(2011, 1, 2, 12, 5, 0))
            self.assertEqual(self.catalogue.project, "Test project")
            self.assertEqual(len(self.catalogue.epics), 2)

            self.assertEqual(self.catalogue.epics[0].name, "E1")
            self.assertEqual(self.catalogue.epics[0].title, "First epic")
            self.assertEqual(len(self.catalogue.epics[0].stories), 2)

            self.assertEqual(self.catalogue.epics[1].name, "E2")
            self.assertEqual(self.catalogue.epics[1].title, "Second epic")
            self.assertEqual(len(self.catalogue.epics[1].stories), 0)

            self.assertEqual(self.catalogue.epics[0].stories[0].name, "S1")
            self.assertEqual(self.catalogue.epics[0].stories[0].title, "First story")
            self.assertEqual(self.catalogue.epics[0].stories[0].points, 3)
            self.assertEqual(self.catalogue.epics[0].stories[0].status, "open")
            self.assertEqual(self.catalogue.epics[0].stories[0].resolution, None)
            self.assertEqual(self.catalogue.epics[0].stories[0].priority, "high")
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios), 2)

            self.assertEqual(self.catalogue.epics[0].stories[1].name, "S2")
            self.assertEqual(self.catalogue.epics[0].stories[1].title, "Second story")
            self.assertEqual(self.catalogue.epics[0].stories[1].points, 3)
            self.assertEqual(self.catalogue.epics[0].stories[1].status, "closed")
            self.assertEqual(self.catalogue.epics[0].stories[1].resolution, "fixed")
            self.assertEqual(self.catalogue.epics[0].stories[1].priority, "high")
            self.assertEqual(len(self.catalogue.epics[0].stories[1].scenarios), 0)

            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].name, "First scenario")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].status, "pass")
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[0].givens), 1)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[0].whens), 1)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[0].thens), 2)

            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].name, "Second scenario")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].status, "mismatch")
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[1].givens), 1)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[1].whens), 1)
            self.assertEqual(len(self.catalogue.epics[0].stories[0].scenarios[1].thens), 2)

            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].givens[0].text, "something")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].whens[0].text, "something happens")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].thens[0].text, "do something")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[0].thens[1].text, "and something else")

            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].givens[0].text, "something")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].whens[0].text, "something happens")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].thens[0].text, "do something")
            self.assertEqual(self.catalogue.epics[0].stories[0].scenarios[1].thens[1].text, "and something else")

