# Link Generator

This GreaseMonkey script injects a "copy-link" button into certain web pages.

Currently supported pages:
- Jira tickets

## Install

You will need to install a GreaseMonkey browser plugin.
The recommended GreaseMonkey plugin is [ViolentMonkey](https://violentmonkey.github.io).

Once the plugin is installed, go to the Dashboard and click the plus `+` button.
Copy the contents of `LinkGenerator.js` into a new script.

You will need to reload any pages currently open to get the button to show up.
A button with a clipboard icon (📋) will show up near the top. 
Click that button to copy the text to the clipboard.

If you paste the link into a rich text context (like an email, PowerPoint, Word document, etc), if will be formatted correctly.
If you paste the link into a plain text context (notepad, command line, etc) it will be formatted in Markdown.