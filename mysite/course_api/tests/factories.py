import factory
from django.contrib.auth import get_user_model
from faker import Faker
from courses_app.models import Course

fake = Faker()
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name() + fake.pystr(min_chars=3, max_chars=6))
    email = factory.LazyAttribute(lambda _: fake.email())
    password = factory.PostGenerationMethodCall('set_password', fake.password())
    phone = factory.LazyAttribute(lambda _: fake.phone_number()[:10])
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    is_staff = False
    is_superuser = False

class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=5))
    creator = factory.SubFactory(UserFactory)

