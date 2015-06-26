#!/bin/bash
#
# Helper script to run tests
# 

export PYTHONPATH=$PWD/src

select_tests(){
	dialog --checklist "Choose tests to run" 15 40 6 \
		1 "test_definator.py" off \
		2 "all" off \
		3 "all except doctest (faster)" off \
		4 "test_terms_controller_fuzz.py" off \
		5 "test_links_fuzz.py" off \
		6 "fuzz tests" off 2> /tmp/aparaatti-dialog

	if [ "$?" != "0" ] ; then return 1; fi
	run_tests
}

run_tests(){
	for choice in $(cat /tmp/aparaatti-dialog)
	do
		case $choice in
			1) py.test test_definator.py;;
			2) py.test --doctest-modules src/;;
			3) py.test -k test_ src/;;
			4) py.test src/tests/fuzz/test_terms_controller_fuzz.py;;
			5) py.test src/tests/fuzz/test_term_links_fuzz.py;;
			6) py.test -k test_ src/tests/fuzz;;
		esac
	done
}

if [[ $# -gt 0 ]]
then
	if [[ ! -z $1 ]]
	then
		if [[ $1 == "-p" ]]
		then
			echo 'running previously selected tests...'
			skip='skip'
			run_tests
		fi
	fi
fi
if [[ -z $skip ]]
then
	select_tests
fi
