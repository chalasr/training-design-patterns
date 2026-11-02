import pytest

from katas.singleton import singletons
from katas.singleton.singletons import ConfigWithMetaclass, ConfigWithNew, get_config

VARIANTS = [ConfigWithNew, ConfigWithMetaclass, get_config]


@pytest.fixture(autouse=True)
def forget_instances():
    """Remettre les singletons à zéro entre deux tests : à vous de compléter."""
    yield


@pytest.mark.parametrize("make", VARIANTS)
def test_two_calls_return_the_same_instance(make):
    assert make() is make()


@pytest.mark.parametrize("make", VARIANTS)
def test_the_instance_has_the_default_settings(make):
    assert make().timezone == "Europe/Paris"


@pytest.mark.parametrize("make", VARIANTS)
def test_a_setting_changed_once_is_seen_everywhere(make):
    make().timezone = "Europe/Brussels"

    assert make().timezone == "Europe/Brussels"


@pytest.mark.parametrize("make", VARIANTS)
def test_the_next_test_starts_from_the_default_settings(make):
    assert make().timezone == "Europe/Paris"


def test_the_module_itself_is_a_singleton():
    import katas.singleton.singletons as again

    assert again is singletons
