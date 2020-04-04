ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BASE_PATH := "${ROOT_DIR}/items"

.PHONY: refresh

refresh: sitemap codes fetch

fetch: codes.txt
	bash -c 'mkdir -p "${BASE_PATH}"/{fetched,failed} && python fetch.py'

sitemap:
	curl -L https://rickowens-production.s3-eu-west-1.amazonaws.com/sitemaps/rickowens_sitemap.xml.gz -o sitemap.xml.gz && gunzip -f sitemap.xml.gz
	cat sitemap.xml | python -c 'import sys;import xml.dom.minidom;s=sys.stdin.read();print(xml.dom.minidom.parseString(s).toprettyxml())' > prettified-sitemap.xml

codes: sitemap.xml
	cat prettified-sitemap.xml | egrep -e '[a-z]{2}[0-9]{2}[fs].+<' | sed -E 's|</?loc>||g' | sed 's/^[[:space:]]*//g' | sort | uniq > codes.txt

pyclean:
	rm -rf ${BASE_PATH}

clean: pyclean
	rm codes.txt *.xml*
