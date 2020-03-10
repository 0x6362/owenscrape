extract: prettify
	cat prettified-sitemap.xml | egrep -e '[a-z]{2}[0-9]{2}[fs].+<' | sed -E 's|</?loc>||g' | sed 's/^[[:space:]]*//g' | sort | uniq > codes.txt

sitemap:
	curl -OL https://rickowens-production.s3-eu-west-1.amazonaws.com/sitemaps/rickowens_sitemap.xml.gz -o sitemap.xml.gz

unzip: sitemap.xml.gz
	gunzip -f sitemap.xml.gz

prettify: sitemap.xml
	cat sitemap.xml | python -c 'import sys;import xml.dom.minidom;s=sys.stdin.read();print(xml.dom.minidom.parseString(s).toprettyxml())' > prettified-sitemap.xml

fetch: codes.txt
	mkdir -p pages && python fetch.py

pyclean:
	rm -f save.p
	rm -rf pages/

clean:
	rm codes.txt *.xml* completed.txt failed.txt
