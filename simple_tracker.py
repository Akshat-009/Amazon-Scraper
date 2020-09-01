from amazon_config import get_web_driver_options,get_chrome_web_driver,set_ignore_certificate_error,set_browser_as_incognito,NAME,BASE_URL,DIRECTORY,CURRENCY
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime
class Report_Generate:
    def __init__(self,file_name,base_url,currency,data):
        self.data=data
        self.file_name=file_name
        self.base_url=base_url
        self.currency=currency
        report={
            "title":self.file_name,
            "date":self.get_date(),
            "best_item":self.get_best(),
            "base_url":self.base_url,
            "products":self.data
        }
        print("Making a file to store data")
        with open (f'{DIRECTORY}/{file_name}.json','w') as f:
            json.dump(report,f)
        print("done")

    def get_date(self):
        date=datetime.now()
        return date.strftime("%d/%m/%Y %H:%M:%S")
    def get_best(self):
        try:
            return sorted(self.data,key=lambda k :k['price'])
        except Exception as e:
            print(e,"could not get best item")
            return None
class Amazon_connect:
    def __init__(self,search_term,base_url,currency):
        self.search_term=search_term
        self.base_url=base_url
        options=get_web_driver_options()
        set_browser_as_incognito(options)
        set_ignore_certificate_error(options)
        self.driver=get_chrome_web_driver(options)
        self.currency=currency
    def run(self):
        print("Running script")
        print(f"Looking for {self.search_term}")
        links= self.get_product_links()
        # print(links)
        print(f"Got {len(links) } products")
        products= self.get_product_info(links)
        print(f"Got information for {len(products)}")
        time.sleep(2)
        self.driver.quit()
        return products
    def get_product_info(self,links):
        asins=self.get_asins(links)
        products=[]
        for asin in asins:
            product=self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products
    def get_single_product_info(self,asin):
        print(f"Scraping for product id {asin}")
        product_short_url=self.short_product_url(asin)
        self.driver.get(product_short_url)
        time.sleep(2)
        title=self.get_title()
        seller=self.get_seller()
        price=self.get_price()
        if title and seller and price:
            product_info={
                "asin":asin,
                "title":title,
                "url":product_short_url,
                "price":price,
                "seller":seller
            }
            return product_info
        else:
            return None
    def get_title(self):
        try:
            return self.driver.find_element_by_id("productTitle").text
        except Exception as e:
            print(e)
            return None
    def get_seller(self):
        try:
            return self.driver.find_element_by_id("sellerProfileTriggerId").text
        except Exception as e:
            print(e)
            return None
    def get_price(self):
        try:
            price =self.driver.find_element_by_id("priceblock_ourprice").text
            price=self.convert_price(price)
            return price
        except NoSuchElementException:
            try:
                ava=self.driver.find_element_by_id("availability").text
                if "In stock" in ava:
                    price=self.driver.find_element_by_class_name('olp-padding-right').text
                    price=self.convert_price(price)
                    return price
            except Exception as e:
                print(e)
                return None
    def convert_price(self,price):
        new_price=price.replace("\u20b9 ","")
        new_price=new_price.replace(",","")
        new_price=float(new_price)
        return new_price
    def short_product_url(self,asin):
        return self.base_url + "dp/"+ asin
    def get_asins(self,links):
        return [self.get_asin(link) for link in links]
    def get_asin(self,product_link):
        return product_link[product_link.find("/dp/") + 4:product_link.find("/ref")]
    def get_product_links(self):
        self.driver.get(self.base_url)
        element=self.driver.find_element_by_id("twotabsearchtextbox")
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        self.driver.get(self.driver.current_url)
        time.sleep(2)
        result_list = self.driver.find_elements_by_class_name('s-result-list')
        links=[]
        try:
            results = result_list[0].find_elements_by_xpath(
                "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print(e)
            return links
        

if __name__=="__main__":
    print("chaal ro hia")
    amazon_connect=Amazon_connect(NAME,BASE_URL,CURRENCY)
    data=amazon_connect.run()
    Report_Generate(NAME,BASE_URL,CURRENCY,data)
    

    