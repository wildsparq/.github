from distutils.log import fatal
import sys
from datetime import datetime
import semver
import re

print("received args:")
print(sys.argv)

if (len(sys.argv) == 5):
    previous_version = sys.argv[1]
    if (previous_version == None or re.search("[A-Za-z]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]{40}", previous_version) != None):
        previous_version = '1.0.0'
    print("Previous Version: " + previous_version)

    previous_version_with_branch_as_prerelease= sys.argv[2]
    if (previous_version_with_branch_as_prerelease == None):
        fatal('Error: previous_version_with_branch_as_prerelease must be provided')
        sys.exit(1)

    print("Previous Version w/ Branch as Build: " + previous_version_with_branch_as_prerelease)

    branch_name = sys.argv[3]
    if (branch_name == ''):
        fatal('Error: branch_name must not be empty')
        sys.exit(1)

    print("Branch Name: " + branch_name)

    commit_body = sys.argv[4]
    if (commit_body == ''):
        print('Error: commit_body should not be empty. Will assume change is a PATCH')
    else:
        print("Commit Body: " + commit_body)

    ver = semver.Version.parse(semver.replace(str(previous_version), prerelease=None, build=None))

    if (branch_name == 'main'):
        if (commit_body.find("[x] Major") != -1 or commit_body.find("[x ] Major") != -1 or commit_body.find("[ x] Major") != -1):
            ver = ver.bump_major()
        elif (commit_body.find("[x] Minor") != -1 or commit_body.find("[x ] Minor") != -1 or commit_body.find("[ x] Minor") != -1):
            ver = ver.bump_minor()
        else:
            ver = ver.bump_patch()
    else: # note: Using prerelease instead of build parameter of semver due to lack of docker support for "+" in image name
        try:
            prev_ver_from_branch = semver.Version.parse(previous_version_with_branch_as_prerelease)
            if (ver == semver.replace(str(prev_ver_from_branch), prerelease=None, build=None)):
                ver = prev_ver_from_branch
            
            build = ver.prerelease
            if (build == None or build.find(branch_name+".") == -1):
                raise Exception("no build for current tag, accepting default prerelease instead")
            else:
                ver = ver.bump_prerelease()
        except:
            ver = semver.replace(str(ver), prerelease=branch_name+"."+str("0"))

    print(ver)
    print(f"::set-output name=version::" + str(ver))

else: 
    fatal('Error: compute-semver.py requires 3 arguments to be passed (previous_version, branch_name, commit_body)')
    sys.exit(1)

