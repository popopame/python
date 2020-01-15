provider "aws" {
  region = "eu-west-1"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "policy" {
  name = "ops-itw"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "ec2:DescribeInstances"
        ],
        "Effect": "Allow",
        "Resource": "*"
      },
      {
        "Action": [
          "ec2:StartInstances",
          "ec2:StopInstances"
        ],
        "Effect": "Allow",
        "Resource": "*",
        "Condition": {
          "StringEquals": {
            "ec2:ResourceTag/OpsItw": "development"
          }
        }
      }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.policy.arn
}

data "archive_file" "package" {
  type        = "zip"
  source_file = "${path.module}/ops_itw.py"
  output_path = "${path.module}/ops_itw.zip"
}

resource "aws_lambda_function" "ops_itw_start" {
  filename         = data.archive_file.package.output_path
  function_name    = "ops-itw-start"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "ops_itw.lambda_handler"
  source_code_hash = data.archive_file.package.output_base64sha256
  runtime          = "python3.8"

  environment {
    variables = {
      TAG_VALUE = "development"
      ACTION    = "start"
    }
  }
}

resource "aws_lambda_function" "ops_itw_stop" {
  filename         = data.archive_file.package.output_path
  function_name    = "ops-itw-stop"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "ops_itw.lambda_handler"
  source_code_hash = data.archive_file.package.output_base64sha256
  runtime          = "python3.8"

  environment {
    variables = {
      TAG_VALUE = "development"
      ACTION    = "stop"
    }
  }
}

resource "aws_cloudwatch_event_rule" "start" {
  name                = "ops-itw-start"
  schedule_expression = "cron(0 8 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "start" {
  rule = aws_cloudwatch_event_rule.start.name
  arn  = aws_lambda_function.ops_itw_start.arn
}

resource "aws_cloudwatch_event_rule" "stop" {
  name                = "ops-itw-stop"
  schedule_expression = "cron(0 20 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "stop" {
  rule = aws_cloudwatch_event_rule.stop.name
  arn  = aws_lambda_function.ops_itw_stop.arn
}

resource "aws_lambda_permission" "start" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ops_itw_start.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.start.arn
}

resource "aws_lambda_permission" "stop" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ops_itw_stop.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.stop.arn
}
