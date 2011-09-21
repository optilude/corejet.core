"""Basic data model
"""

from lxml import etree
import dateutil.parser

from zope.interface import implements

from corejet.core.interfaces import IRequirementsCatalogue
from corejet.core.interfaces import IEpic
from corejet.core.interfaces import IStory
from corejet.core.interfaces import IScenario
from corejet.core.interfaces import IStep

class RequirementsCatalogue(object):
    implements(IRequirementsCatalogue)
    
    def __init__(self,
        extractTime=None,
        testTime=None,
        project=None,
        epics=None,
    ):
        
        self.extractTime = extractTime
        self.testTime = testTime
        self.project = project
        self.epics = epics or []
    
    def populate(self, input):
        self.extractTime = self.testTime = self.project = None
        self.epics = []
        
        tree = etree.parse(input)
        
        catalogueElement = tree.getroot()
        
        extractTime = catalogueElement.get('extractTime')
        if extractTime:
            self.extractTime = dateutil.parser.parse(extractTime)
        
        testTime = catalogueElement.get('testTime')
        if testTime:
            self.testTime = dateutil.parser.parse(testTime)
        
        self.project = catalogueElement.get('project', None)
        
        for epicElement in catalogueElement.iterchildren(tag="epic"):
            
            name = epicElement.get('id')
            title = epicElement.get('title')
            
            epic = Epic(name, title)
            self.epics.append(epic)
            
            for storyElement in epicElement.iterchildren(tag="story"):
                
                name = storyElement.get("id")
                title = storyElement.get("title")
                points = storyElement.get("points")
                status = storyElement.get("requirementStatus")
                resolution = storyElement.get("requirementResolution")
                priority = storyElement.get("priority")
                
                if points:
                    try:
                        points = int(points)
                    except (TypeError, ValueError,):
                        points = None
                
                story = Story(name, title, points=points, status=status,
                    resolution=resolution, priority=priority, epic=epic)
                epic.stories.append(story)

                for givenElement in storyElement.iterchildren(tag="given"):
                    story.givens.append(Step(givenElement.text, 'given'))

                for givenElement in storyElement.iterchildren(tag="when"):
                    story.givens.append(Step(givenElement.text, 'when'))

                for givenElement in storyElement.iterchildren(tag="then"):
                    story.givens.append(Step(givenElement.text, 'then'))
                
                for scenarioElement in storyElement.iterchildren(tag="scenario"):
                    
                    name = scenarioElement.get("name")
                    status = scenarioElement.get("testStatus")
                    
                    scenario = Scenario(name, status=status, story=story)
                    story.scenarios.append(scenario)
                    
                    for givenElement in scenarioElement.iterchildren(tag="given"):
                        scenario.givens.append(Step(givenElement.text, 'given'))
                    
                    for whenElement in scenarioElement.iterchildren(tag="when"):
                        scenario.whens.append(Step(whenElement.text, 'when'))
                    
                    for thenElement in scenarioElement.iterchildren(tag="then"):
                        scenario.thens.append(Step(thenElement.text, 'then'))
    
    def serialize(self):
        
        catalogueElement = etree.Element("requirementscatalogue")
        
        if self.project:
            catalogueElement.set("project", self.project)
        if self.extractTime:
            catalogueElement.set("extractTime", self.extractTime.isoformat())
        if self.testTime:
            catalogueElement.set("testTime", self.testTime.isoformat())
        
        for epic in self.epics:
            epicElement = etree.SubElement(catalogueElement, "epic")
            
            epicElement.set("id", epic.name)
            epicElement.set("title", epic.title)
            
            for story in epic.stories:
                
                storyElement = etree.SubElement(epicElement, "story")
                storyElement.set("id", story.name)
                storyElement.set("title", story.title)
                
                if story.points:
                    storyElement.set("points", str(story.points))
                if story.status:
                    storyElement.set("requirementStatus", story.status)
                if story.resolution:
                    storyElement.set("requirementResolution", story.resolution)
                if story.priority:
                    storyElement.set("priority", story.priority)
                
                for given in story.givens:
                    givenElement = etree.SubElement(storyElement, "given")
                    givenElement.text = given.text

                for when in story.whens:
                    givenElement = etree.SubElement(storyElement, "when")
                    givenElement.text = given.text
                    
                for then in story.thens:
                    givenElement = etree.SubElement(storyElement, "then")
                    givenElement.text = given.text

                for scenario in story.scenarios:
                    
                    scenarioElement = etree.SubElement(storyElement, "scenario")
                    scenarioElement.set("name", scenario.name)
                    
                    if scenario.status:
                        scenarioElement.set("testStatus", scenario.status)
                    
                    for given in scenario.givens:
                        givenElement = etree.SubElement(scenarioElement, "given")
                        givenElement.text = given.text
                    
                    for when in scenario.whens:
                        whenElement = etree.SubElement(scenarioElement, "when")
                        whenElement.text = when.text
                    
                    for then in scenario.thens:
                        thenElement = etree.SubElement(scenarioElement, "then")
                        thenElement.text = then.text
        
        return etree.ElementTree(catalogueElement)
        
    def write(self, output):
        tree = self.serialize()
        tree.write(output, pretty_print=True)
    
class Epic(object):
    implements(IEpic)
    
    def __init__(self, name, title, stories=None):
        self.name = name
        self.title = title
        self.stories = stories or []

    def __setattr__(self, name, value):
        if type(value) in (str, unicode):
            value = value.replace('"', "'")
        return super(Epic, self).__setattr__(name, value)

class Story(object):
    implements(IStory)
    
    def __init__(self, name, title,
        givens=None,
        whens=None,
        thens=None,
        scenarios=None,
        points=None,
        status=None,
        resolution=None,
        priority=None,
        epic=None,
    ):
        self.name = name
        self.title = title
        self.givens = givens or []
        self.whens = whens or []
        self.thens = thens or []
        self.scenarios = scenarios or []
        self.points = points
        self.status = status
        self.resolution = resolution
        self.priority = priority
        self.epic = epic

    def __setattr__(self, name, value):
        if type(value) in (str, unicode):
            value = value.replace('"', "'")
        return super(Story, self).__setattr__(name, value)

class Scenario(object):
    implements(IScenario)
    
    def __init__(self, name,
        givens=None,
        whens=None,
        thens=None,
        status=None,
        story=None,
    ):
        self.name = name
        self.givens = givens or []
        self.whens = whens or []
        self.thens = thens or []
        self.status = status
        self.story = story

    def __setattr__(self, name, value):
        if type(value) in (str, unicode):
            value = value.replace('"', "'")
        return super(Scenario, self).__setattr__(name, value)

class Step(object):
    implements(IStep)
    
    def __init__(self, text, step_type):
        self.text = text
        self.step_type = step_type

    def __setattr__(self, name, value):
        if type(value) in (str, unicode):
            value = value.replace('"', "'")
        return super(Step, self).__setattr__(name, value)
