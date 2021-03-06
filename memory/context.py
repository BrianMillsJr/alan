from short_term import Memory
"""
  This file is used to pass around Alan's memory and other global values.
  For example, context.short_term_memory will return the same object everywhere
  inside alan. Add references to global data structures and classes here.
"""
short_term_memory = Memory()

# Boolean to store alan's current sleep state. Default is False.
sleeping = False

# Boolean to store alan's talking state. Set and unset in alan.speak(). Default to False.
talking = False

# Constant phrase to wake alan from sleep state. Needs to match a phrase in keyphrase.list if opearating in passive mode.
WAKE_PHRASE = "wake up"

# This is a list of running background services, the "stop" command will use this to kill processes.
services = []

# Stop alan from prompting, defaults to false
no_prompt = False

