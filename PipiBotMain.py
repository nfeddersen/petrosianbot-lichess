import requests
import json
from stockfish import Stockfish
import random

stockfish = Stockfish('stockfish_20090216_x64_bmi2.exe', parameters={"Threads": 8, "Minimum Thinking Time": 300})
stockfish.set_depth(15)
stockfish.set_skill_level(25)

api_key = 'pUibzu9IEzv9niob'

headers = {'Authorization': f'Bearer {api_key}'}
game_state_url = 'https://lichess.org/api/stream/event'
game_id = 'placeholder'
is_checkmate = False
bot_challenges = False
gameOver = False
trushTalkURL = 'placeholder'
isChatline = False

trushTalkDict = {
    'trushTalk1': 'Are you kidding ??? What the **** are you talking about man ? You are a biggest looser i ever seen '
                  'in my life!',
    'trushTalk2': 'You was doing PIPI in your pampers when i was beating players much more stronger then you!',
    'trushTalk3': 'You are not proffesional, because proffesionals knew how to lose and congratulate opponents, '
                  'you are like a girl crying after i beat you! Be brave, be honest to yourself and stop this trush '
                  'talkings!!!',
    'trushTalk4': 'Everybody know that i am very good blitz player, i can win anyone in the world in '
                  'single game!',
    'trushTalk5': '"w"esley "s"o is nobody for me, just a player who are crying every single time when '
                  'loosing, ( remember what you say about Firouzja ) !!!',
    'trushTalk6': 'Stop playing with my name, i deserve to have a good name during whole my chess '
                  'carrier, I am Officially inviting you to OTB blitz match with the Prize fund!',
    'trushTalk7': "Both of us will invest 5000$ and winner takes it all!",
    'trushTalk8': "I suggest all other people who's intrested in this situation, just take a look at my "
                  "results in 2016 and 2017 Blitz World championships!",
    'trushTalk9': 'No need to listen for every crying babe, Tigran Petrosyan is always play Fair !',
    'trushTalk10': 'And if someone will continue Officially talk about me like that, we will meet in Court!',
    'trushTalk11': 'God bless with true!',
    'trushTalk12': 'True will never die !',
    'trushTalk13': 'Liers will kicked off...'
    }

