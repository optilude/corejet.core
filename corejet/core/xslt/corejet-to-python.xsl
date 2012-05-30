<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="text" omit-xml-declaration="yes"/>
<xsl:strip-space elements="*"/>
<xsl:variable name="s" select="translate(number(boolean(count(//story) - 1)), '01', '1')"/>
<xsl:variable name="c" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
<xsl:template name="story-number">
  <xsl:value-of select="translate(position(), $s, '')"/>
</xsl:template>
<xsl:template name="scenario-letter">
  <xsl:value-of select="translate(number(boolean(count(parent::node()/scenario) - 1)), '10', substring($c, position(), 1))"/>
</xsl:template>
<xsl:template name="given-letter">
  <xsl:value-of select="translate(number(boolean(count(parent::node()/given) - 1)), '10', substring($c, position(), 1))"/>
</xsl:template>
<xsl:template name="when-letter">
  <xsl:value-of select="translate(number(boolean(count(parent::node()/when) - 1)), '10', substring($c, position(), 1))"/>
</xsl:template>
<xsl:template name="then-letter">
  <xsl:value-of select="translate(number(boolean(count(parent::node()/then) - 1)), '10', substring($c, position(), 1))"/>
</xsl:template>
<xsl:template match="//story">
<xsl:if test="position() &lt; 2">
# -*- coding: utf-8 -*-
import unittest2 as unittest
from corejet.core import Scenario, story, scenario, given, when, then

</xsl:if>
<xsl:if test="position() &gt; 1">
<xsl:text>
</xsl:text>
</xsl:if>
@story(id="<xsl:value-of select="@id"/>", title=u"<xsl:value-of select="@title"/>")
class Story<xsl:call-template name="story-number"/>(unittest.TestCase):
<xsl:for-each select="given">
    @given(u"<xsl:value-of select="text()"/>")
    def given<xsl:call-template name="given-letter"/>(self):
        pass
</xsl:for-each>
<xsl:for-each select="when">
    @when(u"<xsl:value-of select="text()"/>")
    def when<xsl:call-template name="when-letter"/>(self):
        pass
</xsl:for-each>
<xsl:for-each select="then">
    @then(u"<xsl:value-of select="text()"/>")
    def then<xsl:call-template name="then-letter"/>(self):
        self.assertTrue(False, u"This test needs to be finished.")
</xsl:for-each>
<xsl:apply-templates select="scenario"/>
</xsl:template>
<xsl:template match="scenario">
    @scenario(u"<xsl:value-of select="@name"/>")
    class Scenario<xsl:call-template name="scenario-letter"/>(Scenario):
<xsl:for-each select="given">
        @given(u"<xsl:value-of select="text()"/>")
        def given<xsl:call-template name="given-letter"/>(self):
            pass
</xsl:for-each>
<xsl:for-each select="when">
        @when(u"<xsl:value-of select="text()"/>")
        def when<xsl:call-template name="when-letter"/>(self):
            pass
</xsl:for-each>
<xsl:for-each select="then">
        @then(u"<xsl:value-of select="text()"/>")
        def then<xsl:call-template name="then-letter"/>(self):
            self.assertTrue(False, u"This test needs to be finished.")
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>
