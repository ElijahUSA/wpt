# META: timeout=long

import pytest

from tests.support.asserts import assert_dialog_handled, assert_error, assert_success


def forward(session):
    return session.transport.send(
        "POST", "session/{session_id}/forward".format(**vars(session)))


@pytest.mark.capabilities({"unhandledPromptBehavior": "accept"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_handle_prompt_accept(session, create_dialog, dialog_type):
    create_dialog(dialog_type, text="dialog")

    response = forward(session)
    assert_success(response)

    assert_dialog_handled(session, expected_text="dialog")


@pytest.mark.capabilities({"unhandledPromptBehavior": "accept and notify"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_handle_prompt_accept_and_notify(session, create_dialog, dialog_type):
    create_dialog(dialog_type, text="dialog")

    response = forward(session)
    assert_error(response, "unexpected alert open")

    assert_dialog_handled(session, expected_text="dialog")


@pytest.mark.capabilities({"unhandledPromptBehavior": "dismiss"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_handle_prompt_dismiss(session, create_dialog, dialog_type):
    create_dialog(dialog_type, text="dialog")

    response = forward(session)
    assert_success(response)

    assert_dialog_handled(session, expected_text="dialog")


@pytest.mark.capabilities({"unhandledPromptBehavior": "dismiss and notify"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_handle_prompt_dissmiss_and_notify(session, create_dialog, dialog_type):
    create_dialog(dialog_type, text="dialog")

    response = forward(session)
    assert_error(response, "unexpected alert open")

    assert_dialog_handled(session, expected_text="dialog")


def test_handle_prompt_ignore():
    """TODO"""


@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_handle_prompt_default(session, create_dialog, dialog_type):
    create_dialog(dialog_type, text="dialog")

    response = forward(session)
    assert_error(response, "unexpected alert open")

    assert_dialog_handled(session, expected_text="dialog")
