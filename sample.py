import subprocess
import sys
from time import sleep
from clicknium import clicknium as cc, locator, ui
from clicknium.core.models.web.webelement import WebElement

isSharing = True
myYoutubeChannel = "K7 Studio"

def Swap_AccountInsta(tab: WebElement):
    tab.find_element(locator.instagram.switch_button).click()
    tab.find_element(locator.instagram.switch_k7studiogames).click()


def SwapYoutubeChannel(tab: WebElement):
    print("Swapping youtube account")
    tab.find_element(locator.youtube.button_account).click()
    tab.find_element(locator.youtube.button_change_account).click()
    tab.find_element(locator.youtube.button_k7_account).click()


def GetTab(url: str):
    try:
        tab = cc.chrome.attach_by_title_url(url=f"*{url}*",timeout=3)
    except:
        first_tab = cc.chrome.attach_by_title_url('*')
        tab = first_tab.browser.new_tab(url)
    print("Going to another url!")
    tab.goto(url,is_wait_complete=False)
    sleep(1)
    cc.send_hotkey('{ENTER}')

    return tab

def GetPathAndFile(file_path: str):
    # file_path = r"C:\Users\andre\Documents\WeirdStuff\TikTokUploder\Video\animation.mp4"
    splited =file_path.split('\\')
    if (len(splited) == 1):
            splited = file_path.split('/')
    count = len(splited)
    
    file = splited[count-1]
    # C:\Users\andre\Documents\WeirdStuff\TikTokUploder\Video\  animation.mp4
    return (file_path[:-len(file)],file)


def  ChooseFileToUpload(path: str,file: str):
    #Opens a new tab, select the filename and write the path of the file
    cc.find_element(locator.instagram.edit_file_name).set_text(path,'sendkey-after-click')
    cc.send_hotkey('{ENTER}')
    cc.find_element(locator.instagram.edit_file_name).set_text(file,'sendkey-after-click')
    cc.send_hotkey('{ENTER}')

def ClearTextAndInsert(tab,locator_f,text):
    tab.find_element(locator_f).click(by="mouse-emulation")
    cc.send_hotkey('^a')
    cc.send_hotkey('{BACKSPACE}')
    cc.send_text(text)

########################
#### Main Functions ####
########################

def Upload_Youtube(file_path: str,title: str,description: str):
    (path,file) = GetPathAndFile(file_path)
    tab = GetTab("studio.youtube.com/")
    channel_name = tab.find_element(locator.youtube.text_channel_name).get_text().strip("\n ")
    print("Channel name found -> ",channel_name)
    if (channel_name != myYoutubeChannel):
        SwapYoutubeChannel(tab)

    tab.find_element(locator.youtube.button_create).click()
    tab.find_element(locator.youtube.button_load_videos).click()
    tab.find_element(locator.youtube.button_select_files_button).click(by='mouse-emulation')
    ChooseFileToUpload(path,file)
    #Swap the content of the variable
    ClearTextAndInsert(tab,locator.youtube.div_title,title)
    tab.find_element(locator.youtube.div_description).click(by="mouse-emulation")
    cc.send_text(description)
    tab.find_element(locator.youtube.button_not_for_children).click()
    tab.find_element(locator.youtube.button_next_button).click()
    tab.find_element(locator.youtube.button_next_button1).click()
    tab.find_element(locator.youtube.button_next_button2).click()
    tab.find_element(locator.youtube.div_public).click()
    if (isSharing):
        tab.find_element(locator.youtube.button_publish).click()
        print("Uploaded to youtube with sucess!")



    
    

def Upload_TikTok(file_path: str,description: str):
    (path,file) = GetPathAndFile(file_path)
    tab = GetTab("tiktok.com/creator-center/upload?from=upload")
    tab.find_element(locator.tiktok.button_select_file).click()
    #Choose the correct file
    ChooseFileToUpload(path,file)
    #Wait 30s for the video to fully load...
    for i in range(30):
        description_found = tab.find_element(locator.tiktok.caption).get_text()
        sleep(1)
        
        #It's not empty, therefore the video has sucessfully loaded
        if (description_found != ""):
            break

    ClearTextAndInsert(tab,locator.tiktok.caption,description)
    #Share it
    if (isSharing):
        cc.mouse.scroll(-10)
        tab.find_element(locator.tiktok.button_post).click(by='mouse-emulation')
        print("Uploaded to tiktok with sucess")


    

def Upload_Insta(file_path: str,description: str):
    
    (path,file) = GetPathAndFile(file_path)

    tab = GetTab("instagram.com/")
    # tab = cc.chrome.attach_by_title_url(url="*instagram.com/*")
    # tab.goto("instagram.com/")

    cur_user = tab.find_element(locator.instagram.current_account).get_text()
    print("Current user found -> ",cur_user,flush=True)

    if (cur_user == "amdrepinto42"):
        Swap_AccountInsta(tab)

    #Click on create post
    tab.find_element(locator.instagram.create_post).click()
    tab.find_element(locator.instagram.button_select_from_computer).click()
    
    #Choose the correct file
    ChooseFileToUpload(path,file)

    #Click on ratio and select the crop size
    tab.find_element(locator.instagram.button_select_ratio).click(by='mouse-emulation')
    tab.find_element(locator.instagram.button_9_16_ratio).click(by='mouse-emulation')
    
    #Click next
    tab.find_element(locator.instagram.button_next).click(by='mouse-emulation')
    tab.find_element(locator.instagram.button_next1).click(by='mouse-emulation')
    tab.find_element(locator.instagram.my_caption).set_text(description,'sendkey-after-click')
    
    
    #Share it
    if (isSharing):
        tab.find_element(locator.instagram.button_share).click()
        print("Sent to instagram with sucess")



def Upload():
    args_normal = sys.argv[1]
    flag_youtube = False
    flag_insta = False
    flag_tiktok = False
    if (args_normal[0] == '-'):
        for arg in args_normal:
            if (arg == 'y'):
                flag_youtube = True
            elif (arg == 'i'):
                flag_insta = True
            elif (arg == 't'):
                flag_tiktok = True
        
    file_path = sys.argv[2]
    title = sys.argv[3]
    #Sometimes you don't need a description
    if (len(sys.argv) <= 4):
        description = ""
    else:
        description = sys.argv[4]
    print(f"Received arguments|Flags -> Youtube -> {flag_youtube} Insta -> {flag_insta} TikTok -> {flag_tiktok} |\
          \n Path ->  {file_path} | Title -> {title} | description -> {description}")
    full_description = title + "\n" + description

    if (flag_youtube):
        Upload_Youtube(file_path,title,description)
    if (flag_insta):
        Upload_Insta(file_path,full_description)
    if (flag_tiktok):
        Upload_TikTok(file_path,full_description)

def main():
    Upload()



if __name__ == "__main__":
    main()