# Closet Santa Messaging Bot
A bot to manage semi-anonymous messaging through Reddit for the Closet Santa gift exchange.

## How to use
To send messages through the bot, simply click one of the supplied links. A new message will be made with the proper formatting, so all you have to do is type your desired message after `Message:` and the bot will do the rest. Any and all markdown in your message will be retained.

## Reporting
Obviously, we don't need people abusing the anonymous messaging system, so all messages are archived to the hard drive of the bot's computer. The Report links work just like the messaging ones, except they will send a copy of the entire message to the /r/ClosetSanta mods for review. A `Reason:` field is provided for you to comment on why you are reporting the message.

## A Message on How the Bot Works and How Long a Message May Take to Send
The bot will refresh, by default, once every 120 seconds. It will download every new message it recieved in that timespan, then begin sorting through the messages. For every message, the bot will pause for 1 second before moving onto the next message to ensure that each message gets a unique ID (this pause time is in addition to the idle time from the bot analyzing the message). Therefore, depending on the traffic and internet speeds, your message may take anywhere from less than two minutes up to possibly 5-10 minutes to send.

As an example, let's say that the messaging traffic is extremely high, and the bot refreshes to find 250 new messages waiting to be delivered. Let's assume that, on average, each message takes 0.5 seconds to analyze, have the appropriate response message made, and deliver replies. Since the bot sleeps for 1 second, that puts us at 1.5 seconds / message, and at 250 messages, that's 375 seconds for the whole inbox to be cleared, or just over 6 minutes. Then, since the bot ran for more than it's default 2 minute sleep, it immediately checks its inbox again, and we start over. This is a fairly extreme case, but it's just to illustrate the potential of messages getting backed up.

In any case, the last thing the bot does before moving on to the next message is to send you a message back, so when you receive a confirmation message from the bot, you know that your message has just been sent.
