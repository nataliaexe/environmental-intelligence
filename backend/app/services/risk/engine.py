from app.domain.risk import RiskAssessment
from app.services.anomaly.fusion import AnomalyAssessment


class RiskEngine:
    def assess(
        self,
        region_id: str,
        anomaly: AnomalyAssessment,
    ) -> RiskAssessment:
        probability = anomaly.score

        impact = self._estimate_impact(
            severity=anomaly.severity,
        )

        risk_score = (
            probability * 0.6
            + impact * 0.4
        )

        if risk_score >= 0.75:
            severity = "critical"
        elif risk_score >= 0.50:
            severity = "high"
        elif risk_score >= 0.25:
            severity = "moderate"
        else:
            severity = "low"

        hazard_type = self._classify_hazard(
            reasons=anomaly.reasons,
        )

        return RiskAssessment(
            region_id=region_id,
            hazard_type=hazard_type,
            risk_score=round(risk_score, 4),
            probability=round(probability, 4),
            impact=round(impact, 4),
            confidence=round(anomaly.score, 4),
            severity=severity,
            contributing_factors=anomaly.reasons,
        )

    @staticmethod
    def _estimate_impact(
        severity: str,
    ) -> float:
        mapping = {
            "normal": 0.1,
            "warning": 0.4,
            "critical": 0.9,
        }

        return mapping.get(severity, 0.1)

    @staticmethod
    def _classify_hazard(
        reasons: list[str],
    ) -> str:
        reason_set = set(reasons)

        if {
            "high_temperature",
            "low_humidity",
            "low_soil_moisture",
        }.issubset(reason_set):
            return "heat_drought_stress"

        if "high_temperature" in reason_set:
            return "extreme_heat"

        if "low_soil_moisture" in reason_set:
            return "drought"

        if "low_humidity" in reason_set:
            return "dryness"

        return "environmental_anomaly"


risk_engine = RiskEngine()
