import os
import random
import threading
import time
from django.test import Client, LiveServerTestCase, TestCase
from django.urls import reverse
from . import urls  # Import your URL module
from awwwapp.models import FileSection, SectionStatus, User, Catalog, File, SectionKind
from  awwwapp.globals import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestModel(TestCase):
    def test_user_creation(self):
        # create a new user
        user = User.objects.create(name='Test User', login='TestLogin', password='TestPassword')
        # check if user is created
        self.assertTrue(user)
        # check if user is accessible
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.login, 'TestLogin')
        self.assertEqual(user.password, 'TestPassword')
        # remove user from database
        user.delete()
        # check if user is removed
        self.assertFalse(User.objects.filter(name='Test User').exists())

        
    def test_adding_catalog_test(self):
        # create a new user
        user = User.objects.create(name='Test User', login='TestLogin', password='TestPassword')
        # create a new catalog
        catalog = Catalog.objects.create(name='Test Catalog', owner=user)
        # check if catalog is created
        self.assertTrue(catalog)
        # check if catalog is accessible
        self.assertTrue(catalog.is_accessible())
        self.assertEqual(catalog.name, 'Test Catalog')
        self.assertEqual(catalog.owner, user)
        # remove catalog from database
        catalog.delete()
        # check if catalog is removed
        self.assertFalse(Catalog.objects.filter(name='Test Catalog').exists())
        # remove user from database
        user.delete()
        
    def test_adding_file_test(self):
        # create a new user
        user = User.objects.create(name='Test User', login='TestLogin', password='TestPassword')
        # create a new catalog
        catalog = Catalog.objects.create(name='Test Catalog', owner=user)
        # create a new file
        file = File.objects.create(name='Test File', catalog=catalog, owner=user)
        # check if file is created
        self.assertTrue(file)
        # check if file is accessible
        self.assertTrue(file.is_accessible())
        self.assertEqual(file.name, 'Test File')
        self.assertEqual(file.catalog, catalog)
        self.assertEqual(file.owner, user)
        # remove file from database
        file.delete()
        # check if file is removed
        self.assertFalse(File.objects.filter(name='Test File').exists())
        # remove catalog from database
        catalog.delete()
        # remove user from database
        user.delete()

    def test_add_sections_to_file(self):
        # add new user
        user = User.objects.create(name='Test User', login='TestLogin', password='TestPassword')
        # add new catalog
        catalog = Catalog.objects.create(name='Test Catalog', owner=user)
        # add new file
        file = File.objects.create(name='Test File', catalog=catalog, owner=user)
        directives_status = SectionStatus.objects.create(
            name='Not tried',
        )
        comment_status = SectionStatus.objects.create(
            name='Not tried',
        )
        code_status = SectionStatus.objects.create(
            name='Not tried',
        )
        # add new section 
        number_of_sections = FileSection.objects.count()
        first_section = FileSection.objects.create(
            name='directive Section', 
            file=file,
            kind=SectionKind.objects.get(name='compiler directive'),
            start=0,
            end=1,
            status=directives_status,
            content='#include <stdio.h>'
            )
        second_section = FileSection.objects.create(
            name='comment Section',
            file=file,
            kind=SectionKind.objects.get(name='comment'),
            start=2,
            end=3,
            status=comment_status,
            content='// this is a hello world program'
        )
        third_section = FileSection.objects.create(
            name='code Section',
            file=file,
            kind=SectionKind.objects.get(name='code'),
            start=4,
            end=8,
            status=code_status,
            content='int main(){\nprintf("Hello World");\nreturn 0;\n}'
        )
        # check if sections are created
        self.assertTrue(first_section)
        self.assertTrue(second_section)
        self.assertTrue(third_section)
        self.assertEqual(first_section.file, file)
        self.assertEqual(second_section.file, file)
        self.assertEqual(third_section.file, file)
        # delete everything
        user.delete()
        # check if content associated with the user is deleted
        self.assertFalse(User.objects.filter(name='Test User').exists())
        # check if catalog associated with the user is deleted
        self.assertFalse(Catalog.objects.filter(name='Test Catalog').exists())
        # check if file associated with the user is deleted
        self.assertFalse(File.objects.filter(name='Test File').exists())
        # assert sections count it the same as before
        self.assertEqual(FileSection.objects.count(), number_of_sections)


