import sys

import selenium ; sys.dont_write_bytecode = True

from environs import Env

from stockfish import Stockfish

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from Logger import logger

import time

class ChessBot:
    def __init__(self) -> None:
        env = Env()
        env.read_env()

        self.__username  = env.str('USERNAME')
        self.__password  = env.str('PASSWORD')
        self.__stockfish = env.str('STOCKFISH')
        self.__run_count = env.int('RUN_COUNT')

        self.__thread_count = env.int('THREAD_COUNT')
        self.__depth  = env.int('DEPTH')

        if self.__stockfish == "": 
            self.__stockfish = None

        logger.info("The configuration seems valid")

        self.__drivers = webdriver.Firefox()
        logger.info("Firefox driver loaded")

    def getStockfish(self) -> str or None:
        return self.__stockfish

    def getThreadCount(self) -> int:
        return self.__thread_count

    def getDepth(self) -> int:
        return self.__depth

    def getRunCount(self) -> int:
        return self.__run_count

    def login(self) -> None:
        logger.info("Logging in...")
        self.__drivers.get('https://www.chess.com/login')
        while True:
            try:
                bottom_banner = EC.presence_of_element_located((By.CLASS_NAME, 'bottom-banner-close'))
                WebDriverWait(self.__drivers, 1).until(bottom_banner)
                break
            except: pass

        self.__drivers.find_element(By.CLASS_NAME, 'bottom-banner-close').click()

        self.__drivers.find_element(By.ID, 'username').send_keys(self.__username)
        self.__drivers.find_element(By.ID, 'password').send_keys(self.__password)
        self.__drivers.find_element(By.ID, 'login').click()

        logger.info(f"Logged in as {self.__username}!")

    def loadPlayPage(self) -> None:
        logger.info("Loading play page...")
        self.__drivers.get('https://www.chess.com/play/online')
        try:
            popup_close = EC.presence_of_element_located((By.CLASS_NAME, 'ui_outside-close-component'))
            WebDriverWait(self.__drivers, 5).until(popup_close)
            self.__drivers.find_element(By.CLASS_NAME, 'ui_outside-close-component').click()
        except:
            logger.info('No popup found')

    def startGame(self) -> None:
        logger.info("Starting game...")
        self.__drivers.find_element(By.CSS_SELECTOR, '.ui_v5-button-component.ui_v5-button-large.ui_v5-button-primary').click()

    def getGameInformation(self) -> tuple:
        logger.info("Check game is started...")
        while True:
            try:
                popup_close = EC.presence_of_element_located((By.CLASS_NAME, 'draw-button-component'))
                WebDriverWait(self.__drivers, 2).until(popup_close)
                break
            except:
                logger.info("Game is not started yet...")
        logger.info("Game is started!")

        elements = self.__drivers.find_elements(By.CSS_SELECTOR, ".user-username.username")
        logger.info(f"{elements[0].text} vs {elements[1].text}")

        game_code = self.__drivers.current_url.replace('https://www.chess.com/game/live/', '')

        logger.info("Checking user color...")
        if elements[0].text == self.__username:
            logger.info("User is white")
            return (elements[0].text, elements[1].text, "white", game_code)
        else:
            logger.info("User is black")
            return (elements[0].text, elements[1].text, "black", game_code)

    def isGameEnded(self, opponent_name: str, game: int) -> tuple:
        try: 
            element_text = self.__drivers.find_element(By.CSS_SELECTOR, f'.live-game-over-component span:nth-child({game + 1})').text
        except: return False, None

        element_table = element_text.split(' ')
        if element_table[0] == self.__username:
            return True, "win"
        elif element_table[0] == opponent_name:
            return True, "loss"
        else:
            return True, "other"

    def getElementInPosition(self, position: str, player_color: str, retry: bool = False) -> str:
        if player_color == "white": c = "w"
        else: c = "b"
        
        try: 
            self.__drivers.find_element(By.CSS_SELECTOR, f'.piece.{c}p.square-{position}')
            return f".piece.{c}p.square-{position}"
        except:
            try:
                self.__drivers.find_element(By.CSS_SELECTOR, f'.piece.{c}r.square-{position}')
                return f".piece.{c}r.square-{position}"
            except:
                try:
                    self.__drivers.find_element(By.CSS_SELECTOR, f'.piece.{c}n.square-{position}')
                    return f".piece.{c}n.square-{position}"
                except:
                    try:
                        self.__drivers.find_element(By.CSS_SELECTOR, f'.piece.{c}b.square-{position}')
                        return f".piece.{c}b.square-{position}"
                    except:
                        try:
                            self.__drivers.find_element(By.CSS_SELECTOR, f'.piece.{c}q.square-{position}')
                            return f".piece.{c}q.square-{position}"
                        except:
                            try:
                                self.__drivers.find_element(By.CSS_SELECTOR, f'.piece.{c}k.square-{position}')
                                return f".piece.{c}k.square-{position}"
                            except:
                                if not retry:
                                    retry = True
                                    logger.error(f"Pieces not found ({position}). Retrying...")
                                    time.sleep(3)
                                    return self.getElementInPosition(position, player_color, True)
                                else:
                                    logger.error("Pieces not found. Giving up...")
                                    sys.exit()

    def moves(self, moves: str, game_id: int, player_color: str) -> None:
        start_pos = moves[:2].lower().replace("a", "1").replace("b", "2").replace("c", "3").replace("d", "4").replace("e", "5").replace("f", "6").replace("g", "7").replace("h", "8")
        end_pos   = moves[2:4].lower().replace("a", "1").replace("b", "2").replace("c", "3").replace("d", "4").replace("e", "5").replace("f", "6").replace("g", "7").replace("h", "8")
        source = self.__drivers.find_element(By.CSS_SELECTOR, self.getElementInPosition(start_pos, player_color))
        self.__drivers.execute_script(f"""let chessboard = document.getElementById("board-liveGame-{game_id}");

let highlight = document.createElement("div");
highlight.setAttribute("id", "chessbot-highlight");
highlight.setAttribute("class", "highlight square-{end_pos}");
highlight.setAttribute("style", "background-color: rgb(253, 121, 168); opacity: 0.8;");
chessboard.appendChild(highlight);""")
        time.sleep(0.10)
        target = self.__drivers.find_element(By.ID, 'chessbot-highlight')
        ActionChains(self.__drivers).drag_and_drop(source, target).perform()
        time.sleep(0.10)
        self.__drivers.execute_script(f"""let chessboard = document.getElementById("board-liveGame-{game_id}");
chessboard.removeChild(document.getElementById('chessbot-highlight'));""")

    def isMyTurn(self) -> bool:
        element = self.__drivers.find_element(By.CSS_SELECTOR, '#board-layout-player-bottom .clock-component')
        if 'clock-player-turn' in element.get_attribute('class').split():
            return True
        else:
            return False

    def parseMove(self, char: str) -> str:
        return char.replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e").replace("6", "f").replace("7", "g").replace("8", "h")

    def getOpponentMove(self) -> str:
        elements = self.__drivers.find_elements(By.CLASS_NAME, "highlight")

        initial_pos = elements[0].get_attribute('class').split(' ')[1].split('-')[1]
        final_pos = elements[1].get_attribute('class').split(' ')[1].split('-')[1]

        initial_pos = [char for char in initial_pos]
        final_pos = [char for char in final_pos]

        return self.parseMove(initial_pos[0]) + initial_pos[1] + self.parseMove(final_pos[0]) + final_pos[1]

    def checkReviewPopup(self):
        try:
            popup = EC.presence_of_element_located((By.CLASS_NAME, "game-review-popup-component"))
            WebDriverWait(self.__drivers, 5).until(popup)
            self.__drivers.find_element(By.CLASS_NAME, "game-review-popup-close").click()
        except: pass

    def startNewGame(self):
        try:
            button = EC.presence_of_element_located((By.CSS_SELECTOR, ".ui_v5-button-component.ui_v5-button-basic:nth-child(1)"))
            WebDriverWait(self.__drivers, 5).until(button)
            self.__drivers.find_element(By.CSS_SELECTOR, ".ui_v5-button-component.ui_v5-button-basic:nth-child(1)").click()
        except: 
            logger.error("Start new game button not found")
            sys.exit()

