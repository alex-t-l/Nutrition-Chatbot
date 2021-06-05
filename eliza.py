#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
#  eliza.py
#
#  a cheezy little Eliza knock-off by Joe Strout
#  with some updates by Jeff Epler
#  hacked into a module and updated by Jez Higgins
#----------------------------------------------------------------------

import string
import re
import random

class Eliza:
  name = "" # 1. Name
  gender = "" # 2. Gender
  weight = -1 # 3. Weight
  age = -1 # 4. Age
  ffoodexists = False
  ffood = " ... I don't know" # 5. Favorite Food
  fdrinkexists = False
  fdrink = " ... I don't know" # 6. Favorite Drink
  macro = {"c" : 0, "f" : 0, "p" : 0}# 7. Most curious Macronutrient
  meals = -1 # 8. Meals a day
  fl = "" # 9. Fitness Level
  cs = 2000 # 10. Calorie Surplus
  def __init__(self):
    self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE), gPats))
    self.values = list(map(lambda x: x[1], gPats))
    

  #----------------------------------------------------------------------
  # translate: take a string, replace any words found in vocabulary.keys()
  #  with the corresponding vocabulary.values()
  #----------------------------------------------------------------------
  def translate(self, text, vocabulary):
    words = text.lower().split()
    keys = vocabulary.keys();
    for i in range(0, len(words)):
      if words[i] in keys:
        words[i] = vocabulary[words[i]]
    return ' '.join(words)


  #----------------------------------------------------------------------
  #  respond: take a string, a set of regexps, and a corresponding
  #    set of response lists; find a match, and return a randomly
  #    chosen response from the corresponding list.
  #----------------------------------------------------------------------
  def respond(self, text):
    # find a match among keys
    for i in range(0, len(self.keys)):
      match = self.keys[i].match(text)
      if match:
        # found a match ... stuff with corresponding value
        # chosen randomly from among the available options
        resp = random.choice(self.values[i])
        # we've got a response... stuff in reflected text where indicated
        pos = resp.find('%')
        while pos > -1:
          num = int(resp[pos+1:pos+2])
          resp = resp[:pos] + \
            self.translate(match.group(num), gReflections) + \
            resp[pos+2:]
          pos = resp.find('%')
        # fix munged punctuation at the end
        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        return resp
    return None

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#    into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i'd"  : "you would",
  "i've"  : "you have",
  "i'll"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you've": "I have",
  "you'll": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "me",
  "carbohydrates": "carbs",
  "amino acids" : "protein",
  "triglyceride" : "fat",
  "vitamin b3" : "niacin",
  "vitamin b1" : "thiamine"
}

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#  two-element list; the first is a regexp, and the second is a
#  list of possible responses, with group-macros labelled as
#  %1, %2, etc.
#----------------------------------------------------------------------

