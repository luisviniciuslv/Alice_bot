import copy
import json
import random

with open('./cogs/BBB/events.json', 'r', encoding='utf-8') as eve:
  events = json.load(eve)

class Game:
  def __init__(self, brothers):
    self.brothers = brothers
    self.current_brothers = brothers
    self.eliminate_brothers = []
    self.week = 1
    self.day = 1
    self.leader = None
    self.angel = None

  def next_week(self):
    self.week += 1
    self.day = 1

  def create_week_events(self):
    week_events = []
    brothers_without_events = self.current_brothers.copy()

    while len(brothers_without_events) > 0 and self.day <= 7:
      if self.day == 5:
        pass
      
      brothers = []
      brothers_avatar = []
      event = random.choice(events['week'])

      if event['brothers'] > len(brothers_without_events):
        continue

      for i in range(event['brothers']):
        brother = random.choice(brothers_without_events)
        brothers.append(brother)
        brothers_without_events.remove(brother)

        brothers_avatar.append(brother.avatar)

      day_event_text = event['event']

      for i in range(len(brothers)):
        day_event_text = day_event_text.replace(f'B{i+1}', brothers[i].name.split('#')[0].upper())

      week_events.append([day_event_text, brothers_avatar])

      self.day += 1

    self.next_week()
    return week_events


  def __repr__(self):
    return str(self.__dict__)