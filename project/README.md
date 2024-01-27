# Copy Histories Chrome Extension

#### Video Demo: [https://youtu.be/RbAA5gSGCWc](https://youtu.be/RbAA5gSGCWc)

## Description

The Copy Histories Chrome Extension is designed to streamline your browsing experience by keeping track of your copy history within the browser. Picture yourself working across multiple tabs, repeatedly copying text from one tab and pasting it into another. It can be tedious and time-consuming to switch between tabs each time you need to access previously copied text. This extension aims to eliminate that inconvenience by allowing you to save and manage your copy history effortlessly.

### Features:

#### Copy History Storage:
- The extension utilizes the `chrome.storage.local` API to locally store a history of your copied text.
- It intelligently limits the copy history to the latest 20 entries, ensuring efficiency and performance.

#### User Interface:
- A user-friendly popup interface displays a list of your copied texts, providing easy access and management.
- Each entry in the list offers options to copy the text again or delete it from the history, giving you control over your stored data.

#### Keyboard Shortcut:
- Accessing the extension is made convenient with the "Alt+C" keyboard shortcut, allowing quick and seamless interaction.

#### Copy Event Listener:
- The content script (`content.js`) actively listens for copy events on web pages, ensuring that your copy history stays up-to-date.

#### Copy and Delete Actions:
- Users can effortlessly copy a text from the history by clicking on the copy icon or text. The popup window will automatically close after copying.
- Unwanted entries can be removed from the history with a simple click on the delete icon.

#### Bootstrap and Icons Integration:
- Stylish and visually appealing, the extension incorporates Bootstrap for seamless styling and includes Bootstrap icons for an enhanced user interface.

#### Popup Positioning:
- Leveraging display information, the extension intelligently positions the popup window at the center of the screen, ensuring a visually pleasing and accessible experience.

### Execution:

- The extension operates in the background (`background.js`), efficiently managing storage and handling messages.
- The content script (`content.js`) actively listens for copy events on web pages, ensuring real-time updates.
- The popup (`popup.html`, `popup.js`, and `popup.css`) provides a well-designed user interface for managing your copy history.

### Skills and Research:

- The development of this extension involved in-depth research into Chrome extension development and the Chrome extension APIs.
- Understanding the intricacies of handling and storing data locally using `chrome.storage.local`.
- Proficiency in event handling within content scripts.
- Skillful use of Bootstrap for styling, coupled with the integration of icons for an enhanced user interface.
