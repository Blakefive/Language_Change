from pynput.keyboard import Listener, Key
import pyautogui
import pyperclip
from hangul_utils import split_syllables, join_jamos
import time
 
store = set()
store2 = set()
check1 = set([Key.shift_r,Key.home])
check2 =set([Key.shift,Key.esc])
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
KoreanToEnglishchange = {'ㄳ':'rt','ㄵ':'sw','ㄶ':'sg','ㄺ':'fr','ㄻ':'fa','ㄼ':'fq','ㄽ':'ft','ㄾ':'fx','ㄿ':'fv','ㅀ':'fg','ㅄ':'qt','ㅒ':'o','ㅖ':'p','ㅘ':'hk','ㅙ':'ho','ㅚ':'hl','ㅝ':'nj','ㅞ':'np','ㅟ':'nl','ㅢ':'ml','ㅂ':'q','ㅈ':'w','ㄷ':'e','ㄱ':'r','ㅅ':'t','ㅃ':'Q','ㅉ':'W','ㄸ':'E','ㄲ':'R','ㅆ':'T','ㅛ':'y','ㅕ':'u','ㅑ':'i','ㅐ':'o','ㅔ':'p','ㅁ':'a','ㄴ':'s','ㅇ':'d','ㄹ':'f','ㅎ':'g','ㅗ':'h','ㅓ':'j','ㅏ':'k','ㅣ':'l','ㅋ':'z','ㅌ':'x','ㅊ':'c','ㅍ':'v','ㅠ':'b','ㅜ':'n','ㅡ':'m'}
EnglishToKoreanchange = {'O':'ㅒ','P':'ㅖ','q':'ㅂ','w':'ㅈ','e':'ㄷ','r':'ㄱ','t':'ㅅ','Q':'ㅃ','W':'ㅉ','E':'ㄸ','R':'ㄲ','T':'ㅆ','y':'ㅛ','u':'ㅕ','i':'ㅑ','o':'ㅐ','p':'ㅔ','a':'ㅁ','s':'ㄴ','d':'ㅇ','f':'ㄹ','g':'ㅎ','h':'ㅗ','j':'ㅓ','k':'ㅏ','l':'ㅣ','z':'ㅋ','x':'ㅌ','c':'ㅊ','v':'ㅍ','b':'ㅠ','n':'ㅜ','m':'ㅡ'}
overlapcheck1 = {'ㄱㅅ':'ㄳ','ㄴㅈ':'ㄵ','ㄴㅎ':'ㄶ','ㄹㄱ':'ㄺ','ㄹㅁ':'ㄻ','ㄹㅂ':'ㄼ','ㄹㅅ':'ㄽ','ㄹㅌ':'ㄾ','ㄹㅍ':'ㄿ,','ㄹㅎ':'ㅀ','ㅂㅅ':'ㅄ'}
overlapcheck2 = {'ㅗㅏ':'ㅘ','ㅗㅐ':'ㅙ','ㅗㅣ':'ㅚ','ㅜㅓ':'ㅝ','ㅜㅔ':'ㅞ','ㅜㅣ':'ㅟ','ㅡㅣ':'ㅢ'}

def listcheck(data):
    check = 0
    for i in JUNGSUNG_LIST:
        if data == i:
            check = 1
    return check

def overlap2(data):
    for i in range(len(data)):
        try:
            checkdata = data[i] + data[i+1]
            checkdata = overlapcheck2[checkdata]
            data = data[:i] + checkdata + data[i+2:]
        except IndexError:
            break
        except KeyError:
            pass
    return data

def overlap1(data):
    data = overlap2(data) + " "
    print(data)
    for i in range(len(data)):
        try:
            checkdata = data[i:i+3]
            if listcheck(checkdata[2]) == 0:
                try:
                    data = data[:i] + overlapcheck1[checkdata[0] + checkdata[1]] + data[i+2:]
                except KeyError:
                    pass
        except IndexError:
            break
    
    return data

def KoreanToEnglish(data):
    data = split_syllables(data)
    finaldata = ""
    for i in data:
        try:
            finaldata += KoreanToEnglishchange[i]
        except KeyError:
            finaldata += i
    return finaldata
    
def EnglishToKorean(data):
    finaldata = ""
    for i in data:
        try:
            finaldata += EnglishToKoreanchange[i]
        except KeyError:
            try:
                finaldata += EnglishToKoreanchange[i.lower()]
            except KeyError:
                finaldata += i
    return (finaldata)

def isEnglishOrKorean(input_s):
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        if ord('ㄱ') <= ord(c) <= ord('ㅎ'):
            k_count += 1
        if ord('ㅏ') <= ord(c) <= ord('ㅣ'):
            k_count += 1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    print("k_count",k_count)
    print("e_count",e_count)
    return "k" if k_count>e_count else "e"

def handleKeyPress( key ):
    if(key == Key.shift_r) or (key == Key.home):
        store.add( key )
        print(store)
    if (key == Key.shift) or (key == Key.esc):
        store2.add(key)
        
def handleKeyRelease( key ):
    if store == check1:
        print("program")
        
        pyautogui.keyDown('shift')
        pyautogui.keyDown('home')
        time.sleep(0.1)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('home')
        
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('c')
        time.sleep(0.1)
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('c')
        time.sleep(0.2)
        
        pyautogui.hotkey('backspace')
        
        data = pyperclip.paste()
        data = split_syllables(data)
        finaldata = ""
        for i in data:
            print("test",isEnglishOrKorean(i))
            if isEnglishOrKorean(i) == 'k':
                finaldata += KoreanToEnglish(i)
                print("check",KoreanToEnglish(i))
            elif isEnglishOrKorean(i) == 'e':
                finaldata += EnglishToKorean(i)
            print(KoreanToEnglish(i)," | ",finaldata," | ",i)
        finaldata =join_jamos(overlap1(finaldata))
        print(finaldata)
        
        pyperclip.copy(finaldata[:len(finaldata)-1])
        pyautogui.hotkey("ctrl","v")
        
        store.remove(Key.shift_r)
        store.remove(Key.home)
    
    if store2 == check2:
        store2.remove(Key.shift)
        store2.remove(Key.esc)
        return False
    
    if key in store:
        store.remove( key )
        
    if key in store2:
        store2.remove( key )
with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()
