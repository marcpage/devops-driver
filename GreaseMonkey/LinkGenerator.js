// ==UserScript==
// @name         Link Generator
// @namespace    http://github.com/marcpage
// @version      0.0.4
// @description  Add a copy-link button to many sites that has Markdown and HTML formatted links
// @author       MarcAllenPage@gmail.com
// @homepageURL  https://github.com/marcpage/devops-driver/main/GreaseMonkey/README.md
// @updateURL    https://raw.githubusercontent.com/marcpage/devops-driver/main/GreaseMonkey/LinkGenerator.js
// @downloadURL  https://raw.githubusercontent.com/marcpage/devops-driver/main/GreaseMonkey/LinkGenerator.js
// @supportURL   https://github.com/marcpage/devops-driver/issues
// @license      Unlicense; https://opensource.org/license/unlicense/
// @match        https://*.atlassian.com/*
// @match        https://*.atlassian.net/*
// @match        https://dev.azure.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=atlassian.com
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';
    const clipboardIcon = "📋";
    const checkmarkIcon = "✅︎";
    const failureIcon = "❌";
    const plainCheckmarkIcon = "✔";
    const buttonId = "generated_link_button";
    const checkmarkDurationInSeconds = 0.500;
    const secondsBetweenAttempts = 1.0;
    const maximumNumberOfAttempts = 3;

    // =============== Templates ===============

    const MarkdownFormat = "[{{id}}]({{url}}): {{name}}";
    const HtmlFormat = "<a href='{{url}}' target='_blank'>{{id}}</a>: {{name}}";
    const PlainFormat = "{{id}}: {{name}}";

    /**
    * Fills in a template string.
    * @summary Replaces "{{name}}" in a template string with the given mapping value.
    * @param {string} template - The template to start with.
    * @param {object} mappings - Mapping of template name to replacement value.
    * @return {string} The final string.
    */
    function fillInTemplate(template, mappings) {
        return template.replaceAll("{{id}}", mappings.id)
            .replaceAll("{{name}}", mappings.name)
            .replaceAll("{{url}}", mappings.url);
    }

    // =============== Parsers ===============

    /**
    * Gets a sub-element with the given id, or `undefined` if it cannot.
    * @summary Prevents errors by allowing for missing id or even undefined element.
    * @param {DOMElement} element - The element to search on (may be `document`)
    * @param {string} id - The id of the element to find
    * @return {DOMElement} The element with the id under element
    *                           or undefined if not found or element is undefined.
    */
    function getIded(element, id) {
        if (!element) {
            return undefined;
        }

        return element.getElementById(id);
    }

    /**
    * Gets a tag of the given type.
    * @summary Gets the nth tag of the given type.
    * @param {DOMElement} element - The element to search on (may be `document`)
    * @param {string} tagname - The type of tag to search for
    * @param {int} index - Which element to return if multiple (defaults to first)
    * @return {DOMElement} The found element or undefined if element is undefined or no match is found
    */
    function getTag(element, tagname, index=0) {
        var elements = element ? element.getElementsByTagName(tagname) : undefined;

        if (elements && elements.length > index) {
            return elements[index];
        }

        return undefined;

    }
    /**
    * Get a tag that has an attribute with the given string in it.
    * @summary Given a type of tag, searches for tags of that type that have an attribute that contains the given string.
    * @param {DOMElement} element - The element to search on (may be `document`)
    * @param {string} tagname - The type of tag to search for
    * @param {string} attribute - The attribute to check
    * @param {string} contains - The value that should be in the attribute
    * @param {int} index - Which element to return if multiple (defaults to first)
    * @return {DOMElement} The found element or undefined if element is undefined or no match is found
    */
    function getAttributed(element, tagname, attribute, contains, index=0) {
        var elements = element ? element.getElementsByTagName(tagname) : undefined;
        var elements_with_attribute = (elements
                                     ? [...elements].filter(
                                        e => e.getAttribute(attribute)
                                          && e.getAttribute(attribute).includes(contains))
                                     : undefined);

        if (elements_with_attribute && elements_with_attribute.length > index) {
            return elements_with_attribute[index];
        }

        return undefined;
    }

    /**
    * Get the parent element.
    * @summary Safe method to get the parent element
    * @param {DOMElement} element - The element to search on (may be `document`)
    * @return {DOMElement} The found element or undefined if element is undefined or no match is found
    */
    function getParent(element) {
        return element ? element.parentNode : undefined;
    }

    /**
    * Get the value of the given attribute
    * @summary Safely gets the value of the attribute or undefined
    * @param {DOMElement} element - The element to search on (may be `document`)
    * @param {string} attribute - The name of the attribute to get
    * @return {string} Returns the value of the attribute or undefined if element is undefined
    */
    function getAttribute(element, attribute) {
        return element ? element.getAttribute(attribute) : undefined;
    }

    /**
    * Get the innerText of the element
    * @summary Get the innerText or undefined if element is undefined
    * @param {DOMElement} element - The element to search on (may be `document`)
    * @return {string} The innerText or undefined if element is undefined
    */
    function getText(element) {
        return element ? element.innerText : undefined;
    }

    /**
    * Get the value of an input element
    * @summary Get the value or undefined if element is undefined
    * @param {DOMElement} element - The input element to search on (may be `document`)
    * @return {string} The value or undefined if element is undefined
    */
    function getValue(element) {
        return element ? element.value : undefined;
    }

    /**
    * Is the info valid and can be used to create the text
    * @summary Checks if the info is valid and can be converted to text
    * @param {object} info - Object with name, id, and url fields, or undefined
    * @return {boolean} True if info is an object and name, id, and url are all not undefined
    */
    function valid_info(info) {
        if (!info) {
            console.log("Unable to get any info to build link to copy");
        } else if(!(info.name && info.id && info.url)) {
            console.log("Missing information: name="+info.name+" id="+info.id+" url="+info.url);
        }
        return info && info.name && info.id && info.url;
    }

    /**
     * Decriptions of how to navigate various pages
     * @summary Handle different ways to determine the location to
     *              insert the button and how to get the text to copy
     */
    const parsers = [
        {// test site: https://jira.atlassian.com/browse/JSWSERVER-25888
            "name": "Jira version 1",
            "location": function() {return getParent(getTag(getIded(document, "stalker"), "li"));},
            "info": function() {return {
                "name": getText(getIded(document, "summary-val")),
                "id": getAttribute(getIded(document, "key-val"), "data-issue-key"),
                "url": getAttribute(getIded(document, "key-val"), "href"),
            }}
        },
        {
            "name": "Jira version 2",
            "location": function() {return getParent(getTag(getIded(document, "jira-issue-header"), "li"));},
            "info": function() {return {
                "name": getText(getAttributed(document, "h1", "data-testid", "issue.views.issue-base.foundation.summary.heading")),
                "id": getText(getTag(getAttributed(document, "a", "data-testid", "issue.views.issue-base.foundation.breadcrumbs.current-issue.item"), "span")),
                "url": getAttribute(getAttributed(document, "a", "data-testid", "issue.views.issue-base.foundation.breadcrumbs.current-issue.item"), "href"),
            }}
        },
        {
            "name": "Azure DevOps",
            "location": function() {return getAttributed(getIded(document, "skip-to-main-content"), "div", "class", "info-text-wrapper");},
            "info": function() {return {
                "name": getValue(getAttributed(getIded(document, "skip-to-main-content"), "input", "aria-label", "Title Field")),
                "id": getText(getAttributed(getIded(document, "skip-to-main-content"), "span", "aria-label", "ID Field")),
                "url": getAttribute(getTag(getAttributed(getIded(document, "skip-to-main-content"), "div", "class", "workitem-info-bar"), "a"), "href"),
            }}
        },
    ];

    /**
    * Determine which parser is successful at reading the page
    * @summary Walk through `parsers` and find a fit for this page
    * @return {object} Object with fields location {string} and info {function}
    */
    function getParser() {
        for (var i = 0; i < parsers.length; ++i) {
            var location = parsers[i].location();

            if (location) {
                console.log("Parser found: " + parsers[i].name);
                return {"location": location, "info": parsers[i].info};
            }
        }

        return undefined;
    }

    // =============== Mechanism ===============

    /**
    * Flash a given character (emoji) in the button
    * @summary Replaces the clipboard icon with the given character and schedule a refresh of the clipboard
    * @param {string} icon - The emoji to flash in the button
    */
    function flashIcon(icon) {
      document.getElementById(buttonId).innerText = icon;
      setTimeout( function(){
          document.getElementById(buttonId).innerText = clipboardIcon;
      }, checkmarkDurationInSeconds * 1000);
    }

    /**
    * Create the text and put it on the clipboard
    * @summary Creates the various clipboard texts and pushes to the clipboard
    * @param {object} pageInfo - The name, url, and id to turn into text
    * @param {string} htmlTemplate - The template for the rich text
    * @param {string} markdownTemplate - The template for plain text
    * @param {string} icon - The emoji to display for success
    */
    function copyDescriptionToClipboard(pageInfo, htmlTemplate, markdownTemplate, icon) {
        if (!valid_info(pageInfo)) {
            flashIcon(failureIcon);
            return;
        }

        const plainText = fillInTemplate(markdownTemplate, pageInfo);
        const richText = fillInTemplate(htmlTemplate, pageInfo);
        const richTextType = "text/html";
        const plainTextType = "text/plain";
        const htmlBlob = new Blob([richText], { type: richTextType });
        const markdownBlob = new Blob([plainText], {type: plainTextType});
        const data = [new ClipboardItem({
            [richTextType]: htmlBlob,
            [plainTextType]: markdownBlob,
        })];

        navigator.clipboard.write(data).then(
            () => {// Success
                flashIcon(icon);
            },
            () => {
                flashIcon(failureIcon);
            },
        );
    }

    /**
    * Insert the button into the web page
    * @summary Attempts to insert the button into the page. THis function is recursive.
    * @param {int} attempt - The attempt we are on. Defaults to 1.
    */
    function insertButton(attempt=1) {
        var page_type = getParser();

        if (!page_type) {
          if (attempt < maximumNumberOfAttempts) {
            setTimeout( function(){
              insertButton(attempt + 1);
            }, secondsBetweenAttempts * 1000);
          }

          return;
        }

        var button = document.createElement("button");

        button.innerText = clipboardIcon;
        button.id = buttonId;
        button.onclick = function(event) {
            copyDescriptionToClipboard(page_type.info(), HtmlFormat,
                event.shiftKey ? PlainFormat : MarkdownFormat,
                event.shiftKey ? plainCheckmarkIcon : checkmarkIcon);
        }
        page_type.location.appendChild(button);
    }

    insertButton();

})();