A simple lambda function that creates an atom feed based on links from your Twitter timeline.

# Installation

1. Checkout this git repo with `git clone git@github.com:tgecho/tauphi.git`
2. Create and activate a virtualenv for the project
3. Install python dependencies with `pip install -r requirements`
4. Create a Twitter app at `https://apps.twitter.com/`
5. Create an S3 bucket to hold the rss feed (`https://console.aws.amazon.com/s3`)
6. Create an IAM role granting write access to the S3 bucket at `https://console.aws.amazon.com/iam#roles`. Example:

	```
	{
	    "Version": "2012-10-17",
	    "Statement": [
	        {
	            "Effect": "Allow",
	            "Action": [
	                "s3:ListBucket"
	            ],
	            "Resource": [
	                "arn:aws:s3:::{bucket}"
	            ]
	        },
	        {
	            "Sid": "Stmt1451426881000",
	            "Effect": "Allow",
	            "Action": [
	                "s3:*"
	            ],
	            "Resource": [
	                "arn:aws:s3:::{bucket}/*"
	            ]
	        }
	    ]
	}
	```
	
7. Run `python config.py` to create a config file
8. Run `./make_zip.sh` to create a `lambda.zip` bundle
9. Create a new lambda function at `https://console.aws.amazon.com/lambda`
	1. Upload the zip bundle from the earlier step
	2. Assign the role you created
	3. 128 MB of memory should be fine
	4. Add a scheduled Event Source. 1 hour recommended. Keep in mind that the Twitter API rate limits may make less then 15 minutes problematic.
	5. My current runs (500 max items, 7 max days) take 8-20 seconds. Adjust timeouts as needed.


# Status and Todos

I'm pretty happy with how it's currently running. I may refine the item output a bit, but functionally speaking everything seems to work fine. Ideally items would follow the Twitter display guidelines a bit more closely, but this would be fighting against the content sanitization employed by most feed readers.

The installation process suffers greatly from the lack of tooling around Lambda. I want to try out [https://github.com/garnaat/kappa](Kappa) or build something around CloudFormation to streamline the .zip/function/role/event source dance that must be done to get things in place. This is the biggest area for improvement.


# Prior Art

- [Siftlinks](https://siftlinks.com/) is an excellent (paid) service that is *way* easier to set up
- Readtwit (seems to be defunct)
- Feedera (seems to be defunct)
