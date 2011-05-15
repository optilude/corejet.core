class Scenario(object):
    """Base class for scenarios.
    
    Serves two purpose: sets a ``story`` attribute on construction, and
    provides assert* type test methods.
    """
    
    def __init__(self, story):
        self.story = story
    
    # Hack! We want the assert methods, but inheriting from unittest.TestCase
    # does weird things to test discovery
    
    def __getattr__(self, name):
        return getattr(self.story, name)
