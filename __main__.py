from ebay.utils import set_config_file
from ebay.finding import findItemsAdvanced

import json
import web
import re

set_config_file("ebay.apikey")

urls = (
    '/','list'
)

render = web.template.render('templates/',base='base',globals={
})

class list:
    def GET(self):
        response = json.loads(findItemsAdvanced(
            keywords='lego lbs -mega -manual -instruction',
            sortOrder = 'EndTimeSoonest',
        ))
        
        page = response['findItemsAdvancedResponse'][0]
        results = page['searchResult'][0]
        items = results['item']

        lbs_match = re.compile('.*?([0-9\.\- ]+)[ +]*(lb|pound)',re.I)
        
        items_list = []

        for item in items:
            item['price'] = item['sellingStatus'][0]['currentPrice'][0]['__value__']
            item['title'] = item['title'][0].lower()
            item['title'] = item['title'].replace('lego','LEGO')
            
            for frac in [('1/4','.25'),('1/2','.5'),('3/4','.75')]:
                item['title'] = item['title'].replace(' ' + frac[0],frac[1])
                item['title'] = item['title'].replace(frac[0],frac[1])
            
            # End Time
            item['end_time'] = item['listingInfo'][0]['endTime'][0]
            item['end_time'] = item['end_time'].replace('T',' ')
            item['end_time'] = item['end_time'].replace('.000Z','')
            
            # Weight
            try:
                item['weight'] = lbs_match.match(item['title'].replace(' to ','-')).group(1)
                item['weight'] = item['weight'].split('-')[0]
            except:
                item['weight'] = None
            
            # Shipping
            try:
                item['shipping_type'] = item['shippingInfo'][0]['shippingType'][0]
                
                if item['shipping_type'] == 'Calculated':
                    # Rough estimate, could use GetShippingCosts for higher accuracy
                    item['shipping_price'] = float(item['weight']) * 3.49
                else:
                    item['shipping_price'] = item['shippingInfo'][0]['shippingServiceCost'][0]['__value__']
            except:
                item['shipping_price'] = None
            
            # Price
            try:
                item['total_price'] = float(item['shipping_price']) + float(item['price'])
                item['price_per_pound'] = item['total_price'] / float(item['weight'])
                item['price_per_pound'] = "%.2f" % item['price_per_pound']
            except:
                item['total_price'] = None
                item['price_per_pound'] = None
            
            if item['price_per_pound'] and float(item['price_per_pound']) < 10.0:
                items_list.append(item)
            
        return render.list(items_list)

if __name__ == "__main__":
    app = web.application(urls, globals())

    # Just dump to stdout
    b = app.browser()
    b.open('/')
    print b.get_soup().body.div.prettify()