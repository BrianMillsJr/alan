#!/usr/bin/env python
import nltk
import os
import re
from language import grammar, vocabulary
from senses import ears
import sys
from memory import context, store_memories
import environment.system

def listen():
  """
    Function to listen. Modes of listening should be added here.
    Could be listening to terminal or mic etc.

    Returns:
      String: Words input from the user.
  """
  print ""
  words = raw_input(">>> ").strip()
  if words == "alan" or words == "voice" or context.no_prompt:
    # Makes a call to the google voice api to get words from mic.
    print context.no_prompt
    speak("Yes")
    words = ears.ears()
  elif words.isdigit():
    words = int(words)
  return words

def think(words):
  """
    Function to generate some sort of response from the input passed in by listen().

    Args:
      words (String): Words taken in from the listen command.
    Returns:
      String: Returns a response for the given input.
  """
  if vocabulary.vocabulary_check(words):
    return vocabulary.response(words)
  else:
    return grammar.branch(words)


def speak(response):
  """
    Function to speak to the user. Text to speech based on the platform alan is running on.

    Args:
      response (String): The response generated by think().
    Returns:
      None
  """
  # Turn alan's talking context to true.
  context.talking = True

  # TODO: Mirror personal pronouns (you -> me, me-> you)

  # think() returns None if no suitable response is found.
  if not response:
    response = "I don't know how to respond to that."
  response = response.encode('ascii', 'ignore')
 
  #For mac os.
  if sys.platform == "darwin":
    command = 'echo \"{}\" | say '.format(response)
  else:
    # Requires festival on linux.
    command = 'echo \"{}\" | festival --tts'.format(response)
  os.system(command)
  
  # Alan is done talking. Set talking context to false.
  context.talking = False


if __name__ == "__main__":
  """
    Main method should load configurations for alan and initiate interaction loop.
  """
  ""
  # Look for SQLite DB. If not, create it
  if not store_memories.database_exists():
    store_memories.init_db()

  speak("Hello.")
  while True:
    if context.sleeping or context.talking:
      # Process inputs for WAKE_PHRASE, if it matches wake alan up.
      sleep_input = raw_input(">>>")
      print sleep_input
      if sleep_input == context.WAKE_PHRASE:
        context.sleeping = False
        speak("I'm awake now.")
      else:
        continue
    # Try to execute statement and catch an error. Exit on KeyboardInterrupt.
    try:
      speak(think(listen()))
    except KeyboardInterrupt:
      speak("Shutting down.")
      exit()
    except Exception,e:
      print e
      speak("Something went wrong. I can't do that right now.")
      exit()
