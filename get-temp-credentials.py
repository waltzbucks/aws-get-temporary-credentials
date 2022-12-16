# -*- coding: utf-8 -*-
import time, boto3, json, os, datetime
import sys, subprocess
import argparse, tempfile


# install additional module
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# arrow module for calcurator start and end of month
try:
    import pyotp
except:
    install("pyotp")
finally:    
    import pyotp


def get_sts_session(**kwargs):
    session = boto3.session.Session(profile_name=kwargs['profile_name'])
    return session.client('sts')

def get_token_code(**kwargs):
    totp = pyotp.TOTP(kwargs['otp_key'])
    now = datetime.datetime.now()
    return str(totp.at(now))

def get_credentials(**kwargs):

    STSConnection = get_sts_session(profile_name = kwargs['profile'])

    response = STSConnection.get_session_token(
        DurationSeconds = kwargs['duration'],
        SerialNumber = kwargs['mfa_device'],
        TokenCode = kwargs['token_code']
    )

    response['Credentials']['Version'] = 1
    response['Credentials']['Expiration'] = response['Credentials']['Expiration'].isoformat('T')
    
    return response['Credentials']

def get_exptime(**kwargs):
    f = open(kwargs['path'],'r')
    r = json.loads(f.read())['Expiration']
    f.close()
    return datetime.datetime.fromisoformat(r).timestamp()
    

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--device',
                        required=True,
                        help="The MFA Device ARN.")
    parser.add_argument('--duration',
                        required=False,
                        type=int,
                        help="The duration, in seconds, that the temporary "
                             "credentials should remain valid. Minimum value: "
                             "900 (15 minutes). Maximum: 129600 (36 hours). "
                             "Defaults to 43200 (12 hours), or 3600 (one "
                             "hour).")
    parser.add_argument('--force',
                        required=False,
                        action='store_true',
                        help="If need to always new temporary credentials token, "
                        "when use this option forcly stored credentials overwrite")
    parser.set_defaults(force=False)
    parser.add_argument('--otpkey',
                        required=True,
                        help="Your the secret key of virtual MFA device.")
    parser.add_argument('--profile',
                        required=False,
                        help="If using profiles, specify the name here. The "
                        "default profile name is 'default'. The value can "
                        "also be provided via the environment variable "
                        "'AWS_PROFILE'.")
    args = parser.parse_args()
    
    path = tempfile.gettempdir() + f"/{args.profile}.json"
    
    # get profile from param or set the default 
    if not args.profile:
        if os.environ.get('AWS_PROFILE'):
            args.profile = os.environ.get('AWS_PROFILE')
        else:
            args.profile = 'default'

    # get duration from param or set default
    if not args.duration:
        if os.environ.get('MFA_STS_DURATION'):
            args.duration = int(os.environ.get('MFA_STS_DURATION'))
        else:
            args.duration = 28800 # Time setup to temporary credential for keep using on 8 hour 
      
    # temporary credential control through temp file
    if os.path.exists(path) is False or time.time() > get_exptime(path=path) + args.duration or args.force :
        temp_credential = get_credentials(
            profile = args.profile,
            mfa_device = args.device,
            duration = args.duration,
            token_code = get_token_code(otp_key = args.otpkey)            
        )
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(temp_credential, f, ensure_ascii=False, indent=4)      

    f = open(path,'r',encoding='utf8')
    print(f.read())
    f.close()

if __name__ == "__main__":
    main()