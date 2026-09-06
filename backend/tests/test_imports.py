def test_backend_imports() -> None:
    import app
    from app.main import app as fastapi_app

    assert app is not None
    assert fastapi_app is not None


def test_simulator_imports() -> None:
    import simulator
    from simulator.swarm.engine import SwarmSimulation

    assert simulator is not None
    assert SwarmSimulation is not None


def test_anomaly_imports() -> None:
    from app.services.anomaly.fusion import assess_anomaly
    from app.services.anomaly_service import anomaly_service

    assert assess_anomaly is not None
    assert anomaly_service is not None
