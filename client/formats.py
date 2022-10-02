import json
import traceback
import urllib.parse
from io import BytesIO
import collections.abc

collections.Iterable = collections.abc.Iterable


def formatRequest(requestByteIO: BytesIO) -> dict:
    try:
        requestText = requestByteIO.read().decode("utf-8")
        requestData = {}
        requestList = requestText.splitlines()[1:]
        requestData["Request-Method"] = requestText.split("\n")[0].split(" ")[0].replace("\\r", "").replace("\r",
                                                                                                            "").replace(
            "\\r", "")
        requestData["Request-HttpType"] = " ".join(requestText.split("\n")[0].split(" ")[2:]).replace("\r", "")
        requestData["Request-URI"] = urllib.parse.unquote(requestText.split("\n")[0].split(" ")[1])
        for j in range(len(requestList)):
            i = requestList[j]
            name = i.split(": ")[0]
            content = ": ".join(i.split(": ")[1:])
            if i == "":
                requestData["Content-Lines"] = requestList[j:][1:]
                break
            requestData[name] = content
        if "" in requestData: requestData.pop("")
    except:
        print(traceback.format_exc())
        requestData = {}
    return requestData


def formatResponse(contentType: str, statusCode: str, responseText: str | bytes) -> bytes:
    byte = responseText if type(responseText) == bytes else str(responseText).encode("utf-8")
    head = statusCode.encode("utf-8") + "\nContent-Type:".encode("utf-8") + contentType.encode("utf-8") + "\n\n".encode(
        "utf-8") + byte
    return head

"""
def formatHTMLTexts(HTMLText: str, context: dict[str, str]) -> str:
    resultText = HTMLText
    for variableName, variableValue in context.items():
        resultText = resultText.replace(f"<!--SW-TOOLS::{variableName}-->", str(variableValue))
    return resultText


def formatJsonToXml(JSON: dict | list):
    itemFunction = lambda x: 'Item'
    XML = dicttoxml.dicttoxml(JSON, custom_root='Items', item_func=itemFunction, attr_type=False)
    dom = xml.dom.minidom.parseString(XML)
    return dom.toprettyxml(indent="  ")


def formatXmlToJson(XML: str) -> dict:
    return xmltodict.parse(XML)


def formatXmlLog(logs: list) -> str:
    if len(logs) > 40:
        logs = logs[-39:]
    resultList = []
    for i in logs:
        i: tuple[tuple, dict, urllib.parse.ParseResult, str]
        resultList.append({"Connect-Time": i[3], "Connect-Headers": i[1], "Connect-Address": i[0],
                           "Connect-URL": {"Path": i[2].path, "Params": i[2].params, "Query": i[2].query,
                                           "Fragment": i[2].fragment}})
    return formatJsonToXml(resultList)


def formatLog(logs: list):
    logs2 = []
    for i in logs:
        logs2.append(json.loads(i))
    return logs2
"""

