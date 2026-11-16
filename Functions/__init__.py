from time import sleep

from selenium.common.exceptions import *


# Default functions
# Converts pt-BR numbers to float ('1.234,56' -> 1234.56; odds keep the dot).
def replace_comma(v, odd=False):
    str_list = list(v)
    for char in str_list:
        if char == ',':
            str_list[str_list.index(char)] = '.'
        elif char == '.' and not odd:
            str_list[str_list.index(char)] = ''
    new_v = ''.join(str_list)
    if new_v == '':
        return 0.00
    else:
        return float(new_v)


def replace_dot(v):
    str_list = list(str(v))
    for char in str_list:
        if char == '.':
            str_list[str_list.index(char)] = ','
    new_v = ''.join(str_list)
    return new_v


def append_in(file, message):
    with open(file, 'a') as f:
        f.write(message)


def get_gaps(file):
    with open(file, 'r') as f:
        value = f.read()
    return int(value)


def update_gaps(file, gaps):
    with open(file, 'w') as f:
        f.write(f'{gaps + 1}')


# Selenium functions
def click(driver, reference, by):
    while True:
        try:
            if by == 'xpath':
                driver.find_element_by_xpath(reference).click()
            elif by == 'class_name':
                driver.find_element_by_class_name(reference).click()
            else:
                driver.find_element_by_css_selector(reference).click()
            break
        except (
            NoSuchElementException,
            ElementClickInterceptedException,
            StaleElementReferenceException,
            ElementNotInteractableException,
        ):
            pass


def fill(driver, reference, message, by):
    while True:
        try:
            if by == 'xpath':
                driver.find_element_by_xpath(reference).send_keys(message)
            else:
                driver.find_element_by_class_name(reference).send_keys(message)
            break
        except (NoSuchElementException, ElementClickInterceptedException):
            pass


def find(driver, reference, by):
    while True:
        try:
            if by == 'class_name':
                value = driver.find_element_by_class_name(reference).text
            elif by == 'xpath':
                value = driver.find_element_by_xpath(reference).text
            else:
                value = driver.find_element_by_css_selector(reference).text
            return value
        except (NoSuchElementException, StaleElementReferenceException):
            pass


def get_odd(driver, reference, by):
    try:
        if by == 'xpath':
            odd = replace_comma(
                driver.find_element_by_xpath(reference).text, True
            )
        elif by == 'class_name':
            odd = replace_comma(
                driver.find_element_by_class_name(reference).text, True
            )
        else:
            odd = replace_comma(
                driver.find_element_by_css_selector(reference).text, True
            )
    except (
        NoSuchElementException,
        StaleElementReferenceException,
        ValueError,
    ):
        return 0
    else:
        return odd


def screenshot(driver, name, cont, sp_element=None):
    if sp_element is not None:
        driver.execute_script(
            "arguments[0].scrollIntoView();",
            driver.find_element_by_xpath(sp_element),
        )
    else:
        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script(
            "return document.body.scrollHeight"
        )
        driver.set_window_size(total_width, total_height)
    driver.save_screenshot(f"Screenshots/{cont}_{name}.png")


def refresh(driver1, driver2=None, wait=0):
    driver1.refresh()
    if driver2 is not None:
        driver2.refresh()
    sleep(wait)


def finish(driver1, driver2=None):
    driver1.quit()
    if driver2 is not None:
        driver2.quit()


# Simulation: the final "place bet" clicks are commented out, so it only
# re-checks the odds and logs whether the bet would have worked.
def bet(
    driver1,
    driver2,
    sp_parameter,
    bw_parameter,
    team_parameter,
    old_odds,
    n,
    keys1,
    keys2,
):
    # Verifying variables
    print(
        f'Variables: {sp_parameter, bw_parameter, team_parameter, old_odds, n, keys1, keys2}'
    )

    # Function parameter
    testing = False

    # Declaring elements
    print('Declaring elements')
    odd_sp_element = (
        f'//*[@id="main-view"]/ms-fixture-list/div/div/div/div/ms-grid/ms-event-group['
        f'1]/ms-six-pack-event[{sp_parameter}]/div/div/div/ms-option-group[3]/ms-option['
        f'{team_parameter}]/ms-event-pick/div/div/ms-font-resizer'
    )
    odd_bw_element = (
        f'//*[@id="standard:level_type=region,level_id=1000093652"]/div[2]/div/div[1]'
        f'/div[{bw_parameter * 2}]/div/div[1]/button[{team_parameter}]/span[2]'
    )

    # Refreshing to avoid fake gaps
    refresh(driver1, driver2, 2)

    # Clicking on them
    print('Clicking on element - SP')
    click(driver1, odd_sp_element, 'xpath')
    print('Clicking on element - BW')
    click(driver2, odd_bw_element, 'xpath')

    # Sending keys - SportingBet
    print('Sending keys - SP')
    input_field_sp = (
        '//*[@id="betslip"]/div[2]/div/ms-betslip-stakebar/div/div/span/ms-stake/div/ms-stake-input/div'
        '/input '
    )
    click(driver1, input_field_sp, 'xpath')
    fill(driver1, input_field_sp, keys1, 'xpath')

    # Sending keys - BetWarrior
    print('Sending keys - BW')
    input_field_bw = '//*[@id="__next"]/div/div[2]/div[4]/div/div[2]/div/div/div[2]/div/input'
    click(driver2, input_field_bw, 'xpath')
    fill(driver2, input_field_bw, keys2, 'xpath')

    # Printing the situation
    screenshot(driver1, 'bet_sp', n)
    screenshot(driver2, 'bet_bw', n)

    # Verifying if the gap still happening
    print('Getting actual odds')
    new_odd_sp = get_odd(driver1, odd_sp_element, 'xpath')
    new_odd_bw = get_odd(driver2, odd_bw_element, 'xpath')

    # Betting
    print("Let's bet!")
    if old_odds == [new_odd_sp, new_odd_bw]:
        # Printing before click to analyse
        screenshot(driver1, 'pre_click_sp', n)
        screenshot(driver2, 'pre_click_bw', n)

        # Betting
        # click(driver1, '//*[@id="betslip"]/div[2]/div/div/ms-betslip-action-button/div/button/span', 'xpath')
        # click(driver2, '//*[@id="__next"]/div/div[2]/div[4]/div/div[5]/button/span', 'xpath')

        print(
            f'Essa aposta teria dado certo. Antes: {old_odds} || Depois: {[new_odd_sp, new_odd_bw]}\n'
        )

        # Writing and more printing
        if not testing:
            append_in(
                'gaps',
                f'Essa aposta teria dado certo. '
                f'Antes: {old_odds} || Depois: {[new_odd_sp, new_odd_bw]}\n',
            )

        # Printing right after betting
        screenshot(driver1, 'pos_click_sp', n)
        screenshot(driver2, 'pos_click_bw', n)

        sleep(10)

        # Printing after some sleeo
        screenshot(driver1, 'pos_click_sleep_sp', n)
        screenshot(driver2, 'pos_click_sleep_bw', n)
    else:
        # Writing if something went wrong
        print(
            f'Essa aposta não teria dado certo. Antes: {old_odds} || Depois: {[new_odd_sp, new_odd_bw]}\n'
        )
        if not testing:
            append_in(
                'gaps',
                f'Essa aposta não teria dado certo. '
                f'Antes: {old_odds} || Depois: {[new_odd_sp, new_odd_bw]}\n',
            )
