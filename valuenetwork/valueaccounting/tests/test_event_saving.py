import datetime
from decimal import *

from django.test import TestCase
from django.test import Client

from valuenetwork.valueaccounting.models import *
from valuenetwork.valueaccounting.tests.objects_for_testing import *

class EventSavingTest(TestCase):

    """Testing EconomicEvent.save()

        which also optionally updates
        CachedEventSummary and AgentResourceType.

    """

    def setUp(self):

        agent_type = AgentType(
            name="Active",
        )
        agent_type.save()

        self.agent1 = EconomicAgent(
            name="AOne",
            nick="AOne",
            agent_type=agent_type,
        )
        self.agent1.save()

        self.agent2 = EconomicAgent(
            name="ATwo",
            nick="ATwo",
            agent_type=agent_type,
        )
        self.agent2.save()

        self.project1 = Project(
            name="POne",
        )
        self.project1.save()

        self.project2 = Project(
            name="PTwo",
        )
        self.project2.save()

        self.event_type_work = EventType(
            name="Work",
            label="work",
            relationship="work",
            resource_effect="=",
        )
        self.event_type_work.save() 

        self.event_type_todo = EventType(
            name="Todo",
            label="todo",
            relationship="todo",
            resource_effect="=",
        )
        self.event_type_work.save()

        self.optical_work = EconomicResourceType(
             name="Optical Work",
        )
        self.optical_work.save()

        self.electronic_work = EconomicResourceType(
             name="Electronic Work",
        )
        self.electronic_work.save()

    def test_new_contribution_agent_project_resourcetype(self):
        event = EconomicEvent(
            from_agent=self.agent1,
            resource_type=self.optical_work,
            project=self.project1,
            event_type=self.event_type_work,
            quantity=Decimal("1"),
            event_date=datetime.date.today(),
            is_contribution=True,
        )
        event.save()
        #import pdb; pdb.set_trace()
        summary = CachedEventSummary.objects.get(
            agent=self.agent1,
            project=self.project1,
            resource_type=self.optical_work)
        self.assertEqual(summary.quantity, Decimal("1"))
        art = AgentResourceType.objects.get(
            agent=self.agent1,
            resource_type=self.optical_work,
            event_type=self.event_type_work)
        self.assertEqual(art.score, Decimal("1"))

    def test_two_contributions_same_agent_project_resourcetype(self):
        event = EconomicEvent(
            from_agent=self.agent1,
            resource_type=self.optical_work,
            project=self.project1,
            event_type=self.event_type_work,
            quantity=Decimal("1"),
            event_date=datetime.date.today(),
            is_contribution=True,
        )
        event.save()

        event = EconomicEvent(
            from_agent=self.agent1,
            resource_type=self.optical_work,
            project=self.project1,
            event_type=self.event_type_work,
            quantity=Decimal("2"),
            event_date=datetime.date.today(),
            is_contribution=True,
        )
        event.save()
        
        summary = CachedEventSummary.objects.get(
            agent=self.agent1,
            project=self.project1,
            resource_type=self.optical_work)
        self.assertEqual(summary.quantity, Decimal("3"))
        art = AgentResourceType.objects.get(
            agent=self.agent1,
            resource_type=self.optical_work,
            event_type=self.event_type_work)
        self.assertEqual(art.score, Decimal("3"))

    def test_changed_agent(self):
        pass

    def test_changed_project(self):
        event = EconomicEvent(
            from_agent=self.agent1,
            resource_type=self.optical_work,
            project=self.project1,
            event_type=self.event_type_work,
            quantity=Decimal("1"),
            event_date=datetime.date.today(),
            is_contribution=True,
        )
        event.save()
        
        #import pdb; pdb.set_trace()
        event.project = self.project2
        event.save()
        
        summary = CachedEventSummary.objects.get(
            agent=self.agent1,
            project=self.project1,
            resource_type=self.optical_work)
        self.assertEqual(summary.quantity, Decimal("0"))
        summary = CachedEventSummary.objects.get(
            agent=self.agent1,
            project=self.project2,
            resource_type=self.optical_work)
        self.assertEqual(summary.quantity, Decimal("1"))



    def test_changed_resourcetype(self):
        pass

    def test_changed_quantity(self):
        event = EconomicEvent(
            from_agent=self.agent1,
            resource_type=self.optical_work,
            project=self.project1,
            event_type=self.event_type_work,
            quantity=Decimal("1"),
            event_date=datetime.date.today(),
            is_contribution=True,
        )
        event.save()

        event.quantity = Decimal("3")
        event.save()
        
        summary = CachedEventSummary.objects.get(
            agent=self.agent1,
            project=self.project1,
            resource_type=self.optical_work)
        self.assertEqual(summary.quantity, Decimal("3"))
        art = AgentResourceType.objects.get(
            agent=self.agent1,
            resource_type=self.optical_work,
            event_type=self.event_type_work)
        self.assertEqual(art.score, Decimal("3"))

    def test_non_contribution(self):
        event = EconomicEvent(
            from_agent=self.agent1,
            resource_type=self.optical_work,
            project=self.project1,
            event_type=self.event_type_work,
            quantity=Decimal("1"),
            event_date=datetime.date.today(),
        )
        event.save()
        summaries = CachedEventSummary.objects.all()
        self.assertEqual(summaries.count(), 0)
