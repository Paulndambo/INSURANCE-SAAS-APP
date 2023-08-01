from django.conf import settings
#from celery.task import task
from celery import shared_task
from backend.celery import app
from django.db.models import Count

from apps.sales.models import (
    TemporaryDataHolding, 
    TemporaryMemberData,
    TemporaryCancelledMemberData,
    TemporaryDependentImport,
    TemporaryPaidMemberData
)


from apps.sales.mixins import (
    BulkMembersOnboardingMixin,
    MembersCancellationMixin,
    BulkPaidMembersMixin,
    BulkLapsedMembersMixin,
    DependentOnboardingMixin,
    ExtendedDependentOnboardingMixin,
    BeneficiaryOnboardingMixin
)

from apps.sales.main_member_upload_methods.telesales_upload_methods import BulkTelesalesUploadMixin
from apps.sales.main_member_upload_methods.group_upload_methods import BulkGroupMembersOnboardingMixin
from apps.sales.main_member_upload_methods.retail_upload_methods import BulkRetailMemberOnboardingMixin
from apps.sales.sales_flow_methods.retail_policy_purchase import SalesFlowBulkRetailMemberOnboardingMixin
from apps.sales.sales_flow_methods.telesales_sales_flow_member import SalesFlowBulkTelesalesUploadMixin



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
        telesales_mixin = BulkTelesalesUploadMixin(data, 8, "upload")
        telesales_mixin.run()
    else:
        print("No unprocessed telesales members found!!!!!")


@app.task(name="bulk_onboard_retail_members_task")
def bulk_onboard_retail_members_task():
    data = TemporaryMemberData.objects.filter(product__in=[1, 2], processed=False)[:150]
    if data.count() > 0:
        retail_mixin = BulkRetailMemberOnboardingMixin(data, "upload")
        retail_mixin.run()


@app.task(name="onboard_sales_member")
def onboard_sales_flow_member_task(product, data):
    try:
        if product in [1, 2]:
            retail_sales_flow_member_mixin = SalesFlowBulkRetailMemberOnboardingMixin(data)
            retail_sales_flow_member_mixin.run()
        elif product == 8:
            telesales_sales_flow_member_mixin = SalesFlowBulkTelesalesUploadMixin(data, 8)
            telesales_sales_flow_member_mixin.run()
    except Exception as e:
        raise e
    


@app.task(name="bulk_onboard_group_members_task")
def bulk_onboard_group_members_task():
    most_unprocessed = TemporaryMemberData.objects.exclude(product__in=[1, 2, 8]).filter(processed=False).values('product') \
        .annotate(num_members=Count('product')) \
        .order_by('-num_members') \
        .first()

    if most_unprocessed:
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
    else:
        print("There are no group members to process at the moment!!")


@shared_task
def mark_members_as_paid_task():
    data = TemporaryPaidMemberData.objects.filter(processed=False)[:150]

    if data.count() > 0:
        paid_members_mixin = BulkPaidMembersMixin(data)
        paid_members_mixin.run()
    else:
        print("No more payments to process")
    


@app.task
def mark_members_as_cancelled():
    data = TemporaryCancelledMemberData.objects.filter(processed=False, action_type="Cancel")

    if data.count() > 0:
        data_to_process = data[:200]
        cancel_members_mixin = MembersCancellationMixin(data_to_process)
        cancel_members_mixin.run()
    else:
        print("No more cancellations to process")
    

@app.task
def mark_policy_members_as_lapsed():
    data = TemporaryCancelledMemberData.objects.filter(action_type="Lapsed", processed=False)[:150]
    
    if data.count() > 0:
        lapsed_mixin = BulkLapsedMembersMixin(data)
        lapsed_mixin.run()
    else:
        print("No more lapsed members to process!")
    

@app.task(name="onboard_dependents_task")
def onboard_dependents_task():
    dependents = TemporaryDependentImport.objects.filter(relationship_type="Dependent", processed=False)[:300]

    if dependents.count() > 0:
        dependents_mixin = DependentOnboardingMixin(dependents)
        dependents_mixin.run()
    else:
        print("No dependents to onboard!!")


@app.task(name="onboard_extended_dependents_task")
def onboard_extended_dependents_task():
    dependents = TemporaryDependentImport.objects.filter(relationship_type="Extended", processed=False)[:300]

    if dependents.count() > 0:
        dependents_mixin = DependentOnboardingMixin(dependents)
        dependents_mixin.run()
    else:
        print("No extended dependents to onboard!!")


@app.task(name="onboard_beneficiaries_task")
def onboard_beneficiaries_task():
    beneficiaries = TemporaryDependentImport.objects.filter(relationship_type="Beneficiary", processed=False)[:300]

    if beneficiaries.count() > 0:
        beneficiaries_mixin = DependentOnboardingMixin(beneficiaries)
        beneficiaries_mixin.run()
    else:
        print("No extended dependents to onboard!!")