gPats = [
  [r'(.*)gender(.*)',["You identify as "]],
  [r'(.*)name(.*)',["Nice to meet you "]],
  [r'(.*)weight(.*)',["Your weight is "]],
  [r'(.*)age(.*)',["You are "]],
  [r'(.*)favorite food(.*)',["Your favorite food is "]],
  [r'(.*)favorite drink(.*)',["Your favorite drink is "]],
  [r'(.*)fitness level(.*)',["Your fitness level is "]],
  [r'(.*)meals a day(.*)',["You eat "]],
  [r'(.*)calorie surplus(.*)',["Your calorie surplus is "]],
  [r'(.*)Tell me what you know about me(.*)',["This is what I know about you:"]],
  
[r'(.*)how much fat(.*)',
  [  "Fat is part of a well balanced diet and should be eaten in moderation, trans fat should be avoided, and saturated fats should be heavily moderated or cut out.", "Men should aim for 30-38 grams of fiber a day while women should aim for 21 to 25 grams of fiber per day."
  ]],

  [r'(.*)how much carbs(.*)',
  [  "Carbs should make up 45 to 65 percent of your total daily calories, so if you eat " + str(Eliza.cs) + " calories a day, " + " you should aim for " + str(Eliza.cs * .45) + " to " + str((Eliza.cs * .65)) + " calories of your calorie surplus to be in carbs."
  ]],

  [r'(.*)how much protein(.*)',
  [  "You should consume 0.8 grams if protein per kilogram of bodyweight, or 0.36 grams per pound at the minimum.", "If you're looking to increase muscle mass, you should eat at least 0.5 to 0.8 grams of protein a day."
  ]],

 [r'(.*)how much sugar(.*)',
  [   "Try to limit your sugar intake, especially added sugar.",
    "The recommended daily intake of added sugar is no more than 24 grams of sugar for women, 36 grams of sugar for men."]],
  
  [r'(.*)calcium(.*)',
  [  "I'd recommend drinking 3 cups of milk a day.",
    "Cheese is a good source of Calcium."
  ]],  

   [r'(.*)vitamin e(.*)',
  [  "Vegetable oils such as what germ, suinflower, soybean pack a punch of Vitamin E.",
    "Pumpkins and red bell pappers are some nutrient rich vegetables- including being a good source of Vitamin E!",
    "Almonds and nuts have lots of Vitamin E. Easy to prepare and eat!"
  ]], 

  [r'(.*)vitamin k(.*)',
  [  "Kale, spinach, turnip greens, and other green vegetables are full of Vitamin K. That's why you should eat your veggies!",
    "Brussel sprouts, broccolli, cauliflower pack a load of Vitamin K. Don't like the way it tastes? Try boiling it and seasoning or mixing it with other tasty foods!"
  ]], 
  
  [r'(.*)vitamin b6(.*)',
  [  "Salmon has so many vitamins, including B6!",
    "Lean chicken breast has 1.6mg of B6 in each 6 ounces. It also tastes great!",
    "Avocadoes and Potatoes are two vegatables that are high in B6."
  ]], 

  [r'(.*)vitamin b12(.*)',
  [  "Meat, eggs, and anything milk is a great source for Vitamin B12."
  ]], 

  [r'(.*)biotin(.*)',
  [  "You can find biotin in chocolate, cereal, egg yolks, or milk!"
  ]], 
  
  [r'(.*)folate(.*)',
  [  "Asparagus and broccoli has plenty of folate.",
    "Beets and lentils have quite a bit of folate."
  ]],

  [r'(.*)niacin(.*)',
  [  "Need Niacin? Go for avocados, eggs, enriched breads, lean meats, and nuts!."
  ]],

  [r'(.*)pantothenic acid(.*)',
  [  "Avocados, broccoli, poultry, and white/sweet potatoes have pantothenic acid."
  ]],
  
  [r'(.*)thiamine(.*)',
  [  "Dried milk, eggs, enriched breads, lean meats, nuts/seeds, and peas have thiamine."
  ]],
  

  [r'(.*)vitamin a(.*)',
  [  "Beef/Lamb livers are rich in Vitamin A.",
    "Carrots and Papayas are two healthy options full of Vitamin A.",
    "Mangoes or peaches are the way to go!",
    "Sweet potatoes are delicious and full of Vitamin A."
  ]], 

  [r'(.*)vitamin d(.*)',
  [  "Looking for Vitamin D? Go with something fishy and oily...such as salmon, sardines, or mackarel!",
    "Egg yolks pack a punch when it comes to Vitamin D."
  ]], 

  [r'(.*)vitamin c(.*)',
  [   "Orange Juice is a great source of Vitamin C.",
    "Anything citrus will give you a good amount of Vitamin C~"
  ]],

  [r'(.*)iron(.*)',
  [   "You'll find plenty of iron in pretty much any red meat.",
    "Lentils are a tasty legume and is high in iron."
  ]],

   [r'(.*)zinc(.*)',
  [   "Go with meats, shellfish, and legumes for your source of zinc!"
  ]],
  
   [r'(.*)carbs(.*)',
  [   "Vegetables, quinoa, barley, legumes, potatoes, whole grains, are examples of whole carbs you should eat in a healthy diet.", "Fruits and vegetables will do the trick to stay fit", "White rice and oats if you want to bulk."
  ]],

     [r'(.*)protein(.*)',
  [   "Whole eggs, chicken breast, cottage cheese, greek yogurt, lean beef, tuna are some examples of good meats for protein." , "If you want to go plant based for proteins, eat chickpeas, tofu, soy, nuts, beans, and edemame.", "Protein powder is not a bad option if you want to bulk."
  ]],

 [r'(.*)fat(.*)',
  [   "You want to aim to eat good fats. Avocados, Nuts, Olive Oil, are some examples.", "Some surprisingly nutritious sources of fats include cheese, dark chocolate, fatty fish, and whole eggs."
  ]],


 [r'(.*)fiber(.*)',
  [   "Ah yes... fiber, the gut cleaner. Beans, broccoli, berries, avocados, and whole grains will do the trick.", "A fun way to eat fiber is with popcorn, this is a fun snack food as well, dried fruits, potatoes, and nuts are fiber-y as well."
  ]],

  [r'(.*)what should i eat?(.*)',
  [   "Lets eat Pho! Good source of carbs and protein.", "Lets go for a supergreen salad! I like a mid-day vitamin boost!", 
      "How about a bowl of rice and chicken? Basic, lean, and delicious.", "How about an egg salad sandwich"
  ]],

  [r'(.*)hello(.*)',
  [  "Hello... I'm glad you could show up today. Feel free to ask about your macros and micros!",
    "Hi there... how are you and your nutrition today??",
    "Hello, how are you healthy are you feeling today?"]],


  [r'(.*)food(.*)',
  [   "Lets eat Pho! Good source of carbs and protein.", "Lets go for a supergreen salad! I like a mid-day vitamin boost!", 
      "How about a bowl of rice and chicken? Basic, lean, and delicious.", "How about an egg salad sandwich?"
  ]],
  
  [r'(.*)thanks(.*)',
  [   "No problem!"
  ]],

  [r'(.*)yum(.*)',
  [   "Delicious! And nutritious..."
  ]],
  
  [r'(.*)what are the macros?(.*)',
  [   "The macronutrients are Carbohydrates, Fats, and Proteins. These are typically measured in grams!"
  ]],

  [r'(.*)what are the micros?(.*)',
  [   "The micronutrients are calcium, folate, iron, vitamin B6, vitamin B12, vitamin C, vitamin E, zinc, and much more. Most people don't use a micronutrient approach when dieting due to their small size and difficulty to measure."
  ]],

  [r'(.*)should I eat(.*)',
  [  "Think about what %1 contains. Is it a good time to eat %1?",
    "Think about how you usually feel after you eat %1. You are what you eat!",
    "Sit back and think about how you felt when you ate %1. Do you want your body to feel that way again?" ]],

  [r'(.*)should I drink(.*)',
  [  "Think about what %1 contains. Is it a good time to drink some %1?",
    "Think about how you usually feel after you drink %1. Is it worth it to drink %1?",
    "Sit back and think about how you felt when you drank %1. Do you want your body to feel that way again?" ]],

    [r'(.*)why do i need protein (.*)',
  [  "Every cell in your body contains protein. It is needed to help and repair your cells to create new ones~" ]],

    [r'(.*)why do i need carbs(.*)',
  [  "Carbohydrates are your body's main source of energy- which fuels your brain, kidney, heart muscles, and more! Keep getting that bread~" ]],

  [r'(.*)why do i need fat(.*)',
  [  "Your body needs a small amount of fat because they have essential fatty acids which absorb vitamins. These fats can't be made by the body and have to be from an outside source!" ]],

  [r'(.*)why do i need micronutrients(.*)',
  [  "You need a small amount micros because your body can't produce vitamins and minerals on its own...it must be obtained from your food/drinks/or supplements." ]],
  
  [r'(.*)diet(.*)',
  [  "A keto diet is low in carbs and high in fat. It's good for lowering blood sugar/insulin levels, and shifts metabolism  towards fats/ketones. Some foods in keto includes oils, fresh greens, and meat cuts.",
    'The Paleo diet/caveman diet includes lean meats, fish, fruits, vegetables, nuts and seeds. Basically any food that can be hunted and gathered.',
    'The Mediterranean diet has plenty of fruits, vegetables, nuts, seeds, legumes, tubers, whole grains, fish, and seafood. Its good for reducing heart disease risk.',
    'A vegan diet eliminates all meats and animal products. Its great for losing weight but lacks some nutrients typically from meat such as iron or vitamin b12.']],
    
      [r'(.*)feeling(.*)',
  [  "What did you eat to make you feel %1?.",
    "Think about what you consumed to feel %1?",
    "Food directly changes your mood! What you ate today is why you feel %1!"]],

  [r' (.*)you(.*)',
  [  "We should be discussing you and what you eat, not me.",
    "Why do you say that about me? I am simply a machine!",
    "Why do you care whether I %1?"]],

   [r'(.*)\?',
   [  "May I can suggest you something to eat?",
    "Why don't we talk about what you last ate?",
     "Are you interested in learning about other diet types??",
    "Maybe you want to ask about what foods have Vitamin B6?"]],

  [r'(.*)quit(.*)',
  [  "It was great talking to you. Eat well out there!",
    "Goodbye and good luck on your nutritional journey!.",
    "Thank you for talking to Eliza today!"]],



  # [r'Why don\'?t you ([^\?]*)\??',
  # [  "Do you really think I don't %1?",
  #   "Perhaps eventually I will %1.",
  #   "Do you really want me to %1?"]],

  # [r'Why can\'?t I ([^\?]*)\??',
  # [  "Do you think you should be able to %1?",
  #   "If you could %1, what would you do?",
  #   "I don't know -- why can't you %1?",
  #   "Have you really tried?"]],

  # [r'I can\'?t (.*)',
  # [  "How do you know you can't %1?",
  #   "Perhaps you could %1 if you tried.",
  #   "What would it take for you to %1?"]],

  # [r'I am (.*)',
  # [  "Did you come to me because you are %1?",
  #   "How long have you been %1?",
  #   "How do you feel about being %1?"]],

  # [r'I\'?m (.*)',
  # [  "How does being %1 make you feel?",
  #   "Do you enjoy being %1?",
  #   "Why do you tell me you're %1?",
  #   "Why do you think you're %1?"]],

  # [r'Are you ([^\?]*)\??',
  # [  "Why does it matter whether I am %1?",
  #   "Would you prefer it if I were not %1?",
  #   "Perhaps you believe I am %1.",
  #   "I may be %1 -- what do you think?"]],

  # [r'What (.*)',
  # [  "Why do you ask?",
  #   "How would an answer to that help you?",
  #   "What do you think?"]],

  # [r'How (.*)',
  # [  "How do you suppose?",
  #   "Perhaps you can answer your own question.",
  #   "What is it you're really asking?"]],

  # [r'Because (.*)',
  # [  "Is that the real reason?",
  #   "What other reasons come to mind?",
  #   "Does that reason apply to anything else?",
  #   "If %1, what else must be true?"]],

  # [r'(.*) sorry (.*)',
  # [  "There are many times when no apology is needed.",
  #   "What feelings do you have when you apologize?"]],

  # [r'Hello(.*)',
  # [  "Hello... I'm glad you could drop by today.",
  #   "Hi there... how are you today?",
  #   "Hello, how are you feeling today?"]],

  # [r'I think (.*)',
  # [  "Do you doubt %1?",
  #   "Do you really think so?",
  #   "But you're not sure %1?"]],

  # [r'(.*) friend (.*)',
  # [  "Tell me more about your friends.",
  #   "When you think of a friend, what comes to mind?",
  #   "Why don't you tell me about a childhood friend?"]],

  # [r'Yes',
  # [  "You seem quite sure.",
  #   "OK, but can you elaborate a bit?"]],

  # [r'(.*) computer(.*)',
  # [  "Are you really talking about me?",
  #   "Does it seem strange to talk to a computer?",
  #   "How do computers make you feel?",
  #   "Do you feel threatened by computers?"]],

  # [r'Is it (.*)',
  # [  "Do you think it is %1?",
  #   "Perhaps it's %1 -- what do you think?",
  #   "If it were %1, what would you do?",
  #   "It could well be that %1."]],

  # [r'It is (.*)',
  # [  "You seem very certain.",
  #   "If I told you that it probably isn't %1, what would you feel?"]],

  # [r'Can you ([^\?]*)\??',
  # [  "What makes you think I can't %1?",
  #   "If I could %1, then what?",
  #   "Why do you ask if I can %1?"]],

  # [r'Can I ([^\?]*)\??',
  # [  "Perhaps you don't want to %1.",
  #   "Do you want to be able to %1?",
  #   "If you could %1, would you?"]],

  # [r'You are (.*)',
  # [  "Why do you think I am %1?",
  #   "Does it please you to think that I'm %1?",
  #   "Perhaps you would like me to be %1.",
  #   "Perhaps you're really talking about yourself?"]],

  # [r'You\'?re (.*)',
  # [  "Why do you say I am %1?",
  #   "Why do you think I am %1?",
  #   "Are we talking about you, or me?"]],

  # [r'I don\'?t (.*)',
  # [  "Don't you really %1?",
  #   "Why don't you %1?",
  #   "Do you want to %1?"]],

  # [r'I feel (.*)',
  # [  "Good, tell me more about these feelings.",
  #   "Do you often feel %1?",
  #   "When do you usually feel %1?",
  #   "When you feel %1, what do you do?"]],

  # [r'I have (.*)',
  # [  "Why do you tell me that you've %1?",
  #   "Have you really %1?",
  #   "Now that you have %1, what will you do next?"]],

  # [r'I would (.*)',
  # [  "Could you explain why you would %1?",
  #   "Why would you %1?",
  #   "Who else knows that you would %1?"]],

  # [r'Is there (.*)',
  # [  "Do you think there is %1?",
  #   "It's likely that there is %1.",
  #   "Would you like there to be %1?"]],

  # [r'My (.*)',
  # [  "I see, your %1.",
  #   "Why do you say that your %1?",
  #   "When your %1, how do you feel?"]],

  # [r'You (.*)',
  # [  "We should be discussing you, not me.",
  #   "Why do you say that about me?",
  #   "Why do you care whether I %1?"]],

  # [r'Why (.*)',
  # [  "Why don't you tell me the reason why %1?",
  #   "Why do you think %1?" ]],

  # [r'I want (.*)',
  # [  "What would it mean to you if you got %1?",
  #   "Why do you want %1?",
  #   "What would you do if you got %1?",
  #   "If you got %1, then what would you do?"]],

  # [r'(.*) mother(.*)',
  # [  "Tell me more about your mother.",
  #   "What was your relationship with your mother like?",
  #   "How do you feel about your mother?",
  #   "How does this relate to your feelings today?",
  #   "Good family relations are important."]],

  # [r'(.*) father(.*)',
  # [  "Tell me more about your father.",
  #   "How did your father make you feel?",
  #   "How do you feel about your father?",
  #   "Does your relationship with your father relate to your feelings today?",
  #   "Do you have trouble showing affection with your family?"]],

  # [r'(.*) child(.*)',
  # [  "Did you have close friends as a child?",
  #   "What is your favorite childhood memory?",
  #   "Do you remember any dreams or nightmares from childhood?",
  #   "Did the other children sometimes tease you?",
  #   "How do you think your childhood experiences relate to your feelings today?"]],

  # [r'(.*)\?',
  # [  "Why do you ask that?",
  #   "Please consider whether you can answer your own question.",
  #   "Perhaps the answer lies within yourself?",
  #   "Why don't you tell me?"]],

  # [r'quit',
  # [  "Thank you for talking with me.",
  #   "Good-bye.",
  #   "Thank you, that will be $150.  Have a good day!"]],

  # [r'(.*)',
  # [  "Please tell me more.",
  #   "Let's change focus a bit... Tell me about your family.",
  #   "Can you elaborate on that?",
  #   "Why do you say that %1?",
  #   "I see.",
  #   "Very interesting.",
  #   "%1.",
  #   "I see.  And what does that tell you?",
  #   "How does that make you feel?",
  #   "How do you feel when you say that?"]],

  [r'(.*)',
  [  "What does %1 mean?",
     "Maybe you need more carbs!",
     "I hope you're eating healthy!",
     "You're acting like you skipped a meal!"]]]

