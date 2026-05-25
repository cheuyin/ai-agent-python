from google.genai import types
from main import trim_oldest_turn


def make_user_msg(text="hello"):
    return types.Content(role="user", parts=[types.Part(text=text)])


def make_model_msg(text="response"):
    return types.Content(role="model", parts=[types.Part(text=text)])


def test_trim_oldest_turn_single_user_message():
    messages = [make_user_msg()]
    trim_oldest_turn(messages)
    assert len(messages) == 1  # nothing to trim, list unchanged


def test_trim_oldest_turn_two_user_messages():
    turn1_user = make_user_msg("first")
    turn1_model = make_model_msg("first response")
    turn2_user = make_user_msg("second")
    messages = [turn1_user, turn1_model, turn2_user]
    trim_oldest_turn(messages)
    assert len(messages) == 1
    assert messages[0] is turn2_user


def test_trim_oldest_turn_multiple_turns():
    turn1_user = make_user_msg("first")
    turn1_model = make_model_msg("resp1")
    turn2_user = make_user_msg("second")
    turn2_model = make_model_msg("resp2")
    turn3_user = make_user_msg("third")
    messages = [turn1_user, turn1_model, turn2_user, turn2_model, turn3_user]
    trim_oldest_turn(messages)
    # Only the oldest turn (turn1_user + turn1_model) is removed
    assert len(messages) == 3
    assert messages[0] is turn2_user
    assert messages[1] is turn2_model
    assert messages[2] is turn3_user
