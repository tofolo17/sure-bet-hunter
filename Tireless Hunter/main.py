import datetime
from time import time

from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options as Chrome_Options
from selenium.webdriver.firefox.options import Options as Firefox_Options
from urllib3 import exceptions

from Functions import *

# Application timer
run_timer = time()

# Script parameter
firefox_headless = True
chrome_headless = True
testing = False


# Main function
def nba():
    # Function timer
    def_timer = time()

    # Driver variables
    chrome_path = ''
    firefox_path = ''
    chrome_preferences = Chrome_Options()
    firefox_preferences = Firefox_Options()
    if chrome_headless:
        chrome_preferences.add_argument('--headless')
        chrome_preferences.add_argument('window-size=1920x1080')
    if firefox_headless:
        firefox_preferences.add_argument('--headless')
        firefox_preferences.add_argument('window-size=1920x1080')
    chrome_preferences.add_argument("--remote-debugging-port=9222")

    # Driver configuration
    url1 = 'https://sports.sportingbet.com/pt-br/sports/basquetebol-7/aposta/am%C3%A9rica-do-norte-9/nba-6004'
    url2 = 'https://betwarrior.bet/pt-br/sports/basquete/nba'
    driver1 = webdriver.Chrome(executable_path=chrome_path, options=chrome_preferences)
    if not chrome_headless:
        driver1.maximize_window()
    driver2 = webdriver.Firefox(executable_path=firefox_path, options=firefox_preferences)
    if not firefox_headless:
        driver2.maximize_window()
    driver1.get(url1)
    driver2.get(url2)

    print(f"Driver configuration. Check! -- {time() - run_timer:.2f}s")

    try:
        # Login steps - SportingBet
        if not chrome_headless:
            click(driver1, '//*[@id="messages-with-overlay"]/div/vn-content-message/div/span', 'xpath')
        click(driver1, '/html/body/vn-app/vn-dynamic-layout-single-slot[1]/vn-responsive-header/'
                       'header/nav/vn-header-section[2]/vn-h-button[1]/vn-menu-item/a', 'xpath')
        fill(driver1, '//*[@id="username"]/input', '', 'xpath')
        fill(driver1, '//*[@id="password"]/input', '', 'xpath')
        click(driver1, '//*[@id="login"]/form/fieldset/section/div[2]/button', 'xpath')

        print(f"Login steps - SportingBet. Check! -- {time() - run_timer:.2f}s")

        # Login steps - BetWarrior
        click(driver2, '//*[@id="user-trigger"]/div[1]/div/div', 'xpath')
        fill(driver2, '//*[@id="email-input"]/label/div[2]/input', '', 'xpath')
        fill(driver2, '//*[@id="password-input"]/label/div[2]/input', '', 'xpath')
        click(driver2, '//*[@id="login-action"]/span', 'xpath')

        print(f"Login steps - BetWarrior. Check! -- {time() - run_timer:.2f}s")

        sleep(10)

        # amount_sp = replace_comma(find(driver1, 'user-balance', 'class_name')[:-4])
        # amount_bw = replace_comma(find(driver2, '//*[@id="user-trigger"]/div[1]/div/div', 'xpath')[3:])
        amount = 10  # round(min(amount_sp, amount_bw), 2)

        print(f"Get amount of money (R${amount}). Check! -- {time() - run_timer:.2f}s ")

        # Getting live participants
        while True:
            try:
                live_game_count = 3 if testing else len(driver1.find_elements_by_class_name('live-icon'))
                if live_game_count != 0:
                    participants = driver1.find_elements_by_class_name('participant')[:(live_game_count * 2)]
                    live_participants = [[participants[i].text, participants[i + 1].text]
                                         for i in range(0, live_game_count * 2, 2)]
                    break
                else:
                    print(f'No live matches now. Wait a few minutes...\n')
                    refresh(driver1, driver2, 300)
            except (NoSuchElementException, StaleElementReferenceException):
                pass

        print(f"Getting live participants ({live_participants}). Check! -- {time() - run_timer:.2f}s\n")

        # Scrapping loop
        refresh_count = 0
        gap_count = get_gaps('gap_count')
        while True:
            refresh_count += 1
            if datetime.datetime.now().hour not in [0]:  # fix it
                # Getting odds from both sites and organizing it's order
                for i in range(1, live_game_count + 1):
                    sp_participant_1 = live_participants[i - 1][0]
                    reference_odd_sp = f'//*[@id="main-view"]/ms-fixture-list/div/div/div/div/ms-grid/ms-event-group[' \
                                       f'1]/ms-six-pack-event[{i}]/div/div/div/ms-option-group[3]/ms-option[' \
                                       f'1]/ms-event-pick/div/div/ms-font-resizer '
                    odd1_sp = get_odd(driver1, reference_odd_sp, 'xpath')
                    odd2_sp = get_odd(driver1, f'//*[@id="main-view"]/ms-fixture-list/div/div/div/div/ms-grid/ms'
                                               f'-event-group[1]/ms-six-pack-event[{i}]/div/div/div/ms-option-group['
                                               f'3]/ms-option[2]/ms-event-pick/div/div/ms-font-resizer', 'xpath')
                    odd1_bw = odd2_bw = j = 0
                    for j in range(1, live_game_count + 1):
                        bw_participant_1 = find(driver2, f'//*[@id="standard:level_type=region,level_id=1000093652"]'
                                                         f'/div[2]/div/div[1]/div[{2 if j == 1 else j * 2}]/a/div[1]'
                                                         f'/span/div[2] ', 'xpath')
                        if sp_participant_1 in bw_participant_1:
                            odd1_bw = get_odd(driver2, f'//*[@id="standard:level_type=region,level_id=1000093652"]/div['
                                                       f'2]/div/div[1]/div[{2 if j == 1 else j * 2}]/div/div[1]/button['
                                                       f'2]/span[2]', 'xpath')
                            odd2_bw = get_odd(driver2, f'//*[@id="standard:level_type=region,level_id=1000093652"]/div['
                                                       f'2]/div/div[1]/div[{2 if j == 1 else j * 2}]/div/div[1]/button['
                                                       f'1]/span[2]', 'xpath')
                            break
                    comparison_01 = f'Odd do {sp_participant_1} no SP - {odd1_sp:.2f} x {odd1_bw:.2f} -' \
                                    f' Odd do {sp_participant_1} no BW'
                    comparison_02 = f'Odd do {live_participants[i - 1][1]} no SP - {odd2_sp:.2f} x {odd2_bw:.2f} -' \
                                    f' Odd do {live_participants[i - 1][1]} no BW'
                    print(f'Partida {i}\n{comparison_01}\n{comparison_02}')
                    # Declaring variables and betting
                    if 0 not in [odd1_bw, odd2_bw, odd1_sp, odd2_sp]:
                        bet1_bw = round((amount * odd1_sp) / (odd2_bw + odd1_sp), 2)
                        bet1_sp = round(amount - bet1_bw, 2)
                        bet2_bw = round((amount * odd2_sp) / (odd1_bw + odd2_sp), 2)
                        bet2_sp = round(amount - bet2_bw, 2)
                        if min([bet1_sp, bet1_bw, bet2_sp, bet2_bw]) >= 3:
                            if (bet1_sp * odd1_sp) - amount > 0:
                                print('')
                                update_gaps('gap_count', gap_count)
                                screenshot(driver1, 'gap_sp', gap_count, sp_element=reference_odd_sp)
                                screenshot(driver2, 'gap_bw', gap_count)
                                append_in('gaps',
                                          f'\nTimer (1): {time() - run_timer:.2f}s\n'
                                          f'{comparison_01}\n'
                                          f'{comparison_02}\n'
                                          f'Capital investido: R${amount:.2f}\n'
                                          f'No SportingBet: R${bet1_sp} * {odd1_sp:.2f} = R${bet1_sp * odd1_sp:.2f}\n'
                                          f'No BetWay: R${bet1_bw} * {odd2_bw:.2f} = R${bet1_bw * odd2_bw:.2f}\n'
                                          f'Lucro: R${(bet1_sp * odd1_sp) - amount:.2f}\n'
                                          f'Equivale a {((bet1_sp * odd1_sp) - amount) * 100 / amount:.2f}%\n')
                                bet(driver1, driver2, i, j, 1, [odd1_sp, odd2_bw],
                                    gap_count, replace_dot(bet1_sp), replace_dot(bet1_bw))
                                finish(driver1, driver2)
                                nba()
                                break  # is this necessary?
                            elif (bet2_sp * odd2_sp) - amount > 0:
                                print('')
                                update_gaps('gap_count', gap_count)
                                screenshot(driver1, 'gap_sp', gap_count, sp_element=reference_odd_sp)
                                screenshot(driver2, 'gap_bw', gap_count)
                                append_in('gaps',
                                          f'\nTimer (2): {time() - run_timer:.2f}s\n'
                                          f'{comparison_01}\n'
                                          f'{comparison_02}\n'
                                          f'Capital investido: R${amount:.2f}\n'
                                          f'No SportingBet: R${bet2_sp} * {odd2_sp:.2f} = R${bet2_sp * odd2_sp:.2f}\n'
                                          f'No BetWay: R${bet2_bw} * {odd1_bw:.2f} = R${bet2_bw * odd1_bw:.2f}\n'
                                          f'Lucro: R${(bet2_sp * odd2_sp) - amount:.2f}\n'
                                          f'Equivale a {((bet2_sp * odd2_sp) - amount) * 100 / amount:.2f}%\n')
                                bet(driver1, driver2, i, j, 2, [odd2_sp, odd1_bw],
                                    gap_count, replace_dot(bet2_sp), replace_dot(bet2_bw))
                                finish(driver1, driver2)
                                nba()
                                break
                # Conditionals to refresh or restart
                if (time() - def_timer) > 600:
                    print(f"Let's restart. Wait a few minutes... -- {time() - run_timer:.2f}s\n")
                    finish(driver1, driver2)
                    nba()
                elif refresh_count >= 100:
                    refresh(driver1, driver2, 10)
                    print(f'Refresh realized. -- {time() - run_timer:.2f}s\n')
                    refresh_count = 0
            else:
                finish(driver1, driver2)
                exit()
    except (exceptions.MaxRetryError, common.exceptions.WebDriverException):
        print(f'Something went wrong. Wait a few minutes... -- {time() - run_timer:.2f}s\n')
        finish(driver1, driver2)
        nba()


nba()
