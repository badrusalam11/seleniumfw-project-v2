import time
from behave import given, when, then
from seleniumfw.browser_factory import BrowserFactory
from selenium.webdriver.support.ui import Select, WebDriverWait


@given('the user already login')
def step_impl(context):
    browser_factory = BrowserFactory() #this is mandatory
    context.driver = browser_factory.create_driver()
    context.driver.get("https://katalon-demo-cura.herokuapp.com/")
    context.driver.maximize_window()
    context.driver.find_element("id", "btn-make-appointment").click()
    context.driver.find_element("id", "txt-username").send_keys("John Doe")
    context.driver.find_element("id", "txt-password").send_keys("ThisIsNotAPassword")
    context.driver.find_element("id", "btn-login").click()

@when('the user select facility with {facility}')
def step_impl(context, facility):
    time.sleep(2)
    dropdown_facility = Select(context.driver.find_element("id", "combo_facility"))
    dropdown_facility.select_by_value(facility) 

@when('the user check apply hospital readmission with {is_check_readmission}')
def step_impl(context, is_check_readmission):
    if is_check_readmission == "true":
        context.driver.find_element("id", "chk_hospotal_readmission").click()

@when('the user select healthcare program with {healthcare_program}')
def step_impl(context, healthcare_program):
    context.driver.find_element("xpath", f"//input[@value='{healthcare_program}']")
    

@when('the user select visit date with {visit_date}')
def step_impl(context, visit_date):
    context.driver.find_element("id", "txt_visit_date").send_keys(visit_date)

@when('the user fill comment with {comment}')
def step_impl(context, comment):
    context.driver.find_element("id", "txt_comment").send_keys(comment)
    context.driver.find_element("id", "btn-book-appointment").click()

@then('the user successfully made appointment')
def step_impl(context):
    time.sleep(2)
    element = context.driver.find_element("xpath", "//h2[normalize-space()='Appointment Confirmation']")
    context.driver.save_screenshot("appointment.png")
    assert element.is_displayed()
    context.driver.quit()
