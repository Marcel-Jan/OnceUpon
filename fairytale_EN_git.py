import random
import csv
import smtplib
import keyring
import logging
__author__ = 'Marcel-Jan Krijgsman'

logging.basicConfig(filename="fairytale_EN.log",
                    level=logging.DEBUG)

MAIL_USER = "fairytale@family.org"
MAIL_PASSWORD = keyring.get_password("mail", MAIL_USER)


def load_cards(card_file):
    card_list = []
    with open(card_file, 'r') as f:
        card_lines = f.readlines()
        for card_item in card_lines:

            # Append to cardList, stripping new line characters.
            card_list.append(card_item.strip())
    return card_list


# Determine number of cards to be dealt.
def find_number_of_cards (d_number_of_players):
    if d_number_of_players == 2:
        d_cards_per_player = 10
    elif d_number_of_players == 3:
        d_cards_per_player = 8
    elif d_number_of_players == 4:
        d_cards_per_player = 8
    elif d_number_of_players == 5:
        d_cards_per_player = 6
    elif d_number_of_players >= 6:
        d_cards_per_player = 5
    return d_cards_per_player


def mail_intro_cards(d_player, receiver, cards, d_happily_card):
    server = smtplib.SMTP('smtp.family.org', 587)
    login = MAIL_USER  # your login
    password = MAIL_PASSWORD  # your password

    server.login(MAIL_USER, MAIL_PASSWORD)
    sender = 'fairytale@family.org'
    receivers = receiver

    card_string = "\n ".join(cards)

    mail_subject = "Your Once Upon A Time cards are here"
    mail_body = f"""From: From Fairy Tale <fairytale@family.org>
    To: {receiver}
    
    Hello {d_player},

    Here are your Fairy Tale cards:
    
    {card_string}
    
    Use these topics in the fairy tale that you are telling.
    
    
    And this is your Happily Ever After card:
    \"{d_happily_card}\"
    
    This is how your fairy tale ends.
    
    
    Happy story telling!
    """
    message = 'Subject: {}\n\n{}'.format(mail_subject, mail_body)
    logging.debug(f'message = {message}')

    try:
        # send your message with credentials specified above
        server.sendmail(sender, receivers, message)
        logging.debug('Sent')
        print('Sent')
    except smtplib.SMTPServerDisconnected:
        logging.debug('Failed to connect to the server. Wrong user/password?')
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        logging.debug(f'SMTP error occurred: {str(e)}')
        print('SMTP error occurred: ' + str(e))


def mail_card(d_player, receiver, cards):
    server = smtplib.SMTP('smtp.family.org', 587)
    login = MAIL_USER  # your login
    password = MAIL_PASSWORD  # your password

    server.login(MAIL_USER, MAIL_PASSWORD)
    sender = 'fairytale@family.org'
    receivers = receiver

    card_string = "\n ".join(cards)

    mail_subject = "Here is another Once Upon A Time card"
    mail_body = f"""From: From Fairy Tale <fairytale@family.org>
    To: {receiver}

    Hello {d_player},

    You've got another Once Upon A Time card:

    {card_string}

    Happy story telling!
    """
    message = 'Subject: {}\n\n{}'.format(mail_subject, mail_body)
    logging.debug(f'Mail: {message}')
    # print(message)

    try:
        # send your message with credentials specified above
        server.sendmail(sender, receivers, message)
        logging.debug('Sent')
        print('Sent')
    except smtplib.SMTPServerDisconnected:
        logging.debug('Failed to connect to the server. Wrong user/password?')
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        logging.debug(f'SMTP error occurred: {str(e)}')
        print('SMTP error occurred: ' + str(e))


def deal_cards(card_stack, number_of_cards_to_deal):
    cards_dealt = random.sample(card_stack, number_of_cards_to_deal)

    # Remove cards from the stack. We're not dealing these again.
    for card_in_player_stack in cards_dealt:
        card_stack.remove(card_in_player_stack)
    # Return the remaining card stack and the cards dealt to the player
    return card_stack, cards_dealt


def deal_happily_card(d_remaining_happily_stack):
    # happily_card[player] = deal_happily_card(remaining_happily_stack)
    pick_happily_card = random.choice(remaining_happily_stack)
    remaining_happily_stack.remove(pick_happily_card)
    return d_remaining_happily_stack, pick_happily_card


def show_n_cards(player_cards):
    d_number_of_cards = len(player_cards)
    print(f'Number of cards: {d_number_of_cards}')
    logging.debug(f'Number of cards: {d_number_of_cards}')
    return d_number_of_cards


def play_card(d_dealt_cards, card_name):
    logging.debug(f'draw_card({d_dealt_cards}, {card_name})')
    logging.debug(f'card_name: {card_name}')
    # print(f'card_name: {card_name}')
    logging.debug(f'd_dealt_cards: {d_dealt_cards}')
    # print(f"d_dealt_cards: {d_dealt_cards}")
    search_result = [item for item in d_dealt_cards if card_name in item]
    # print(f"len(search_result): {len(search_result)}")
    if len(search_result) > 0:
        d_dealt_cards.remove(card_name)
        logging.debug(f'd_dealt_cards: {d_dealt_cards}')
        # print(f"d_dealt_cards: {d_dealt_cards}")
    else:
        print(f"{card_name} is not in the cards!")
        logging.debug(f'{card_name} is not in the cards!')
    if len(d_dealt_cards) == 0:
        print("We have a winner!!")
        logging.debug('We have a winner!!')
    return d_dealt_cards


