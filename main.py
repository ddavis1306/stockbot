#!/usr/bin/env/ python3
from config import api_key

from bestbuy.apis import BestBuy
bb = BestBuy(api_key)
#a_prod = bb.ProductAPI.search(query="sku=6514052", format="json")
a_prod = bb.ProductAPI.search_by_sku(sku=6514052)
bb.ProductAPI.search(searchTerm="hard drive", onSale="true")
bb.StoreAPI.search_by_city(city="Atlanta")
bb.CategoryAPI.search_by_category_id(category_id="abcat0011001")
print(bb.BestBuy.search_by_sku(sku=6514052))
