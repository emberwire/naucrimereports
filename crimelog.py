# Created by Connor Schwirian
# Copyright 2017 Mercer Media, LLC.
# Last updated 21 March 2017
# Version b.3

# Features to implement:
# - Add best practice instructions for NAU generator
# - Change sexhomkid before you put this on github
# - REFACTOR

import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from StringIO import StringIO
import re
import os
from datetime import datetime

def pdfparser(data, name):

    # Change sexhomkid and chil

    fp = file(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    elements = []

    for page in PDFPage.get_pages(fp, maxpages=0, password='', caching=True, check_extractable=True):
        interpreter.process_page(page)
        elements.append(retstr.getvalue())

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()

    string = ''
    mis = []
    fel = []
    chil = []

    sexhomkid = []
    dui = []

    names = []

    dept = ''
    date = ''

    for longStr in elements:
        for char in longStr:
            string += char
            if ('\n\n' in string):
                if ('flagstaff police department' in string.lower()):
                    dept = 'Flagstaff Police Department'
                    if ('BULLETIN' in string):
                        #print(string[string.find('FROM') + 5:string.find('TO') - 1])
                        #date = string[string.find('TO') + 3:-2]
                        date = string[string.find('FROM') + 5:string.find('TO') - 1]
                    string = ''
                elif ('coconino county sheriff' in string.lower()):
                    dept = 'Coconino County Sheriff\'s Department'
                    if ('BULLETIN' in string):
                        #print(string[string.find('FROM') + 5:string.find('TO') - 1])
                        #date = string[string.find('TO') + 3:-2]
                        date = string[string.find('FROM') + 5:string.find('TO') - 1]
                    string = ''
                elif ('BULLETIN' in string):
                    #print(string[string.find('FROM') + 5:string.find('TO') - 1])
                    #date = string[string.find('TO') + 3:-2]
                    date = string[string.find('FROM') + 5:string.find('TO') - 1]
                    string = ''
                elif ('(M)' in string or '(F)' in string or '(C)' in string):
                    string = string.replace('\n', ' ')
                    string = string[:-2]
                    if (not 'VICTIM' in string[:string.find(' of')] and not 'State' in string[:string.find(' of')] and not 'Juvenile' in string[:string.find(' of')] and not 'Victim' in string[:string.find(' of')]):
                        names.append(string[:string.find(' of')])
                    if (not 'ARIZONA' in string[:string.find(";")]):
                        loop_index = string.find("of")
                        space_index = loop_index + 3 + (string[loop_index + 3:string.find(";")].find(" "))
                        for i in range(space_index - 2, space_index):
                            if (i < len(string) - 1):
                                if (string[i] in "0123456789"):
                                    string = string[:i] + "*" + string[i + 1:]
                            else:
                                if (string[i] in "0123456789"):
                                    string = string[:i] + "*"
                    if ('(M)' in string):
                        if (string not in mis):
                            mis.append(string)
                    elif ('(F)' in string):
                        itemlow = string.lower()
                        if ('sex' in itemlow or 'rape' in itemlow or 'kidnap' in itemlow or 'homicide' in itemlow):
                            if (string not in sexhomkid):
                                sexhomkid.append(string)
                        elif ('dui' in itemlow):
                            if (string not in dui):
                                dui.append(string)
                        else:
                            if (string not in fel):
                                fel.append(string)
                    else:
                        if (string not in chil):
                            chil.append(string)
                    string = ''
                else:
                    string = ''

    crimeCount = len(mis) + len(fel) + len(chil) + len(dui) + len(sexhomkid)

    filedate = date.replace(',', '')
    filedate = filedate.replace(' ', '')
    months = {'January': '01',
              'February': '02',
              'March': '03',
              'April': '04',
              'May': '05',
              'June': '06',
              'July': '07',
              'August': '08',
              'September': '09',
              'October': '10',
              'November': '11',
              'December': '12'}

    if ("FPD" in data):
        filedate = filedate[filedate.find("-") + 1::]

    index = re.search("\d", filedate).start()

    fdate = filedate[-4:] + months[filedate[:index]] + filedate[index:-4]
    direct = os.getcwd()
    direct += "/" + fdate
    if (not os.path.exists(direct)):
        os.makedirs(direct)

    if (not os.path.exists(direct + '/' + data[:-4])):
        os.makedirs(direct + '/' + data[:-4])

    outfile = './' + fdate + '/' + data[:-4] + '/' + data[:-4] + '_' + fdate + '_crimelog'+ '.txt'
    textfile = open(outfile, 'w')

    textfile.write('<!--' + dept + ' Crime Data ')
    textfile.write(date + ' ')
    textfile.write('Total Crimes: ' + str(crimeCount) + ' ')
    textfile.write('Copyright ' + datetime.now().strftime('%Y') + ' The Coconino Post, LLC-->')
    textfile.write('[vc_row][vc_column][vc_column_text]\n')

    textfile.write('<h3 style=\"text-align: center;\"><strong>')
    textfile.write(dept + ' Crime Log</strong></h3>\n')

    textfile.write('<h3 style=\"text-align: center;\"><strong>Date of Crimes: ' + date + '</strong></h3>\n')

    textfile.write('[/vc_column_text][/vc_column][/vc_row][vc_row parallax=\"\"][vc_column][vc_tta_accordion][vc_tta_section i_icon_fontawesome=\"fa fa-exclamation-circle\" add_icon=\"true\" title=\"Sexual Assault, Homicide, Rape, and Kidnapping Offenses\" tab_id=\"1485042133193-14b8bd7b-0dd4\"][vc_column_text]\n')
    if (sexhomkid == []):
        textfile.write('No crimes to report.\n')
    else:
        for item in sexhomkid:
            textfile.write('<strong>')
            textfile.write(item[:item.find(' of')] + '</strong>')
            textfile.write(item[item.find(' of'):] + '\n\n')

    textfile.write('[/vc_column_text][/vc_tta_section][vc_tta_section i_icon_fontawesome=\"fa fa-car\" add_icon=\"true\" title=\"Driving Under the Influence Crimes\" tab_id=\"1485042133216-42e2abf5-c608\"][vc_column_text]\n')
    if (dui == []):
        textfile.write('No crimes to report.\n')
    else:
        for item in dui:
            textfile.write('<strong>')
            textfile.write(item[:item.find(' of')] + '</strong>')
            textfile.write(item[item.find(' of'):] + '\n\n')

    textfile.write('[/vc_column_text][/vc_tta_section][vc_tta_section i_icon_fontawesome=\"fa fa-gavel\" add_icon=\"true\" title=\"Other Felonies\" tab_id=\"1485042842240-2d4effa8-9b16\"][vc_column_text]\n')
    if (fel == []):
        textfile.write('No crimes to report.\n')
    else:
        for item in fel:
            textfile.write('<strong>')
            textfile.write(item[:item.find(' of')] + '</strong>')
            textfile.write(item[item.find(' of'):] + '\n\n')

    textfile.write('[/vc_column_text][/vc_tta_section][vc_tta_section i_type=\"material\" i_icon_material=\"vc-material vc-material-new_releases\" add_icon=\"true\" title=\"Misdemeanors\" tab_id=\"1485042946452-2937bb7f-dba1\"][vc_column_text]\n')
    if (mis == []):
        textfile.write('No crimes to report.\n')
    else:
        for item in mis:
            textfile.write('<strong>')
            textfile.write(item[:item.find(' of')] + '</strong>')
            textfile.write(item[item.find(' of'):] + '\n\n')

    textfile.write('[/vc_column_text][/vc_tta_section][vc_tta_section i_icon_fontawesome=\"fa fa-wpforms\" add_icon=\"true\" title=\"Citations\" tab_id=\"1485129791444-88172e6d-f8cd\"][vc_column_text]\n')
    if (chil == []):
        textfile.write('No crimes to report.\n')
    else:
        for item in chil:
            textfile.write(item + '\n\n')

    textfile.write('[/vc_column_text][/vc_tta_section][vc_tta_section i_icon_fontawesome=\"fa fa-check-circle\" add_icon=\"true\" title=\"Full List of Crimes\" tab_id=\"1485044674237-13c5b160-0ad3\"][vc_column_text]\n')
    # if (sexhomkid == []):
        # textfile.write('No crimes to report.\n')
        # pass
    # else:
    if (not sexhomkid == []):
        for item in sexhomkid:
            textfile.write('<strong>')
            textfile.write(item[:item.find(' of')] + '</strong>')
            textfile.write(item[item.find(' of'):] + '\n\n')
    # if (dui == []):
        # textfile.write('No crimes to report.\n')
        # pass
    # else:
    if (not dui == []):
        for item in dui:
            textfile.write('<strong>')
            textfile.write(item[:item.find(' of')] + '</strong>')
            textfile.write(item[item.find(' of'):] + '\n\n')
    # if (fel == []):
        # textfile.write('No crimes to report.\n')
        # pass
    # else:
    if (not fel == []):
        for item in fel:
            textfile.write('<strong>')
            textfile.write(item[:item.find(' of')] + '</strong>')
            textfile.write(item[item.find(' of'):] + '\n\n')
    # if (mis == []):
        # textfile.write('No crimes to report.\n')
        # pass
    # else:
    if (not mis == []):
        for item in mis:
            textfile.write('<strong>')
            textfile.write(item[:item.find(' of')] + '</strong>')
            textfile.write(item[item.find(' of'):] + '\n\n')
    # if (chil == []):
        # textfile.write('No crimes to report.\n')
        # pass
    # else:
    if (not chil == []):
        for item in chil:
            textfile.write(item + '\n\n')

    textfile.write('[/vc_column_text][/vc_tta_section][/vc_tta_accordion][/vc_column][/vc_row][vc_row][vc_column][vc_message]\n')
    textfile.write('The Coconino Post does not support the use of crime information to threaten, harass, or intimidate individuals identified in crime data. Appropriate action will be taken if an individual uses crime data inappropriately.\n\n')
    textfile.write('While The Coconino Post does its best to verify information, crime data is provided by law enforcement agencies and does not undergo vetting by The Coconino Post\'s staff.\n\n')
    textfile.write('If you have any questions regarding crime data, please email <a href="mailto:newsroom@coconinopost.com">newsroom@coconinopost.com</a>.\n[/vc_message][/vc_column][/vc_row]')

    textfile.close()

    # Summary

    if (not os.path.exists(direct + '/Summaries')):
        os.makedirs(direct + '/Summaries')

    outfile = './' + fdate + '/' + 'Summaries/' + data[:-4] + '_' + fdate + '_summary'+ '.txt'
    textfile = open(outfile, 'w')

    textfile.write(dept + ' Crime Data\n')
    textfile.write("Date of Crime Log: " + date + '\n')
    textfile.write('Total Crimes: ' + str(crimeCount) + '\n\n')
    textfile.write("Report Ran By: " + name + "\n")

    procdate = datetime.now().strftime("%Y_%m_%d")
    proctime = datetime.now().strftime("%H:%M:%S")

    textfile.write("Date Processed: " + procdate + "\n")
    textfile.write("Time Processed: " + proctime + "\n")

    textfile.write('Copyright ' + filedate[-4:] + ' The Coconino Post, LLC\n\n\n')

    textfile.close()

    # Tags

    outfile = './' + fdate + '/' + data[:-4] + '/' + data[:-4] + '_' + fdate + '_tags.txt'
    textfile = open(outfile, 'w')

    if (data[:-4] == "FPD"):
        textfile.write("Flagstaff, Crimes, Police, Department, ")
    else:
        textfile.write("Coconino, County, Sheriff, Office, Crimes, ")

    for i in range(len(names) - 1):
        textfile.write(names[i] + ', ')

    textfile.write(names[len(names) - 1])

    textfile.close()



def crime_creator(name):

    date = raw_input("Enter the date for this log (eg. January 03, 2017): ")
    months = {'january': '01',
              'february': '02',
              'march': '03',
              'april': '04',
              'may': '05',
              'june': '06',
              'july': '07',
              'august': '08',
              'september': '09',
              'october': '10',
              'november': '11',
              'december': '12'}
    date_edit = date[-4:] + months[(date[:date.find(",") - 3]).lower()] + date[date.find(",") - 2:date.find(",")]
    directory = os.getcwd() + "/" + date_edit


    num = int(raw_input("Enter the number of incidents to be entered: "))
    count = num
    crimes = []

    while (count > 0):
        crime = []
        print("\nCrime " + str(num - count + 1) + "\n")
        nature = raw_input("Enter the nature of the incident: ")
        location = raw_input("Enter the location of the incident: ")
        result = raw_input("Enter the result of the incident: ")

        crime.append(nature)
        crime.append(location)
        crime.append(result)

        crimes.append(crime)

        count -= 1


    if (not os.path.exists(directory)):
        os.makedirs(directory)
    if (not os.path.exists(directory + "/NAU")):
        os.makedirs(directory + "/NAU")

    outfile = directory + "/NAU/NAUPD_" + date_edit + "_crimelog.txt"
    textfile = open(outfile, "w")

    textfile.write("[vc_row][vc_column][vc_column_text]\n")
    textfile.write("<h3 style=\"text-align: center;\"><strong>NAU Police Department Crime Log</strong></h3>")
    textfile.write("<h3 style=\"text-align: center;\"><strong>Date of Crimes: " + date + "</strong></h3>\n")
    textfile.write("[/vc_column_text][/vc_column][/vc_row]\n")
    textfile.write("[vc_row parallax=""][vc_column][vc_tta_accordion][vc_tta_section i_icon_fontawesome=\"fa fa-check-circle\" add_icon=\"true\" title=\"Full List of Crimes\" tab_id=\"1485044674237-13c5b160-0ad3\"][vc_column_text]\n")
    for crime in crimes:
        textfile.write("<strong>" + crime[0] + "</strong>, " + crime[1] + ", " + crime[2] + "\n\n")
    textfile.write("[/vc_column_text][/vc_tta_section][/vc_tta_accordion][/vc_column][/vc_row]")

    textfile.write("[vc_row][vc_column][vc_message]\n")
    textfile.write("The Coconino Post does not support the use of crime information to threaten, harass, or intimidate individuals identified in crime data. Appropriate action will be taken if an individual uses crime data inappropriately.\n\n")
    textfile.write("While The Coconino Post does its best to verify information, crime data is provided by law enforcement agencies and does not undergo vetting by The Coconino Post's staff.\n\n")
    textfile.write("If you have any questions regarding crime data, please email <a href=\"mailto:newsroom@coconinopost.com\">newsroom@coconinopost.com</a>.\n")
    textfile.write("[/vc_message][/vc_column][/vc_row]")

    textfile.close()


    outfile = directory + "/NAU/NAUPD_" + date_edit + "_tags.txt"
    textfile = open(outfile, "w")

    textfile.write("Northern, Arizona, University, Crimes")

    textfile.close()

    # Summary

    if (not os.path.exists(directory + '/Summaries')):
        os.makedirs(directory + '/Summaries')

    outfile = './' + date_edit + '/' + 'Summaries/' + 'NAUPD_' + date_edit + '_summary'+ '.txt'
    textfile = open(outfile, 'w')

    textfile.write('Nothern Arizona Univeristy Police Department Crime Data\n')
    textfile.write("Date of Crime Log: " + date + '\n')
    textfile.write('Total Crimes: ' + str(num) + '\n\n')
    textfile.write("Report Ran By: " + name + "\n")

    procdate = datetime.now().strftime("%Y_%m_%d")
    proctime = datetime.now().strftime("%H:%M:%S")

    textfile.write("Date Processed: " + procdate + "\n")
    textfile.write("Time Processed: " + proctime + "\n")

    textfile.write('Copyright ' + datetime.now().strftime("%Y") + ' The Coconino Post, LLC\n\n\n')

    textfile.close()



if (__name__ == "__main__"):
    name = raw_input("Who are you: ")
    if (len(sys.argv) == 1):
        if (raw_input("Would you like to process NAU crime information (y/n): ") == "y"):
            crime_creator(name)
    else:
        if (raw_input("Would you like to process NAU crime information (y/n): ") == "y"):
            crime_creator(name)
        pdfparser(sys.argv[1], name)
        if (len(sys.argv) == 3):
            pdfparser(sys.argv[2], name)

    print("***Process Completed***")
