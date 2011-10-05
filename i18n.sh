#!/bin/bash
i18ndude rebuild-pot --pot corejet/core/locales/gherkin.pot --create gherkin corejet/core

sed -i -e 's/\\/\\\\/g' corejet/core/locales/gherkin.pot

i18ndude sync --pot corejet/core/locales/gherkin.pot corejet/core/locales/*/LC_MESSAGES/gherkin.po

msgfmt corejet/core/locales/en/LC_MESSAGES/gherkin.po -o corejet/core/locales/en/LC_MESSAGES/gherkin.mo
msgfmt corejet/core/locales/fi/LC_MESSAGES/gherkin.po -o corejet/core/locales/fi/LC_MESSAGES/gherkin.mo

