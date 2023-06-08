#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

KEYWORDS = ["超声成像", "超声微泡", "纳米医学", "超声响应", "颈动脉易损斑块", "脑卒中"]
RESULT = {}


def search_polysemant_link(browser, keyword, link, links):
    has_polysemant = False
    js = "window.open('{}','_blank');"
    browser.execute_script(js.format(link))
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    #time.sleep(3)
    try:
        polysemant_list = browser.find_element(By.CLASS_NAME, 'polysemant-list-lemma-title')
        if polysemant_list:
            items = browser.find_elements(By.CLASS_NAME, 'item')
            for item in items:
                sub_title = item.find_element(By.TAG_NAME, 'a').get_attribute("title")
                sub_href = item.find_element(By.TAG_NAME, 'a').get_attribute("href")
                if sub_title and sub_href and "医" in sub_title and sub_title not in links.keys():
                    links[keyword + "-" + sub_title] = sub_href
                    has_polysemant = True
    except:
        pass

    browser.close()
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    return has_polysemant


class Search_Baidu:
    def __init__(self):  # 类构造函数，用于初始化selenium的webdriver
        url = 'https://www.baidu.com/'  # 这里定义访问的网络地址
        self.url = url

        options = webdriver.ChromeOptions()
        # options.add_experimental_option("prefs",
        #                                 {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        # 这里使用chrome浏览器，而且使用我们刚才安装的webdriver_manager的chrome driver，并赋值上面的浏览器设置options变量
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s，由于自动化需要等待网页控件的加载，所以这里设置一个默认的等待超时，时长为10秒

    def tear_down(self):
        self.browser.close()  # 最后，关闭浏览器

    def search_links(self, keyword):
        # 打开百度网页
        self.browser.get(self.url)
        # 等待搜索框出现，最多等待10秒，否则报超时错误
        search_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="kw"]')))
        # 在搜索框输入搜索的关键字
        search_input.send_keys(keyword)
        # 回车
        search_input.send_keys(Keys.ENTER)
        # 等待10秒钟
        self.browser.implicitly_wait(8)
        # 找到所有的搜索结果
        results = self.browser.find_elements(By.CSS_SELECTOR, ".t a , em , .c-title-text")
        # 遍历所有的搜索结果
        links = {}
        for result in results:
            try:
                # 搜索结果的标题
                title = result.get_attribute("text").strip()
                # 搜索结果的网址
                link = result.get_attribute("href")
            except:
                continue
            if link:
                if "百度百科" in title:
                    # print(title, ":", link)
                    # 查找同义词链接
                    if search_polysemant_link(self.browser, keyword, link, links) is False:
                        links[title] = link

        #print("links:", links)
        return links

    def search(self, links):
        # print("开始搜索信息...")
        for title, link in links.items():
            print("搜索:", title)
            js = "window.open('{}','_blank');"
            self.browser.execute_script(js.format(link))
            handles = self.browser.window_handles
            self.browser.switch_to.window(handles[-1])
            # TODO: work
            results = self.browser.find_elements(By.CSS_SELECTOR, ".t a , em , .c-title-text")
            key_flag = False
            lemma = None
            for result in results:
                try:
                    lemma_desc = result.find_element(By.XPATH, "//div[@class='lemma-desc']").text
                    if lemma and lemma == lemma_desc:
                        continue
                    print("职业：", lemma_desc)
                    if "医" not in lemma_desc:
                        print("非医药领域专家")
                        break
                    lemma = lemma_desc
                except:
                    pass

                # try:
                #     h2s = result.find_elements(By.XPATH, "//h2")
                #     h2s = [h.text for h in h2s]
                #     if "研究方向" not in h2s:
                #         print("无研究方向")
                #         break
                # except:
                #     pass
                try:
                    paras = result.find_elements(By.XPATH, "//div[@class='para']")
                except:
                    paras = []
                if paras:
                    for para in paras:
                        for key in KEYWORDS:
                            if key in para.text:
                                print("查询到关键字:", key)
                                RESULT[title + "-" + key] = link
                                with open("search_result_tmp.txt", "a+") as file:
                                    file.write("标题: {}, 链接: {} \n".format(title + "-" + key, link))
                                key_flag = True
                                break
                        if key_flag:
                            break
                if key_flag:
                    break
            if key_flag is False:
                print("未查询到关键字")
            self.browser.close()
            self.browser.switch_to.window(handles[-2])


