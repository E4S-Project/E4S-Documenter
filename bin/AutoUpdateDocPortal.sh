#!/bin/bash
WEBHOST=`hostname -f`  #yu.nic.uoregon.edu
EMAIL=/tmp/docportal_today
rm $EMAIL
SENDTO=wspear@cs.uoregon.edu

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
startDir=`pwd`
spackDir="$DIR/../spack"
testsuiteDir="$DIR/../testsuite"
baseDir="$DIR/.."
repoDir="~/public_html/E4S/E4S-Project.github.io"



cd "$baseDir/testsuite"
git pull

if [ -d "$testsuiteDir" ]; then
	cd "$testsuiteDir"
	git pull
else
	cd "$baseDir"
	git clone https://github.com/E4S-Project/testsuite.git
fi

if [ -d "$spackDir" ]; then
    cd "$spackDir"
    git pull
else
    cd "$baseDir"
    git clone https://github.com/spack/spack.git
fi

source "$spackDir/share/spack/setup-env.sh"
mkdir -p "$baseDir/autogen" 
mkdir -p "$baseDir/backup" 
mv "$baseDir"/autogen/* "$baseDir"/backup || true
cd "$baseDir"
${baseDir}/bin/DocPortalGen.py ${baseDir}/autogen/ ${baseDir}/data/e4s_products.yaml --yaml &>> $EMAIL
genRet=$?

if [ $genRet -ne 0 ]; then
	SUBJECT="DocPortal FAULT"
	scp /tmp/docportal_today $WEBHOST:~/public_html/E4S
	ssh $WEBHOST "cat ~/public_html/E4S/docportal_today" | mailx -s "${SUBJECT}" wspear@cs.uoregon.edu
fi


diffLines=`diff -y --suppress-common-lines  ${baseDir}/autogen/DocPortal.yml ${baseDir}/backup/DocPortal.yml | wc -l`

echo "$diffLines" &>> $EMAIL

if [ "$diffLines" -gt 0 ]; then
    cp ${baseDir}/autogen/DocPortal.yml $repoDir
    cd $repoDir
    git pull --no-edit
    git commit ./DocPortal.yml -m "DocPortal update (Automatic)"
    git push &>> $EMAIL  #  $baseDir/autogen/push_out.txt
    cd $startDir
    SUBJECT="DocPortal UPDATED"
else
    SUBJECT="DocPortal UNCHANGED"
fi

#scp /tmp/docportal_today $WEBHOST:~/public_html/E4S
cp /tmp/docportal_today ~/public_html/E4S
#ssh $WEBHOST 
cat ~/public_html/E4S/docportal_today | mailx -s "${SUBJECT}" $SENDTO

