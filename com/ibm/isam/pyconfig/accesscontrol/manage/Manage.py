"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Factory import Factory
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging

class Manage(RestClient):
    __metaclass__ = abc.ABCMeta

    RUNTIME_TUNING = "/mga/runtime_tuning"
    TEMPLATE_FILES = "/mga/template_files"

    logger = Logger("Manage")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Manage, self).__init__(baseUrl, username, password, logLevel)
        Manage.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # Runtime Parameters
    #

    def updateTuningParameter(self, parameter, value):
        methodName = "updateTuningParameter()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnValue(jsonObj, "value", value)

        endpoint = "%s/%s/v1" % (Manage.RUNTIME_TUNING, str(parameter))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    #
    # Runtime Template Files
    #

    # Directories

    def createTemplateFileDirectory(self, path, dirName):
        methodName = "createTemplateFileDirectory()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "dir_name", dirName)
        Utils.addOnStringValue(jsonObj, "type", "dir")

        endpoint = "%s/%s" % (Manage.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def getTemplateFileDirectory(self, path, recursive=None):
        methodName = "getTemplateFileDirectory()"
        Manage.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnValue(parameters, "recursive", recursive)

        endpoint = "%s/%s" % (Manage.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpGetJson(endpoint, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content if isinstance(content, list) else content.get("contents")

        Manage.logger.exitMethod(methodName, str(result))
        return result

    # Files

    def createTemplateFile(self, path, fileName, content):
        methodName = "createTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "file_name", fileName)
        Utils.addOnStringValue(jsonObj, "content", content)
        Utils.addOnStringValue(jsonObj, "type", "file")

        endpoint = "%s/%s" % (Manage.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def deleteTemplateFile(self, path, fileName):
        methodName = "getTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/%s" % (Manage.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpDeleteJson(endpoint)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def getTemplateFile(self, path, fileName):
        methodName = "getTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/%s" % (Manage.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpGetJson(endpoint)

        if statusCode == 200 and content is not None:
            result = content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def importTemplateFile(self, path, fileName, filePath):
        methodName = "updateTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        try:
            with open(filePath, 'rb') as template:
                files = {"file": template}

                endpoint = "%s/%s/%s" % (Manage.TEMPLATE_FILES, str(path), str(fileName))
                statusCode, content = self.httpPostFile(endpoint, files=files)

                if statusCode == 200:
                    result = True if content is None else content
        except IOError, e:
            Manage.logger.error(methodName, str(e))

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def updateTemplateFile(self, path, fileName, content=""):
        methodName = "updateTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "content", content)
        Utils.addOnStringValue(jsonObj, "type", "file")

        endpoint = "%s/%s/%s" % (Manage.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result
