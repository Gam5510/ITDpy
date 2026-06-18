"""Example: report a post for spam."""
from itdpy import ITDClient, ReportTargetType, ReportReason

POST_ID = "REPLACE_WITH_POST_UUID"
with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    report = client.reports.report(
        POST_ID,
        target_type=ReportTargetType.POST,
        reason=ReportReason.SPAM,
        description="This post is spam.",
    )
    print(f"Report submitted: id={report.id}")
