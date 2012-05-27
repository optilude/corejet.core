CoreJet
=======

CoreJet is a Behaviour Driven Testing specification and approach, with
implementations in Python and Java. See http://corejet.org for more details.

This package provides core CoreJet functionality in Python. You will probably
also be interested in `corejet.testrunner` and possibly `corejet.jira`_.

Why not Cucumber?
-----------------

There are various packages that implement a similar style of BDD testing in
Python, usually based on `Cucumber`_. CoreJet has one important philosophical
difference: Instead of writing stories and scenarios in plain text files,
they are intended to be managed as part of a requirements management system
such as JIRA (hence `corejet.jira`_). This manages epics, stories and
scenarios, as well as the lifecycle and metadata surrounding requirements:
whether they are open or closed, how big (in story points) they are, and how
valuable they are to business users (priority).

A "requirements catalogue source" extracts them from this system into either
an intermediary XML format (see below) or directly into the CoreJet data
model (again, see below). The test runner (`corejet.testrunner`_) first
fetches the current requirements catalogue, then executes all CoreJet tests,
matching up stories (by id) and scenarios (by name) and setting the status
of each to either "pass", "fail", "pending" (not yet implemented) or
"mismatch" (a given/when/then step in a scenario is out of sync with the
requirements management system).

The output of this analysis is written to an augmented CoreJet XML file. This
is then used to generate a visualisation of the state of the project (see
`corejet.visualization`_), with colour coding to indicate how much of the
project is in fact complete, where "complete" means it has passing automated
tests that accurately represent the business' acceptance criteria.

Installation
============

You can install ``corejet.core`` as a dependency of your package, e.g. in
``setup.py`` adding::

    install_requires=['corejet.core']

or, if you prefer to keep your tests in an extra::

    extras_require = {'test': ['corejet.core']}

Note however that ``corejet.core`` relies on the `lxml`_ library. This is
sometimes a bit tricky to install on OS X and older Linux platforms. If you
are using Buildout to install your packages, you may want to use
``z3c.recipe.lxml`` to install ``lxml``: Add ``lxml`` as the *first* item
in your ``parts`` list and then add this section::

    [lxml]
    recipe = z3c.recipe.staticlxml
    egg = lxml

Test syntax
===========

To write CoreJet tests in Python, you can use the decorators found in this
package in combination with ``unittest`` style test cases. To do this, you
should depend on ``corejet.core`` in your own package (or at least in its
list of test dependencies), and probably also ``unittest2`` if working in
Python 2.6 or earlier.

Here is an example::

    import unittest2 as unittest
    from corejet.core import Scenario, story, scenario, given, when, then

    @story(id="S1", title="As a user, I can log in")
    class Login(unittest.TestCase):

        @scenario("Invalid username")
        class InvalidUsername(Scenario):

            @given("A user 'joebloggs' with password 'secret'")
            def setupUser(self):
                # Some precondition logic, e.g.
                createUser('jobloggs', 'secret')

            @when("Entering the username 'jobloggs' and password 'secret'")
            def attemptLogin(self):
                # Call some action logic, e.g.
                loginAs('jobloggs', 'secret')

            @then("An error is shown")
            def checkOutput(self):
                # Perform some assertion, e.g.
                errorMessages = getErrorMessages()
                self.assertTrue("Invalid username" in errorMessages)

        @scenario("Invalid password")
        class InvalidPassword(Scenario):

            @given("A user 'joebloggs' with password 'secret'")
            def setupUser(self):
                # Some precondition logic, e.g.
                createUser('jobloggs', 'secret')

            @when("Entering the username 'joebloggs' and password 'uhoh'")
            def attemptLogin(self):
                # Call some action logic, e.g.
                loginAs('joebloggs', 'uhph')

            @then("An error is shown")
            def checkOutput(self):
                # Perform some assertion, e.g.
                errorMessages = getErrorMessages()
                self.assertTrue("Invalid password" in errorMessages)

You can have as many or as few scenarios as you want. The ``Scenario`` base
class provides access to an attribute ``self.story``, which is an instance of
the outer ``@story``-annotated test case class. This allows access to shared
attributes or state. You can also use standard ``unittest `` conventions like
``setUp()`` and ``tearDown()`` on the outer class (but not on the ``Scenario``
classes) to manage your test fixtures.

In fact, at runtime, each inner scenario class is turned into a standard
method on the outer story class with the name ``test_<ScenarioName>()``,
which, when called, will call each of the ``@given``-annotated methods in the
inner class, then each of the ``@when``-annotated methods, then each of the
``@then``-annotated methods.

