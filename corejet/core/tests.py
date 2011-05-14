import unittest2 as unittest
from corejet.core import story, scenario, given, when, then

@story(id="CTI-1", title="As a user I can log in to the System")
class LoginTest(unittest.TestCase):
    
    @given("there is a user 'joebloggs' with password 'password'")
    def userOnLoginPageAndAccountIsLocked(self):
        pass
    
    @scenario("User successful login")
    class LoginSuccess:
        
        @when("I try to log in with username 'joebloggs' and password 'password'")
        def enterCredentials(self):
            self.fail("yonk")
        
        @then("the system grants me access")
        def accessIsGranted(self):
            self.fail("yonk")
        
        @then("I am taken to a home page")
        def takenToHomePage(self):
            self.fail("yonk")

    @scenario("Failed login")
    class LoginPasswordFail:

        @when("I try to log in with username 'joebloggs' and password 'badpassword'")
        def enterBadCredentials(self):
            pass

        @then("the system does not grant me access")
        def accessNotGranted(self):
            self.fail("yonk")
        
        @then("I am taken back to the login page")
        def takenToLoginPage(self):
            pass
        
        @then("I am shown an error message indicating that my username or password was incorrect")
        def shownCredentialsErrorMessage(self):
            pass
    
    @scenario("Outage")
    class Outage:
        
        @given("the back end repository is not available")
        def backEndRepositoryOutage(self):
            pass
        
        @when("I try to log in with username 'joebloggs' and password 'password'")
        def enterCredentials(self):
            pass
        
        @then("I am shown an error")
        def shownError(self):
            pass
