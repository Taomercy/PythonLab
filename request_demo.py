# import requests
#
# response = requests.get("http://www.baidu.com/")
# print(response.text)


class Animal(object):

    def drinking(self):
        print('animal drinking')

    def eating(self, food):
        print('animal eating')


class Cat(Animal):

    def drinking(self):
        super().drinking()

    def eating(self, food):
        print("eating %s" % food)


cat = Cat()
cat.drinking()
cat.eating("meat")
