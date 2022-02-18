import booking.constants as const
import os
import time

from selenium import webdriver
from booking.booking_filtros import BookingFiltration

''' Clase que hereda todos los metodos de webdriver.Chrome'''
class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/Users/Mateo/Desktop/Selenuim/Drivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] = self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    # Salir del sitio
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    # Abrir el sitio
    def land_first_page(self):
        self.get(const.BASE_URL)

    # Cambiar la moneda
    def cambiar_moneda(self, moneda=None):
        monedaEl = self.find_element_by_css_selector(
            'button[data-tooltip-text="Elegir la moneda"]'
        )
        monedaEl.click()
        moneda_seleccionadaEl = self.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={moneda}"]'
        )
        moneda_seleccionadaEl.click()
    
    # Seleccionar destino
    def seleccionar_destino(self, destino):
        campo_destino = self.find_element_by_id('ss')
        campo_destino.clear() # Limpia el input
        campo_destino.send_keys(destino)
        
        primer_res = self.find_element_by_css_selector(
            'li[data-i="0"]'
        )
        primer_res.click()
        
    # Seleccionar Check-in y Check-out
    def seleccionar_fecha(self, check_in, check_out):            
        check_inEl = self.find_element_by_css_selector(
            f'td[data-date="{check_in}"]'
        )
        check_inEl.click()
        
        check_outEl = self.find_element_by_css_selector(
            f'td[data-date="{check_out}"]'
        )
        check_outEl.click()
        
    # Seleccionar Adultos
    def seleccionar_adultos(self, num=1):
        adultoEl = self.find_element_by_id('xp__guests__toggle')
        adultoEl.click()
        
        # Restar personas hasta el minimo para que esté en el minimo y de ahí aumentar
        while True:
            decrementar_adultoEl = self.find_element_by_css_selector(
                'button[aria-label="Reducir cantidad de Adultos"]'
            )
            
            decrementar_adultoEl.click()
            # Si el valor de adultos llega a 1 hay que salir del while
            valor_adultosEl = self.find_element_by_id('group_adults')
            valor_adultos = valor_adultosEl.get_attribute('value') # Devuelve la cantidad de adultos
            if int(valor_adultos) == 1:
                break
        
        aumentar_adultoEl = self.find_element_by_css_selector(
            'button[aria-label="Aumentar cantidad de Adultos"]'
        )
        
        for _ in range(num - 1):
            aumentar_adultoEl.click()
            
    # Seleccionar Habitaciones
    def seleccionar_habitaciones(self, num=1):
        # Restar personas hasta el minimo para que esté en el minimo y de ahí aumentar
        while True:
            decrementar_habitacionEl = self.find_element_by_css_selector(
                'button[aria-label="Reducir cantidad de Habitaciones"]'
            )
            
            decrementar_habitacionEl.click()
            # Si el valor de habitaciones llega a 1 hay que salir del while
            valor_habitacionEl = self.find_element_by_id('no_rooms')
            valor_habitacion = valor_habitacionEl.get_attribute('value') # Devuelve la cantidad de habitaciones
            if int(valor_habitacion) == 1:
                break
        
        aumentar_habitacionEl = self.find_element_by_css_selector(
            'button[aria-label="Aumentar cantidad de Habitaciones"]'
        )
        
        for _ in range(num - 1):
            aumentar_habitacionEl.click()
          
    # Apretar boton
    def click_button(self):
        search_button = self.find_element_by_css_selector(
            'button[type="submit"]'
        )        
        search_button.click()
    
    # Aplicar los filtros
    def aplicar_filtros(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        time.sleep(2)
        filtration.sort_price_lower_first()
        
    # Ingresar al destino
    def ingresar_destino(self):
        btn = self.find_element_by_css_selector('a[role="button"]')
        btn.click()