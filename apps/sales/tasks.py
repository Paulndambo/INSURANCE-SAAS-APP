from django.conf import settings
#from celery.task import task
from celery import shared_task
from backend.celery import app
from django.db.models import Count

from apps.sales.models import TemporaryDataHolding, TemporaryMemberData


from apps.sales.mixins import (
    BulkMembersOnboardingMixin,
    FamilyMemberOnboardingMixin,
    MembersCancellationMixin,
    BulkPaidMembersMixin
)

from apps.sales.telesales_upload_methods import BulkTelesalesUploadMixin
from apps.sales.group_upload_methods import BulkGroupMembersOnboardingMixin
from apps.sales.retail_upload_methods import BulkRetailMemberOnboardingMixin


@app.task(name="salimiana")
def salimiana():
    print("**************Salimiana***************")



def onboard_new_members_task():
    members = TemporaryDataHolding.objects.filter(upload_type="new_members").order_by("-created").first()

    if members:
        bulk_mixin = BulkMembersOnboardingMixin(members)
        bulk_mixin.run()
    else:
        print("*******************************All Members Have Been Processed!*********************************")


@app.task(name="bulk_onboard_telesales_members_task")
def bulk_onboard_telesales_members_task():
    data = TemporaryMemberData.objects.filter(product=8, processed=False)

    if data.count() > 0:
        telesales_mixin = BulkTelesalesUploadMixin(data, product=8)
        telesales_mixin.run()
    else:
        print("No unprocessed telesales members found!!!!!")


@app.task(name="bulk_onboard_retail_members_task")
def bulk_onboard_retail_members_task():
    data = TemporaryMemberData.objects.filter(product__in=[1, 2], processed=False)[:150]
    if data.count() > 0:
        retail_mixin = BulkRetailMemberOnboardingMixin(data)
        retail_mixin.run()


@app.task(name="bulk_onboard_group_members_task")
def bulk_onboard_group_members_task():
    most_unprocessed = TemporaryMemberData.objects.exclude(product__in=[1, 2, 8]).filter(processed=False).values('product') \
        .annotate(num_members=Count('product')) \
        .order_by('-num_members') \
        .first()
    
    number_of_processed_members = most_unprocessed["num_members"]
    product = most_unprocessed["product"]

    if number_of_processed_members < 200:
        data = TemporaryMemberData.objects.filter(product=product, processed=False)
        group_mixin = BulkGroupMembersOnboardingMixin(data, product)
        group_mixin.run()
    elif number_of_processed_members > 200:
        data = TemporaryMemberData.objects.filter(product=product, processed=False)[:200]
        group_mixin = BulkGroupMembersOnboardingMixin(data, product)
        group_mixin.run()


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
