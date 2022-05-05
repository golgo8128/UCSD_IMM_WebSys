#!/bin/bash

pushd ${RS_PROG_DIR}/rs_Python/rs_Python_Pack3
git pull
cd ${RS_PROG_DIR}/rs_R/rs_R_Pack4
git pull

popd

git pull

for idir in "UCSD_IMM_DB" "UCSD_IMM_Log" "UCSD_IMM_WorkSpace"
do
   echo "Setting file and (sub)directory permission of ${idir} ..."
   find ${idir} -type d -exec chmod ugo+rwx \{\} \;
   find ${idir} -type f -exec chmod ugo+rw  \{\} \;
done

# chmod ugo+rwx UCSD_IMM_DB
# chmod ugo+rw UCSD_IMM_DB/db.sqlite3

sudo service apache2 restart

