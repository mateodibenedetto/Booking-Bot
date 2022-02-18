''' Este archivo va a contener una clase con metodos para instanciar.
Los cuales van a ser responsables de interactuar con nuestro sitio luego de tener algunos resultados para aplicar lod filtros'''

from selenium.webdriver.remote.webdriver import WebDriver

class BookingFiltration:
    def __init__(self, driver:WebDriver): # driver:WebDrive le estamos indicando el tipo de datos que va a ser el parametro
        self.driver = driver
        
    def apply_star_rating(self, *stars): # * = pasar muchos argumentos atraves de uno
        star_filtration_box = self.driver.find_element_by_css_selector('div[data-filters-group="class"]')
        star_child_elements = star_filtration_box.find_elements_by_css_selector('*')
        
        for star_value in stars:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} estrellas': # strip() = trim()
                    star_element.click()
                    
                    
    def sort_price_lower_first(self):
        element = self.driver.find_element_by_css_selector(
            'li[data-id="price"]'
        )
        element.click()
        