def modifyGender():
  if Eliza.gender == "":
    print("I do not know your gender. What do you identify as?")
    i = input()
    Eliza.gender = i
  return "You are a " + str(Eliza.gender) + " I will remember this."
  print("You currently identify as a " + str(Eliza.gender) + ". What do you want to change it to?")
  i = input()
  Eliza.gender = i
  return str(Eliza.gender) + " I will remember this."

def modifyName():
  if Eliza.name != "":
    return str(Eliza.name) + "."
  print("Please tell me your name.")
  i = input()
  Eliza.name = i
  return str(Eliza.name) + "."

def modifyWeight():
  if Eliza.weight == -1:
    print("I want to know your weight, enter it now.")
    i = input()
    Eliza.weight = i
    return str(Eliza.weight) + " pounds. Thank you for telling me."
  return str(Eliza.weight) + ". You already told me."

def modifyAge():
  if Eliza.age != -1:
    return str(Eliza.age) + "."
  print("Please tell me your age..")
  i = input()
  Eliza.age = i
  return str(Eliza.age) + "."
                  
def favFood():
  if Eliza.ffoodexists:
    return str(Eliza.ffood + ".")
  print("What is your favorite food?")
  i = input()
  Eliza.ffood = i
  Eliza.ffoodexists = True
  return str(Eliza.ffood + ".")

  
