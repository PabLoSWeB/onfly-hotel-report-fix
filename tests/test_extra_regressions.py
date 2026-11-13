"""Testes adicionais (não fazem parte dos testes fornecidos)."""

from helpers import run_cli


def test_reads_all_rows_beyond_200(tmp_path):
    """Nenhuma reserva pode ser descartada na leitura do CSV."""
    rows = [{"reservation_id": f"R-{i}", "amount": "10.00"} for i in range(250)]
    report = run_cli(tmp_path, rows)
    summary = report["summary"]
    assert summary["total_reservations"] == 250
    assert summary["confirmed_reservations"] == 250
    assert summary["total_amount_brl"] == "2500.00"


def test_top_hotels_tie_is_broken_by_hotel_id_ascending(tmp_path):
    """Em empate de valor, o menor hotel_id vem primeiro."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "500.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "500.00"},
        ],
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02"]


def test_no_billable_reservation_yields_zero_average(tmp_path):
    """Sem noites faturáveis, a média é '0.00' (sem divisão por zero)."""
    report = run_cli(tmp_path, [{"reservation_id": "R-1", "status": "CANCELLED"}])
    summary = report["summary"]
    assert summary["total_room_nights"] == 0
    assert summary["average_nightly_rate_brl"] == "0.00"
    assert report["by_month"] == []
    assert report["top_hotels"] == []


def test_generated_at_uses_fixed_offset(tmp_path):
    """generated_at usa o offset fixo -03:00."""
    report = run_cli(tmp_path, [{"reservation_id": "R-1"}])
    assert report["generated_at"].endswith("-03:00")
