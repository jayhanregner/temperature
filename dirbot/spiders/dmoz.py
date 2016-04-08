from scrapy.spiders import Spider
from scrapy.selector import Selector

from dirbot.items import Website


class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["weatherforyou.com"]
    days = map(str, ['01', '02', '03', '04', '05', '06', '07', '08', '09', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31])
    months = map(str, ['01', '02', '03', '04', '05', '06', '07', '08', '09', 10, 11, 12])
    years = map(str, range(2011,2017,1))
    stations = ['angeles','antipolo','bacoor','baliuag','binangonan','bulaon','cabanatuan','cainta','calamba','cavite','cebu','clark','dasmarinas','davao','digos','guyong','hagonoy','iba','imus','laoag','lapu-lapu','lipa','mabalacat','mactan','malolos','mandaue','manila','meycauayan','montalban','ninoy+aquino','olongapo','san+fernando','san+jose+del+monte','san+mateo','san+pablo','san+pedro','sangley+point','santa+cruz','santa+rosa','silang','subic+bay+weather+station','tagum','talisay','tanza','tarlac','taytay','toledo','vigan','zamboanga']
    start_urls = []

    for station in stations:
        for year in years:
            for month in months:
                for day in days:
                    url_1 = "http://www.weatherforyou.com/reports/index.php?forecast=pass&pass=archive&zipcode=&pands=&place="
                    url_2 = "&state=&icao=&country=ph&month="
                    url_3 = "&day="
                    url_4 = "&year="
                    url_5 = "&dosubmit=Go"
                    if (int(year) >= 2012):
                        start_urls.append(url_1 + station + url_2 + month + url_3 + day + url_4 + year + url_5)
                    if (int(month) >= 9):
                        start_urls.append(url_1 + station + url_2 + month + url_3 + day + url_4 + year + url_5)
                    if ((int(month) == 8) & (int(day) >= 3)):
                        start_urls.append(url_1 + station + url_2 + month + url_3 + day + url_4 + year + url_5)

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        try:
            sel = Selector(response)
            item = Website()
            item['station'] = sel.xpath('//div[@id = "middlepagecontent"]/div/div/span[@class="headerText"]/text()').extract()[0]
            item['month'] = sel.xpath('//tr/td[@valign="top"]/form/select[@name="month"]/option[@selected]/text()').extract()[0]
            item['day'] = sel.xpath('//tr/td[@valign="top"]/form/select[@name="day"]/option[@selected]/text()').extract()[0]
            item['year'] = sel.xpath('//tr/td[@valign="top"]/form/select[@name="year"]/option[@selected]/text()').extract()[0]
            item['time'] = sel.xpath('//tr/td[@valign="top"]/table/tr/td[1]/span/text()').extract()
            item['weather'] = sel.xpath('//tr/td[@valign="top"]/table/tr/td[2]/span/text()').extract()
            old_temp = sel.xpath('//tr/td[@valign="top"]/table/tr/td[3]/span/text()').extract()
            new_temp = []
            for temp in old_temp:
                new_temp.append(temp[temp.find("/")+1:temp.find("C")-1])
            item['temperature'] = new_temp
            old_dew = sel.xpath('//tr/td[@valign="top"]/table/tr/td[4]/span/text()').extract()
            new_dew = []
            for dew in old_dew:
                new_dew.append(dew[dew.find("/")+1:dew.find("C")-1])
            item['dewpoint'] = new_dew
            item['humidity'] = sel.xpath('//tr/td[@valign="top"]/table/tr/td[5]/span/text()').extract()
            item['winds'] = sel.xpath('//tr/td[@valign="top"]/table/tr/td[7]/span/text()').extract()
            yield item
        except IndexError as e:
            return
