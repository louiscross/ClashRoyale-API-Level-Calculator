
# Clash Royale Level 16 Progression Calculator

This tool uses the official Clash Royale API to simulate card upgrades from your real collection and estimate how much gold and XP you need to reach your next King Level (or a target level). It also shows your maximum achievable King Level with your current cards and optional Wild Cards, plus an upgrade path breakdown.

Built with Python 3.9 and the Clash Royale API:

Python 3.9: https://www.python.org/downloads/release/python-390/
Clash Royale API: https://developer.clashroyale.com/#/
<img width="1087" height="741" alt="image" src="https://github.com/user-attachments/assets/e50c339d-390c-4a37-a5db-ac0017e7089d" />



## How to compile and run

- Firstly you will need python 3.9 installed, as well as the requests library.

you can install the requests library by using the command:

    pip install requests

on the command line.

- Then run ClashRoyaleUI.py to login

<img width="1067" height="378" alt="image" src="https://github.com/user-attachments/assets/9b55ea02-f277-4a64-9005-cb0f5849ac66" />


apart from this, there are two pieces of data you need to find in order to use the tool fully: 

- The first is a valid token from your [Clash Royale developer account](https://developer.clashroyale.com/#/).
  
If you do not have an account create one for free, and once created follow through to [your account](https://developer.clashroyale.com/#/account) and create a key.
( use https://api.ipify.org/ to find ip to whitelist )

- The second is your Clash Royale Player tag

Which you can find from your profile in game




## Description

This is a simple tool to help you calculate how far you are from your next level or next king tower level and the maximum capabilities of your account. The logic of this tool is relatively straight forward:

You use clashroyale's API to gather data from your account. Namely your current level, experience toard next level as well as all of the cards you currently hold, the levels which they are and the amount of each card.

We then sort these cards from its level ascending and take turns upgrading them. If the card doesnt have enough to be upgraded it is discarded. If the card is max level it is discarded. Once a card is upgraded. The account and card details will be updated to reflect this change and the loop will continue until either the desired level is reached or you run out of cards to upgrade.

Unfortunately the API only provides cards and card amounts as well as basic account info, it cannot show you gold on the account of magic items, so these we will have to enter manually.

The tool does not require you to make use of the magic items function, as forcing this would be annoying to those who want to save specific items. however if used it will aim to make the most efficient choices when consuming.

By default the tool aims to show you the maximum possible level of your account given its current state, however you can also use this to check the cost needed for individual levels
<img width="249" height="95" alt="image" src="https://github.com/user-attachments/assets/7689e0d6-0ff3-43f1-8fce-248129eb6419" />


By using your real gold amount you will find out your maximum possible level given the amount of cards your account has, however you can choose to use an arbitrary high coin value to see what level you could reach given 

<img width="745" height="504" alt="image" src="https://github.com/user-attachments/assets/3897d5a8-63b2-4c39-84e4-901f60be8244" />



## Motivation

Why did i make this? I have been playing the game for abit of time with friends and always seemed to wonder how long it would take to reach certain milestones, i went to google for this exact tool but to my suprise, out of all of the services between the wiki and fan made sites there seems to be nothing out there to solve this problem. This suprised me so i decided to put something together to solve this as im sure i am not the only person wanting to find out how far away i am to leveling up.


   




