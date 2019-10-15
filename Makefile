

script:
	highlight -O rtf -K 18 script.py | pbcopy

s3:
	highlight -O rtf -K 18 s3.py | pbcopy

util:
	highlight -O rtf -K 18 newscheck/util.py | pbcopy

core:
	highlight -O rtf -K 18 newscheck/core.py | pbcopy


test_script:
	highlight -O rtf -K 18 newscheck/test_script.py | pbcopy
