
from main import apply_leave, update_status, view_leaves

def test_apply_leave():
    assert apply_leave("Rahul", 2, "Fever") == "Leave applied successfully"

def test_invalid_days():
    assert apply_leave("Amit", 0, "Personal") == "Invalid leave days"

def test_view_leaves():
    assert isinstance(view_leaves(), list)

def test_update_status():
    assert update_status(0, "Approved") == "Status updated successfully"
