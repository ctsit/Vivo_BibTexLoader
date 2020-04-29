import os
import sys
import time
import datetime
from datetime import date
from selenium import webdriver


def main(downloadpath):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
      "download.default_directory": downloadpath,
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True,
      "plugins.always_open_pdf_externally": True
    })
    driver = webdriver.Chrome(chrome_options=options)

    webofscience_str = "https://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=6FseAuF91F1EyTi3c9o&preferencesSaved="
    driver.get(webofscience_str)
    time.sleep(5)

    # from selenium import webdriver
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC
    # from selenium.webdriver.common.by import By

    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='codefile_iframe']")))
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ok' and @value='OK'][starts-with(@onclick,'loginui')]"))).click()


    advanced_search = driver.find_element_by_xpath("/html/body/div[9]/div/ul/li[4]/a").click()
    select_timespan = driver.find_element_by_xpath("//*[@id='timespan']/div[2]/div/select")
    for option in select_timespan.find_elements_by_tag_name('option'):
        if 'Current week' in option.text:
            option.click()
    searchElement = driver.find_element_by_xpath("//*[@id='value(input1)']")
    searchElement.send_keys("AD=(University Florida OR Univ Florida OR UFL OR UF)")
    driver.find_element_by_xpath('//*[@id="search-button"]').click()
    time.sleep(5)
    record_num = driver.find_element_by_css_selector('#set_1_div > a').text
    driver.find_element_by_css_selector('#set_1_div > a').click()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="exportTypeName"]').click()
    save_file = driver.find_element_by_xpath('//*[@id="saveToMenu"]')
    time.sleep(1)
    for option in save_file.find_elements_by_tag_name('li'):
        if 'Other File Formats' in option.text:
            option.click()
    driver.find_element_by_xpath('//*[@id="numberOfRecordsRange"]').click()
    # record_start_num = driver.find_element_by_xpath('//*[@id="records-range-from"]/input')
    # record_start_num.send_keys("1")
    # record_end_num = driver.find_element_by_xpath('//*[@id="records-range-to"]/input')
    # record_end_num.send_keys(record_num)
    save_file_type = driver.find_element_by_xpath('//*[@id="bib_fields"]')
    for option in save_file_type.find_elements_by_tag_name('option'):
        if 'Full Record' in option.text and 'Cited References' not in option.text:
            option.click()
    save_file_format = driver.find_element_by_xpath('//*[@id="saveOptions"]')
    for option in save_file_format.find_elements_by_tag_name('option'):
        if option.text == 'BibTeX':
            option.click()
    driver.find_element_by_xpath('//*[@id="exportButton"]').click()
    time.sleep(5)
    driver.close()

    day = datetime.date.today().strftime("%A")
    day_of_month = datetime.datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1
    date = datetime.datetime.today().strftime('%m_%d_%Y')
    new_filename = day[:2]+"_"+date+"_wk_"+str(week_number)+".bib"
    old_file = os.path.join(downloadpath, 'savedrecs.bib')
    new_file = os.path.join(downloadpath, new_filename)
    os.rename(old_file, new_file)


if __name__ == '__main__':
    main(sys.argv[1])