The reason for this trick is to ensure standard test collectors work. In fact,
a CoreJet test should work with any standard testrunner that can execute
``unittest`` tests.

Of course, the main reason to use CoreJet is to generate a report of completed
functional coverage. To do this, you can use the test runner in
`corejet.testrunner`_ combined with a requirements catalogue source. See that
package for details.

Data model
==========

The standard CoreJet data model is represented in this package in the
module ``corejet.core.model``, and described by the interfaces in
``corejet.core.interfaces``. There main class is the
``RequirementsCatalogue``, which contains a list of ``Epic`` object, which in
turn contain a list of ``Story`` objects, which in turn contain a list of
``Scenario`` objects, which in turn contain three lists (given, when and then)
of ``Step`` objects.

See the documentation in the source for more details.

XML parsing and serialization
-----------------------------

The ``RequirementsCatalog`` class provides methods ``populate()`` and
``write()``, which can read and write, respectively, a standard CoreJet XML
file  to initialise or serialise the catalogue.

Here is an example file for the one story and and two scenarios above,
contained in a fictitious epic::

    <requirementscatalogue project="Acme Corp" extractTime="2011-05-15T19:00:00">
      <epic id="E1" title="User management">
        <story id="S1" title="As a user, I can log in" requirementStatus="closed" resolution="fixed" priority="high">
          <scenario name="Invalid username">
            <given>A user 'joebloggs' with password 'secret'</given>
            <when>Entering the username 'jobloggs' and password 'secret'</when>
            <then>An error is shown</then>
          </scenario>
          <scenario name="Invalid password">
            <given>A user 'joebloggs' with password 'secret'</given>
            <when>Entering the username 'joebloggs' and password 'uhoh'</when>
            <then>An error is shown</then>
          </scenario>
        </story>
      </epic>
    </requirementscatalogue>

Scenario parser
===============

Scenarios are often written in "Gherkin" syntax (as per the Cucumber
framework, form which CoreJet is partly inspired).

Scenarios can be written in plain text like so::

    Scenario: Invalid username
    Given A user 'joebloggs' with password 'secret'
    When Entering the username 'jobloggs' and password 'secret'
    Then An error is shown

    Scenario: Invalid password
    Given A user 'joebloggs' with password 'secret'
    When Entering the username 'joebloggs' and password 'uhoh'
    Then An error is shown

    Scenario: Cancel button
    Given A user 'joebloggs' with password 'secret'
    When Entering the username 'joebloggs' and password 'uhoh'
     And Clicking the 'cancel' button
    Then The user is taken away from the page
     And A warning is shown

Scenarios may be preceded by a background description composed of one or more
"Given" clauses affecting every scenario::

    Given I'm logged in
     And I've got superuser privileges

    Scenario: ...

In addition, there is basic support for "Scenario Outline" with "Examples".

The full Gherkin syntax is more involved, but to parse this simplified style
of scenarios and append them to a story, you can use the function
``corejet.core.parser.appendScenarios``. It takes a ``Story`` and a string
containing the acceptance criteria text as its two arguments.

The parser is relatively forgiving, but note:

 * The parser is case-insensitive
 * Zero or more scenarios may be present
 * Scenarios must start with "Scenario: " followed by a name
 * The "Given" clause is optional, but must come first in a scenario
 * The "When" clause is required, and must come before the "Then" clause
 * The "Then"" clause is also required
 * An "And" or "But" clause can come after any "Given", "When" or "Then", but
   not first.

Generating test skeletons
=========================

``corejet.core`` ships with an XSLT stylesheet for generating test skeletons
for Python unittest. If you are using buildout, you can install a helper
script for executing the XSLT-transformation with::

    [corejet2py]
    recipe = zc.recipe.rgg
    eggs = corejet.core
    scripts = corejet2py

And execute it with::

    bin/corejet2py path/to/corejet.xml

Try ``bin/corejet2py --help`` for more information.

.. _corejet.recipe.testrunner: http://pypi.python.org/pypi/corejet.recipe.testrunner
.. _corejet.testrunner: http://pypi.python.org/pypi/corejet.testrunner
.. _corejet.jira: http://pypi.python.org/pypi/corejet.jira
.. _corejet.visualization: http://pypi.python.org/pypi/corejet.visualization
.. _lxml: http://lxml.de
.. _Cucumber: http://cukes.info