def favFood():
    if Eliza.ffoodexists:
      return str(Eliza.ffood + ".")
    print("What is your favorite food?")
    i = input()
    Eliza.ffood = i
    Eliza.ffoodexists = True
    return str(Eliza.ffood + ".")

def favDrink():
  if Eliza.fdrinkexists:
      return str(Eliza.fdrink + ".")
  if Eliza.fdrink != " ... I don't know":
    return str(Eliza.age) + "."
  print("What is your favorite drink?")
  i = input()
  Eliza.fdrink = i
  Eliza.fdrinkexists = True
  return str(Eliza.fdrink + ".")
  

def modifyMeals():
  if Eliza.meals != -1:
    return str(Eliza.meals) + "."
  print("Please tell me how many meals you eat a day..")
  i = input()
  Eliza.meals = i
  return str(Eliza.meals) + " meals a day."
  
def fitnessLevel():
  if Eliza.fl != "":
    return str(Eliza.fl) + "."
  print("What is your fitness level?")
  i = input()
  Eliza.fl = i
  return str(Eliza.fl + ".")

def calorieSurplus():
  print("What is your calorie surplus? (How many calories do you eat on average in a day? default is 2000.)")
  i = input()
  Eliza.cs = i
  return str(Eliza.cs + " calories a day.")

