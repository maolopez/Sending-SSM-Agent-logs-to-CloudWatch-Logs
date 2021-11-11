from xml.etree.ElementTree import ElementTree, tostring
import xml.etree.ElementTree as ET
import subprocess

command = 'cp -p seelog.xml.template seelog.xml'
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

add_line = 'my-line'

def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

content = '<seelog type="adaptive" mininterval="2000000" maxinterval="100000000" critmsgcount="500" minlevel="info"><exceptions><exception filepattern="test*" minlevel="error"/></exceptions><outputs formatid="fmtinfo"><console formatid="fmtinfo"/><rollingfile type="size" filename="{{LOCALAPPDATA}}\Amazon\SSM\Logs\{{EXECUTABLENAME}}.log" maxsize="30000000" maxrolls="5"/><filter levels="error,critical" formatid="fmterror"><rollingfile type="size" filename="{{LOCALAPPDATA}}\Amazon\SSM\Logs\errors.log" maxsize="10000000" maxrolls="5"/></filter><custom name="cloudwatch_receiver" formatid="fmtdebug" data-log-group="{}"/></outputs><formats><format id="fmterror" format="%Date %Time %LEVEL [%FuncShort @ %File.%Line] %Msg%n"/><format id="fmtdebug" format="%Date %Time %LEVEL [%FuncShort @ %File.%Line] %Msg%n"/><format id="fmtinfo" format="%Date %Time %LEVEL %Msg%n"/></formats></seelog>'.format(add_line)
res = bytes(content, 'utf-8')

root = ET.fromstring(res)
indent(root)
tree = ET.ElementTree(root)

with open(f"seelog.xml", 'w+'):
    tree.write("seelog.xml", encoding="utf-8", xml_declaration=True)

