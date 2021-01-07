import requests,threading,random,time,os,json,ctypes
from colorama import Fore
os.system("cls")
print(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}ClothingStealer made by {Fore.WHITE}Walter{Fore.LIGHTBLACK_EX} | Licensed under {Fore.WHITE}MIT {Fore.LIGHTBLACK_EX}License")
print(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Discord: {Fore.WHITE}Walter#7772")
groupid = input(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}GroupID: {Fore.WHITE}")
config = json.load(open("config.json", encoding="UTF-8"))
ids = []
done = []
def status():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f"ClothingStealer | Left To Steal: {len(ids)} | Stole: {len(done)-len(ids)}")
for _ in range(1):
    threading.Thread(target=status).start()
if os.path.exists("Shirts") == False:
    os.makedirs("Shirts")
if os.path.exists("Pants") == False:
    os.makedirs("Pants")
def idsleecher(groupid):
    cursor=""
    global ids
    while True:
        try:
            data = requests.get(f"https://catalog.roblox.com/v1/search/items?category=Clothing&creatorTargetId={groupid}&creatorType=Group&cursor={cursor}&limit=100&sortOrder=Desc&sortType=Updated").json()
            cursor = data['nextPageCursor']
            for x in data['data']:
                if x['id'] not in done:
                    ids.append(x['id'])
                    done.append(x['id'])
        except Exception as e:
            if cursor == None:
                print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Leeched all {Fore.WHITE}Id's")
                break


def steal():
    while True:
        try:
            if ids:
                assetid = ids.pop()
                print(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Stealing ID: {Fore.WHITE}{assetid}")
                dataa = requests.get(f"http://api.roblox.com/Marketplace/ProductInfo?assetId={assetid}").json()
                name = dataa["Name"]
                if dataa['AssetTypeId'] == 11:
                    type="Shirts"
                elif dataa['AssetTypeId'] == 12:
                    type="Pants"
                templateid=(requests.get(f"https://assetdelivery.roblox.com/v1/asset/?id={assetid}").text.split("?id=")[1].split("</url>")[0])
                imageurl = requests.get(f"https://assetdelivery.roblox.com/v1/assetId/{templateid}").json()['location']
                image = requests.get(imageurl).content
                try:
                    open(f"{type}/{name}.png","wb").write(image)
                    if not os.stat(f"{type}/{name}.png").st_size > 8500:
                        os.remove(f"{type}/{name}.png")
                        print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Banned/Bad Template: {Fore.WHITE}{assetid}")
                    else:
                        print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Stole asset: {Fore.WHITE}{name}{Fore.LIGHTBLACK_EX} | ID: {Fore.WHITE}{assetid}")
                except Exception as e:
                    open(f"{type}/{type}{random.randint(5,500000)}.png","wb").write(image)
        except Exception as e:
            print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Error has occurred | stored in {Fore.WHITE}errors.txt")
            open("errors.txt","a").write(f"{str(e)}\n")

for _ in range(1):
    threading.Thread(target=idsleecher,args=[groupid]).start()
for _ in range(config['stealer_threads']):
    threading.Thread(target=steal).start()
