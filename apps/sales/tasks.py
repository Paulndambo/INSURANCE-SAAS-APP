from django.conf import settings
#from celery.task import task
from celery import shared_task
from backend.celery import app

from apps.sales.models import TemporaryDataHolding


from apps.sales.mixins import (
    BulkMembersOnboardingMixin,
    FamilyMemberOnboardingMixin,
    MembersCancellationMixin,
    BulkPaidMembersMixin
)


@app.task
def onboard_new_members_task():
    members = TemporaryDataHolding.objects.filter(upload_type="new_members").order_by("-created").first()

    if members:
        bulk_mixin = BulkMembersOnboardingMixin(members)
        bulk_mixin.run()
    else:
        print("*******************************All Members Have Been Processed!*********************************")


@shared_task
def mark_members_as_paid_task():
    data = TemporaryDataHolding.objects.filter(
        upload_type="paid_members").order_by("-created").first()

    if data:
        paid_members_mixin = BulkPaidMembersMixin(data)
        paid_members_mixin.run()


@app.task
def mark_members_as_cancelled():
    data = TemporaryDataHolding.objects.filter(
        upload_type="cancelled_members").order_by("-created").first()

    if data:
        cancel_members_mixin = MembersCancellationMixin(data)
        cancel_members_mixin.run()


@app.task
def onboard_family_members():
    data = TemporaryDataHolding.objects.filter(
        upload_type="family_members").order_by("-created").first()

    if data:
        # print('You are uploading family members')
        family_members_mixin = FamilyMemberOnboardingMixin(data)
        family_members_mixin.run()
