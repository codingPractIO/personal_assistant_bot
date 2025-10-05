import pytest
from core import EventDispatcher


def test_subscribe_and_emit_single_event():
    """Проверяет, что событие вызывается с зарегистрированным обработчиком."""
    dispatcher = EventDispatcher()
    results = []
    
    # Подписываемся на событие TEST_EVENT
    dispatcher.subscribe("TEST_EVENT", lambda payload: results.append(payload))
    
    # Генерируем событие TEST_EVENT
    dispatcher.emit("TEST_EVENT", {"key": "value"})
    
    # Проверяем, что обработчик был вызван с переданными данными
    assert results == [{"key": "value"}]


def test_emit_without_subscriber():
    """Проверяет, что генерация события без подписчика не вызывает ошибок."""
    dispatcher = EventDispatcher()
    
    # Генерируем событие без подписчиков
    try:
        dispatcher.emit("TEST_EVENT", {"key": "value"})
    except Exception as e:
        pytest.fail(f"Emit without subscriber raised an exception: {e}")


def test_multiple_subscribers_for_one_event():
    """Проверяет, что все обработчики для одного события вызываются."""
    dispatcher = EventDispatcher()
    results = []
    
    # Подписываемся на событие одним и тем же событием несколькими обработчиками
    dispatcher.subscribe("TEST_EVENT", lambda payload: results.append(f"Handler1: {payload['key']}"))
    dispatcher.subscribe("TEST_EVENT", lambda payload: results.append(f"Handler2: {payload['key']}"))
    
    # Генерируем событие
    dispatcher.emit("TEST_EVENT", {"key": "value"})
    
    # Проверяем, что оба обработчика были вызваны
    assert results == ["Handler1: value", "Handler2: value"]


def test_multiple_events_and_handlers():
    """Проверяет, что обработчики событий изолированы между собой."""
    dispatcher = EventDispatcher()
    results = []
    
    # Подписываемся на разные события
    dispatcher.subscribe("EVENT_A", lambda payload: results.append(f"EventA: {payload['key']}"))
    dispatcher.subscribe("EVENT_B", lambda payload: results.append(f"EventB: {payload['key']}"))
    
    # Генерируем события
    dispatcher.emit("EVENT_A", {"key": "valueA"})
    dispatcher.emit("EVENT_B", {"key": "valueB"})
    
    # Проверяем, что каждое событие сработало лишь для нужного обработчика
    assert results == ["EventA: valueA", "EventB: valueB"]


def test_unrelated_event_does_not_trigger_handlers():
    """Проверяет, что обработчики срабатывают только на связанные события."""
    dispatcher = EventDispatcher()
    results = []
    
    # Подписываемся на событие EVENT_A
    dispatcher.subscribe("EVENT_A", lambda payload: results.append(f"EventA: {payload['key']}"))
    
    # Генерируем неприятное событие EVENT_B
    dispatcher.emit("EVENT_B", {"key": "valueB"})
    
    # Проверяем, что обработчики EVENT_A не сработали
    assert results == []


def test_event_with_no_payload():
    """Проверяет, что событие может быть вызвано без полезной нагрузки."""
    dispatcher = EventDispatcher()
    results = []
    
    # Подписываемся на событие TEST_EVENT
    dispatcher.subscribe("TEST_EVENT", lambda payload: results.append(payload))
    
    # Генерируем событие без полезной нагрузки
    dispatcher.emit("TEST_EVENT", None)
    
    # Проверяем, что обработчик сработал с None
    assert results == [None]


def test_subscribe_multiple_events():
    """Проверяет регистрацию нескольких обработчиков на разные события."""
    dispatcher = EventDispatcher()
    results = []
    
    # Подписываемся на несколько событий
    dispatcher.subscribe("EVENT_A", lambda payload: results.append(f"A: {payload}"))
    dispatcher.subscribe("EVENT_B", lambda payload: results.append(f"B: {payload}"))
    
    # Генерируем одновременно несколько событий
    dispatcher.emit("EVENT_A", "dataA")
    dispatcher.emit("EVENT_B", "dataB")
    
    # Проверяем, что обработчики вызваны для соответствующих событий
    assert results == ["A: dataA", "B: dataB"]


def test_emit_order_of_subscribers():
    """Проверяет, что обработчики вызываются в порядке подписки."""
    dispatcher = EventDispatcher()
    results = []
    
    # Подписываем несколько обработчиков одного события
    dispatcher.subscribe("TEST_EVENT", lambda payload: results.append("First"))
    dispatcher.subscribe("TEST_EVENT", lambda payload: results.append("Second"))
    dispatcher.subscribe("TEST_EVENT", lambda payload: results.append("Third"))
    
    # Генерируем событие
    dispatcher.emit("TEST_EVENT", None)
    
    # Проверяем, что порядок вызова обработчиков соответсвует порядку подписки
    assert results == ["First", "Second", "Third"]