if __name__ == "__main__":
    #names = "卜军，艾连中，安少辉，安渊，敖华飞，白辰光，白林泉，白志山，鲍晓荣，毕庆员，蔡立志，蔡亮，蔡全才，蔡忠勇，曹广文，曹贵平，曹恒，曹俊诚，曹旭妮，曹颖瑛，曾和平，曾小勤，常时新，车焱，陈爱华，陈斌，陈彩莲，陈德来，陈方，陈红宇，陈华江，陈剑华，陈江野，陈立侨，陈洛南，陈曼，陈能，陈平平，陈盛，陈思宇，陈涛，陈廷，陈彤，陈万生，陈玺，陈向芳，陈向军，陈晓川，陈晓东，陈一民，陈仪香，陈银广，陈雨，陈悦婷，陈增爱，陈振民，陈志钢，程登峰，程金科，程晋，程树群，楚文海，崔国民，崔杰峰，代智，戴宁，单成祥，邓本强，邓春晖，邓勇辉，刁永发，丁彬，丁芳宝，丁和远，丁红，丁健青，丁晶，董健，董文心，董彦君，董艳，杜朝辉，杜大军，杜建忠，杜晶，杜巧玲，杜荣，杜玉珍，段俊生，范慧敏，范列英，范同祥，方从启，方兰，方宁远，方晓生，房永征，冯传良，冯纯，冯瑞，冯世进，冯志勇，奉建芳，奉树成，付新，傅德良，傅乐峰，傅志泉，甘礼华，高春芳，高锋，高华，高建华，高乃平，高玉竹，高振锋，葛先辉，龚海梅，龚景海，龚尚庆，龚士良，龚学庆，龚学忠，龚毅，顾冬云，顾金楼，顾卫琼，顾幸生，顾勇，关佶红，关明，管剑龙，管阳太，管一晖，归琳，桂有珍，郭非凡，郭美丽，郭其一，郭玮，郭兴明，郭旭光，郭耘，郭振红，海舰，韩华，韩继红，韩力，韩林，韩燕，韩昱晨，郝矿荣，郝沛，何谷峰，何剑锋，何丽，何敏娟，何纳，何玉安，何振娟，贺樑，贺文智，侯健，侯尚伟，胡宝洋，胡波，胡传平，胡国汉，胡国宏，胡钧，胡良剑，胡林峰，胡乃红，胡伟达，胡彦杰，胡耀敏，胡志前，花强，黄典贵，黄富强，黄行许，黄吉平，黄建民，黄军海，黄霖，黄鹏羽，黄清海，黄庆安，黄蔚，黄晓宇，黄萱菁，黄勇平，黄远东，惠利健，霍莉莉，季红斌，贾建军，贾金锋，贾能勤，贾薇，贾伟平，贾鑫明，贾运滨，贾真，江浩，江来，江玉海，姜达，姜红，姜虹，姜立新，姜林娣，姜小清，姜雪峰，姜育刚，姜政，蒋轶，解晶莹，金立伦，金庆辉，金石琦，金贤敏，金震东，靳令经，荆杰泰，景贵飞，阚海斌，康九红，孔祥银，寇春海，寇煦丰，郎美东，郎万中，黎立新，黎占亭，李爱民，李斌，李冰，李超伦，李大力，李冬，李福彬，李刚，李昊，李和兴，李鹤，李红波，李怀芳，李辉，李吉平，李继安，李江，李江(探索类)，李晶，李景广，李军，李克勇，李敏，李铭，李琦芬，李荣斌，李儒新，李润平，李善群，李卫东，李文，李霞，李向清，李小平，李晓波，李效民，李欣欣，李秀珍，李轩，李延红，李雁，李扬，李亦学，李永军，李永生，李勇平，李元春，李跃华，廉井财，梁婉琪，梁晓华，廖玮，林春，林光武，林厚文，林丽，林绍梁，林天全，林文松，林羿，刘炳亚，刘春，刘道军，刘锋，刘国华，刘海峰，刘海林，刘洪，刘建华，刘建胜，刘金龙，刘堃，刘丽兰，刘鲁明，刘琦，刘清华，刘善荣，刘士远，刘世勇，刘天西，刘锡平，刘小龙，刘星光，刘旭，刘学超，刘亚男，刘要稳，刘永忠，刘宇，刘月明，刘长虹，刘志伟，刘忠堂，刘祖德，柳建设，龙亿涛，卢洪洲，卢伟，陆尔奕，陆国才，陆灏，陆嘉惠，陆建平，陆琦，罗成，罗维，罗学廷，罗正鸿，罗智坚，罗佐杰，吕凡，吕森林，吕志前，马缚龙，马晓芃，毛志勇，茅凯黎，梅天胜，梅永丰，孟志强，苗茂华，缪长虹，倪鑫，宁志军，牛玉刚，钮月萍，欧阳波，潘良文，潘秋辉，潘巍峻，潘炜华，潘裕柏，庞拂飞，裴艳中，彭晨，彭慧胜，彭俊彪，彭清，浦鸿汀，钱风雷，钱昆，钱平，钱夕元，钱旭红，钱跃竑，乔洁，乔信起，秦厚荣，秦燕，邱惠斌，邱卫东，曲乐丰，曲新凯，曲选辉，任建兴，任捷，任涛，荣绍丰，阮昊，阮仁良，邵成浩，邵雷，邵莉，邵振，邵正中，邵志敏，邵宗平，沈峰，沈锋，沈甫明，沈红斌，沈洪兴，沈坤炜，沈纳，沈庆涛，沈文忠，沈亚领，沈跃栋，沈赞，师咏勇，施斌，施建蓉，石铁流，石毅，石忠锐，时玉舫，史萍，史玉玲，侍洪波，束成钢，水雯箐，宋力昕，宋利格，苏冰，苏良碧，苏晓，苏永华，苏志军，苏洲，隋国栋，孙兵，孙道远，孙瑞涛，孙树林，孙希文，孙晓东，孙衍刚，孙艺华，孙勇伟，孙蕴伟，孙真荣，他得安，谭敏佳，谭学军，谭砚文，汤建平，汤学华，唐峰，唐功利，唐漾，唐赟，陶敏芳，陶晓峰，陶有山，滕银成，田雪莹，童维勤，万文杰，汪登斌，汪福顺，汪海东，汪午，汪锡金，汪长春，王兵，王昌惠，王春瑞，王德平，王芳，王冠，王瀚漓，王昊阳，王浩，王贺瑶，王红梅，王红艳，王惠杰，王继光，王建波，王建华，王建宇，王剑，王久林，王立峰，王连军，王梁华，王琳，王梅，王美华，王梦灵，王敏，王群山，王如彬，王瑞，王胜，王胜昌，王松坡，王廷云，王文昭，王献忠，王小平，王兴军，王学生，王雅杰，王亚宜，王野平，王依婷，王莹，王营冠，王永刚，王瑜珺，王雨田，王玉东，王玉龙，王远弟，王震虹，王志敏，王祝萍，王铸钢，危辉，危平，韦烨，魏东芝，魏国亮，温家洪，温玉刚，吴成铁，吴德升，吴凡，吴国华，吴华香，吴建民，吴健平，吴杰，吴立刚，吴敏，吴强，吴泰志，吴婉莹，吴伟，吴义政，武多娇，武志祥，席芊，夏保佳，夏明，夏涛，夏韵，向明亮，肖建如，肖俊杰，肖明，肖仰华，谢东，谢雷东，谢晓峰，谢晓明，谢幼华，谢玉才，熊辉明，胥明，徐晨，徐大春，徐丰，徐海光，徐海萍，徐辉雄，徐雷鸣，徐美华，徐庆，徐彦辉，徐洋，徐烨，许传亮，许大康，许洪卫，许华，许建荣，许平，许青，许硕贵，许政敏，薛罡，薛燕陵，薛纭，严怀成，严军，严望军，颜宏利，颜新，羊亚平，杨东，杨海芸，杨慧娟，杨杰，杨金虎，杨立群，杨立桃，杨珉，杨庆诚，杨松旺，杨婉花，杨小虎，杨奕清，杨永，杨勇生，杨宇，杨志，尧德中，姚建忠，姚天明，姚薇，姚原，叶定伟，叶海峰，叶林，叶属峰，易诚青，易红良，易建军，易志国，殷峻，尹峰，尹周平，由文辉，游波，于红，于洪斌，于靖，于随然，于文强，余宏宇，余金明，余金培，余学斌，余优成，俞继卫，俞麟，俞文杰，俞雄，虞先濬，虞心红，郁玮玮，袁非，袁逖飞，袁卫平，袁友禄，袁政，原三领，原一高，翟琦巍，詹黎，詹帅，詹玉林，战兴群，张超，张朝云，张辰，张大军，张登松，张蝶青，张东民，张昉，张国军，张国柱，张洪信，张华，张家华，张建华，张杰，张洁，张军，张玲霞，张铭，张强，张青红，张庆华，张涛，张文，张文川，张文驹，张晓玲，张学渊，张琰，张艳梅，张焱，张燕捷，张冶文，张益，张毅，张永刚，张勇，张羽，张玉忠，张育才，章健，章璞，章序文，赵晖，赵婧，赵晓祥，赵学，赵延欣，赵长印，郑华军，郑嘹赢，郑平，郑向鹏，郑循江，郑莹，郑正奇，钟超，钟春玖，钟大放，钟建江，钟萍，钟一声，周斌，周常河，周光文，周海文，周洁，周琳，周平玉，周倩，周胜，周婷，周祥山，周晓东，周选围，周永丰，周永新，周裕德，朱冬生，朱国行，朱焕乎，朱杰，朱静吟，朱科明，朱南文，朱睿，朱申敏，朱新远，朱钰方，朱志荣，朱自强，祝德秋，祝迎春，庄启昕，庄晓莹，邹豪，邹建新，邹俊，左建勇，左曙光"
    names = "邓本强，胡波，胡国汉，曲乐丰，王继光，王敏，王群山，王如彬，王瑞，王胜，王胜昌，王松坡，王廷云，王文昭，王献忠，王小平，王兴军，王学生，王雅杰，王亚宜，王野平，王依婷，王莹，王营冠，王永刚，王瑜珺，王雨田，王玉东，王玉龙，王远弟，王震虹，王志敏，王祝萍，王铸钢，危辉，危平，韦烨，魏东芝，魏国亮，温家洪，温玉刚，吴成铁，吴德升，吴凡，吴国华，吴华香，吴建民，吴健平，吴杰，吴立刚，吴敏，吴强，吴泰志，吴婉莹，吴伟，吴义政，武多娇，武志祥，席芊，夏保佳，夏明，夏涛，夏韵，向明亮，肖建如，肖俊杰，肖明，肖仰华，谢东，谢雷东，谢晓峰，谢晓明，谢幼华，谢玉才，熊辉明，胥明，徐晨，徐大春，徐丰，徐海光，徐海萍，徐辉雄，徐雷鸣，徐美华，徐庆，徐彦辉，徐洋，徐烨，许传亮，许大康，许洪卫，许华，许建荣，许平，许青，许硕贵，许政敏，薛罡，薛燕陵，薛纭，严怀成，严军，严望军，颜宏利，颜新，羊亚平，杨东，杨海芸，杨慧娟，杨杰，杨金虎，杨立群，杨立桃，杨珉，杨庆诚，杨松旺，杨婉花，杨小虎，杨奕清，杨永，杨勇生，杨宇，杨志，尧德中，姚建忠，姚天明，姚薇，姚原，叶定伟，叶海峰，叶林，叶属峰，易诚青，易红良，易建军，易志国，殷峻，尹峰，尹周平，由文辉，游波，于红，于洪斌，于靖，于随然，于文强，余宏宇，余金明，余金培，余学斌，余优成，俞继卫，俞麟，俞文杰，俞雄，虞先濬，虞心红，郁玮玮，袁非，袁逖飞，袁卫平，袁友禄，袁政，原三领，原一高，翟琦巍，詹黎，詹帅，詹玉林，战兴群，张超，张朝云，张辰，张大军，张登松，张蝶青，张东民，张昉，张国军，张国柱，张洪信，张华，张家华，张建华，张杰，张洁，张军，张玲霞，张铭，张强，张青红，张庆华，张涛，张文，张文川，张文驹，张晓玲，张学渊，张琰，张艳梅，张焱，张燕捷，张冶文，张益，张毅，张永刚，张勇，张羽，张玉忠，张育才，章健，章璞，章序文，赵晖，赵婧，赵晓祥，赵学，赵延欣，赵长印，郑华军，郑嘹赢，郑平，郑向鹏，郑循江，郑莹，郑正奇，钟超，钟春玖，钟大放，钟建江，钟萍，钟一声，周斌，周常河，周光文，周海文，周洁，周琳，周平玉，周倩，周胜，周婷，周祥山，周晓东，周选围，周永丰，周永新，周裕德，朱冬生，朱国行，朱焕乎，朱杰，朱静吟，朱科明，朱南文，朱睿，朱申敏，朱新远，朱钰方，朱志荣，朱自强，祝德秋，祝迎春，庄启昕，庄晓莹，邹豪，邹建新，邹俊，左建勇，左曙光"
    name_list = names.split("，")
    search = Search_Baidu()
    for name in name_list:
        links = search.search_links(name)
        if links:
            search.search(links)
    search.tear_down()
    # links = search.search_links("卜军")
    # search.search(links)
    # search.tear_down()

    print("最终名单", RESULT)
    with open("search_result.txt", "w") as file:
        for name, link in RESULT.items():
            file.write(f"Name: {name}, link is: {link} \n")
