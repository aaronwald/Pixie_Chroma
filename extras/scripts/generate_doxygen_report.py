# This hacky script finds functions not currently covered by Doxygen comments, which will not appear in the Doxygen output.

import time
import os

print("Generating report from Doxygen log contents...")

doxy_data = []
with open("extras/docs/doxy.log","r+") as f:
    doxy_data = f.read().split("\n")

doxy_ignore = []
with open("extras/reports/doxygen/.doxyignore","r+") as f:
    doxy_ignore = f.read().split("\n")

output = ""

for item in doxy_data:
    if not "ICON_" in item:
        if "not documented" in item or "are not (all) documented" in item:
            log_string = item.split("warning: ")[1]

            log_string = log_string.split(" ")
            log_string[4] = "**"+log_string[4]+"**"
            log_string = ' '.join([str(x) for x in log_string])

            log_string.replace("is not documented", "**is not documented**")
            log_string.replace("are not (all) documented", "**are not (all) documented**")

            allowed = True
            for item in doxy_ignore:
                if len(item) >= 3:
                    if item in log_string:
                        allowed = False

            if allowed:
                output += "- :x: "
                output += log_string
                output += "\n"
            else:
                print("SKIPPING (.doxyignore): "+log_string)
                
final_output = []
output = output.split("\n")

for item in output:
    skip = False
    for reference in final_output:
        if item == reference:
            skip = True

    if not skip:
        if len(item) >= 3:
            final_output.append(item)

output_string = "### Doxygen coverage report: \n#### Any undocumented objects currently seen by Doxygen will appear here after every CI test!\n---------------------------------------------------------\n"

if len(final_output) == 0:
    output_string += ":heavy_check_mark: **All checks passed, nothing left undocumented!**"
else:
    output_string += ("\n".join(final_output))
    output_string += "\n\n" + "To see more information, check the [full Doxygen log](../../../docs/doxy.log)."

with open("extras/reports/doxygen/README.md","w+") as f:
    f.write(output_string)

   
print("--- Report saved in extras/reports/doxygen/README.md")
