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
    python3 --version`
    ```
    
<br>

## 3. Python module install

`pyotp` and `boto3` are required for this script. Install with pip as follows. 

```bash
python3 -m pip install boto3 pyotp
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
    python3 $home/.aws/get-temp-credentials.py \
     --device (MFA_DEVICE_ARN) \
     --otpkey (MFA_SECRET_KEY) \
     --profile (YOUR_AWS_CLI_PROFILE)
    ```
    
    response >
    
    ```json
    {
        "AccessKeyId": "",
        "SecretAccessKey": "",
        "SessionToken": "",
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
credential_process = python3 /home/username/.aws/get-temp-credential.py --device (MFA_DEVICE_ARN) --otpkey (MFA_SECRET_KEY) --profile (YOUR_AWS_CLI_PROFILE)
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
    "UserId": "ABCDEFGHIJKLMNOPQRST:botocore-session-1646724170",
    "Account": "123456789012",
    "Arn": "arn:aws:sts::123456789012:assumed-role/myassume/botocore-session-1646724170"
}
```