def compute(res, s):
  if "(.*)carb(.*)" in res.lower() or "(.*)carb(.*)" in s.lower():
    Eliza.macro["c"] += 1
  if "(.*)fat(.*)" in res.lower() or "(.*)fat(.*)" in s.lower():
    Eliza.macro["f"] += 1
  if "(.*)protein(.*)" in res.lower() or "(.*)protein(.*)" in s.lower():
    Eliza.macro["p"] += 1

#  Most curious macro
def maxMacro():
  max_key = max(Eliza.macro,  key = Eliza.macro.get)
  if max_key == "c":
    return "carbohydrates"
  if max_key == "f":
    return "fats"
  if max_key == "p":
    return "proteins"
  return "???" # Shouldn't get here

def memory():
  print("Your name is " + Eliza.name + ".") if Eliza.name != "" else print("I don't know your name")
  print("You identify as a " + Eliza.gender + ".") if Eliza.gender != "" else print("I don't know your gender.")
  print("You weigh " + str(Eliza.weight) + "lbs.") if Eliza.weight != -1 else print("I don't know how much you weigh.")
  print("You are " + str(Eliza.age) + " years old.") if Eliza.age != -1 else print("I don't know your age.")
  print("Your favorite food is " + Eliza.ffood + " .") if Eliza.ffoodexists else print("I don't know your favorite food because you never told me.")
  print("Your favorite beverage is " + Eliza.fdrink + ".") if Eliza.fdrinkexists else print("I don't know your favorite drink because you never told me.")  
  print("The macronutrient you are most curious about is " + maxMacro() + ".")
  print("You eat " + Eliza.meals + " meals per day.") if Eliza.meals != -1 else print("I don't know how many meals you eat a day because you never told me.")
  print("Your fitness level is " + Eliza.fl + ".") if Eliza.fl != "" else print("I don't know your fitness level because you never told me.")
  print("Your calorie surplus is about " + str(Eliza.cs) + " calories per day.") if Eliza.cs != 2000 else print("I assume your calorie surplus is 2000 calories per day on average, since you have told me what your exact surplus is.")
  return ""
