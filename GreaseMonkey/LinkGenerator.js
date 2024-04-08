// ==UserScript==
// @name         Link Generator
// @namespace    http://github.com/marcpage
// @version      0.0.3
// @description  Add a copy-link button to many sites that has Markdown and HTML formatted links
// @author       MarcAllenPage@gmail.com
// @homepageURL  https://github.com/marcpage/devops-driver/main/GreaseMonkey/README.md
// @updateURL    https://raw.githubusercontent.com/marcpage/devops-driver/main/GreaseMonkey/LinkGenerator.js
// @downloadURL  https://raw.githubusercontent.com/marcpage/devops-driver/main/GreaseMonkey/LinkGenerator.js
// @supportURL   https://github.com/marcpage/devops-driver/issues
// @license      Unlicense; https://opensource.org/license/unlicense/
// @match        https://*.atlassian.com/*
// @match        https://*.atlassian.net/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=atlassian.com
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';
    const clipboardIcon = "📋";
    const checkmarkIcon = "✅︎";
    const plainCheckmarkIcon = "✔";
    const buttonId = "generated_link_button";
    const checkmarkDurationInSeconds = 0.500;

    // =============== Templates ===============
    const MarkdownFormat = "[{{id}}]({{url}}): {{name}}";
    const HtmlFormat = "<a href='{{url}}' target='_blank'>{{id}}</a>: {{name}}";
    const PlainFormat = "{{id}}: {{name}}";

    function fillInTemplate(template, mappings) {
        return template.replaceAll("{{id}}", mappings.id)
            .replaceAll("{{name}}", mappings.name)
            .replaceAll("{{url}}", mappings.url);
    }

    // =============== Jira ===============
    function getJiraInfo() {
        // <h1 id="summary-val">Browser extensions for capturing webpages to Trello Cards</h1>
        // <a class="issue-link" data-issue-key="TRELLO-168" href="/browse/TRELLO-168" id="key-val" rel="2007610">TRELLO-168</a>
        var title_container = document.getElementById("summary-val");
        var identifier_link = document.getElementById("key-val");
        var title = title_container ? title_container.innerText : title_container;
        var identifier = (identifier_link 
                            ? identifier_link.getAttribute("data-issue-key") 
                            : identifier_link);
        var link = (identifier_link 
                    ? new URL(identifier_link.getAttribute("href"), window.location) 
                    : identifier_link);

        if (title && identifier && link) {
            return {"name": title, "id": identifier, "url": link};
        }
        
        return undefined;
    }

    // =============== Mechanism ===============
    function copyDescriptionToClipboard(pageInfo, htmlTemplate, markdownTemplate, icon) {
        if (!pageInfo) {
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
                document.getElementById(buttonId).innerText = icon;
                setTimeout ( function(){
                    document.getElementById(buttonId).innerText = clipboardIcon;
                }, checkmarkDurationInSeconds * 1000);
            },
            () => {
                alert("Unable to set the clipboard")
            },
        );
    }

    function insertJiraWidget() {
        // Breadcrumbs section is something like:
        //  <ol class="... breadcrumbs ...">
        var container = Array.from(document.getElementsByTagName("ol"))
                            .filter(o => o.className.includes("breadcrumbs"));

        var lastBreadCrumb = container[container.length - 1]; // last breadcrumb
        var button = document.createElement("button");

        button.innerText = clipboardIcon;
        button.id = buttonId;
        button.onclick = function(event) {
            copyDescriptionToClipboard(getJiraInfo(), HtmlFormat, 
                event.shiftKey ? PlainFormat : MarkdownFormat, 
                event.shiftKey ? plainCheckmarkIcon : checkmarkIcon);
        }
        lastBreadCrumb.appendChild(button); // add button to end of last breadcrumb
    }

    // test site: https://jira.atlassian.com/browse/JSWSERVER-25888
    insertJiraWidget();

})();