def draw_card(d_player, d_dealt_cards, d_remaining_card_stack):
    logging.debug(f'draw_card({d_player}, {d_dealt_cards}, {d_remaining_card_stack})')
    # Pick random card from stack
    # print(f'd_dealt_cards: {d_dealt_cards}')
    logging.debug(f'd_dealt_cards: {d_dealt_cards}')
    pick_card = random.choice(d_remaining_card_stack)
    # print(f'pick_card: {pick_card}')
    logging.debug(f'pick_card: {pick_card}')
    # Add card to hand of player
    d_dealt_cards.append(pick_card)
    # print(f'd_dealt_cards: {d_dealt_cards}')
    logging.debug(f'd_dealt_cards: {d_dealt_cards}')
    # Remove cards from the stack. We're not dealing these again.
    logging.debug(f'Remove {pick_card} from {d_remaining_card_stack}')
    d_remaining_card_stack.remove(pick_card)
    # print(f'd_remaining_card_stack: {d_remaining_card_stack}')
    # mail_cards(d_player, receiver, cards)
    logging.debug(f'Mail {pick_card} to {d_player}. address {player_mail[d_player]}')
    mail_card(d_player, player_mail[d_player], pick_card)
    return d_dealt_cards, d_remaining_card_stack


def search_cards(d_dealt_cards, search_term):
    print(f'Search term: {search_term}')
    logging.debug(f'Search term: {search_term}')
    search_result = [item for item in d_dealt_cards if search_term in item]
    print(f'Search result: {search_result}')
    logging.debug(f'Search result: {search_result}')
    return search_result


logging.debug('Start of new game.')

# def game_loop():
# List of players. To be read from a csv later
player_csv = csv.reader(open('playerlist.csv'))

player_mail = {}
for player_row in player_csv:
    # Ignore header
    if player_row != ['Name', 'Mail']:
        player_key = player_row[0]
        player_mail[player_key] = player_row[1:]

# print(player_mail)
# print(player_mail.keys())
player_list = []
for player in player_mail.keys():
    player_list.append(player)

print(f'player_list: {player_list}')
logging.debug(f'player_list: {player_list}')

# player_list = ["Bart", "Lisa", "Maggie", "Homer", "Marge", "Grampa", "Flanders"]
number_of_players = len(player_list)

# Load regular Once Upon A Time cards
card_file = "onceupon_cards_EN.txt"
card_list = load_cards(card_file)
remaining_card_stack = card_list.copy()
print(f"Number of Once Upon a Time cards: {len(remaining_card_stack)}")
logging.debug(f'Number of Once Upon a Time cards: {len(remaining_card_stack)}')
print(f'player_list: {player_list}')
logging.debug(f'player_list: {player_list}')

# Load Happily Ever After cards
happily_file = "happilyeverafter_EN.txt"
happily_list = load_cards(happily_file)
remaining_happily_stack = happily_list.copy()
print(f'Number of Happily Ever After cards: {len(remaining_happily_stack)}')
logging.debug(f'Number of Happily Ever After cards: {len(remaining_happily_stack)}')

# Calculate number of Once Upon A Time cards per player
number_of_cards = find_number_of_cards(number_of_players)
print('number_of_cards: ' + str(number_of_cards))
logging.debug('number_of_cards: ' + str(number_of_cards))


dealt_cards = {}
happily_card = {}
for player in player_list:
    print('player: ' + player)
    logging.debug(f'player: {player}')
    # Deal cards for one player
    remaining_card_stack, dealt_cards[player] = deal_cards(remaining_card_stack, number_of_cards)
    # print(dealt_cards[player])
    logging.debug(f'card dealt: {dealt_cards[player]}')
    # remaining_happily_stack
    remaining_happily_stack, happily_card[player] = deal_happily_card(remaining_happily_stack)
    # print(f'happily_card[{player}]: {happily_card[player]}')
    logging.debug(f'happily_card[{player}]: {happily_card[player]}')

    mail_intro_cards(player, player_mail[player], dealt_cards[player], happily_card[player])

print(f'Number of Once Upon a Time cards left: {len(remaining_card_stack)}')
logging.debug(f'Number of Once Upon a Time cards: {len(remaining_card_stack)}')
print(f'Number of Happily Ever After cards left: {len(remaining_happily_stack)}')
logging.debug(f'Number of Happily Ever After cards: {len(remaining_happily_stack)}')

for player in player_list:
    print(f'{player} has {str(len(dealt_cards[player]))} cards left.')
    logging.debug(f'{player} has {str(len(dealt_cards[player]))} cards left.')




