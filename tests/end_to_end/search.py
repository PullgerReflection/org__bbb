# from pullgerReflection.com_linkedin.tests import unit as unit_com_linkedin
# from pullgerMultiSessionManager import api as pullgerMM__API
from rest_framework.test import APITestCase
from django.test import tag
# ----------
from pullgerAccountManager.tests.tools import unitOperationsAM
from pullgerAccountManager__REST.tests.tools import unitOperationsAMRest
# ----------
from pullgerReflection.org__bbb.tests.tools import unitOperationsR
# from pullgerReflection.com_linkedin__REST.tests.tool import unitOperationsRRest
# from pullgerReflection.com_linkedin__TT import api
# from pullgerReflection.com_linkedin.models import models_people
# ----------
from pullgerMultiSessionManager.tests.tools import unitOperationsMSM
from pullgerDataSynchronization.tests.tools import unitOperationsDS
from pullgerMultiSessionManager__REST.tests import unitOperationsMSMRest
# ----------
from pullgerMultiSessionManager import apiMSM
from pullgerDataSynchronization import apiDS


class Test001Search(APITestCase):
    @tag('TDD')
    def test_000_00_API_full(self):
        unitOperationsR.add_category(self)
        unitOperationsR.add_city(self)
        unitOperationsR.add_search_request_all(self)

        session = unitOperationsMSM.add_new_session_selenium_standard(self)

        sent_task_count = unitOperationsDS.send_all_task_for_processing(self)

        for counter in range(sent_task_count):
            apiMSM.execute_task_in_the_queue()

        unitOperationsMSM.kill_session(self, session)

    @tag('PROD')
    def test_002_00_API_simple(self):
        unitOperationsR.add_category(self)
        unitOperationsR.add_city(self)
        element_search_request = unitOperationsR.add_search_request(self)

        session = unitOperationsMSM.add_new_session_selenium_standard(self)
        element_search_request.sync(session=session)

        unitOperationsMSM.kill_session(self, session)

    # @tag('PROD')
    # def test_002_00_API_multi_session_full_circle_load(self):
    #     # ----------------- Prepare -----------------
    #     unitOperationsAM.add_account_for_linkedin(self)
    #     session = unitOperationsMSM.add_new_linkedin_session(self)
    #     unitOperationsMSM.make_all_session_authorization(self)
    #     # ----------------- Search request load -----------------
    #     unitOperationsR.add_location(self)
    #     unitOperationsR.add_search(self)
    #
    #     sent_task_count = api.send_all_task_for_processing()
    #     self.assertEqual(1, sent_task_count, "Incorrect num task sent people to load.")
    #
    #     result_execution = apiMSM.execute_task_in_the_queue()
    #     self.assertEqual(result_execution, True, "Task not executed")
    #
    #     people_result = models_people.People.objects.all()
    #     self.assertNotEqual(len(people_result), 0, "People elements is empy.")
    #
    #     apiMSM.execute_finalizer()
    #     # ----------------- People load -----------------
    #     sent_task_count = api.send_all_task_for_processing()
    #     self.assertEqual(len(people_result), sent_task_count, "Incorrect num task sent people to load.")
    #
    #     for exec_circles in range(sent_task_count):
    #         result_execution = apiMSM.execute_task_in_the_queue()
    #         self.assertEqual(result_execution, True, "Error on task execution")
    #
    #     people_result = models_people.People.objects.all()
    #     for cur_people in people_result:
    #         pass
    #
    #     companies_result = models_people.Companies.objects.all()
    #     self.assertNotEqual(len(companies_result), 0, "Companies elements is empy.")
    #
    #     apiMSM.execute_finalizer()
    #     # ----------------- Company load -----------------
    #     # sent_task_count = api.send_all_task_for_processing()
    #     # self.assertEqual(len(companies_result), sent_task_count, "Incorrect num task sent people to load.")
    #     #
    #     # for exec_circles in range(sent_task_count):
    #     #     result_execution = apiMSM.execute_task_in_the_queue()
    #     #     # self.assertEqual(result_execution, True, "Error on task execution")
    #     #
    #     # apiMSM.execute_finalizer()
    #     # ----------------- Ending -----------------
    #     unitOperationsMSM.kill_session(self, session)
    #
    # @tag('PROD')
    # def test_000_00_API_direct_search_request_load(self):
    #
    #     unitOperationsR.add_location(self)
    #     unitOperationsAM.add_account_for_linkedin(self)
    #     session = unitOperationsMSM.add_new_linkedin_session(self)
    #     unitOperationsMSM.make_all_session_authorization(self)
    #
    #     search_element = unitOperationsR.add_search(self)
    #     search_element.sync(session=session)
    #
    #     search_results = search_element.get_results()
    #     self.assertNotEqual(len(search_results), 0, "Results is empy.")
    #
    #     people_result = models_people.People.objects.all()
    #     self.assertNotEqual(len(people_result), 0, "People elements is empy.")
    #
    #     unitOperationsMSM.kill_session(self, session)
    #
    # @tag('TEST')
    # def test_000_00_search_REST_load_head_browser(self):
    #     # -----------------    Prepare REST     -----------------
    #     unitOperationsRRest.set_up_unit(self)
    #     # ------------------ Prepare -----------------------------
    #     unitOperationsAMRest.add_account_for_linkedin(self)
    #
    #     # unitOperationsMSMRest.add_session_linkedin_no_head(self)
    #     unitOperationsMSMRest.add_session_linkedin_standard(self)
    #     unitOperationsMSMRest.make_all_session_authorization(self)
    #     # ----------------- Search request load -----------------
    #     unitOperationsRRest.add_location(self)
    #     unitOperationsRRest.add_search(self)
    #
    #     unitOperationsRRest.send_all_task_to_processing(self)
    #     unitOperationsMSMRest.execute_task_in_the_queue(self)
    #
    #     response_people = self.client.get("/pullgerR/com_linkedin/api/people")
    #     self.assertEqual(response_people.status_code, 200, "Incorrect companies get data")
    #     self.assertNotEquals(response_people.data["data"]["count"], 0, "Incorrect list count")
    #     #  ----------------- Search request load -----------------
    #     unitOperationsRRest.send_all_task_to_processing(self)
    #
    #     unitOperationsMSMRest.execute_task_in_the_queue(self)
    #     unitOperationsMSMRest.execute_task_in_the_queue(self)
    #     unitOperationsMSMRest.execute_task_in_the_queue(self)
    #
    #     pass
