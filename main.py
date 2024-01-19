from telethon import TelegramClient, events, Button
import asyncio
import os
# Set your API ID, API hash, and phone number with country code
api_id = ''#api id
api_hash = ''#api hash
phone_number = ''#mobile number with country code

# Define the list of main and temporary user IDs
main_ids = []#bot account id
temp_ids = []#sudo users 

# Create a new TelegramClient instance
client = TelegramClient('session_name', api_id, api_hash)

# Start the client
client.start(phone=phone_number)
print('Client started successfully!')

# Initialize the lists of sent, unsent, and failed groups
sent_groups = []
unsent_groups = []
failed_groups = []
spammer_running = False
# Define a global variable to keep track of whether the message sending is ac
async def send_text_multiple_times(text, amount, event):
    global spammer_running
    for i in range(amount):
        # Check if the spammer is still running
        if not spammer_running:
            break
        await event.respond(text)

# Register the command handler
@client.on(events.NewMessage(pattern='.spam (.*)', from_users=temp_ids))
async def handle_spam(event):
    global spammer_running
    print("Received message:", event.pattern_match.group(1))
    # Get the text and amount from the command message
    text, amount = event.pattern_match.group(1).rsplit(r'\n', 1)
    amount = int(amount)

    # Start spamming
    spammer_running = True
    await send_text_multiple_times(text, amount, event)

# Register the stop command handler
@client.on(events.NewMessage(pattern='.rest', from_users=temp_ids))
async def handle_stop(event):
    global spammer_running
    if spammer_running:
        spammer_running = False   
    else:
        await event.respond('No spamming running.', buttons=None)
      
# Listen for incoming messages
@client.on(events.NewMessage)
async def handle_message(event):
  try: 
        # Get the sender's user ID 
        sender_id = event.message.from_id.user_id
        if event.raw_text == '.ping':
                if sender_id in main_ids:
            # If the sender is in the main IDs list, edit the message
                  await event.edit('<code>I am active!</code>', parse_mode='html')
                elif sender_id in temp_ids:
            # If the sender is in the temporary IDs list, send a normal message
                  await event.respond('<code>I am active!</code>', parse_mode='html')
        else:
            # Ignore the message if the sender is not in either list
            pass
    # Ignore all other types of incoming message
       
        
        if event.raw_text.startswith('/set'):
            message = event.raw_text[5:].strip()
            if sender_id in main_ids:
              os.remove("time.txt")
              with open("time.txt", "a") as file: file.write(str(message))
              await client.edit_message(event.message,'<code>✅ Success!</code>', parse_mode='html')   
            
            elif sender_id in temp_ids:
              os.remove("time.txt")
              with open("time.txt", "a") as file: file.write(str(message))
              await event.respond('<code>✅ Success!</code>', parse_mode='html')   

            
      
        elif event.raw_text.startswith('/run'):
            os.remove("myfile.txt")
            message = event.raw_text[5:].strip()

            if not message:
                if sender_id in main_ids:
                    # If the sender is in the main IDs list, edit the message
                    await client.edit_message(event.message, '<b>Please provide a message to send.</b>\n\nSend The Text Like :- <code>/run message</code>', parse_mode='html')
                elif sender_id in temp_ids:
                    # If the sender is in the temporary IDs list, send a warning message
                    await event.respond('<b>Please provide a message to send.</b>\n\nSend The Text Like :- <code>/run message</code>', parse_mode='html')
                else:
                    # Ignore the message if the sender is not in either list
                    pass
            else:
                dialogs = await client.get_dialogs()
                groups = [d for d in dialogs if d.is_group]
                # Start sending the message every 10 seconds to all the target groups
                message_sending = True
                while message_sending:
                    for g in groups:
                        try:
                           if os.path.exists("myfile.txt"):
                             content = open('myfile.txt', 'r').read()
                             if str(content) != str("True"):
                               await client.send_message(g.id, message, disable_web_page_preview=True, parse_mode='html')                   
                               print(f"Sent message to group {g.title}")
                               sent_groups.append(g.id)
                             else:
                               print("Breaked")
                               message_sending = False
                               break;
                           else:
                             await client.send_message(g.id, message, parse_mode='html')                   
                             print(f"Sent message to group {g.title}")
                             sent_groups.append(g.id)
                        except Exception as e:
                            print(f"Failed to send message to group {g.title}: {e}")
                    failed_groups.append(g.id)
                    await asyncio.sleep(int(open('time.txt', 'r').read()))
                            

        elif event.raw_text == '/stop':
            if sender_id in main_ids or sender_id in temp_ids:
                # If the sender is in either list, send a confirmation message
                await event.respond('<code>The message sending has been stopped.</code>', parse_mode='html')
                # Stop the message sending loop
                message_sending = False
                with open("myfile.txt", "a") as file: file.write("True")
                print('stopping')
            else:
                # Ignore the message if the sender is not in either list
                pass
              
        
      
# If the sender is not in the main IDs list, send a warning message
      
                
                
        
        

  except Exception as e:
        print('Error:', e)

# Run the client
client.run_until_disconnected()
        
