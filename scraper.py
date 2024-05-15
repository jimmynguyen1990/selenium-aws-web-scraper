from requests import options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By

WEBSITE_URL = 'https://www.freeconferencealerts.com/topicevent/human-rights'


def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver


def get_conference_urls(driver):
  driver.get(WEBSITE_URL)
  CONFERENCE_DIV_CLASS = 'conf-event-right'
  conference_divs = driver.find_elements(By.CLASS_NAME, CONFERENCE_DIV_CLASS)
  conference_urls = [
      conf_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
      for conf_div in conference_divs
  ]
  return conference_urls


def parse_conference(conference_url, driver):
  driver.get(conference_url)
  s_month = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[1]/div[@class='clndr-sec']/div[@class='month']"
  ).text

  s_day = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[1]/div[@class='clndr-sec']/div[@class='date']"
  ).text

  s_year = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[1]/div[@class='clndr-sec']/div[@class='year']"
  ).text

  e_month = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[3]/div[@class='clndr-sec']/div[@class='month']"
  ).text

  e_day = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[3]/div[@class='clndr-sec']/div[@class='date']"
  ).text

  e_year = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='date-to-date']/ul/li[3]/div[@class='clndr-sec']/div[@class='year']"
  ).text

  serial = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][1]"
  ).text

  title = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/h1"
  ).text

  organizer = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][6]/span"
  ).text

  start_date = f'{str(s_year).strip()}-{str(s_month).strip()}-{str(s_day).strip()}'

  end_date = f'{str(e_year).strip()}-{str(e_month).strip()}-{str(e_day).strip()}'

  proposal_deadline = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][5]/span"
  ).text

  city = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][7]/span"
  ).text

  nation = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][7]"
  ).text

  link = driver.find_element(
      By.XPATH,
      "/html/body/section[@class='upcmig-cnf']/div[@class='container']/div[@class='row']/div[@class='col-md-9']/div[@class='left-body-txt']/div[@class='body-txt-sec']/div[@class='body-txt'][2]/a[@class='conf_select']"
  ).text

  return {
      'serial': modify_serial(serial),
      'title': title,
      'organizer': organizer,
      'start_date': start_date,
      'end_date': end_date,
      'proposal_deadline': proposal_deadline,
      'city': modify_city(city),
      'nation': modify_nation(nation),
      'link': link
  }


def modify_nation(nation):
  return nation.split(',')[-1].strip()


def modify_city(city):
  return city.split(',')[0].strip()

def modify_serial(serial):
  return serial.split('-')[-1].strip()

if __name__ == '__main__':
  #Creating driver
  driver = get_driver()

  #Getting conference urls
  conference_urls = get_conference_urls(driver)

  conference_data = [parse_conference(url, driver) for url in conference_urls]

  print(len(conference_data))