#---------------------------------------------------------------------- 
#  command_interface
#----------------------------------------------------------------------
def command_interface():
  print('Macro/Micro Suggestor\n---------')
  print('Talk to the program by typing in plain English. Use lower-case letters for micronutrient and macronutrients.')
  print('Enter Tell me what you know about me when you are done.')
  print('='*72)
  print('Hello. What macro/micro do you want to know more of? Or maybe need something to eat?')

  s = ''
  macroman = Eliza();
  while s != 'quit':
    try:
      s = input('> ')
    except EOFError:
      s = 'quit'
    print(s)
    while s[-1] in '!.':
      s = s[:-1]
    res = macroman.respond(s)
    if res == "You identify as ":
      res += modifyGender()
    elif res == "Your weight is ":
      res += modifyWeight()
    elif res == "Nice to meet you ":
      res += modifyName()
    elif res == "You are ":
      res += modifyAge()
    elif res == "Your favorite food is ":
      res += favFood()
    elif res == "Your favorite drink is ":
      res += favDrink()
    elif res == "Your fitness level is ":
      res += fitnessLevel()
    elif res == "Your calorie surplus is ":
      res += calorieSurplus()
    elif res == "You eat ":
      res += modifyMeals()
    elif res == "This is what I know about you:":
      memory()
      res = ""
    
    compute(res, s)
    print(res)
      



if __name__ == "__main__":
  command_interface()


