# aws-get-temporary-credentials

This is a script written so that you can receive a temporary credential by automatically receiving a token code using the MFA secret key issued by AWS. 

# Prerequisite

## 1. AWS CLI install

Guide link: [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

<br>

## 2. Python3 Install

- Download and install python3 from [https://www.python.org/downloads/](https://www.python.org/downloads/). 
- Check the installed version. 

    ```bash
    python --version`
    ```
    
<br>

## 3. Python module install

`pyotp` and `boto3` are required for this script. Install with pip as follows. 

```bash
python -m pip install boto3 pyotp
```

- If pip is not installed, please check the [link] (https://pip.pypa.io/en/stable/installation/). 

<br>

# IAM User setup

## 1. MFA Secret key

- When issuing MFA, you must copy the `secret key`. 
- Make a copy of the issued `MFA Device ARN`. 

<br>

## 2. script execution test

- Check if the temporary authentication key can be received by executing the `MFA secret key` and `device ARN` copied in the above process by attaching the values to each option as shown below. 
    
    ```bash
    python $home/.aws/ctc-temp-credential.py \
     --device (MFA_DEVICE_ARN) \
     --otpkey (MFA_SECRET_KEY) \
     --profile (YOUR_AWS_CLI_PROFILE)
    ```
    
    response >
    
    ```json
    {
        "AccessKeyId": "ASIAULDOYXF5ZASBROSK",
        "SecretAccessKey": "6ZtOLb0gT3HBCieeldJO1w58RCpFQsm7NtNjpKpR",
        "SessionToken": "IQoJb3JpZ2luX2VjEE8aDmFwLW5vcnRoZWFzdC0yIkcwRQIgLTavhqFdZLccaF4i14N2Mee3lb8O+n/mkCCpWjBPa0MCIQDLGQp+qcJa3fpRtbF8krvjWbwhvcPw06Jne++MhTR5Lir4AQi4//////////8BEAAaDDI5ODczMjUzNDEzOSIM2Xdumy5y0MmxylU4KswBIgfiVhEMRUvugSQkVmMOn30I4u9GicO6/nWp/fmNcdl3DNDXQt2z8bUkkmLSQrhGA7u50QJBGowOnYnZL6QVaxj9aiG2bmnL6uFSM03x/FUidkDnd0sPqdVHGau+388wC0YI1MyMPU+emarZgFTUtUk0vv7OR7ENp04OXAIysmRUzKdXgnOeEa4tMZOvDaWkYd7/U172TmpfkvyHleUcy145AcUyf2aMZRZWEmjRdw/V9e4Q+j2Lj5hcovRtl1BhdPezZcUeUDGDH61bMM//m5EGOpgBCKdE9A7A3bQGZiL5FCr1fDi+SZKEBvTqJhAIc6zWQ8bgOyhpjUOvQ4whnf8wSioD9yP/udYpoaV7T14US9MeFZJd+kNFT80e74tnFA4RYBMafprCx9+qQObZ0nmo7++r0gLS8K+G9jaXJpTymk8mnMZVuNQneS8QkiWiJb42AdkAde+kfNtCzhWETKIWdOUrh9k7Yzf4bU4=",
        "Expiration": "2022-03-05T15:03:43+00:00",
        "Version": 1
    }
    ```

<br><br>

# AWS CLI Config setup

## 1. config setup for temporary credential

- Add the command used in the test above to `.aws/config` as follows.
- The location (path) of the script file must be an 'absolute path'. 

```
[profile temp-cred]
region = ap-northeast-2
output = json
credential_process = python /home/username/.aws/get-temp-credential.py --device (MFA_DEVICE_ARN) --otpkey (MFA_SECRET_KEY) --profile (YOUR_AWS_CLI_PROFILE)
```
    
<br>

## 2. config setup for assume role profile

- Copy Role ARN information from Assume target account.

    e.g) `arn:aws:iam::123456789012:role/myassume`

- Set the assume profile.

```
[profile myassume]
region=ap-northeast-2
source_profile = temp-cred
role_arn = arn:aws:iam::123456789012:role/myassume
output = json
```
    
<br>

## 3. Test

Check the temporary credentials with the customer profile myassume in the config set above. 

```bash
aws --profile myassume sts get-caller-identity
```

response >

```json
{
    "UserId": "AROAUDQ6F5DODABM76FAE:botocore-session-1646724170",
    "Account": "123456789012",
    "Arn": "arn:aws:sts::123456789012:assumed-role/mzc_solutions_architect/botocore-session-1646724170"
}
```
