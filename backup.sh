#!/bin/bash
#assumes running as root or sudo the script
#backup script
su postgres;
cd ;
name="database";
if [[ -e $name.bak ]] ; then
    i=0
    while [[ -e $name$i.bak ]] ; do
        let i++
    done
    name=$name$i
fi
 
file_name="$name".bak;
touch file_name;
pg_dumpall > "$file_name";
exit;
cd ;
#backup the website
name="websitebackup"
if [[ -e $name.tar.gz ]] ; then
    i=0
    while [[ -e $name$i.tar.gz ]] ; do
        let i++
    done
    name=$name$i
fi
backup_name="$name"
mv websitebackup.tar.gz "$backup_name".tar.gz
tar -zcpvf websitebackup.tar.gz . &> /dev/null 2>&1;
