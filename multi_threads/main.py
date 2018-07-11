import argparse
from base.general_spider import generalSpider

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please choose the type you want crawl')
    parser.add_argument('--url',action = 'store_true',help='url spider')
    parser.add_argument('--sku',action = 'store_true',help='sku spider')
    args = parser.parse_args()
    # print(args.sku)
    if args.sku:
        p = generalSpider()
        p.main('sku')
    elif args.url:
        p = generalSpider()
        p.main('url')