class TestLoginRegistration(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_registrationtest(self):
        url = 'http://127.0.0.1:8000/register_viev/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        form_data = {
            'name': 'Test User',
            'login': 'TestLogin',
            'password': 'TestPassword',
        }
        response = self.client.post('http://127.0.0.1:8000/register_viev/', data=form_data, follow=True)

        # Assert the response
        self.assertEqual(response.status_code, 200)

    test_registrationtest.order = 1

    def test_logintest(self):
        url = ''
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        form_data = {
            'login': 'TestLogin',
            'password': 'TestPassword',
        }
        response = self.client.post('', data=form_data, follow=True)
        # Assert the response
        self.assertEqual(response.status_code, 200)

    test_logintest.order = 2

    @classmethod
    def tearDownClass(cls):
        # remove user from database
        User.objects.filter(name='Test User').delete()

class TestVievs(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.driver = webdriver.Firefox()
        time.sleep(1)
        # open browser
        
        url = 'http://127.0.0.1:8000/register_viev/'
        response = cls.client.get(url)
        
        if response.status_code != 200:
            # raise an error to fail the test
            raise ValueError('Unexpected response code: %s' % response.status_code)
        
        form_data = {
            'name': 'Test User',
            'login': 'TestLogin',
            'password': 'TestPassword',
        }
        response = cls.client.post('http://127.0.0.1:8000/register/', data=form_data, follow=True)

        # Assert the response
        if response.status_code != 200:
            # raise an error to fail the test
            raise ValueError('Unexpected response code: %s' % response.status_code)
    
        url = ''
        response = cls.client.get(url)
        if response.status_code != 200:
            # raise an error to fail the test
            raise ValueError('Unexpected response code: %s' % response.status_code)

        form_data = {
            'login': 'TestLogin',
            'password': 'TestPassword',
        }
        response = cls.client.post('http://127.0.0.1:8000/login/', data=form_data, follow=True)
        # Assert the response
        if response.status_code != 200:
            # raise an error to fail the test
            raise ValueError('Unexpected response code: %s' % response.status_code)
        
        # assert response has  
        
    def test_registration(self):
        url = 'http://127.0.0.1:8000/register_viev/'
        response = self.client.get(url)
        
        if response.status_code != 200:
            # raise an error to fail the test
            raise ValueError('Unexpected response code: %s' % response.status_code)
        
        # get some random number
        random_number = random.randint(0, 1000000)
        
        form_data = {
            'name': 'Test User' + str(random_number),
            'login': 'TestLogin' + str(random_number),
            'password': 'TestPassword' +    str(random_number),
        }
        response = self.client.post('http://127.0.0.1:8000/register/', data=form_data, follow=True)

        # Assert the response
        if response.status_code != 200:
            # raise an error to fail the test
            raise ValueError('Unexpected response code: %s' % response.status_code)
        
        url = ''
        response = self.client.get(url)
        if response.status_code != 200:
            # raise an error to fail the test
            raise ValueError('Unexpected response code: %s' % response.status_code)

        form_data = {
            'login': 'TestLogin' + str(random_number),
            'password': 'TestPassword' + str(random_number),
        }
        response = self.client.post('http://127.0.0.1:8000/login/', data=form_data, follow=True)
        # Assert the response
        if response.status_code != 200:
            # raise an error to fail the test
            raise ValueError('Unexpected response code: %s' % response.status_code)
        
        

    def test_change_standard_test(self):
        response = self.client.get('http://127.0.0.1:8000/frontend/')
        # Assert that the "STANDARD" button is present on the page
        self.assertContains(response, 'STANDARD')
        # click the "STANDARD" button

        
        response = self.client.post('http://127.0.0.1:8000/frontend/', {'button': 'STANDARD'})
        # Assert that the "STANDARD" button is pressed
        #self.assertEqual(response, 'C11')
        response = self.client.post('http://127.0.0.1:8000/frontend/', {'button': 'C11'})
        assert compiler_options['standard'] == 'C11'
        self.assertEqual(response.status_code, 200)

    def test_change_processor_test(self):
        response = self.client.get('http://127.0.0.1:8000/frontend/')
        # Assert that the "PROCESSOR" button is present on the page
        self.assertContains(response, 'PROCESOR')
        response = self.client.post('http://127.0.0.1:8000/frontend/', {'button': 'PROCESSOR'})
        # Assert that the "PROCESSOR" button is pressed
        self.assertContains(response, 'mcs51')

        response = self.client.post('/frontend/', {'processor': 'mcs51'})
        #wait for server to process the request
        time.sleep(1)
        print(compiler_options['processor'])
        #assert compiler_options['processor'] == 'mcs51'
        self.assertEqual(response.status_code, 200)

    def test_change_optimization_test(self):
        response = self.client.get('http://127.0.0.1:8000/frontend/')
        # Assert that the "OPTIMIZATION" button is present on the page
        self.assertContains(response, 'OPTYMALIZACJE')
        response = self.client.post('http://127.0.0.1:8000/frontend/', {'button': 'OPTYMALIZACJE'})
        # Assert that the "OPTIMIZATION" button is pressed
        self.assertContains(response, '--nogcse')
        self.assertContains(response, '--noinvariant')
        response = self.client.post('http://127.0.0.1:8000/frontend/', {'button': '--nogcse'})
        response = self.client.post('http://127.0.0.1:8000/frontend/', {'button': '--noinvariant'})
        #assert compiler_options['optimization'] == ['--nogcse', '--noinvariant']
        self.assertEqual(response.status_code, 200)
        

    def test_add_file_and_change_sections_test(self):
        self.driver.get('http://127.0.0.1:8000/frontend/')
        # click on the first element on the "pasek menu" button
        element = self.driver.find_element(By.ID, 'pasekmenu_new_catalog')
        element.click()
        # fill the form with id adding_file_dropbox
        form_element = self.driver.find_element(By.ID, 'adding_catalog_dropbox')
        name_input = form_element.find_element(By.NAME, 'name')
        name_input.send_keys('nazwa katalogu')
        description_input = form_element.find_element(By.NAME, 'description')
        description_input.send_keys('opis katalogu')
        element = self.driver.find_element(By.ID, 'create_catalog')
        element.click()    
        time.sleep(1)
        element = self.driver.find_element(By.NAME, 'catalog')
        element.click()

        element = self.driver.find_element(By.ID, 'pasekmenu_new_catalog')
        element.click()
        # fill the form with id adding_file_dropbox
        form_element = self.driver.find_element(By.ID, 'adding_catalog_dropbox')
        name_input = form_element.find_element(By.NAME, 'name')
        name_input.send_keys('nazwa katalogu 1')
        description_input = form_element.find_element(By.NAME, 'description')
        description_input.send_keys('opis katalogu 1')
        #form_element.submit()
        # press button "Create"
        element = self.driver.find_element(By.ID, 'create_catalog')
        element.click()
        # click on elemont of class "catalog"
        # wait for server to process the request    
        time.sleep(1)
        element = self.driver.find_element(By.NAME, 'catalog')
        element.click()

        element = self.driver.find_element(By.ID, 'pasekmenu_new_file')
        element.click()
        # fill the form with id adding_file_dropbox
        form_element = self.driver.find_element(By.ID, 'adding_file_dropbox')
        name_input = form_element.find_element(By.NAME, 'name')
        name_input.send_keys('nazwa pliku')
        description_input = form_element.find_element(By.NAME, 'description')
        description_input.send_keys('opis pliku')
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
        file_input.send_keys(os.getcwd() + '/awwwapp/hellotest.c')
        element = self.driver.find_element(By.ID, 'create_file')
        element.click()
        element = self.driver.find_element(By.NAME, 'file')
        element.click()
        # assert that something has appeared in the "TekstProgramu" section
        element = self.driver.find_element(By.ID, 'program_code')
        #get html from the element
        html = element.get_attribute('innerHTML')
        #assert that the html is not empty
        self.assertNotEqual(html, '')
        #click on buttonn with id="STANDARD"
        element = self.driver.find_element(By.NAME, 'STANDARD')
        element.click()
        # find all elements with name="standard"
        elements = self.driver.find_elements(By.NAME, 'standard')
        #click one of them
        elements[1].click()
        #click on buttonn with id="OPTYMALIZACJE"
        element = self.driver.find_element(By.NAME, 'OPTYMALIZACJE')
        element.click()
        # find all elements with name="optimization"
        elements = self.driver.find_elements(By.NAME, 'optimizations')
        #click one of them
        elements[1].click()
        
        #click on buttonn with id="PROCESOR"
        element = self.driver.find_element(By.NAME, 'PROCESOR')
        element.click()
        # find all elements with name="processor"
        elements = self.driver.find_elements(By.NAME, 'processor')
        #click one of them
        elements[1].click()
        #click on buttonn with id="ZALEŻNE-z80"
        element = self.driver.find_element(By.NAME, 'ZALEŻNE-z80')
        element.click()
        element = self.driver.find_element(By.NAME, 'catalog')
        element.click()
        element = self.driver.find_element(By.ID, 'pasekmenu_delete_catalog')
        element.click()
        element = self.driver.find_element(By.ID, 'pasekmenu_display')
        element.click()
        # assert that something has appeared in the "code_fragment" section
        element = self.driver.find_element(By.ID, 'code_fragment')
        #get html from the element
        html = element.get_attribute('innerHTML')
        #assert that the html is not empty
        self.assertNotEqual(html, '')
        element = self.driver.find_element(By.ID, 'pasekmenu_delete_file')
        element.click()
        

    
    def test_change_processor_test(self):
        self.driver.get('http://127.0.0.1:8000/frontend/')
        # click on element with id="PROCESOR"
        element = self.driver.find_element(By.NAME, 'PROCESOR')
        element.click()
        # assert that the "mcs51" button is present on the page
        element = self.driver.find_element(By.ID, 'mcs51')
        self.assertNotEqual(element, None)
        # click on element with id="mcs51"
        element = self.driver.find_element(By.ID, 'mcs51')
        element.click()
        # click on element with id="ZALEŻNE-mcs51"
        element = self.driver.find_element(By.NAME, 'ZALEŻNE-mcs51')
        element.click()
        # click on element with id="--mmodel-small"
        element = self.driver.find_element(By.ID, '--mmodel-small')
        element.click()
        


    def test_change_compiler_options_test(self):
        self.driver.get('http://127.0.0.1:8000/frontend/')
        # click on element with id="OPTYMALIZACJE"
        element = self.driver.find_element(By.NAME, 'OPTYMALIZACJE')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        # assert that the "--nogcse" button is present on the page
        element = self.driver.find_element(By.ID, '--nogcse')
        self.assertNotEqual(element, None)
        # click on element with id="--nogcse"
        element = self.driver.find_element(By.ID, '--nogcse')
        element.click()
        
    

    def test_change_standatd(self):
        self.driver.get('http://127.0.0.1:8000/frontend/')
        # click on element with id="STANDARD"
        element = self.driver.find_element(By.NAME, 'STANDARD')
        # scroll to the element
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # wait for the element to be clickable
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.NAME, 'STANDARD')))
        element.click()
        # assert that the "--std-c99" button is present on the page
        element = self.driver.find_element(By.ID, 'C99')
        self.assertNotEqual(element, None)
        # click on element with id="--std-c99"
        element = self.driver.find_element(By.ID, 'C99')
        element.click()
        



    @classmethod
    def tearDownClass(cls):
        # remove user from database
        User.objects.filter(name='Test User').delete() 
        # click on 


# Create your tests here.
