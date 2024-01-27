# Copy Histories Chrome Extension

#### Video Demo:  [https://youtu.be/RbAA5gSGCWc](https://youtu.be/RbAA5gSGCWc)

#### Description

This project is help you to save your copy-history on your browser. Imagine you work on many tabs on browser, so you need to copy same text from another tabs to another tabs again and again by switching tabs so it is really annoying for you during working. When you want to use the text that you have ever copied before, you need to find and switch to the old tab to copy that text again. So I create this project to help you to save your copy history and you can use your text without spending time to go back to the old place for searching the your last copied text.

## Features:

### Copy History Storage:
- The extension stores the copied text history locally using the `chrome.storage.local` API.
- It limits the copy history to the latest 20 entries.

### User Interface:
- The extension has a popup interface that displays a list of copied texts.
- Each entry in the list has options to copy the text again or delete it from the history.

### Keyboard Shortcut:
- Users can open the extension using the keyboard shortcut "Alt+C."

### Copy Event Listener:
- The content script (`content.js`) listens for the copy event on web pages and sends the copied text to the background script.

### Copy and Delete Actions:
- The extension allows users to copy a text from the history again by clicking on the copy icon or text. The window will auto close after copy.
- Users can delete entries from the history by clicking on the delete icon.

### Bootstrap and Icons Integration:
- The extension uses Bootstrap for styling and includes Bootstrap icons for the UI.

### Popup Positioning:
- The extension uses information about the display to position the popup window at the center of the screen.

## Execution:

- The extension runs in the background (`background.js`) to manage storage and handle messages.
- The content script (`content.js`) listens for copy events on web pages.
- The popup (`popup.html`, `popup.js`, and `popup.css`) provides the user interface.

## Skills and Research:

- I need to be research with Chrome extension development and the Chrome extension APIs.
- Understanding how to handle and store data locally using chrome.storage.local.
- Knowledge of event handling in content scripts.
- Styling using Bootstrap and integrating icons.
