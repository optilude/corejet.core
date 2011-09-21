from zope.interface import Interface
from zope import schema

class IStep(Interface):
    """A given/when/then step
    """
    
    text = schema.TextLine(title=u"Step text")
    step_type = schema.Choice(title=u"Step type", values=("given", "when", "then,"))

class IScenario(Interface):
    """A scenario comprising multiple given, when and/or then steps
    """
    
    name = schema.TextLine(title=u"Scenario name")
    
    givens = schema.List(title=u"Given clauses", value_type=schema.Object(schema=IStep))
    whens = schema.List(title=u"Given clauses", value_type=schema.Object(schema=IStep))
    thens = schema.List(title=u"Given clauses", value_type=schema.Object(schema=IStep))
    
    status = schema.Choice(title=u"Status", values=('pass', 'fail', 'pending', 'mismatch', 'superfluous',), required=False)
    
    story = schema.Object(schema=Interface, required=False)

class IStory(Interface):
    """A story comprising multiple scenarios
    """
    
    name = schema.TextLine(title=u"Story name")
    
    title = schema.TextLine(title=u"Story title")
    
    givens = schema.List(title=u"Given clauses", value_type=schema.Object(schema=IStep))
    whens = schema.List(title=u"Given clauses", value_type=schema.Object(schema=IStep))
    thens = schema.List(title=u"Given clauses", value_type=schema.Object(schema=IStep))
    
    scenarios = schema.List(title=u"Scenarios", value_type=schema.Object(schema=IScenario))
    
    points = schema.Int(title=u"Story points", required=False)
    status = schema.TextLine(title=u"Status", required=False)
    resolution = schema.TextLine(title=u"Resolution", required=False)
    priority = schema.TextLine(title=u"Priority", required=False)
    
    epic = schema.Object(schema=Interface, required=False)

class IEpic(Interface):
    """An epic comprising multiple stories
    """
    
    name = schema.TextLine(title=u"Story name")
    
    title = schema.TextLine(title=u"Story title")
    
    stories = schema.List(title=u"Stories", value_type=schema.Object(schema=IStory))

class IRequirementsCatalogue(Interface):
    """A requirements catalogue comprising multiple epics
    """
    
    extractTime = schema.Datetime(title=u"Extract time")
    testTime = schema.Datetime(title=u"Test time")
    project = schema.TextLine(title=u"Project")
    epics = schema.List(title=u"Epic", value_type=schema.Object(schema=IEpic))

    def populate(input):
        """Populate from XML representation in the file-like object input
        """
    
    def serialize():
        """Return a serialisation of this catalogue as an lxml ElementTree
        """
    
    def write(output):
        """Write XML representation to the file-like object output
        """

# Fix schemata we can't set immediately due to circular dependencies
IStory['epic'].schema = IEpic
IScenario['story'].schema = IStory
