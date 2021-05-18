from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options as Chrome_Options
from urllib3 import exceptions

from Functions import *

# Script parameters
headless = False

# Bet parameters
team = 'Pistons'
stake1 = 50
odd1 = 1.95  # Precisa ser maior que 1.65 (Betano)
lucro = 0
stake2 = round((stake1 * odd1 / (1 + lucro)) - stake1, 2)
odd2 = round(stake1 * odd1 / stake2, 2)

print(odd2, stake2)


def nba():
    # Driver variables
    path = ''
    preferences = Chrome_Options()
    if headless:
        preferences.add_argument('--headless')
        preferences.add_argument('window-size=1920x1080')
    else:
        preferences.add_argument('--start-maximized')
    preferences.add_argument("--remote-debugging-port=9222")

    # Driver initiation
    url = 'https://sports.sportingbet.com/pt-br/sports/basquetebol-7/aposta/am%C3%A9rica-do-norte-9/nba-6004'
    driver = webdriver.Chrome(executable_path=path, options=preferences)
    driver.get(url)

    print("Let's start.")

    try:
        # Login steps
        if not headless:
            click(driver, '//*[@id="messages-with-overlay"]/div/vn-content-message/div/span', 'xpath')
        click(driver, '/html/body/vn-app/vn-dynamic-layout-single-slot[1]/vn-responsive-header/'
                      'header/nav/vn-header-section[2]/vn-h-button[1]/vn-menu-item/a', 'xpath')
        fill(driver, '//*[@id="username"]/input', '', 'xpath')
        fill(driver, '//*[@id="password"]/input', '', 'xpath')
        click(driver, '//*[@id="login"]/form/fieldset/section/div[2]/button', 'xpath')

        sleep(5)

        # Getting match parameter
        while True:
            try:
                position = 0
                participants = driver.find_elements_by_class_name('participants-pair-game')
                if len(participants) != 0:
                    for participant in participants:
                        if team.lower() in participant.text.lower():
                            driver.execute_script("arguments[0].scrollIntoView();", participant)
                            participant.click()
                            break
                    break
            except (NoSuchElementException, StaleElementReferenceException):
                pass
        team_parameter = 1 if position % 2 == 1 else 2

        # Getting odd2
        loop_count = 0
        refresh_count = 0
        while True:
            target_element = f'//*[@id="main-view"]/ng-component/div/ms-option-group-list/div[1]/ms-option-panel[1]' \
                             f'/ms-period-option-group/ms-regular-option-group/div/ms-option[{team_parameter}]/ms-' \
                             f'event-pick/div/div[2]'
            odd_target = get_odd(driver, target_element, 'xpath')
            print(odd_target)
            if odd_target >= odd2:
                print('Headshot!')
                click(driver, target_element, 'xpath')
                input_field_sp = '//*[@id="betslip"]/div[2]/div/ms-betslip-stakebar/' \
                                 'div/div/span/ms-stake/div/ms-stake-input/div/input '
                click(driver, input_field_sp, 'xpath')
                fill(driver, input_field_sp, str(stake2), 'xpath')
                click(driver, '//*[@id="betslip"]/div[2]/div/div/ms-betslip-action-button/div/button/span', 'xpath')
                sleep(10)
                finish(driver)
                exit()
            elif refresh_count > 5:
                print('Reiniciando função.')
                finish(driver)
                nba()
            elif loop_count > 250:
                print('Atualizando página.')
                refresh(driver)
                loop_count = 0
                refresh_count += 1
            else:
                loop_count += 1
    except (exceptions.MaxRetryError, common.exceptions.WebDriverException) as e:
        print(f'Erro inesperado: {e}. Reiniciando.')
        finish(driver)
        nba()


nba()
