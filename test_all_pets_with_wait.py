import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:/chromedrivers/chromedriver.exe')
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield
   pytest.driver.quit()


def test_all_pets():
   pytest.driver.find_element(By.ID, 'email').send_keys('testsapi@gmail.com')
   pytest.driver.find_element(By.ID, 'pass').send_keys('asdf5577')
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   pytest.driver.implicitly_wait(10)
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-img-top')
   pytest.driver.implicitly_wait(10)
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-title')
   pytest.driver.implicitly_wait(10)
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-text')

   for i in range(len(names)):
      assert names[i].text != ''
      assert images[i].get_attribute('src') != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0