if __name__ == '__main__':
    bot = ChessBot()
    bot.login()
    bot.loadPlayPage()

    stockfish = Stockfish(path = bot.getStockfish(), depth = bot.getDepth(), parameters = {"Threads": bot.getThreadCount()})

    bot.startGame()

    game = 0 ; wins = 0 ; losses = 0 ; others = 0
    while game < bot.getRunCount():
        player_name, opponent_name, player_color, game_id = bot.getGameInformation()

        game += 1
        moves_table = []
        showed_opponent_turn = False

        if player_color == "white":
            time.sleep(1)
            moves_table.append("e2e4")
            bot.moves("e2e4", game_id, player_color)
            logger.info("Player move (White): e2e4")

        while True:
            end_game, results = bot.isGameEnded(opponent_name, game)
            if end_game:
                if results == "win":
                    wins += 1
                elif results == "loss":
                    losses += 1
                elif results == "other":
                    others += 1
                break
            else:
                if bot.isMyTurn():
                    opponent_move = bot.getOpponentMove()
                    moves_table.append(opponent_move)
                    logger.info(f"Opponent move ({'white' if player_color == 'black' else 'black'}): {opponent_move}")
                    
                    time.sleep(1)

                    stockfish.set_position(moves_table)
                    best_move = stockfish.get_best_move()
                    print(best_move)

                    time.sleep(1)
                    
                    bot.moves(best_move, game_id, player_color)
                    moves_table.append(best_move)
                    logger.info(f"Player move ({player_color}): {best_move}")
                    
                    showed_opponent_turn = False
                else:
                    if not showed_opponent_turn:
                        logger.info("Opponent's turn. Waiting...")
                        showed_opponent_turn = True
                    time.sleep(2)
        
        time.sleep(2)
        bot.checkReviewPopup()
        bot.startNewGame()

    print("\nThe bot has finished all its games!")
    print(f"{game} games played:")
    print(f"- {wins} Victory\n\
- {losses} Losses\n\
- {others} Others")