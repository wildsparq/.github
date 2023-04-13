from distutils.log import fatal
import sys
from datetime import datetime
import semver

if (len(sys.argv) == 4):
    previous_version = sys.argv[1]
    if (previous_version == None):
        previous_version = '1.0.0'
    print("Previous Version: " + previous_version)

    branch_name = sys.argv[2]
    if (branch_name == ''):
        fatal('Error: branch_name must not be empty')
        sys.exit(1)

    print("Branch Name: " + branch_name)

    commit_body = sys.argv[3]
    if (commit_body == ''):
        fatal('Error: commit_body must not be empty')
        sys.exit(1)

    print("Commit Body: " + commit_body)

    

    

    ver = semver.Version.parse(previous_version)

    if (branch_name == 'main'):
        if (commit_body.find("[x] Major") != -1 or commit_body.find("[x ] Major") != -1 or commit_body.find("[ x] Major") != -1):
            ver = ver.bump_major()
        elif (commit_body.find("[x] Minor") != -1 or commit_body.find("[x ] Minor") != -1 or commit_body.find("[ x] Minor") != -1):
            ver = ver.bump_minor()
        else:
            ver = ver.bump_patch()
    else:
        build = ver.build
        if (build == None or build.find(branch_name+".") == -1):
            ver = semver.replace(str(ver), build=branch_name+"."+str("1"))
        else:
            ver = ver.bump_build()

    print(ver)
    print(f"::set-output name=version::" + str(ver))

else: 
    fatal('Error: compute-semver.py requires 3 arguments to be passed (previous_version, branch_name, commit_body)')
    sys.exit(1)

