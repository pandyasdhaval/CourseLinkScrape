# This is the latest working part of this project
# It is able to log in and go through each subject in F19 SEM
# and click the download button in the table of contents
# To Update: make wait times dynamic -> rn it does compulsory waits which makes it a bit too slow


from selenium import webdriver
import time

my_options = webdriver.ChromeOptions()
my_options.add_argument('--ignore-certificate-errors')
my_options.add_argument('--test-type')
my_options.add_argument('chromedriver.exe')  # change this to the have the path of your executable chromedriver (i have chosen to keep it in the same dir) 
driver = webdriver.Chrome(options=my_options)
driver.implicitly_wait(10)


def run_driver():
    try:
        driver.get('https://courselink.uoguelph.ca/shared/login/login.html')

        login_button = driver.find_element_by_id('sso2')
        login_button.click()

        driver.find_element_by_id('inputUsername').send_keys('')  # input your Username here
        driver.find_element_by_id('inputPassword').send_keys('')  # input your Password here
        driver.find_element_by_xpath('//button[text()="Sign in"]').click()

        time.sleep(10)

        # The tags before each #shadow-root (open) are as follows
        # d2l-my-courses, class="d2l-my-courses-widget d2l-token-receiver"
        # shadow-root
        # d2l-my-courses-container
        # shadow-root
        # now we hit multiple d2l-tab-panel tabs (corresponds to each SEM) hence we select the one we need
        # d2l-my-courses-content
        # shadow-root
        # now we hit multiple d2l-enrollment-card (corresponds to each subject) hence we select the one we need
        # shadow-root
        # d2l-card
        # shadow-root
        # div a (i.e. link inside the div tag)
        # now click that link

        for count, subject in enumerate(driver.execute_script(
                              'return document.querySelector("d2l-my-courses.d2l-my-courses-widget.d2l-token-receiver")'
                              '.shadowRoot.querySelector("d2l-my-courses-container")'
                              '.shadowRoot.querySelectorAll("d2l-tab-panel")[4]'
                              '.querySelector("d2l-my-courses-content")'
                              '.shadowRoot.querySelectorAll("d2l-enrollment-card")'
                              )):

            driver.execute_script("""
                var counter = arguments[0];
                """
                'return document.querySelector("d2l-my-courses.d2l-my-courses-widget.d2l-token-receiver")'
                                  '.shadowRoot.querySelector("d2l-my-courses-container")'
                                  '.shadowRoot.querySelectorAll("d2l-tab-panel")[4]'
                                  '.querySelector("d2l-my-courses-content")'
                                  '.shadowRoot.querySelectorAll("d2l-enrollment-card")[counter]'
                                  '.shadowRoot.querySelector("d2l-card")'
                                  '.shadowRoot.querySelector("div a")', count
                                  ).click()

            time.sleep(3)
            driver.find_element_by_link_text('Content').click()

            time.sleep(3)
            # first find element by xpath added to give it context on where to find it
            # it would work without it as well
            driver.find_element_by_xpath('//div[@class="d2l-twopanelselector-side-padding"]').find_elements_by_xpath('//li/a')[3].click()

            time.sleep(3)
            driver.find_element_by_xpath('//div[@id="d2l_two_panel_selector_main"]').find_element_by_xpath('//button[text()="Download"]').click()

            time.sleep(60)

            driver.back()
            time.sleep(1)

            driver.back()
            time.sleep(1)


        time.sleep(5)
        driver.find_elements_by_class_name('d2l-dropdown-opener')[4].click()

        time.sleep(1)
        driver.find_element_by_link_text('Log Out').click()

        time.sleep(5)
    finally:
        time.sleep(5)
        driver.quit()
    return


run_driver()

