
## terminal: python select_contacts_from_ics.py <file-name>

import os, re, sys

## Read file - of wrong file or format print exception
try:
    file = open(sys.argv[1]).read()
except:
    print('ERROR: Add a ICS file to your command: python select_contacts_from_ics.py <file-name>')


## define patterns to obtain start and end positions
start_pattern = 'BEGIN:VEVENT'
end_pattern = 'END:VCALENDAR'
## Identify positions start and end
start = re.search(start_pattern,str(file)).span()[0]
end = re.search(end_pattern,file).span()[0]


## Trim calendar file to use for iteration
header = file[:start].strip()
footer = '\n' + file[end:]
file = file[start:end] # trimmed file

## add &sep in one line so we can use this as unified
## way to split the whole file through "&semp"
file = file.replace('END:VEVENT','END:VEVENT&sep')
data = file.split('&sep')


## extraction pattern for every single entry. Necessary to show the
## user what is to be extracted
pattern = '(SUMMARY:[^\s]+)(.*)(\nTRANSP)'

i = 1 # simple count variable
new_list = [] # all entries we want to add

for element in data:
    if element != '\n':
        try:
            match = re.search(pattern, element).group(2).strip()
            print('\n###### ', match, ' ######')
        except:
            print('Unknown pattern: ', element)
            print('{} pattern not found - check cal file'.format(i))
            i = i+1
        print('relevant? y (YES) / (NO) any other key')
        user_input = input()
        if user_input == 'y':
            new_list.append(element)


## create new calendar element (ics)
return_cal = '\n'.join(new_list)
## remove \n that sometimes is added by the chrome plugin (should not occur any longer -> line 40)
return_cal = return_cal.replace('END:VEVENT\n','END:VEVENT')

## add header and footer to assure ics conformity
return_cal = header+return_cal+footer


## write file
with open('new_birthdays.ics','w') as f:
    f.write(return_cal)

print('Success, new cal generated: new_birthdays.ics')
