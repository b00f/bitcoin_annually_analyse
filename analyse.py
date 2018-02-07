"""
analyse bitcoin price from CSV data based on blockchain.info's data (not 100% accurate, especially before 2010)
"""

import urllib2

turl = "https://blockchain.info/charts/market-price?showDataPoints=false&timespan=all&show_header=true&daysAverageString=1&scale=0&format=csv&address="

s = urllib2.urlopen(turl).read()

with open('btcdata.csv','w') as f:
    f.write(s)


def getd():
    with open('btcdata.csv','r') as f:
        lines = f.readlines()
        
    return lines

def avgc(li):
    s = sum(li[:])
    r = s/len(li)
    return r

def print_info(interval = 'm'):
    d = getd()
    count = 0
    sump = 0
    old = 1 if interval == 'm' else 2009
    avglist = list()
    lastavg = None
    price0 = -1
    if interval == 'y':
        print '** BTC yearly price information **'
        print ''
        print 'Year .. Start of year  .. End of year .. Avg for year .. Increase'
    else:
        print '** BTC mothly price information **'
        print ''
        print 'Month .. Start of month  .. End of month .. Avg for month .. Increase'
            
    for x in d[:]:
        x = x.replace('\n','')
        date,price = x.split(',')
        price = float(price)
        nt = date.split(' ')[0]
        if price == 0.0: continue
        if price0 == -1: price0 = price
        y,m,d = nt.split('-')
        avglist.append(price)
        the_interval = m if interval == 'm' else y
        if the_interval != old: 
            avgy = avgc(avglist)
            incr = 0
            if lastavg != None:
                incr = avgy/lastavg
                lastavg = avgy
            else:
                lastavg = avgy
            
            if interval == 'y':
                print old,'  ','{:>10}'.format("%.2f" % round(price0,2)),'{:>14}'.format("%.2f" % round(price,2)),'  ','{:>12}'.format("%.2f" % round(avgy,2)),'  ','{:>10}'.format("%.2f" % round(incr,2))
            else:
                if m == '01':
                   print ''
                print '{}-{}'.format(y, m),'  ','{:>10}'.format("%.2f" % round(price0,2)),'{:>14}'.format("%.2f" % round(price,2)),'  ','{:>12}'.format("%.2f" % round(avgy,2)),'  ','{:>10}'.format("%.2f" % round(incr,2))
            
            price0 = -1
            old = the_interval
            avglist = list()

        sump += price
        count+=1
    
    print '\n\n'

print_info('y')
print_info('m')
