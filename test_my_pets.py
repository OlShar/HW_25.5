import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:/chromedrivers/chromedriver.exe')
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield
   pytest.driver.quit()


def test_my_pets():
   pytest.driver.find_element(By.ID, 'email').send_keys('testsapi@gmail.com')
   pytest.driver.find_element(By.ID, 'pass').send_keys('asdf5577')
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

   names = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
   images = pytest.driver.find_elements(By.XPATH, '//tbody/tr/th/img')
   animal_types = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
   age = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
   string_count_of_pets = pytest.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]").text
   number_of_table_rows = pytest.driver.find_elements(By.XPATH, '//tbody/tr')


   # Количество строк таблицы соответствует количеству питомцев в блоке статистики пользователя.
   count_of_pets = string_count_of_pets.split('\n')[1].split(':')[1]
   assert int(count_of_pets) == len(number_of_table_rows)


   # Хотя бы у половины питомцев есть фото.
   try:
      count_of_images = 0
      for i in range(int(count_of_pets)):
         if images[i].get_attribute('src') != '':
            count_of_images += 1
      assert (int(count_of_pets)) / 2 <= count_of_images

   except AssertionError:
      print('\n!!!Более половины питомцев не имеют фото')


   # У всех питомцев есть имя, возраст и порода.
   for i in range(len(number_of_table_rows)):
      assert names[i].text != ''
      assert animal_types[i].text != ''
      assert age[i].text != ''


   # У всех питомцев разные имена.
   try:
      list_of_names = []
      for i in range(len(number_of_table_rows)):
         list_of_names.append(names[i].text)
      assert len(list_of_names) == len(set(list_of_names))

   except AssertionError:
      print('\n!!!Есть повторяющиеся имена')


   # В списке нет повторяющихся питомцев.
   try:
      list_of_pets = []
      for i in range(len(number_of_table_rows)):
         description_of_pet = pytest.driver.find_elements(By.XPATH, f'//tbody/tr[{i + 1}]/td[not(@class="smart_cell")]')
         column_name = description_of_pet[0].text
         column_animal_types = description_of_pet[1].text
         column_age = description_of_pet[2].text
         list_description_of_pet = [column_name, column_animal_types, column_age]

         list_of_pets.append(tuple(list_description_of_pet))

      unique_list_of_pets = list(dict.fromkeys(list_of_pets))
      assert len(unique_list_of_pets) == len(list_of_pets)

   except AssertionError:
      print('\n!!!Есть одинаковые питомцы')












