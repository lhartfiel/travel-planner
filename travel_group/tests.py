from django.test import TestCase

# Create your tests here.
from travel_group.models import TravelGroup
from travel_users.models import CustomUser


class TestTravelGroup(TestCase):
    # Test Travel Groups
    def setUp(self):
        # Create the test data
        self.user = CustomUser.objects.create(username='TestUser', first_name='Jane', last_name='Doe', email='test@test.com', emergency_email='test2@test.com')
        self.travel_group1 = TravelGroup.objects.create(trip_name='Test Trip 1')
        self.travel_group1.travelers.add(self.user)
        self.travel_group2 = TravelGroup.objects.create(trip_name='Test Trip 2')
        self.user.trav_groups.add(self.travel_group2)

    def test_user(self):
        self.assertEqual(self.user.username, 'TestUser')
        self.assertIn(self.travel_group1, self.user.trav_groups.all())
        self.assertIn(self.travel_group2, self.user.trav_groups.all())

    def test_travel_group(self):
        self.assertEqual(self.travel_group1.trip_name, 'Test Trip 1')
        self.assertIn(self.user, self.travel_group1.travelers.all())


