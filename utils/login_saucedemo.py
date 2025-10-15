from selenium.webdriver.common.by import By

def login_saucedemo(driver):
    # 1) Entrar a la página
    driver.get('https://www.saucedemo.com')
    
    # 2) Verificar título de la página
    assert driver.title == 'Swag Labs' 

    # 3) Login
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')
    driver.find_element(By.ID, 'login-button').click()