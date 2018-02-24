# coding:utf-8
#Version : 0.2 Beta
#Latest Update:2018-02-24
#


#THIS IS AN UNSTABLE VERSION

#link.txt ʾ����"https://pan.baidu.com/s/xxxx----2333"
#Ŀǰ��֧�ִ���ȡ�����������ת��

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,os,sys

os.system('cls')
# Define Log Moudle
import logging
logFileName = (str(time.ctime())+"_LOG.log").replace(":","-").replace(" ","")
logger = logging.getLogger(__name__)
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler(logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)
#Log Level
logger.setLevel(logging.INFO)#��־����

def findPath(WebDri,URL,destDir):#��ȡת��Ŀ¼
	try:
		isFound = False
		nodePaths = WebDri.find_elements_by_class_name("treeview-txt")
		#debugNodePaths = WebDri.find_elements_by_css_selector("span."+destDir)
		#logger.debug(debugNodePaths)
		logger.debug("[+] nodePaths : %s" % str(nodePaths))
		for item in nodePaths:
			#print item.get_attribute("node-path")
			if (item.get_attribute("node-path") == destDir):
				print ("[+] �ɹ���λĿ���ļ��� : %s " % destDir)
				logger.info("[+] �ɹ���λĿ���ļ��� : %s " % destDir)
				logger.debug("[*] Ŀ���ļ���ԭʼ��Ϣ : %s" % str(item))
				item.click()
				isFound = True
				break
		return isFound
	except:
		logger.exception("[-] �������� : %s" % URL)
		return False

def startTransfer(WebDri,URL,code,destDir):#ת��������
	print ("[*] ���ڻ�ȡ %s ��ȡ�� %s ..." % (URL,code))
	logger.info("[*] ���ڻ�ȡ %s ��ȡ�� %s ...." % (URL,code))
	WebDri.get(URL)
	enterCodeBtn= WebDri.find_elements_by_class_name('g-button-blue-large')
	logger.debug("[*] ȷ����ȡ�밴ťԭʼ��Ϣ : %s" % str(enterCodeBtn))
	codeTextEdit = WebDri.find_elements_by_class_name('LxgeIt')
	logger.debug("[*] ��ȡ�������ԭʼ��Ϣ: %s" % str(codeTextEdit))
	if(codeTextEdit != []):
		codeTextEdit[0].send_keys(list(code))
		logger.debug("[*] ��ȡ�� : %s ������." % code)
		enterCodeBtn[0].click()
	else:
		return False
	try:#��λת�水ť
		time.sleep(4)
		transferBtn = WebDri.find_elements_by_class_name('g-button')
		logger.debug("[*] ת�水ťԭʼ��Ϣ : %s" % str(transferBtn))
		if (transferBtn == []):
			print ("[-] �޷�ת���ļ� %s" % URL)
			logger.warn("[-] Cannot �޷�ת���ļ� %s" % URL)
			return False
		else:
			for item in transferBtn:
				if (item.get_attribute('title') == unicode("���浽����","gb2312")):
					logger.debug("[+] �Ѷ�λת�水ť %s " % str(item))
					logger.info("[+] �Ѷ�λת�水ť")
					item.click()
					break
	except:
		logger.exception("[-] �������� : %s" % URL)
		return False

	try:#�ж��Ƿ��½
		time.sleep(1)
		qrcode = WebDri.find_elements_by_class_name("tang-pass-qrcode-img")
		if (qrcode != []):
			print ("[-] ���ȵ�¼ !!!!!")
			logger.error("No Logon.")
			sys.exit()
	except:
		logger.exception("[-] �������� : %s" % URL)
		return False

	try:#��ʼת��
		time.sleep(2)
		nodeSplitList = destDir.split("/")
		dir = ""
		for i in range(1,len(nodeSplitList)):#ѭ������findPath()��ȷ��ת��Ŀ¼
			dir += ("/"+nodeSplitList[i])
			logger.debug("[*] Current Dir : %s " % dir)
			if findPath(WebDri,URL,dir):
				print ("[+] �ѷ���Ŀ¼ %s" % dir)
				logger.info("[+] �ѷ���Ŀ¼ %s" % dir)
				time.sleep(2)
				continue
			else:
				print ("[-] �޷���λĿ��Ŀ¼ : %s" % dir)
				logger.error("[-] �޷���λĿ��Ŀ¼ : %s ԭʼĿ��Ŀ¼ : %s " % (dir,destDir))
				return False
		pathConfirmBtn = WebDri.find_elements_by_class_name('g-button')
		if pathConfirmBtn == []:
			print ("[-] �޷�ת���ļ� %s" % URL)
			logger.error("[-] �޷�ת���ļ� %s" % URL)
			return False
		for item in pathConfirmBtn:
			if (item.get_attribute('title') == unicode("ȷ��","gb2312")):
				logger.debug("[+] �Ѷ�λת��Ŀ¼ȷ�ϰ�ť %s " % str(item))
				logger.info("[+] �Ѷ�λת��Ŀ¼ȷ�ϰ�ť")
				item.click()
				return True
	except:
		logger.exception("[-] �������� : %s" % URL)
		return False

def login(WebDri):
	WebDri.get("https://pan.baidu.com/")
	print("��¼���̺��뽫ҳ���л�������վ��ȷ����ҳ������Ϻ���ִ����һ��")
	raw_input("[?] ��ȷ�����Ѿ��ɹ���¼����.")
	logger.info("[+] Logon In")
	print ("[+] Logon In")

def main():
	try:
		errorLinkList = []
		gotLinkList = []
		destDir = "/Test/Testt"
		linkList = []
		try:
			with open("link.txt","r") as f:
				linkList = f.readlines()
				f.close()
		except:
			print ("[-] �޷���ָ���ļ�����鿴��־")
			logger.exception("[*] Error On Opening File.")
			return
		print ("[*] ���ҵ� %d ������." % len(linkList))
		logger.info("[*] ���ҵ� %d ������." % len(linkList))
		print("[*] ��������Chrome")
		browser = webdriver.Chrome()
		login(browser)
		for item in linkList:
			item = item.strip()
			URL = item.split("----")[0]
			code = item.split("----")[1][:4]
			print ("[*] ��ʼ�ļ�ת�����")
			logger.info("[*] ��ʼ�ļ�ת�����")
			if (startTransfer(browser,URL,code,destDir) == False):
				errorLinkList.append((URL+"----"+code))
				print ("[-] �������� : %s" % URL)
				logger.error(("[-] �������� : %s" % URL))
			else:
				gotLinkList.append((URL+"----"+code+"\n"))
				print ("[+] �ɹ�ת���ļ� : %s [%d/%d]" % (URL,len(gotLinkList),len(linkList)))
				print ("\n")
				logger.debug(str(gotLinkList))
				with open("gotLink.txt","w+") as f:
					f.writelines(gotLinkList)
					f.close()
		print ("[*] %d ���Ӵ���" % len(errorLinkList))
		logger.info("[*] %d ���Ӵ���" % len(errorLinkList))
		errFile = open("errLink.txt","w+")
		for item in errorLinkList:
			errFile.write(item)
			errFile.write("\n")
			print item
		errFile.close()
		print ("[+] All Task Done.Exiting...")
		browser.quit()
	except:
		logger.exception("")

if (__name__ == "__main__"):
	main()