while True:
    state_session = requests.Session()
    request = state_session.get(game_state_url, headers=headers, stream=True)
    for line in request.iter_lines():
        if len(line) == 0:
            print('Request response is empty.')
        if len(line) != 0:
            if gameOver:
                print('\nThe game has concluded. Bot is now on standby.')
                gameOver = False
                break

            challenge_state_json = json.loads(line)
            if challenge_state_json['type'] == 'challenge':
                print('Tigran Petrosyan has been challenged.')

                challenge_id = challenge_state_json['challenge']['id']
                challenger = challenge_state_json['challenge']['challenger']['id']
                print('Challenge ID is: ' + challenge_id + '. Challenger is: ' + challenger)

                if challenge_state_json['challenge']['variant']['key'] != 'standard' or challenge_state_json['challenge']['speed'] == 'correspondence':
                    requests.post('https://lichess.org/api/challenge/' + challenge_id + '/decline', params={
                    },
                                  headers={
                                      'Authorization': f'Bearer {api_key}'
                                  })
                    print('Challenge has been declined for improper variant or time control.')
                    break

                else:
                    requests.post('https://lichess.org/api/challenge/' + challenge_id + '/accept', params={
                    },
                                  headers={
                                      'Authorization': f'Bearer {api_key}'
                                  })

            current_move = 'placeholder'
            best_move = 'placeholder'
            position = ['placeholder']
            black_position = ['placeholder']
            white = True

            second_session = requests.Session()
            request = second_session.get(game_state_url, headers=headers, stream=True)

            for line in request.iter_lines():
                game_start_json = json.loads(line)
                game_id = game_start_json['game']['id']
                trushTalkURL = 'https://lichess.org/api/bot/game/' + game_id + '/chat/'
                print('Game ID is: ' + game_id + '\n')
                break

            game_stream_url = 'https://lichess.org/api/bot/game/stream/' + game_id
            bot_move_url = 'https://lichess.org/api/bot/game/' + game_id + '/move/'

            s = requests.Session()
            r = s.get(game_stream_url, headers=headers, stream=True)

            i = 0
            move_count = 0

            for line in r.iter_lines():
                if isChatline:
                    isChatline = False

                if len(line) != 0:
                    isGameOverJSON = json.loads(line)
                    if 'status' in isGameOverJSON:
                        if isGameOverJSON['status'] != 'started':
                            gameOver = True
                            randInt = random.randint(1, 13)
                            requests.post(url=trushTalkURL, params={}, headers=headers, data={'room': 'player', 'text':
                               {trushTalkDict['trushTalk' + str(randInt)]}})
                            break

                    start_json = json.loads(line)
                    if start_json['type'] == 'chatLine':
                        isChatline = True

                    if not isChatline:
                        i = i + 1
                        move_count = move_count + .5
                        move_count = float(move_count)

                        if move_count.is_integer():
                            move_count = int(move_count)
                            move_count = str(move_count)
                            print('It is move ' + move_count + '.')
                            move_count = float(move_count)
                            randInt = random.randint(1, 26)
                            if randInt <= 13:
                                requests.post(url=trushTalkURL, params={}, headers=headers,
                                              data={'room': 'player', 'text':
                                                  {trushTalkDict['trushTalk' + str(randInt)]}})

                        if i == 1:
                            if start_json["white"]['id'] == "pipibot":
                                white = True
                                print('I am white.')
                            else:
                                white = False
                                print('I am black.')

                            if start_json['speed'] == 'bullet' and i == 1:
                                stockfish.set_depth(15)
                                stockfish.set_skill_level(20)
                            elif start_json['speed'] == 'blitz' and i == 1:
                                stockfish.set_depth(15)
                                stockfish.set_skill_level(25)
                            elif start_json['speed'] == 'rapid' and i == 1:
                                stockfish.set_depth(19)
                                stockfish.set_skill_level(30)
                            elif start_json['speed'] == 'classical' and i == 1:
                                stockfish.set_depth(20)
                                stockfish.set_skill_level(30)
                            elif start_json['speed'] == 'correspondence' and i == 1:
                                stockfish.set_depth(20)
                                stockfish.set_skill_level(30)

                        if white and i == 1:
                            position.clear()
                            stockfish.set_position()

                            best_move = 'e2e4'
                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })
                            best_move = str(best_move)
                            position.append(best_move)
                            stockfish.set_position(position)

                        if white and i == 3:
                            current_move = start_json["moves"]
                            current_move = str(current_move)
                            current_move = current_move.split()
                            current_move = current_move[-1]
                            position.append(current_move)

                            stockfish.set_position(position)

                            best_move = 'e1e2'
                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })
                            best_move = str(best_move)
                            position.append(best_move)
                            stockfish.set_position(position)

                        if white and i == 5:
                            current_move = start_json["moves"]
                            current_move = str(current_move)
                            current_move = current_move.split()
                            current_move = current_move[-1]
                            position.append(current_move)

                            stockfish.set_position(position)

                            best_move = 'e2e3'

                            if current_move == 'c8g4':
                                best_move = 'f2f3'
                            if current_move == 'd5d4':
                                best_move = 'g1f3'

                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })
                            best_move = str(best_move)
                            position.append(best_move)
                            stockfish.set_position(position)

                        if not white and i == 1:
                            print('I am waiting to move.')

                        if not white and i == 2:
                            black_position.clear()
                            current_move = start_json["moves"]
                            current_move = str(current_move)
                            current_move = current_move.split()
                            current_move = current_move[-1]
                            black_position.append(current_move)

                            stockfish.set_position(black_position)
                            best_move = 'e7e5'
                            black_position.append(best_move)

                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })

                        if not white and i == 4:
                            current_move = start_json["moves"]
                            current_move = str(current_move)
                            current_move = current_move.split()
                            current_move = current_move[-1]
                            black_position.append(current_move)

                            stockfish.set_position(black_position)
                            best_move = 'e8e7'
                            if current_move == 'd1h5':
                                best_move = 'd7d6'
                            if current_move == 'c1g5':
                                best_move = 'f7f6'

                            black_position.append(best_move)

                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })

                        if not white and i == 6:
                            current_move = start_json["moves"]
                            current_move = str(current_move)
                            current_move = current_move.split()
                            current_move = current_move[-1]
                            black_position.append(current_move)

                            stockfish.set_position(black_position)
                            best_move = 'e7e6'
                            print(black_position)

                            if current_move == 'c1g5' or current_move == 'd4d5':
                                best_move = 'f7f6'
                            if current_move == 'd1d5':
                                best_move = 'd7d6'
                            if current_move == 'e5c6':
                                best_move = 'd7c6'
                            if black_position[-2] == 'd7d6':
                                best_move = 'e8e7'
                            if current_move == 'f1c4':
                                best_move = stockfish.get_best_move()
                            if black_position[-2] == 'f7f6':
                                best_move = 'e8e7'


                            black_position.append(best_move)

                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })
                        if not white and i == 8 and black_position[-2] == 'e8e7':
                            current_move = start_json["moves"]
                            current_move = str(current_move)
                            current_move = current_move.split()
                            current_move = current_move[-1]
                            black_position.append(current_move)

                            best_move = 'e7e6'
                            black_position.append(best_move)

                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })

                    if not isChatline:
                        # If bot is white and first move has already been played
                        if white and not i % 2 == 0 and i > 5:
                            current_move = start_json["moves"]
                            current_move = str(current_move)
                            current_move = current_move.split()
                            current_move = current_move[-1]
                            position.append(current_move)

                            stockfish.set_position(position)
                            best_move = stockfish.get_best_move()
                            position.append(best_move)

                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })
                        # If bot is black and first move has been played
                        if not white and i % 2 == 0 and i > 6:
                            current_move = start_json["moves"]
                            current_move = str(current_move)
                            current_move = current_move.split()
                            current_move = current_move[-1]
                            black_position.append(current_move)

                            stockfish.set_position(black_position)
                            best_move = stockfish.get_best_move()
                            black_position.append(best_move)

                            requests.post(bot_move_url + best_move, params={
                            },
                                          headers={
                                              'Authorization': f'Bearer {api_key}'
                                          })

    continue
