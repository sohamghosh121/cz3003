echo 'Start pydoc2 server for django documentation'
DJANGO_SETTINGS_MODULE='cms.settings'
export DJANGO_SETTINGS_MODULE
PYTHONPATH=`pwd`
export PYTHONPATH
pydoc -p8888
echo started
