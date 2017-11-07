""" Script for analyzing if MMD file is in compliance with requirements.

Difference from v4 is:
    - works for single file in difference with entire directory. Returns True if
      file is in compliance with requirements. False if not.


USAGE:
    - checkObject = CheckMMD(mmd_file)
    - file_status = checkObject.check_mmd()

AUTHOR: Trygve Halsne, 07.03.2017 (dd.mm.YYYY)

STATUS/REVISION:
    - 20.01.2016 : All validation methods are implemented. Lack of specification
                   for
                    - keywords
                    - metadata_status

"""
import sys
import inspect
import lxml.etree as ET
import os
import re
import operator
import glob
import time
from myCheckMMDFunctions import containString, multipleLanguages, validKeywords, validText, validDateFormat

class CheckMMD():
    """ Class to verify if MMD file is in compliance with requirements
    """

    def __init__(self, mmd_file):
        self.mmd_file = mmd_file

    def check_abstract(self, abstract):
        """ Check if abstract is valid """
        languages = []
        for child in abstract:
            if not len(child.text) > 25:
                print "\t abstract is too short \n"
                return False
            if not (child.attrib.values() == []):
                languages.append(child.attrib.values())

        return multipleLanguages(languages=languages)

    def check_collection(self, collection):
        """ Check if collection is valid"""
        valid_keywords = ['CC', 'NMAP', 'ADC', 'GCW', 'NMDC', 'SIOS', 'NSDN', 'DOKI',
                        'DAM', 'ACCESS', 'NBS', 'APPL'] # Could ref a list
        collection_keywords = [child.text for child in collection]

        return validKeywords(collection_keywords,valid_keywords)


    def check_keywords(self, keywords):
        """ Check keyword requirements """
        #print "Fixme: check_keywords must be verified \n "
        # if contains vocabulary && is valid
        # if keyword is levelled or not
        # specification not finished
        return True

    def check_iso_topic_category(self, iso_topic_category):
        """ Check ISO topic category requirements """
        valid_keywords = ['farmin', 'biota', 'boundaries',
                         'climatologyMeteorologyAtmosphere', 'economy', 'elevation',
                         'environment', 'geoscientificinformation', 'health',
                          'imageryBaseMapsEarthCover', 'intelligenceMilitary',
                          'inlandWaters', 'location', 'oceans', 'planningCadastre',
                          'society', 'structure', 'transportation',
                          'utilitiesCommunications'] #could read from a ref. list

        iso_topic_category_keywords = [child.text for child in iso_topic_category]
        return validKeywords(iso_topic_category_keywords,valid_keywords)


    def check_title(self, title):
        """ Check title requirements """
        languages = []
        for child in title:
            if not len(child.text) <= 220:
                print "\t Title is to short \n"
                return False
            if not (child.attrib.values() == []):
                languages.append(child.attrib.values())

        return multipleLanguages(languages=languages)

    def check_last_metadata_update(self, last_metadata_update):
        """ Check last update of metadata record """
        if len(last_metadata_update)>1:
            print "\t Error: Multiple last_metadata_update elements in file"
            return False

        return validDateFormat(last_metadata_update[0].text)

    def check_metadata_identifier(self, metadata_identifier):
        """ Check if metadata identifier fulfill requirements """
        invalid = '/\: '

        if len(metadata_identifier) > 1:
            print "\t Error: Multiple metadata_identifier elements in file"
            return False

        return validText(metadata_identifier[0].text, invalid)

    def check_temporal_extent(self, temporal_extent):
        """ Check if temporal extent fulfill requirements """
        valid_keywords = ['start_date','end_date']

        keywords = [date.tag for child in temporal_extent for date in child]
        validDates = [validDateFormat(date.text) for child in temporal_extent for date in child]

        if all(element == True for element in validDates) and containString(keywords, valid_keywords):
            return True
        else:
            print "\t Error: Wrong date format or keyword typos"
            return False


    def check_metadata_status(self, metadata_status):
        """ Check metadata status """
        if len(metadata_status)>1:
            return False

        return True # must be verified

    def check_dataset_production_status(self, dataset_production_status):
        """ Check keyword for dataset production status """
        valid_keywords = ['Planned', 'In Work', 'Complete', 'Obsolete']

        if len(dataset_production_status) > 1:
            print "\t Error: Multiple dataset_production_status elements in file"
            return False

        keywords = [child.text for child in dataset_production_status]
        return validKeywords(keywords,valid_keywords)

    def check_rectangle(self, rectangle):
        """ Check geographic extent/rectangle for projection points """
        valid_directions = ['north', 'south', 'west', 'east']

        if len(rectangle) > 1:
            print "\t Error: Multiple rectangle elements in file. \n"
            return False

        coord = {}
        try:
            for child in rectangle[0]:
                for direction in valid_directions:
                    if direction in child.tag:
                        coord[format(direction)] = float(child.text)

            if not (-180 <= coord['west'] < coord['east'] <= 180): return False
            if not (-90 <= coord['south'] < coord['north'] <= 90): return False

            return True
        except ValueError:
            print '\t Could not extract valid directions from rectangle. \n'
            return False

    def check_mmd(self):
        """ Method for initiating the verification process
        """
        mmd_file = self.mmd_file
        file_requirements = {'metadata_identifier' : False, 'metadata_status' : False,
                            'collection' : False, 'title' : False, 'abstract' : False,
                            'last_metadata_update' : False,
                            'dataset_production_status' : False,
                            'iso_topic_category' : False, 'temporal_extent': False,
                            'rectangle' : False, 'keywords' : False}
        print "\nChecking file: \n\t%s" % mmd_file
        tree = ET.ElementTree(file=mmd_file)
        root = tree.getroot()
        print "Comments: \n"
        for requirement in file_requirements.iterkeys():
            element = tree.findall('.//mmd:' + requirement,namespaces=root.nsmap)
            if element != []:
                if eval(str('self.check_' + requirement))(element):

                    file_requirements[requirement]=True
                else:
                    print '\t ' + requirement + ' is None '

        ### PRINT RESULTS
        print '\nResults:'
        for element in sorted(file_requirements.items(),key=operator.itemgetter(1),reverse=True):
            if element[1]:
                print '\t  \x1b[0;30;42m %s \x1b[0m : %-12s' %('OK', element[0])
            else:
                print '\t  \x1b[0;36;41m %s \x1b[0m : %-12s' %('Invalid', element[0])

        if all(file_requirements.itervalues()):
            print '\n' + mmd_file + " - satisfy MMD requirements."
            return True
        else:
            print '\n' + mmd_file + " - does not satisfy MMD requirements."
            return False


def main():
    mmd_file= '/home/trygveh/documents/nbs/file_conversion/output/foo/S2A_MSIL1C_20170119T110351_N0204_R094_T32VMN_20170119T110348.xml'
    check_file = CheckMMD(mmd_file)
    if check_file.check_mmd():
        print "\nIT WORKS"


if __name__ == '__main__':
    main()
