from apps.sales.models import FailedUploadData


def create_upload_error_log(action_type: str, data: dict, member_type: str, reason: str):
    """
    Create a an upload error report instance
    """
    if action_type.lower() == "Cancel".lower():
        try:
            FailedUploadData.objects.create(
                member=data,
                member_type=member_type,
                reason=reason,
            )
        except Exception as e:
            raise e
    elif action_type.lower() == "Lapsed".lower():
        try:
            FailedUploadData.objects.create(
                member=data,
                member_type=member_type,
                reason=reason,
            )
        except Exception as e:
            raise e
    elif action_type.lower() == "paid_member".lower():
        try:
            FailedUploadData.objects.create(
                member=data,
                member_type=member_type,
                reason=reason,
            )
        except Exception as e:
            raise e
