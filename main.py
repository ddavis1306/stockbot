#/usr/bin/env/ python3
import config

from twython import Twython, TwythonError

# create a Twython object by passing the necessary secret passwords
twitter = Twython(config.api_key, config.api_secret, config.access_token, config.token_secret)



from bestbuy.apis import BestBuy
bb = BestBuy(api_key)
    
bb.ProductAPI.search_by_sku(sku=9776457)
bb.ProductAPI.search(searchTerm="hard drive", onSale="true")
bb.StoreAPI.search_by_city(city="Atlanta")
bb.CategoryAPI.search_by_category_id(category_id="abcat0011001")