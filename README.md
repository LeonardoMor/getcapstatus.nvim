# getcapstatus.nvim
This plugin provides a function that returns true if Caps lock is on and false otherwise.

#Thoughts
- `capswatchdog` is going to be a client. It will watch the status of the Caps lock key. When that status changes, it will send a message to the server indicating the new status.
- The server on the NeoVim side, will be listening for updates. When an update arrives, the new value will be saved into a global variable that holds the Caps lock status and that makes it available to anything on NeoVim. The function reads this global variable and and return true or false accordingly.
