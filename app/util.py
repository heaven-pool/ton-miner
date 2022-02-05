import re
import platform

def get_ubuntu_version(version_id: str):
    if re.search('20', version_id):
        return 'ubuntu20'
    elif re.search('18', version_id):
        return 'ubuntu18'
    else:
        NotImplementedError(version_id)


def get_os_type():
    '''
        uname = platform.uname()
        uname.system -> windows, linux

        Linux
        uname.version
        know ubuntu by version
        uname_result(system='Linux', node='ip-172-31-2-187', release='5.11.0-1022-aws', version='#23~20.04.1-Ubuntu SMP Mon Nov 15 14:03:19 UTC 2021', machine='x86_64', processor='x86_64')

        know hiveos by version
        uname_result(system='Linux', node='Rig_4138467', release='5.4.0-hiveos', version='#140.hiveos.210813 SMP Fri Aug 13 11:40:32 UTC 2021', machine='x86_64', processor='x86_64')
    '''
    uname = platform.uname()
    if uname.system == 'Windows':
        return 'windows'
    elif uname.system == 'Linux':
        if 'Ubuntu' in uname.version:
            version_id = re.search('VERSION_ID=(.*)\\n', open('/etc/os-release', 'r').read()).group(0)
            return get_ubuntu_version(version_id)
        elif 'hiveos' in uname.version:
            return 'hiveos'
        else:
            NotImplementedError(uname)
    else:
        NotImplementedError(uname)